def node_label_is_in_index(
    node_label_set: set[str], node_label_index: set[str]
) -> bool:
    return bool(node_label_set.intersection(node_label_index))
