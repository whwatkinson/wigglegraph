from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_nodes_rels_pattern_regex,
)

from wiggle_query_language.clauses.regexes import ILLEGAL_CHARS

# MAKE *;
MAKE_STATEMENT_ALL_REGEX = compile(
    r"(?P<make_stmt_all>MAKE\s*\(.+\);)", flags=IGNORECASE
)


# (left:NodeLabel{LeftParams})-[r:LM{LMParams}]->(middle:NodeLabel{MiddleParams})-[r2:MR{MRParams}]->(right:NodeLabel{RightParams});
NODES_RELS_PATTERN_REGEX = compile(
    rf"{get_nodes_rels_pattern_regex()}",
    flags=IGNORECASE,
)

# AKME (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    (
        r"\s?(?P<make_syntax_error>maek|mkae|mkea|meak|meka|amke|amek|akme"
        r"|akem|aemk|aekm|kmae|kmea|kame|kaem|kema|keam|emak|emka|eamk|eakm|ekma|ekam)\s?\("
    ),
    flags=IGNORECASE,
)

# #%&*
ILLEGAL_CHARS_REGEX = compile(rf"[{ILLEGAL_CHARS}]", flags=IGNORECASE)


if __name__ == "__main__":
    print(get_nodes_rels_pattern_regex())

    stmt = """MAKE (left_node_handle1:LeftNodeLabel1{int: 1}), (left_node_handle2:LeftNodeLabel2{int: 1}), (left_node_handle3:LeftNodeLabel3{int: 1});"""
    foo = [x.groupdict() for x in NODES_RELS_PATTERN_REGEX.finditer(stmt) if x.group()]

    a = 1
