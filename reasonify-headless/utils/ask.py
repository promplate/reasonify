from typing import TYPE_CHECKING

from promplate import ChainContext
from promplate.llm.base import AsyncGenerate

from reasonify import chain
from reasonify.utils.context import Context
from reasonify.utils.tool import tool


def register_self_as_tool(generate: AsyncGenerate):
    @tool
    async def ask_ai(question: str) -> str:
        """Ask a brilliant AI for help. Both input and output are natural language text."""

        if TYPE_CHECKING:
            context = ChainContext()

        async for context in chain.astream({"query": question}, generate):
            pass

        return "\n".join(Context(context)["response"])
