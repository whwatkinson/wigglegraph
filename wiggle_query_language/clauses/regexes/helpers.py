EXTRA_ALLOWED_CHARS = "@"
ILLEGAL_CHARS = "#%&*$"


def get_all_params_regex() -> str:
    """
    Generates the regex for the parameters for a Node or Rel.
    :return: A regex expression.
    """
    return rf"[{{}}\w:\s,'\"\.\[\]{EXTRA_ALLOWED_CHARS}]+"


def get_handle_label_regex(name: str) -> str:
    # TODO factor out handle:label
    return rf"(?P<{name}_handle>\w*)\s*:\s*(?P<{name}_label>\w+)"


def get_node_pattern_regex(node_name: str) -> str:
    """
    Generates the regex patten for a Node
    :param node_name: The name of the Node.
    :return: A regex expression.
    """
    return rf"\s*(?P<{node_name}_node>\(\s*(?P<{node_name}_node_handle>\w*)\s*:\s*(?P<{node_name}_node_label>\w+)\s*(?P<{node_name}_node_props>{get_all_params_regex()})?\s*\)\s*)"


def get_rel_pattern_regex(rel_name: str) -> str:
    """
    Generates the regex patten for a Rel.
    :param rel_name: The name of the Rel.
    :return: A regex expression.
    """
    return rf"\s*(?P<{rel_name}_rel><?-*\[\s*(?P<{rel_name}_rel_handle>\w*)\s*:\s*(?P<{rel_name}_rel_label>\w*)\s*(?P<{rel_name}_rel_props>{get_all_params_regex()})?\s*]-*>?\s*)"


def get_nodes_rels_pattern_regex() -> str:
    """
    Creates a regex expression matching all permutations for up to three nodes and two relationships.

    Where a Node is:   (LeftHandle : NodeLabel {NodeProperties})
    Where a Rel is:    <?-[Rel1Handle : REL1LABEL {Rel1Properties}]->?

    Minimum match:  (left)
    Maximum match:  (left)-[REL1]->(middle)-[REL2]->(right)
    :return: A regex pattern that matches the above.

    """
    left_node_regex = get_node_pattern_regex("left")
    left_middle_rel_regex = get_rel_pattern_regex("left_middle")
    middle_node_regex = get_node_pattern_regex("middle")
    middle_right_rel_regex = get_rel_pattern_regex("middle_right")
    right_node_regex = get_node_pattern_regex("right")

    return rf"{left_node_regex}?{left_middle_rel_regex}?{middle_node_regex}?{middle_right_rel_regex}?{right_node_regex}?"
