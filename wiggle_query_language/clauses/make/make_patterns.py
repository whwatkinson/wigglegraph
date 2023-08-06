from re import compile, IGNORECASE

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(
    r"\s*(?P<make_stmt_all>MAKE\s*\(.+\);)\s*", flags=IGNORECASE
)

NODE_PATTERN = compile(r"\s*\w*\s*:\s*\w+\s*", flags=IGNORECASE)
REL_PATTERN = compile(r"", flags=IGNORECASE)
PARAMS_PATTERN = compile(r"", flags=IGNORECASE)


MAKE_STATEMENT_ALL_V2 = compile(
    r"(?P<left>\(\s*\w*\s*:\s*\w+\s*(?P<left_props>[{}\w:\s,'\".\[\]]+)?\s*\))(?P<rel>\s*<?-\[\s*\w*\s*:\s*\w*\s*(?P<rel_props>[{}\w:\s,'\".\[\]]+)?\s*]->?\s*)?(?P<middle>\(\s*\w*\s*:\s*\w+\s*(?P<middle_props>[{}\w:\s,'\".\[\]]+)?\s*\)?)(?P<re2l>\s*<?-\[\s*\w*\s*:\s*\w*\s*(?P<rel_2_props>[{}\w:\s,'\".\[\]]+)?\s*]->?\s*)?(?P<right2>\(\s*\w*\s*:\s*\w+\s*(?P<right_props>[{}\w:\s,'\".\[\]]+)?\s*\)?)?",
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
