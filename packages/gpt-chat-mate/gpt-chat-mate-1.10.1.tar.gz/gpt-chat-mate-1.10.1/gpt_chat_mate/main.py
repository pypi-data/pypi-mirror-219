import os
import sqlite3

import openai
from func_timeout import FunctionTimedOut, func_timeout
from pyfiglet import Figlet

from . import __version__
from .base_shell import BaseShell
from .chat_shell import ChatShell
from .print_utils import pretty_print_messages, print_markdown


class GPTChatMate(BaseShell):
    prompt = "GPTChatMate>"

    def __init__(self):
        print(Figlet().renderText(f"GPTChatMate {__version__}"))
        super().__init__()

    @staticmethod
    def do_exit(_):
        """exit the program"""
        return True

    def generate_chat_name(self, system_prompt: str) -> str:
        print("Using chatGPT to generate chat name...")
        messages = [
            dict(
                role="system",
                content="You are a professional name creator for chatGPT chats. You are given a chatGPT system"
                "prompt and you generate 2 to 3 word names that describe the chat",
            ),
            dict(
                role="user",
                content=f"Name this system prompt: {system_prompt}\nPrint just the name and no other text",
            ),
        ]
        resp = func_timeout(
            self.config.openai_req_timeout,
            openai.ChatCompletion.create,
            kwargs=dict(model=self.config.gpt_model, messages=messages),
        )
        return resp["choices"][0]["message"]["content"]

    def valid_id(self, _id) -> bool:
        if _id == "":
            print("You must provide an ID.")
            return False
        if not _id.isnumeric():
            print("Given ID must be a number.")
            return False
        existing_chats = self.get_chat_ids()
        if int(_id) not in existing_chats:
            print(f"No chat exists for ID {_id}")
            return False
        return True

    def do_delete(self, _id):
        """
        delete <ID>

            where <ID> is the ID of the chat you want to delete.
        """
        if not self.valid_id(_id):
            return
        self.delete_chat(int(_id))

    def do_chat(self, _id):
        """
        chat optional[<ID>]

            where <ID> is the ID of a previous chat. A new chat will be created automatically if
            no ID is given.
        """
        if _id == "":
            name = input(
                "Please name the chat (leave blank to let chatGPT name it for you):\nname>"
            )
            system_prompt = input("Please provide a system prompt:\nsystem prompt>")

            if system_prompt == "paste":
                system_prompt = self.paste_mode("system prompt>")

            if name == "":
                try:
                    name = self.generate_chat_name(system_prompt)
                except (Exception, FunctionTimedOut) as e:
                    print(
                        "An attempt was made to generate a name, but something went wrong:"
                    )
                    print(e)
                    return

            messages = [dict(role="system", content=system_prompt)]
            chat_id = self.insert_chat(name, system_prompt)
        elif not self.valid_id(_id):
            return
        else:
            chat_id = int(_id)
            messages = self.get_messages(chat_id)
            print("Current chat history:")
            pretty_print_messages(messages, self.config.print_style)
        ChatShell(chat_id, messages, config=self.config).cmdloop()

    def do_list(self, _):
        """
        list

            list the names of the chats that already exist.
        """
        existing_chats = self.get_chats()
        if len(existing_chats) > 0:
            print("Existing chats:")
            print_markdown(
                "\n".join(f"{chat_id}. {name}" for chat_id, name in existing_chats),
                self.config.print_style,
            )
            return

        print('No chats exist yet. Run the "chat" command to start one.')

    def do_ls(self, line):
        """Alias of list command"""
        return self.do_list(line)

    def do_duplicate(self, line):
        """
        duplicate <ID>
            Duplicates a chat's system prompt into a new chat so that this
            doesn't have to be done manually by the user.
        """
        if not self.valid_id(line):
            return

        self.duplicate_chat(int(line))

    def do_rename(self, line):
        """
        rename <ID> optional[<name>]
            Allows user to rename a chat.
        """
        args = line.split(" ")
        if not self.valid_id(args[0]):
            return

        chat_id = int(args[0])
        if len(args) > 1:
            new_name = " ".join(args[1:])
        else:
            system_prompt = self.get_system_prompt(chat_id)
            new_name = self.generate_chat_name(system_prompt)

        self.update_chat_name(chat_id, new_name)

    def do_esp(self, line):
        """
        esp <ID>
            (e)dit (s)ystem (p)rompt allows user to edit the system prompt of a chat
        """
        if not self.valid_id(line):
            return

        chat_id = int(line)
        system_prompt = self.get_system_prompt(chat_id)
        system_prompt = self.prompt_with_editor(system_prompt)

        self.update_system_prompt(chat_id, system_prompt)
        print(f"System prompt for chat {chat_id} now set to:\n\n{system_prompt}")

    def preloop(self):
        if os.path.exists(".key"):
            with open(".key") as f:
                openai.api_key = f.read().strip()
        else:
            print("No .key file found.")
            key = input("Please enter your OpenAI API key:")
            with open(".key", "w") as f:
                f.write(key)
            openai.api_key = key

        if sqlite3.sqlite_version_info[1] < 35:
            print(
                "ERROR: Bad sqlite3 version.\n"
                f"Your version: {sqlite3.sqlite_version}\n"
                "Required version: >3.35.0"
            )
        if not os.path.exists(self.config.db_filename):
            print("no DB found. Creating one.")
            self.init_db()

        self.do_list("")


def main():
    GPTChatMate().cmdloop()


if __name__ == "__main__":
    main()
