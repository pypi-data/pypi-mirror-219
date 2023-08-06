from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_by_name


class ColorPalette:
    CYAN = "\033[96m"
    ENDC = "\033[0m"


def color_print(color, text):
    print(f"{color}{text}{ColorPalette.ENDC}")


def print_markdown(text, style):
    print(
        highlight(
            text,
            get_lexer_by_name("markdown"),
            Terminal256Formatter(style=style),
        )
    )


def pretty_print_messages(messages: list[dict], style: str):
    for message in messages:
        color_print(ColorPalette.CYAN, message["role"])
        print_markdown(message["content"], style)
