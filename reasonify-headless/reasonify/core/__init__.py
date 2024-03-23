from promplate import Chain

from .step1 import step1
from .step2 import step2
from .step3 import step3
from .step4 import step4

chain = Chain(step1, step2, step3, step4)


@chain.pre_process
def _(context):
    context["query"] = context["messages"][-1]["content"]
