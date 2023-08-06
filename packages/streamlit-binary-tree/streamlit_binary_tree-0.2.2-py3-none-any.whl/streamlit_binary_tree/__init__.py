import os
import math
import numpy as np
from typing import List
import streamlit as st
import streamlit.components.v1 as components
from sklearn.tree import _tree
from sklearn.tree._classes import DecisionTreeClassifier as DCTClass

_RELEASE = True
_DEBUG = True
_NAME = "streamlit_binary_tree"

if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(_NAME, path=build_dir)
else:
    _component_func = components.declare_component(
        _NAME,
        url="http://localhost:3001",
    )


def human_format(n, precision=0, large_value_precision=None):
    if large_value_precision is None:
        large_value_precision = precision

    suffix = ["", "k", "M", "B", "T"]
    n = float(n)
    suffix_idx = max(
        0,
        min(len(suffix) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))),
    )
    n = n / 10 ** (3 * suffix_idx)

    precision = precision if suffix_idx == 0 else large_value_precision
    format = f",.{precision}f"

    return f"{n:{format}}{suffix[suffix_idx]}"


def content_text(number, percentage, perc_precision=1, percentage_first=True):
    if type(number) == list or type(number) == np.ndarray:
        num_texts = []
        perc_texts = []
        for n, p in zip(number, percentage):
            num_text = human_format(n, large_value_precision=1)
            perc_text = f"{p:{f'.{perc_precision}%'}}"

            num_texts.append(num_text)
            perc_texts.append(perc_text)

        num_text = ", ".join(num_texts)
        perc_text = ", ".join(perc_texts)

    else:
        num_text = human_format(number, large_value_precision=1)
        perc_text = f"{percentage:{f'.{perc_precision}%'}}"

    text = (
        f"{perc_text} ({num_text})" if percentage_first else f"{num_text} ({perc_text})"
    )
    return text


def combine_hex_values(colors, weight):
    colors = [c[1:] for c in colors]
    colors = ["".join([char * 2 for char in c]) if len(c) == 3 else c for c in colors]
    if weight <= 0:
        weights = [-weight, 1 + weight, 0]
    else:
        weights = [0, 1 - weight, weight]
    total_weight = sum(weights)
    red = int(
        sum([int(k[0:2], 16) * v for k, v in zip(colors, weights)]) / total_weight
    )
    green = int(
        sum([int(k[2:4], 16) * v for k, v in zip(colors, weights)]) / total_weight
    )
    blue = int(
        sum([int(k[4:6], 16) * v for k, v in zip(colors, weights)]) / total_weight
    )
    zpad = lambda x: x if len(x) == 2 else "0" + x
    color = zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])
    color = "#" + color
    return color


def get_balanced_class_weight(y):
    unique, counts = np.unique(np.array(y), return_counts=True)
    counts = 1 / counts
    class_weights = {u: c for u, c in zip(unique, counts)}
    return class_weights


