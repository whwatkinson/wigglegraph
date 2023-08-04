from typing import Optional

from exceptions.wql.make import MakeClauseSyntaxError
from models.wql.raw_query import Make
from wiggle_query_language.clauses.make.make_patterns import (
    MAKE_STATEMENT_ALL,
    MAKE_STATEMENT_CHECK_SYNTAX,
)


def check_params():
    pass


def check_make_syntax(make_matches: list[str]) -> None:
    """
    Checks the syntax of the MAKE statement
    :param make_matches:
    :return:
    """

    query_string = "".join(make_matches)

    if matches := MAKE_STATEMENT_CHECK_SYNTAX.findall(query_string):
        for match in matches:
            raise MakeClauseSyntaxError(
                f"SyntaxError: {match} was not recognised did you mean MAKE?"
            )

    # TODO check params

    return None


def extract_all_make_statements(query_string: str) -> Optional[list[str]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements
    """

    if make_matches := MAKE_STATEMENT_ALL.findall(query_string):
        return make_matches

    # TODO check for syntax errors and return early with helpful message

    check_make_syntax(make_matches)

    return None


def extract_make_statement_from_query(query_string: str) -> Optional[list[Make]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """

    make_matches = extract_all_make_statements(query_string)

    check_make_syntax(make_matches)

    matches_validated = make_matches

    if make_matches:
        return [Make(statement=stmt) for stmt in matches_validated]
    else:
        return None
