def get_params_regex(name: str) -> str:
    return rf"(?P<{name}>[{{}}\w:\s,'\".\[\]]+)"


def get_node_pattern_regex(node_name: str) -> str:
    node_params_regex = get_params_regex(f"{node_name}_node_props")

    return rf"\s*(?P<{node_name}_node>\(\s*(?P<{node_name}_node_handle>\w*)\s*:\s*(?P<{node_name}_node_label>\w+)\s*{node_params_regex}?\s*\)\s*)"


def get_rel_pattern_regex(rel_name: str) -> str:
    rel_params_regex = get_params_regex(f"{rel_name}_rel_props")
    return rf"\s*(?P<{rel_name}_rel><?-\[\s*(?P<{rel_name}_rel_handle>\w*)\s*:\s*(?P<{rel_name}_rel_label>\w*)\s*{rel_params_regex}?\s*]->?\s*)"


def get_nodes_rels_pattern_regex() -> str:
    left_node_regex = get_node_pattern_regex("left")
    left_middle_rel_regex = get_rel_pattern_regex("left_middle")
    middle_node_regex = get_node_pattern_regex("middle")
    middle_right_rel_regex = get_rel_pattern_regex("middle_right")
    right_node_regex = get_node_pattern_regex("right")

    return rf"{left_node_regex}?{left_middle_rel_regex}?{middle_node_regex}?{middle_right_rel_regex}?{right_node_regex}?"
