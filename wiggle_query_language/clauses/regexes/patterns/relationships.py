from re import compile, IGNORECASE

from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_all_params_regex,
)

# -[r:Rel]->
RELATIONSHIP_DIR_CHECK_REGEX = compile(
    rf"(?P<foo><?-+\[\s*\w*\s*:?\s*(?P<rel_name>\w*)\s*{get_all_params_regex()}-+>?)",
    flags=IGNORECASE,
)


# ()-->()
# UNNAMED_RELATIONSHIP_REGEX = compile(r"\)(?P<unnamed_rel><?-*>?)\(", flags=IGNORECASE)
