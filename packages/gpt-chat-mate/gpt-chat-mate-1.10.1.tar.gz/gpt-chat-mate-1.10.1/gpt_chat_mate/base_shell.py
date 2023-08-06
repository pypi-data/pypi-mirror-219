import cmd
import json
import os
import readline
import sqlite3
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from typing import Optional

from .print_utils import ColorPalette, color_print, print_markdown


@dataclass
class Config:
    db_filename: str
    gpt_model: str
    print_style: str
    token_limit: int
    openai_req_timeout: int = 60
    default_editor: str = "vim"
    editor_on_paste: bool = False


class BaseShell(cmd.Cmd):
    """Shared shell class for handling database stuff and other functionality."""

    def __init__(self, config: Optional[Config] = None):
        super().__init__()
        if config is None:
            self.set_config()
        else:
            self.config = config

    def set_config(self):
        if os.path.exists(".config.json"):
            with open(".config.json") as f:
                self.config = Config(**json.load(f))
            return

        print("No config found. Generating one.")
        self.config = Config(
            db_filename="chat.db",
            gpt_model="gpt-3.5-turbo",
            print_style="monokai",
            token_limit=4097,
        )
        with open(".config.json", "w") as f:
            f.write(json.dumps(asdict(self.config), indent=4))

    def db_query(self, query: str, params=()):
        with sqlite3.connect(self.config.db_filename) as con:
            cur = con.cursor()
            cur.execute(query, params)
            result = cur.fetchall()
            cur.close()
            con.commit()

        return result

    def init_db(self):
        self.db_query(
            """
            CREATE TABLE chat(
                chat_id integer primary key,
                name text
            );
        """,
        )
        self.db_query(
            """
            CREATE TABLE message(
                message_id integer primary key,
                chat_id integer,
                role text,
                content text,
                FOREIGN KEY(chat_id) REFERENCES chat(chat_id)
            );
        """,
        )

    def insert_message_pair(self, chat_id: int, user_msg: dict, assist_msg: dict):
        """Inserts a user and assisntant message pair into the database."""
        self.db_query(
            "INSERT INTO message (chat_id, role, content) VALUES (?, ?, ?), (?, ?, ?);",
            (
                chat_id,
                user_msg["role"],
                user_msg["content"],
                chat_id,
                assist_msg["role"],
                assist_msg["content"],
            ),
        )

    def insert_chat(self, name: str, system_prompt: str) -> int:
        chat_id = self.db_query(
            "INSERT INTO chat (name) VALUES (?) RETURNING chat_id;",
            (name,),
        )[0][0]
        self.db_query(
            "INSERT INTO message (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, "system", system_prompt),
        )
        return chat_id

    def duplicate_chat(self, chat_id: int):
        dup_chat_id = self.db_query(
            """
            INSERT INTO chat (name)
            SELECT name FROM chat WHERE chat_id = ?
            RETURNING chat_id;
            """,
            (chat_id,),
        )[0][0]
        self.db_query(
            """
            INSERT INTO message (chat_id, role, content)
            SELECT ?, role, content FROM message WHERE role = 'system' AND chat_id = ?;
        """,
            (dup_chat_id, chat_id),
        )

    def update_chat_name(self, chat_id: int, name: str):
        self.db_query("UPDATE chat SET name = ? WHERE chat_id = ?;", (name, chat_id))

    def update_system_prompt(self, chat_id: int, system_prompt: str):
        self.db_query(
            "UPDATE message SET content = ? WHERE role = 'system' AND chat_id = ?",
            (system_prompt, chat_id),
        )

    def get_chat_ids(self) -> list[int]:
        return [item[0] for item in self.db_query("SELECT chat_id FROM chat;")]

    def get_chats(self) -> tuple[int, str]:
        return self.db_query("SELECT chat_id, name FROM chat;")

    def get_system_prompt(self, chat_id: int) -> str:
        return self.db_query(
            "SELECT content FROM message WHERE role = 'system' AND chat_id = ?",
            (chat_id,),
        )[0][0]

    def get_messages(self, chat_id: int) -> list[dict]:
        return [
            dict(role=role, content=content)
            for role, content in self.db_query(
                "SELECT role, content FROM message WHERE chat_id = ?", (chat_id,)
            )
        ]

    def delete_chat(self, chat_id: int):
        self.db_query("DELETE FROM message where chat_id = ?", (chat_id,))
        self.db_query("DELETE FROM chat where chat_id = ?", (chat_id,))
        print(f"Chat {chat_id} deleted.")

    def prompt_with_editor(self, in_text: str) -> str:
        # using .md so that an editor like vim will highlight the text
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".md") as tmp_file:
            tmp_file.write(in_text)
            tmp_file.flush()

            subprocess.call([self.config.default_editor, tmp_file.name])

            tmp_file.seek(0)
            return tmp_file.read().strip()

    def paste_mode(self, prompt) -> str:
        """Shared function for multiline prompts"""
        if self.config.editor_on_paste:
            result = self.prompt_with_editor("")
            readline.add_history(result)
            color_print(ColorPalette.CYAN, "user")
            print_markdown(result, self.config.print_style)
            return result

        print('Paste mode activated. "EOF" indicates the end of the prompt.')
        lines = []
        while True:
            line = input(f"(paste){prompt}")
            if line == "EOF":
                con_line = "\n".join(lines)
                readline.add_history(con_line)
                return con_line
            lines.append(line)