def export_dict(
    tree: DCTClass,
    feature_names=None,
    feature_value_formats=None,
    class_names=None,
    class_colors=None,
    class_weights=None,
    sample_header="Samples",
    event_header="Events",
    sample_perc_precision=1,
    event_perc_precision=1,
    percentage_first=True,
    binary_formatting=False,
):
    """Export a decision tree in dict format.
    Parameters
    ----------
    decision_tree : decision tree classifier
        The decision tree to be exported
    feature_names : list of strings, optional (default=None)
        Names of each of the features.
    max_depth : int, optional (default=None)
        The maximum depth of the representation. If None, the tree is fully
        generated.
    Returns
    -------
    a dictionary of the format <tree> := {
        'feature' <int> | <string>,
        'threshold' : <float>,
        'impurity' : <float>,
        'n_node_samples' : <int>,
        'left' : <tree>,
        'right' : <tree>,
        'value' : [<int>],
    }
    if feature_names is provided, it is used to map feature indices
    to feature names.  All types (including the value list) are native
    python types as opposed to numpy types to make exporting to json
    and other pythonic operations easier.
    Examples
    --------
    >>> from sklearn.datasets import load_iris
    >>> from sklearn import tree
    >>> import json
    >>> clf = tree.DecisionTreeClassifier()
    >>> iris = load_iris()
    >>> clf = clf.fit(iris.data, iris.target)
    >>> d = tree.export_dict(clf)
    >>> j = json.dumps(d, indent=4)
    """
    tree_ = tree.tree_
    master_list = []
    if feature_value_formats is None:
        feature_value_formats = ["0.2f"] * tree.max_features_
    if class_colors is None:
        class_colors = [
            "#198038",
            "#fa4d56",
            "#1192e8",
            "#6929c4",
            "#b28600",
            "#009d9a",
            "#9f1853",
            "#002d9c",
            "#ee538b",
            "#570408",
            "#005d5d",
            "#8a3800",
            "#a56eff",
        ]
    class_equal_color = "#fff"
    if class_names is None:
        class_names = [str(i) for i in range(int(tree_.n_classes))]
    classes = [
        {"id": i, "name": c, "color": class_colors[i]}
        for i, c in enumerate(class_names)
    ]
    tmp_class_weights = {k: 1 for k in range(int(tree_.n_classes[0]))}
    if class_weights is not None:
        for k, class_weight in class_weights.items():
            tmp_class_weights[k] = class_weight
    class_weights = list(tmp_class_weights.values())

    value_weighted_percs = np.transpose(tree_.value) / sum(np.transpose(tree_.value))
    root_bad_value = value_weighted_percs[1][0][0]
    max_bad_value = max(value_weighted_percs[1][0])
    min_bad_value = min(value_weighted_percs[1][0])
    value_weighted_percs = [
        v.flatten().tolist() for v in np.transpose(value_weighted_percs)
    ]

    value_percs = [v / cw for v, cw in zip(np.transpose(tree_.value), class_weights)]
    value_percs /= sum(value_percs)
    value_percs = [v.flatten().tolist() for v in np.transpose(value_percs)]

    # i is the element in the tree_ to create a dict for
    def recur(i, master_dict, path="", depth=0):
        if i == _tree.TREE_LEAF:
            return None

        feature_idx = int(tree_.feature[i])
        threshold = float(tree_.threshold[i])
        samples = tree_.n_node_samples[i]
        value = value_percs[i]
        value_weighted = value_weighted_percs[i]

        if binary_formatting:
            bad_value = value_weighted[1]
            if bad_value >= root_bad_value:
                ratio = (bad_value - root_bad_value) / (max_bad_value - root_bad_value)
            else:
                ratio = (bad_value - root_bad_value) / (root_bad_value - min_bad_value)

            color = combine_hex_values(
                [class_colors[0], class_equal_color, class_colors[1]],
                ratio,
            )
        else:
            if np.argmax(value) == np.argmin(value):
                color = class_equal_color
            else:
                color = class_colors[np.argmax(value)]

        hasChildren = feature_idx != _tree.TREE_UNDEFINED
        left_idx = int(tree_.children_left[i])
        right_idx = int(tree_.children_right[i])

        samples_value = content_text(
            tree_.n_node_samples[i],
            tree_.n_node_samples[i] / tree_.n_node_samples[0],
            perc_precision=sample_perc_precision,
            percentage_first=percentage_first,
        )

        if binary_formatting:
            bads_value = content_text(
                value[1] * samples,
                value[1],
                perc_precision=event_perc_precision,
                percentage_first=percentage_first,
            )
        else:
            bads_value = content_text(
                [v * samples for v in value],
                value,
                perc_precision=event_perc_precision,
                percentage_first=percentage_first,
            )

        event_header_val = event_header

        if binary_formatting and event_header_val == "Events":
            event_header_val = dataset.target_names[1]

        tree_dict = {
            "node_id": i,
            "impurity": float(tree_.impurity[i]),
            "n_node_samples": int(samples),
            "value": value,
            "contents": [
                f"{sample_header}: {samples_value}",
                f"{event_header_val}: {bads_value}",
            ],
            "path": path,
            "color": color,
        }

        if hasChildren:
            feature = feature_names[feature_idx] if feature_names else str(feature_idx)
            format = feature_value_formats[feature_idx]
            tree_dict["feature"] = feature
            tree_dict["threshold"] = threshold

            tree_dict["left"] = {
                "id": left_idx,
                "condition": f"{feature} ≤ {threshold:{format}}",
            }
            tree_dict["right"] = {
                "id": right_idx,
                "condition": f"{feature} > {threshold:{format}}",
            }

        master_list.append(tree_dict)

        if hasChildren:
            recur(
                left_idx,
                master_dict,
                f'{path} ⮞ {tree_dict["left"]["condition"]}',
                depth + 1,
            )
            recur(
                right_idx,
                master_dict,
                f'{path} ⮞ {tree_dict["right"]["condition"]}',
                depth + 1,
            )

    recur(0, master_list, "Root")

    return master_list, classes


