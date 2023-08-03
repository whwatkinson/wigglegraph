from re import compile

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT = compile(r"(?P<make>[MAKEmake]{4}.+;)")
