from re import compile, IGNORECASE

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE)

NODE_PATTERN = compile(r"\s*\w*\s*:\s*\w+\s*", flags=IGNORECASE)
REL_PATTERN = compile(r"", flags=IGNORECASE)

PARAMS_PATTERN = compile(
    r"(?P<left_node>\(\s*(?P<left_node_handle>\w*)\s*:\s*(?P<left_node_label>\w+)\s*(?P<left_node_props>[{}\w:\s,'\".\[\]]+)?\s*\))\s*(?P<rel_left_middle><?-\[\s*(?P<rel_left_middle_handle>\w*)\s*:\s*(?P<rel_left_middle_label>\w*)\s*(?P<rel_lm_props>[{}\w:\s,'\".\[\]]+)?\s*]->?)?\s*(?P<middle_node>\(\s*(?P<middle_node_handle>\w*)\s*:\s*(?P<middle_node_label>\w+)\s*(?P<middle_node_props>[{}\w:\s,'\".\[\]]+)?\s*\)?)\s*(?P<rel_middle_right><?-\[\s*(?P<rel_middle_right_handle>\w*)\s*:\s*(?P<rel_middle_right_label>\w*)\s*(?P<rel_mr_props>[{}\w:\s,'\".\[\]]+)?\s*]->?)?\s*(?P<right_node>\(\s*(?P<right_node_handle>\w*)\s*:\s*(?P<right_node_label>\w+)\s*(?P<right_node_props>[{}\w:\s,'\".\[\]]+)?\s*\)?)?",
    flags=IGNORECASE,
)

# EKAM (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[adeijklmnorswz]{3,6})\s?\(", flags=IGNORECASE
)

# {first_name:'Harry' | last_name:'Watkinson' | favourite_number: 6 | favourite_color: 'green'}
MAKE_STATEMENT_CHECK_PARAMS_SYNTAX = compile(
    r"{\s*(?P<params>[\w:'\"\s|.,\-\[\]]+)\s*}"
)

# _ = r"(?P<left>\(\s*\w*\s*:\s*\w+\s*(?P<left_props>[{}\w:\s,'\"\.\[\]]+)?\s*\)(?P<rel>\s*<?-\[\s*\w*\s*:\s*\w*\s*(?P<rel_props>[{}\w:\s,'\"\.\[\]]+)?\s*\]->?\s*)?(?P<right>\(\s*\w*\s*:\s*\w+\s*(?P<right_props>[{}\w:\s,'\"\.\[\]]+)?\s*\)?))"