def get_node_data(data, node_id):
    node_ids = [item["node_id"] for item in data]
    idx = node_ids.index(node_id)
    node_data = data[idx]
    return node_data


def get_summary_streamlit(node_data, classes, spacing=[3, 2]):
    col1, col2 = st.columns(spacing)

    with col1:
        st.header("Node data")
        st.write(
            f"""**Node ID:**  
                 {node_data['node_id']}"""
        )
        st.write(
            f"""**Path:**  
                 {node_data['path']}"""
        )
        for content in node_data["contents"]:
            left, right = content.split(":")
            st.write(
                f"""**{left}:**  
                     {right}"""
            )

    with col2:
        st.header("Classes")
        for c in classes:
            st.markdown(
                f"""<span style="background-color: {c['color']}; padding:5px;">{c['name']}</span>""",
                unsafe_allow_html=True,
            )


def binary_tree(
    data: List[dict],
    key: str = None,
    expanded_depth: int = 3,
    show_node_ids: bool = True,
    style: dict = None,
):
    """
    Creates an interactive foldable binary tree based on input data.

    Args:
        data (List[dict]): Data for tree in list format. List item format should be as follows-
            [{
                "node_id": int,
                "left": {
                    "id": int,
                    "condition": str
                },
                "right": {
                    "id": int,
                    "condition": str
                },
                "contents": List[str],
                "color": str
            }]
        key (str, optional): Name of tree. Defaults to None.
        expanded (bool, optional): Whether completely expanded at the start. Defaults to True.
        show_node_ids (bool, optional): Whether node ids are shown at the left of every single node. Defaults to True.
        style (_type_, optional): Styling info: font style, color, spacing. Defaults to default_style.
        default_style = {
            "max_height": "2400px",
            "padding_quantum": "5px",
            "edge_size": "100px",
            "edge_color": "#c2c9cc",
            "edge_hover_color": "#adc2cc",
            "node_size": "120px",
            "node_border_color": "#c2c9cc",
            "node_color": "#fff",
            "node_hover_color": "#d5e6f0",
            "font_family": "arial",
            "font_size": "0.7em",
            "text_color": "#333",
            "text_hover_color": "#111",
            "text_outline_color": "#fff",
            "text_outline_alpha": "0.4",
            "button_color": "#70b4c2",
            "button_hover_color": "#2d6186",
            "transition_time": "0.7s",
        }

    Returns:
        int: Selected node id

    Example Usage:
        Tree with dummy data and changed style.

        from sklearn.datasets import load_iris, load_breast_cancer
        from sklearn import tree

        st.set_page_config(layout="wide")

        # Breast Cancer dataset (Binary Classification)
        clf = tree.DecisionTreeClassifier(
            class_weight="balanced", max_depth=4, random_state=42
        )
        dataset = load_breast_cancer()
        clf = clf.fit(
            dataset.data,
            dataset.target,
        )
        get_balanced_class_weight(dataset.target)
        data, classes = export_dict(
            clf,
            feature_names=list(dataset.feature_names),
            class_names=list(dataset.target_names),
            class_weights=get_balanced_class_weight(dataset.target),
            binary_formatting=True,
        )

        st.markdown("---")
        node_id = binary_tree(
            data,
            key="dct_sample_breast_cancer_dataset",
            show_node_ids=True,
            style={"node_size": "120px"},
        )
        node_data = get_node_data(data, node_id)
        get_summary_streamlit(node_data, classes)
        st.markdown("---")

        # Iris dataset (Multi-class Classification)
        clf = tree.DecisionTreeClassifier(
            class_weight="balanced", max_depth=4, random_state=42
        )
        dataset = load_iris()
        clf = clf.fit(
            dataset.data,
            dataset.target,
        )
        get_balanced_class_weight(dataset.target)
        data, classes = export_dict(
            clf,
            feature_names=list(dataset.feature_names),
            class_names=list(dataset.target_names),
            class_weights=get_balanced_class_weight(dataset.target),
        )

        st.markdown("---")
        node_id = binary_tree(
            data,
            key="dct_sample_iris_dataset",
            show_node_ids=True,
            style={"node_size": "120px"},
        )
        node_data = get_node_data(data, node_id)
        get_summary_streamlit(node_data, classes)
        st.markdown("---")

    """

    default_style = {
        "max_height": "2400px",
        "padding_quantum": "5px",
        "edge_size": "100px",
        "edge_color": "#c2c9cc",
        "edge_hover_color": "#adc2cc",
        "node_size": "120px",
        "node_border_color": "#c2c9cc",
        "node_color": "#fff",
        "node_hover_color": "#d5e6f0",
        "font_family": "arial",
        "font_size": "0.7em",
        "text_color": "#333",
        "text_hover_color": "#111",
        "text_outline_color": "#fff",
        "text_outline_alpha": "0.4",
        "button_color": "#70b4c2",
        "button_hover_color": "#2d6186",
        "transition_time": "0.7s",
    }

    style = {} if (style is None) else style
    filtered_style = {k: v for k, v in style.items() if k in default_style.keys()}
    style = default_style.copy()
    for k in style.keys():
        if k in filtered_style:
            style[k] = filtered_style[k]

    component_value = _component_func(
        data=data,
        key=key,
        default=0,
        expanded_depth=expanded_depth,
        show_node_ids=show_node_ids,
        style=style,
    )

    return component_value


