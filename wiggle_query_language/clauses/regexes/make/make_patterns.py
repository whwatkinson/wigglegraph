from re import IGNORECASE, compile


from wiggle_query_language.clauses.regexes.patterns.clause_helpers import (
    get_clause_all_regex,
    get_clause_permutations_regex,
)

# MAKE .*;
MAKE_STATEMENT_ALL_REGEX = compile(
    pattern=rf"{get_clause_all_regex('MAKE')}", flags=IGNORECASE
)


# MAEK (node1:NodeLabel);
MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    pattern=rf"{get_clause_permutations_regex('MAKE')}",
    flags=IGNORECASE,
)
