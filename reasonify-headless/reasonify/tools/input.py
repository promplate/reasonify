from contextlib import suppress

from ..utils.tool import tool


@tool
def input(prompt=""):
    """return the input from the user, useful for asking questions to the user"""

    with suppress(ModuleNotFoundError):
        from js import window

        if res := window.prompt(prompt):
            return res

        raise IOError("User cancelled the input (refused to input anything)")

    from builtins import input

    return input(prompt)
