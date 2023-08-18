from re import compile, IGNORECASE

from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_all_params_regex,
    get_rel_pattern_regex,
)


# -[r:Rel]->
RELATIONSHIP_DIR_CHECK_REGEX = compile(
    pattern=rf"(?P<foo><?-+\[\s*\w*\s*:?\s*(?P<rel_name>\w*)\s*{get_all_params_regex()}-+>?)",
    flags=IGNORECASE,
)


# (NodeHandle: NodeLabel {NodeProps})
RELATIONSHIP_HANDLE_LABEL_PARAMS_REGEX = compile(
    pattern=rf"{get_rel_pattern_regex('this')}", flags=IGNORECASE
)

# ()-->()
# UNNAMED_RELATIONSHIP_REGEX = compile(r"\)(?P<unnamed_rel><?-*>?)\(", flags=IGNORECASE)
