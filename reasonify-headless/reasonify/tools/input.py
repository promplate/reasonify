from js import window

from ..utils.tool import tool


@tool
def input(prompt: str):
    """return the input from the user, useful for asking questions to the user"""

    if res := window.prompt(prompt):
        return res

    raise IOError("User cancelled the input (refused to input anything)")
