import os
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_component_func = components.declare_component("card_component", path=build_dir)


def card(title, content, tags, key=None):
    """Create a new instance of "my_component".
    """
    _ = _component_func(title=title, content=content, tags=tags, key=key)

