from re import MULTILINE
from re import compile as re_compile
from typing import Literal

sub_trailing_spaces = re_compile(r"[ \t]+$", MULTILINE)
sub_multiple_lines = re_compile(r"\n{4,}")


def post_process(text: str):
    text = text.replace("\r", "")
    text = sub_trailing_spaces.sub("", text)
    text = sub_multiple_lines.sub("\n\n\n", text)
    return text


Strategy = Literal["innerText", "plain", "markdown"]


def pre_process(html: str, strategy: Strategy = "innerText"):
    match strategy:
        case "innerText":
            from .dom import temp_element

            with temp_element() as div:
                div.innerHTML = html
                return div.innerText

        case "plain":
            from html_text import extract_text

            return extract_text(html)

        case "markdown":
            from html2text import html2text

            return html2text(html, bodywidth=0)
