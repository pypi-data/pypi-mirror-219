import os
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
component_func = components.declare_component("card", path=build_dir)


def card(title, content, tags, key=None):
    """Create a new instance of "my_component".
    """
    _ = component_func(title=title, content=content, tags=tags, key=key)

