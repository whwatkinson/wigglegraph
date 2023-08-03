from typing import Optional

from models.wql.raw_query import Make
from wiggle_query_language.clauses.make.make_patterns import MAKE_STATEMENT_BROAD


def check_params():
    pass


def check_make_syntax():
    pass


def extract_all_make_statements():
    pass


def extract_make_statement_from_query(query_string: str) -> Optional[list[Make]]:
    """
    Extracts the MAkE statement from the query body
    :param query_string:
    :return: A list of MAKE statements
    """

    matches = MAKE_STATEMENT_BROAD.findall(query_string)

    # TODO check for syntax errors and return early with helpful message

    matches_validated = matches

    if matches:
        return [Make(statement=stmt) for stmt in matches_validated]
    else:
        return None
