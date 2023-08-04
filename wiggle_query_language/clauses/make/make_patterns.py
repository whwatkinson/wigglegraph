from re import compile

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(r"\s*(?P<make_stmt_all>MAKE.+|make.+;)\s*")

# EKAM (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[MmNnJjKkAaSsZzIiOoLlEeWwRrDd]{3,6})\s?\("
)

# {first_name:'Harry' | last_name:'Watkinson' | favourite_number: 6 | favourite_color: 'green'}
MAKE_STATEMENT_CHECK_PARAMS_SYNTAX = compile(
    r"{\s*(?P<params>[\w:'\"\s|.,\-\[\]]+)\s*}"
)
