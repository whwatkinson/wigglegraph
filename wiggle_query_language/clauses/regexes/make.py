from re import IGNORECASE, compile


def get_node_pattern_regex(node_name: str) -> str:
    return rf"(?P<{node_name}_node>\(\s*(?P<{node_name}_node_handle>\w*)\s*:\s*(?P<{node_name}_node_label>\w+)\s*(?P<{node_name}_node_props>[{{}}\w:\s,'\".\[\]]+)?\s*\)?)"


def get_rel_pattern_regex(rel_name: str) -> str:
    return rf"(?P<{rel_name}_rel><?-\[\s*(?P<{rel_name}_rel_handle>\w*)\s*:\s*(?P<{rel_name}_rel_label>\w*)\s*(?P<{rel_name}_rel_props>[{{}}\w:\s,'\".\[\]]+)?\s*]->?)"


def get_pattern_regex() -> str:
    left_node_regex = get_node_pattern_regex("left")
    middle_node_regex = get_node_pattern_regex("middle")
    right_node_regex = get_node_pattern_regex("right")
    left_middle_rel_regex = get_rel_pattern_regex("left_middle")
    middle_right_rel_regex = get_rel_pattern_regex("middle_right")

    return rf"{left_node_regex}\s*{left_middle_rel_regex}?\s*{middle_node_regex}\s*{middle_right_rel_regex}?\s*{right_node_regex}?"


# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE)


NODES_RELS_PATTERN = compile(
    rf"{get_pattern_regex()}",
    flags=IGNORECASE,
)

# AKME (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[adeijklmnorswz]{3,6})\s?\(", flags=IGNORECASE
)

# {first_name:'Harry' , last_name:'Watkinson' , favourite_number: 6 , favourite_color: 'green'}
MAKE_STATEMENT_CHECK_PARAMS_SYNTAX = compile(
    r"{\s*(?P<params>[\w:'\"\s|.,\-\[\]]+)\s*}",
    flags=IGNORECASE,
)


if __name__ == "__main__":
    print(get_pattern_regex())
