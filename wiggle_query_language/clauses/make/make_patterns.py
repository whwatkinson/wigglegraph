from re import compile

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(r"\s*(?P<make_stmt_all>[MAKEmake]{4}.+;)\s*")

# Mak (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel;
MAKE_STATEMENT_CHECK_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[MmNnJjKkAaSsZzIiOoLlEeWwRrDd]{3,6})\s?\("
)
