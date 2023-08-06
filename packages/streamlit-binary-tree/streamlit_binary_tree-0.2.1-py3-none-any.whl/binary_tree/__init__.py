import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "binary_tree",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("binary_tree", path=build_dir)

default_style = {
    "font_family": "arial",
    "font_size": "0.7em",
    "max_height": "2400px",
    "edge_size": "150px",
    "node_size": "100px",
    "padding_quantum": "5px",
    "edge_color": "#ccc",
    "edge_hover_color": "#94a0b4",
    "node_color": "#fff",
    "node_border_color": "#999",
    "node_hover_color": "#c8e4f8",
    "text_color": "#333",
    "text_hover_color": "#333",
    "button_color": "rgb(185, 145, 145)",
    "button_hover_color": "rgb(150, 0, 0)",
    "transition_time": "0.7s",
}


def binary_tree(data, key=None, expanded=True, show_node_ids=True, style=default_style):
    component_value = _component_func(
        data=data,
        key=key,
        default=0,
        expanded=expanded,
        show_node_ids=show_node_ids,
        style=style,
    )

    return component_value


if not _RELEASE:
    import streamlit as st
    import json

    st.set_page_config(layout="wide")

    with open("tree_data.json") as f:
        data = json.load(f)

    # st.write(data)
    st.markdown("---")

    name = "Decision Tree"
    node_id = binary_tree(data, key="dct", show_node_ids=True)

    st.markdown("---")

    st.write(node_id)
