from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes.make_patterns_helpers import (
    EXTRA_ALLOWED_CHARS,
    ILLEGAL_CHARS,
    get_all_params_regex,
    get_nodes_rels_pattern_regex,
)

# MAKE (node1:NodeLabel)-[rel1:REL]->(node2:NodeLabel);
MAKE_STATEMENT_ALL_REGEX = compile(
    r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE
)


# (left:NodeLabel)-[r:LM]->(middle:NodeLabel)-[r2:MR]->(right:NodeLabel);
NODES_RELS_PATTERN_REGEX = compile(
    rf"{get_nodes_rels_pattern_regex()}",
    flags=IGNORECASE,
)

# AKME (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    r"\s?(?P<make_syntax_error>[adeijklmnorswz]{3,6})\s?\(", flags=IGNORECASE
)

# #%&*
ILLEGAL_CHARS_REGEX = compile(rf"[{ILLEGAL_CHARS}]", flags=IGNORECASE)

# {first_name:'Harry' , last_name:'Watkinson' , favourite_number: 6 , favourite_color: 'green'}
MAKE_STATEMENT_CHECK_PARAMS_SYNTAX_REGEX = compile(
    rf"(?P<all_props>{{[\w:\s,'\"\.\[\]{EXTRA_ALLOWED_CHARS}]+}})",
    flags=IGNORECASE,
)

# <-[*:*]->
RELATIONSHIP_DIR_CHECK_REGEX = compile(
    rf"(?P<foo><?-+\[\s*\w*\s*:?\s*(?P<rel_name>\w*)\s*{get_all_params_regex()}-+>?)",
    flags=IGNORECASE,
)

# foo: 1, bar: "2"
NOT_LIST_KEY_VALUE_REGEX = compile(
    rf"(?P<property_name>\w+)\s*:\s*(?P<property_value>[\w'\"\.{EXTRA_ALLOWED_CHARS}]+)",
    flags=IGNORECASE,
)

# int: 1, float: 3.14, bool: true, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [
ALL_PARAMS_KEY_VALUE_REGEX = compile(
    r"(?P<property_name>\w+)\s*:\s*(?P<property_value>(?P<none>null)|(?P<bool>true|false)|(?P<float>\d+\.\d+)|(?P<int>[0-9]+)|(?P<list>\[[\w,\s'\"\.@\+]+\])|(?P<string>[\w+\'\"@\.\s]+))",
    flags=IGNORECASE,
)

# baz: [1, 2, 3, 4]
LIST_KEY_VALUE_REGEX = compile(
    rf"(?P<property_name>[\w]+)\s*:\s*(?P<property_value>\[[\w,\s'\"\.{EXTRA_ALLOWED_CHARS}]+])",
    flags=IGNORECASE,
)

# [1, '2', "2_4", "3 4", 3.14]
PARAM_LIST_VALUE_REGEX = compile(
    rf"(?P<list_value>\[[\w,\s'\"\.{EXTRA_ALLOWED_CHARS}]+])", flags=IGNORECASE
)


if __name__ == "__main__":
    print(get_nodes_rels_pattern_regex())

    stmt = """MAKE (left_node_handle1:LeftNodeLabel1{int: 1}), (left_node_handle2:LeftNodeLabel2{int: 1}), (left_node_handle3:LeftNodeLabel3{int: 1});"""
    foo = [x.groupdict() for x in NODES_RELS_PATTERN_REGEX.finditer(stmt) if x.group()]

    a = 1
