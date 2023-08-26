from typing import Optional

from models.wql import ParsedReport


def parse_report_statement_from_query_string(
    query_string: str,
) -> Optional[ParsedReport]:
    """
    Take the raw query and parse it.
    :param query_string: The query from the User.
    :return: A parsed query.
    """
    return dict()
