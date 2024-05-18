from micropip import install

from ..utils.tool import tool


@tool
async def pip_install(requirements: str | list[str]):
    """
    Install a package or list of packages to this runtime environment.
    If you are going to use a 3-party library, you should install it first.
    """

    return await install(requirements, keep_going=True)
