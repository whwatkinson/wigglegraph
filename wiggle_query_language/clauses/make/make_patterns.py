from re import compile

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_BROAD = compile(r"\s*(?P<make>[MAKEmake]{4}.+;)\s*")

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel;
MAKE_STATEMENT_CHECK_SYNTAX = compile(r"")
