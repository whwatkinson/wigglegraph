from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes.helpers import (
    get_nodes_rels_pattern_regex,
    get_params_regex,
)


# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL = compile(r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE)


# (left:NodeLabel)-[r:LM]->(middle:NodeLabel)-[r2:MR]->(right:NodeLabel);
NODES_RELS_PATTERN = compile(
    rf"{get_nodes_rels_pattern_regex()}",
    flags=IGNORECASE,
)

# AKME (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX = compile(
    r"\s?(?P<make_syntax_error>[adeijklmnorswz]{3,6})\s?\(", flags=IGNORECASE
)

# {first_name:'Harry' , last_name:'Watkinson' , favourite_number: 6 , favourite_color: 'green'}

MAKE_STATEMENT_CHECK_PARAMS_SYNTAX = compile(
    rf"\s*{get_params_regex()}\s*",
    flags=IGNORECASE,
)

# <-[*:*]->
# TODO replace this with the get_params_regex
RELATIONSHIP_DIR_CHECK = compile(
    rf"<?-\[\s*\w*\s*:\s*\w*\s*{get_params_regex()}->?", flags=IGNORECASE
)

if __name__ == "__main__":
    print(get_nodes_rels_pattern_regex())

    stmt = """MAKE (left_node_handle1:LeftNodeLabel1{int: 1}), (left_node_handle2:LeftNodeLabel2{int: 1}), (left_node_handle3:LeftNodeLabel3{int: 1});"""
    foo = [x.groupdict() for x in NODES_RELS_PATTERN.finditer(stmt) if x.group()]

    a = 1
