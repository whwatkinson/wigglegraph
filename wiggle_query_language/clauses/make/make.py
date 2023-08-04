from typing import Optional

from exceptions.wql.make import MakeClauseSyntaxError, MakeParamSyntaxError
from models.wql.raw_query import Make
from wiggle_query_language.clauses.make.make_patterns import (
    MAKE_STATEMENT_ALL,
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX,
    MAKE_STATEMENT_CHECK_PARAMS_SYNTAX,
)


def check_make_params(make_matches: list[str]) -> None:
    """
    Very crude check that the params match up with the colons
    :param make_matches:  The extracted MAKE statements.
    :return: None ar an Exception
    """

    for stmt in make_matches:

        param_string = MAKE_STATEMENT_CHECK_PARAMS_SYNTAX.findall(stmt)

        # TODO remove double loop, most of the time will be one match..
        for param_match in param_string:

            # params are delimited by a pipe (|)
            exp_param_count = param_match.count("|") + 1
            colon_count = param_match.count(":")

            if exp_param_count != colon_count:
                raise MakeParamSyntaxError(f"SyntaxError: {stmt} missing : or |")

    return None


def check_make_clause_syntax(make_matches: list[str]) -> None:
    """
    Checks the syntax of the MAKE statement.
    :param make_matches: The extracted MAKE statements.
    :return: None or an Exception
    """

    query_string = "".join(make_matches)

    if matches := MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX.findall(query_string):
        for match in matches:
            raise MakeClauseSyntaxError(
                f"SyntaxError: {match} was not recognised did you mean MAKE?"
            )

    # TODO check params
    check_make_params()

    return None


def extract_all_make_statements(query_string: str) -> Optional[list[str]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """

    if make_matches := MAKE_STATEMENT_ALL.findall(query_string):
        return make_matches

    # TODO check for syntax errors and return early with helpful message

    check_make_clause_syntax(make_matches)

    return None


def extract_make_statement_from_query(query_string: str) -> Optional[list[Make]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """

    make_matches = extract_all_make_statements(query_string)

    matches_validated = make_matches

    if make_matches:
        return [Make(statement=stmt) for stmt in matches_validated]
    else:
        return None
