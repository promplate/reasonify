from typing import Literal

from pyodide.http import pyfetch

from ..utils.html import Strategy, post_process, pre_process
from ..utils.tool import tool


class FetchFailed(Exception): ...


@tool
async def read_page(url: str, parse_as: Literal["innerText", "plain", "markdown"] = "markdown") -> tuple[int, str]:
    """
    fetch the content of a web page,
    returns its status code and text content.
    If the user asks about up-to-date information, you should use this tool.

    > Note that you shouldn't parse the result. You should treat it as cleaned text.
    """

    if parse_as not in ("innerText", "plain", "markdown"):
        raise ValueError("Invalid value for `parse_as`. Must be one of 'innerText', 'plain', 'markdown'.")

    try:
        return await _fetch(url, parse_as)
    except OSError as e:
        raise FetchFailed(*e.args) from None


async def _fetch(url: str, strategy: Strategy):
    try:
        res = await pyfetch(url)
    except OSError:
        res = await pyfetch(f"/api/proxy?url={url}")

    content = await res.text()

    return res.status, post_process(pre_process(content, strategy))
