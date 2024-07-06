from functools import cache
from re import MULTILINE
from re import compile as re_compile

from js import HTMLDivElement, HTMLTemplateElement, document
from pyodide.http import pyfetch

from ..utils.tool import tool


class FetchFailed(Exception): ...


@tool
async def fetch(url: str) -> tuple[int, str]:
    """
    fetch the content of a web page,
    returns its status code and text content.
    """

    try:
        return await _fetch(url)
    except OSError as e:
        raise FetchFailed(*e.args) from None


async def _fetch(url: str):
    try:
        res = await pyfetch(url)
    except OSError:
        res = await pyfetch(f"/api/proxy?url={url}")

    content = await res.text()

    return res.status, post_process(purify(content))


@cache
def get_root_node():
    template: HTMLTemplateElement = document.createElement("template")  # type: ignore
    return template.content


def purify(html: str):
    div: HTMLDivElement = get_root_node().appendChild(document.createElement("div"))  # type: ignore
    div.innerHTML = html
    return div.innerText


sub_trailing_spaces = re_compile(r"[ \t]+$", MULTILINE)
sub_multiple_lines = re_compile(r"\n{4,}")


def post_process(text: str):
    text = text.replace("\r", "")
    text = sub_trailing_spaces.sub("", text)
    text = sub_multiple_lines.sub("\n\n\n", text)
    return text
