from isomorphic_fetch import fetch

from ..utils.html import Strategy, post_process, pre_process
from ..utils.tool import tool


class FetchFailed(Exception): ...


@tool
async def read_page(url: str, parse_as: Strategy = "markdown") -> tuple[int, str]:
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
        res = await fetch(url)
    except OSError:
        res = await fetch(f"/api/proxy?url={url}")

    return res.status, post_process(pre_process(res.text, strategy))
