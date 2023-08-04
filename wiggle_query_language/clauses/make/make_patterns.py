from re import compile, IGNORECASE

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(
    r"\s*(?P<make_stmt_all>MAKE\s*\(.+\);)\s*", flags=IGNORECASE
)

# EKAM (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[adeijklmnorswz]{3,6})\s?\(", flags=IGNORECASE
)

# {first_name:'Harry' | last_name:'Watkinson' | favourite_number: 6 | favourite_color: 'green'}
MAKE_STATEMENT_CHECK_PARAMS_SYNTAX = compile(
    r"{\s*(?P<params>[\w:'\"\s|.,\-\[\]]+)\s*}"
)
