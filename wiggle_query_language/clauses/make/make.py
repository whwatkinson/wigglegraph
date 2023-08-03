from typing import Optional

from wiggle_query_language.clauses.make.make_patterns import MAKE_STATEMENT


def extract_make_statement_from_query(query_string: str) -> Optional[list[str]]:
    """
    Extracts the MAkE statement from the query body
    :param query_string:
    :return: A list of MAKE statements
    """
    matches = MAKE_STATEMENT.findall(query_string)

    if matches:
        return matches
    else:
        return None
