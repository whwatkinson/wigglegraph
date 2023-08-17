from exceptions.wql.parsing import (
    ClauseSyntaxError,
)
from wiggle_query_language.clauses.regexes.make.make_patterns import (
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)


def check_make_clause_spelling(query_string: str) -> bool:
    """
    Checks the MAKE for a spelling mistake.
    :param query_string: The extracted MAKE statements.
    :return: True or raises and exception.
    """

    if matches := MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX.findall(query_string):
        for match in matches:
            raise ClauseSyntaxError(
                message=f"SyntaxError: {match} was not recognised did you mean MAKE?"
            )

    return True
