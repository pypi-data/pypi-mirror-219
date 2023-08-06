from collections import defaultdict
import os
import math
import pandas as pd
import numpy as np
from typing import List
import streamlit as st
import streamlit.components.v1 as components
from sklearn.tree import _tree
from sklearn.tree._classes import DecisionTreeClassifier as DCTClass

_RELEASE = True
_DEBUG = True
_NAME = "streamlit_binary_tree"

CATEGORICAL_INDICATOR = " !@#$ "
BINARY_INDICATOR = " $#@! "

# If release, use build or use dev
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
    """Human formats large numbers

    Args:
        n (int): Number to format
        precision (int, optional): Precision of output. Defaults to 0.
        large_value_precision (int, optional): Precision of larger number output. Defaults to precision if None.

    Returns:
        str: Readable small number
    """
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
    """Return readable number with percentage out of total.

    Args:
        number (int or list): Number of samples
        percentage (float or list): % samples out of total samples
        perc_precision (int, optional): Precision of percentage. Defaults to 1.
        percentage_first (bool, optional): Whether to put percentage first. Defaults to True.

    Returns:
        str: Formatted output
    """
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


def get_color_from_ternary_gradient(colors, weight):
    """Provides color from gradient defined by three provided colors according to weight given.

    Args:
        colors (list of size 3): Colors defining ternary gradient
        weight (int): Weight to calculate color

    Returns:
        str: Color from gradient as hex
    """
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
    """Return balanced class weight according to provided y

    Args:
        y (list or np.array): Target Values

    Returns:
        dict: Class weights in dict
    """
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

    Args:
        tree (decision tree classifier): The decision tree to be exported
        feature_names (list of strings, optional): Names of each of the features. Defaults to None.
        feature_value_formats (defaultDict, optional): Formats for each feature value (used in Connectors). Defaults to "0.2f".
        class_names (list of strings, optional): Names of each of the classes. Defaults to None.
        class_colors (list of strings, optional): Hex of each of the class colors. Defaults to default class colors.
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
        class_weights (dict of floats, optional): Dict with weights of the classes. Defaults to 1.
        sample_header (str, optional): Header for samples line item. Defaults to "Samples".
        event_header (str, optional): Header for events line item. Defaults to "Events".
        sample_perc_precision (int, optional): Precision of % of samples line item. Defaults to 1.
        event_perc_precision (int, optional): Precision of % of events line item. Defaults to 1.
        percentage_first: Whether to show % first. Defaults to True.
        binary_formatting: Improves formatting of dict for binary classification.
            Blends outputted colors and shows only class 1 in line items.

    Returns (list):
        list of dictionaries of the format
            {
                "node_id": id (int),
                "impurity": gini impurity (float),
                "n_node_samples": num of samples (int),
                "value": weighted event values (list of int),
                "contents": [
                    Samples text (str),
                    Events text (str),
                ],
                "path": path (str),
                "color": color hex (str),
                "feature": feature name (str)
                "threshold": threshold of split (float)
                "left":{
                    "id": id (int)
                    "condition": condition of split (str)
                }
                "right":{
                    "id": id (int)
                    "condition": condition of split (str)
                }
            }

    Examples:
        from sklearn.datasets import load_iris
        from sklearn import tree
        import json
        clf = tree.DecisionTreeClassifier()
        iris = load_iris()
        clf = clf.fit(iris.data, iris.target)
        d = tree.export_dict(clf)
        j = json.dumps(d, indent=4)
    """
    tree_ = tree.tree_
    master_list = []
    if feature_value_formats is None:
        feature_value_formats = defaultdict(lambda: "0.2f")
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

            color = get_color_from_ternary_gradient(
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
            event_header_val = class_names[1]

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
            feature = (
                feature_names[feature_idx]
                if feature_names is not None
                else str(feature_idx)
            )
            format = feature_value_formats[feature]
            tree_dict["feature"] = feature
            tree_dict["threshold"] = threshold

            if BINARY_INDICATOR in feature:
                left_condition = f"{feature.split(BINARY_INDICATOR)[1]} is FALSE"
            elif CATEGORICAL_INDICATOR in feature:
                left_condition = f"{feature.split(CATEGORICAL_INDICATOR)[0]} IS NOT {feature.split(CATEGORICAL_INDICATOR)[1]}"
            else:
                left_condition = f"{feature} ≤ {threshold:{format}}"

            if BINARY_INDICATOR in feature:
                right_condition = f"{feature.split(BINARY_INDICATOR)[1]} is TRUE"
            elif CATEGORICAL_INDICATOR in feature:
                right_condition = f"{feature.split(CATEGORICAL_INDICATOR)[0]} IS {feature.split(CATEGORICAL_INDICATOR)[1]}"
            else:
                right_condition = f"{feature} > {threshold:{format}}"

            tree_dict["left"] = {
                "id": left_idx,
                "condition": left_condition,
            }
            tree_dict["right"] = {
                "id": right_idx,
                "condition": right_condition,
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
    """Get node data from list of nodes data

    Args:
        data (list of dict): List of Node dicts
        node_id (int): id of node

    Returns:
        dict: node data
    """
    node_ids = [item["node_id"] for item in data]
    idx = node_ids.index(node_id)
    node_data = data[idx]
    return node_data


def get_summary_streamlit(node_data, classes, spacing=[3, 2]):
    """Display summary for tree visual using streamlit components (Nodes + Classes)

    Args:
        node_data (dict): Node data of selected node
        classes (int): id of node
        spacing (list of 2 ints): Input to streamlit column spacing. Defaults to [3,2]
    """
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


def binary_tree_component(
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
        expanded_depth (int, optional): Initial expanded depth of the tree. Defaults to 3.
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
                "font_family": '"Helvetica Neue",Helvetica,Arial,sans-serif',
                "font_size": "0.7em",
                "text_color": "#111",
                "text_hover_color": "#000",
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
        "font_family": '"Helvetica Neue",Helvetica,Arial,sans-serif',
        "font_size": "0.7em",
        "text_color": "#111",
        "text_hover_color": "#000",
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


def binary_tree(
    key,
    data_set,
    features,
    target,
    clf_params=None,
    feature_value_formats=None,
    categorise_binaries=True,
    class_names=None,
    class_colors=None,
    show_node_ids=True,
    expanded_depth=3,
    style=None,
    spacing=[3, 2],
    sample_header="Samples",
    event_header="Events",
    sample_perc_precision=1,
    event_perc_precision=1,
    percentage_first=True,
    binary_formatting=False,
):
    """Creates an interactive binary tree.

    Args:
        key (str): Name of tree
        data_set (DataFrame): The data to make the decision tree on
        features (list of str): Features of the tree
        target (str): Target of the tree
        clf_params (dict): Parameters for the classifier
        feature_value_formats (defaultDict, optional): Formats for each feature value (used in Connectors). Defaults to "0.2f".
        categorise_binaries (bool, optional): Whether to treat binary features as categories. Defaults to True.
        class_names (list of strings, optional): Names of each of the classes. Defaults to None.
        class_colors (list of strings, optional): Hex of each of the class colors. Defaults to default class colors.
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
        expanded_depth (int, optional): Initial expanded depth of the tree. Defaults to 3.
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
                "font_family": '"Helvetica Neue",Helvetica,Arial,sans-serif',
                "font_size": "0.7em",
                "text_color": "#111",
                "text_hover_color": "#000",
                "text_outline_color": "#fff",
                "text_outline_alpha": "0.4",
                "button_color": "#70b4c2",
                "button_hover_color": "#2d6186",
                "transition_time": "0.7s",
            }
        spacing (list of 2 ints): Input to streamlit column spacing for summary. Defaults to [3,2]
        class_weights (dict of floats, optional): Dict with weights of the classes. Defaults to 1.
        sample_header (str, optional): Header for samples line item. Defaults to "Samples".
        event_header (str, optional): Header for events line item. Defaults to "Events".
        sample_perc_precision (int, optional): Precision of % of samples line item. Defaults to 1.
        event_perc_precision (int, optional): Precision of % of events line item. Defaults to 1.
        percentage_first: Whether to show % first. Defaults to True.
        binary_formatting: Improves formatting of dict for binary classification.
            Blends outputted colors and shows only class 1 in line items.

    Examples:
        Examples with dummy data

        # Breast Cancer dataset (Binary Classification)

        dataset_breast_cancer = load_breast_cancer()
        features_breast_cancer = list(dataset_breast_cancer.feature_names)
        target_breast_cancer = "target"
        classes_breast_cancer = list(dataset_breast_cancer.target_names)
        df_breast_cancer = pd.DataFrame(dataset_breast_cancer.data)
        df_breast_cancer.columns = features_breast_cancer
        df_breast_cancer[target_breast_cancer] = list(dataset_breast_cancer.target)

        binary_tree(
            "breast_cancer",
            df_breast_cancer,
            features_breast_cancer,
            target_breast_cancer,
            show_node_ids=True,
            style={"node_size": "120px", "edge_size": "150px"},
            class_names=list(dataset_breast_cancer.target_names),
            binary_formatting=True,
        )

        # Breast Cancer dataset with categorical features (Binary Classification)

        dataset_breast_cancer2 = load_breast_cancer()
        features_breast_cancer2 = list(dataset_breast_cancer2.feature_names)
        target_breast_cancer2 = "target"
        classes_breast_cancer2 = list(dataset_breast_cancer2.target_names)
        df_breast_cancer2 = pd.DataFrame(dataset_breast_cancer2.data)
        df_breast_cancer2.columns = features_breast_cancer2
        df_breast_cancer2[target_breast_cancer2] = list(dataset_breast_cancer2.target)
        df_breast_cancer2["mean compactness band"] = pd.cut(
            df_breast_cancer2["mean compactness"],
            [-np.Inf, 0.2, 0.5, 0.8, np.Inf],
            labels=["<0.2", "0.2-0.5", "0.5-0.8", ">0.8"],
        )
        df_breast_cancer2["mean area flag"] = (df_breast_cancer2["mean area"] > 1000).map(
            {True: 1, False: 0}
        )
        features_breast_cancer2 = [
            "mean compactness band",
            "mean area flag",
        ]

        binary_tree(
            "breast_cancer2",
            df_breast_cancer2,
            features_breast_cancer2,
            target_breast_cancer2,
            show_node_ids=True,
            style={"node_size": "120px", "edge_size": "150px"},
            class_names=list(dataset_breast_cancer2.target_names),
            binary_formatting=True,
        )

        # Iris dataset (Multi-class Classification)

        dataset_iris = load_iris()
        features_iris = list(dataset_iris.feature_names)
        target_iris = "target"
        classes_iris = list(dataset_iris.target_names)
        df_iris = pd.DataFrame(dataset_iris.data)
        df_iris.columns = features_iris
        df_iris[target_iris] = list(dataset_iris.target)

        binary_tree(
            "iris",
            df_iris,
            features_iris,
            target_iris,
            show_node_ids=True,
            style={"node_size": "120px"},
            class_names=list(dataset_iris.target_names),
        )

    """
    if clf_params is None:
        clf_params = {
            "class_weight": "balanced",
            "max_depth": 4,
            "min_samples_leaf": 0.005,
            "min_impurity_decrease": 1e-4,
            "random_state": 42,
        }

    clf = tree.DecisionTreeClassifier()
    clf = clf.set_params(**clf_params)

    X = data_set[features]
    y = data_set[target]

    if categorise_binaries:
        for col in X.columns:
            if set(X[col].unique()) == {0, 1}:
                X.rename(columns={col: f"{BINARY_INDICATOR}{col}"}, inplace=True)

    X = pd.get_dummies(X, prefix_sep=CATEGORICAL_INDICATOR)
    X.columns = [str(col) for col in X.columns]

    features = X.columns

    clf = clf.fit(X, y)

    if clf_params["class_weight"] == "balanced":
        class_weights = get_balanced_class_weight(y)
    else:
        class_weights = clf_params["class_weight"]

    data, classes = export_dict(
        clf,
        feature_names=features,
        feature_value_formats=feature_value_formats,
        class_names=class_names,
        class_colors=class_colors,
        class_weights=class_weights,
        sample_header=sample_header,
        event_header=event_header,
        sample_perc_precision=sample_perc_precision,
        event_perc_precision=event_perc_precision,
        percentage_first=percentage_first,
        binary_formatting=binary_formatting,
    )

    st.markdown("---")
    node_id = binary_tree_component(
        data,
        key=key,
        show_node_ids=show_node_ids,
        expanded_depth=expanded_depth,
        style=style,
    )
    node_data = get_node_data(data, node_id)
    get_summary_streamlit(node_data, classes, spacing=spacing)
    st.markdown("---")


# ------------------------------------------------------------------------------------
# Debugging is developing
if _DEBUG:
    from sklearn.datasets import load_iris, load_breast_cancer
    from sklearn import tree

    st.set_page_config(layout="wide")

    # Breast Cancer dataset (Binary Classification)
    dataset_breast_cancer = load_breast_cancer()
    features_breast_cancer = list(dataset_breast_cancer.feature_names)
    target_breast_cancer = "target"
    classes_breast_cancer = list(dataset_breast_cancer.target_names)
    df_breast_cancer = pd.DataFrame(dataset_breast_cancer.data)
    df_breast_cancer.columns = features_breast_cancer
    df_breast_cancer[target_breast_cancer] = list(dataset_breast_cancer.target)

    binary_tree(
        "breast_cancer",
        df_breast_cancer,
        features_breast_cancer,
        target_breast_cancer,
        show_node_ids=True,
        style={"node_size": "120px", "edge_size": "150px"},
        class_names=list(dataset_breast_cancer.target_names),
        binary_formatting=True,
    )

    # Breast Cancer dataset with categorical features (Binary Classification)
    dataset_breast_cancer2 = load_breast_cancer()
    features_breast_cancer2 = list(dataset_breast_cancer2.feature_names)
    target_breast_cancer2 = "target"
    classes_breast_cancer2 = list(dataset_breast_cancer2.target_names)
    df_breast_cancer2 = pd.DataFrame(dataset_breast_cancer2.data)
    df_breast_cancer2.columns = features_breast_cancer2
    df_breast_cancer2[target_breast_cancer2] = list(dataset_breast_cancer2.target)
    df_breast_cancer2["mean compactness band"] = pd.cut(
        df_breast_cancer2["mean compactness"],
        [-np.Inf, 0.2, 0.5, 0.8, np.Inf],
        labels=["<0.2", "0.2-0.5", "0.5-0.8", ">0.8"],
    )
    df_breast_cancer2["mean area flag"] = (df_breast_cancer2["mean area"] > 1000).map(
        {True: 1, False: 0}
    )
    features_breast_cancer2 = [
        "mean compactness band",
        "mean area flag",
    ]

    binary_tree(
        "breast_cancer2",
        df_breast_cancer2,
        features_breast_cancer2,
        target_breast_cancer2,
        show_node_ids=True,
        style={"node_size": "120px", "edge_size": "150px"},
        class_names=list(dataset_breast_cancer2.target_names),
        binary_formatting=True,
    )

    # Iris dataset (Multi-class Classification)

    dataset_iris = load_iris()
    features_iris = list(dataset_iris.feature_names)
    target_iris = "target"
    classes_iris = list(dataset_iris.target_names)
    df_iris = pd.DataFrame(dataset_iris.data)
    df_iris.columns = features_iris
    df_iris[target_iris] = list(dataset_iris.target)

    binary_tree(
        "iris",
        df_iris,
        features_iris,
        target_iris,
        show_node_ids=True,
        style={"node_size": "120px"},
        class_names=list(dataset_iris.target_names),
    )
