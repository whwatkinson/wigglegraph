from re import compile, IGNORECASE

from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_nodes_rels_pattern_regex,
)

# (left:NodeLabel{LeftParams})-[r:LM{LMParams}]->(middle:NodeLabel{MiddleParams})-[r2:MR{MRParams}]->(right:NodeLabel{RightParams});
NODES_RELS_PATTERN_REGEX = compile(
    rf"{get_nodes_rels_pattern_regex()}",
    flags=IGNORECASE,
)
