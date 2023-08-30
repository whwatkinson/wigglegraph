from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes.patterns.clause_helpers import (
    get_clause_permutations,
)

CLAUSE = "REPORT"

# REPORT .*;
REPORT_STATEMENT_ALL_REGEX = compile(
    pattern=rf"(?P<report_stmt_all>({CLAUSE.upper()}|{CLAUSE.lower()}).+;)",
    flags=IGNORECASE,
)

# TROPER foo;
REPORT_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX = compile(
    pattern=rf"(?P<report_stmt_all>({get_clause_permutations(CLAUSE)}).+;)",
    flags=IGNORECASE,
)
