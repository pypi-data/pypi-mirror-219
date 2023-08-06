import openai
import tiktoken
from func_timeout import FunctionTimedOut, func_timeout

from .base_shell import BaseShell
from .print_utils import ColorPalette, color_print, print_markdown


def num_tokens_from_messages(
    messages: list[dict], model: str = "gpt-3.5-turbo-0301"
) -> int:
    """Returns the number of tokens used by a list of messages.
    This was copied straight from openai docs.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    elif model == "gpt-3.5-turbo":
        # Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif model == "gpt-4":
        # Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
            See https://github.com/openai/openai-python/blob/main/chatml.md
            for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += (
                    tokens_per_name  # role is always required and always 1 token
                )
    num_tokens += 3  # every reply is primed with <im_start>assistant
    return num_tokens


class ChatShell(BaseShell):
    prompt = "prompt>"

    def __init__(self, chat_id, messages, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = chat_id
        self.messages = messages

    @staticmethod
    def do_exit(_):
        """Exits the chat shell"""
        return True

    def do_paste(self, _):
        """Enters "paste mode" where you can create a multiline prompt"""
        return self.default(self.paste_mode(self.prompt))

    def get_output_messages(self):
        """Once the chat exceeds the model's token limit, we can't send the
        whole chat back to the API. We have to start cutting it off so that
        we can stay within the limit.
        """
        token_limit = self.config.token_limit
        # 0 is always the system prompt, and we always want that in the output
        token_count = num_tokens_from_messages(
            [self.messages[0]], model=self.config.gpt_model
        )
        system_idx = int(len(self.messages) / -1)
        i = -1
        while token_count <= token_limit:
            if i == system_idx:
                # this means that we hit the system prompt before hitting the token limit.
                #  meaning that we can just send everything
                return self.messages
            token_count += num_tokens_from_messages(
                [self.messages[i]], model=self.config.gpt_model
            )
            i -= 1

        i += 1
        if token_count > token_limit:
            i += 1
        return [self.messages[0]] + self.messages[i:]

    def default(self, line):
        if line == "":
            return

        user_msg = dict(role="user", content=line)
        self.messages.append(user_msg)
        try:
            resp = func_timeout(
                self.config.openai_req_timeout,
                openai.ChatCompletion.create,
                kwargs=dict(
                    model=self.config.gpt_model,
                    messages=self.get_output_messages(),
                ),
            )
            resp_msg = dict(**resp["choices"][0]["message"])
            color_print(ColorPalette.CYAN, "assistant")
            print_markdown(resp_msg["content"], self.config.print_style)
            self.messages.append(resp_msg)
            self.insert_message_pair(self.chat_id, user_msg, resp_msg)
        except (Exception, FunctionTimedOut) as e:
            print("Something went wrong while executing the query to openai")
            print(e)
