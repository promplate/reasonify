from inspect import signature
from typing import TYPE_CHECKING, Callable

from .context import Context


class Injector[T]:
    def __init__(self, getter: Callable[[], T]):
        self.getter = getter


def dispatch_context[T](func: Callable[..., T]) -> Callable[..., T]:
    injectors = {}
    defaults = {}

    params = signature(func).parameters

    for name, parameter in params.items():
        if parameter.default == parameter.empty or name == "c":
            continue
        elif isinstance(parameter.default, Injector):
            injectors[name] = parameter.default.getter
        else:
            defaults[name] = parameter.default

    params = list(params)

    def wrapper(*args):
        *args, context = args  # only the last one is `context`, the rest are positional arguments (such as `self`)
        c = Context.ensure(context)

        for k, v in defaults.items():
            if k not in c:
                c[k] = v

        for k, v in injectors.items():
            if k not in c:
                c[k] = v()

        return func(*args, **{name: c[name] if name != "c" else c for name in params[len(args) :]})

    return wrapper


if TYPE_CHECKING:

    def inject[T](getter: Callable[[], T]) -> T: ...

else:
    inject = Injector