if _DEBUG:
    from sklearn.datasets import load_iris, load_breast_cancer
    from sklearn import tree

    st.set_page_config(layout="wide")

    # Breast Cancer dataset (Binary Classification)
    clf = tree.DecisionTreeClassifier(
        class_weight="balanced", max_depth=4, random_state=42
    )
    dataset = load_breast_cancer()
    clf = clf.fit(
        dataset.data,
        dataset.target,
    )
    get_balanced_class_weight(dataset.target)
    data, classes = export_dict(
        clf,
        feature_names=list(dataset.feature_names),
        class_names=list(dataset.target_names),
        class_weights=get_balanced_class_weight(dataset.target),
        binary_formatting=True,
    )

    st.markdown("---")
    node_id = binary_tree(
        data,
        key="dct_sample_breast_cancer_dataset",
        show_node_ids=True,
        style={"node_size": "120px"},
    )
    node_data = get_node_data(data, node_id)
    get_summary_streamlit(node_data, classes)
    st.markdown("---")

    # Iris dataset (Multi-class Classification)
    clf = tree.DecisionTreeClassifier(
        class_weight="balanced", max_depth=4, random_state=42
    )
    dataset = load_iris()
    clf = clf.fit(
        dataset.data,
        dataset.target,
    )
    get_balanced_class_weight(dataset.target)
    data, classes = export_dict(
        clf,
        feature_names=list(dataset.feature_names),
        class_names=list(dataset.target_names),
        class_weights=get_balanced_class_weight(dataset.target),
    )

    st.markdown("---")
    node_id = binary_tree(
        data,
        key="dct_sample_iris_dataset",
        show_node_ids=True,
        style={"node_size": "120px"},
    )
    node_data = get_node_data(data, node_id)
    get_summary_streamlit(node_data, classes)
    st.markdown("---")
