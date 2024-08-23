from micropip import install

from ..utils.tool import tool


@tool
async def pip_install(*requirements: str):
    """install 3rd-party packages to this runtime environment"""

    return await install(sum(map(str.split, requirements), []), keep_going=True)
