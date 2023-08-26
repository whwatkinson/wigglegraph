from re import compile, IGNORECASE

from wiggle_query_language.clauses.regexes.patterns.clause_helpers import (
    get_clause_all_regex,
    get_clause_permutations_regex,
)

CLAUSE = "REPORT"

# REPORT .*;
REPORT_STATEMENT_ALL_REGEX = compile(
    pattern=rf"{get_clause_all_regex(CLAUSE)}", flags=IGNORECASE
)

# TROPER (node1:NodeLabel);
REPORT_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    pattern=rf"{get_clause_permutations_regex(CLAUSE)}",
    flags=IGNORECASE,
)
