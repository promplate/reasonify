from promplate.prompt.template import Component
from promplate_recipes.context import layers


def register_component(name: str):
    def wrapper(component: Component):
        component_layer[name] = component
        return component

    return wrapper


layers.append(component_layer := {})
