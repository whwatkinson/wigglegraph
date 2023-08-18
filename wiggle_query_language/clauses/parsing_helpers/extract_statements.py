from typing import Optional


from models.wql.enums.clauses import Clause
from wiggle_query_language.clauses.parsing_helpers.parse_statement_checks import (
    check_clause_spelling,
)
from wiggle_query_language.clauses.regexes.make.make_patterns import (
    MAKE_STATEMENT_ALL_REGEX,
)


def extract_all_statements(query_string: str, clause: Clause) -> Optional[list[str]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :param clause: The WQL clause.
    :return: A list of MAKE statements.
    """
    match clause:
        case Clause.MAKE:
            clause_all_regex = MAKE_STATEMENT_ALL_REGEX
        case Clause.FIND:
            clause_all_regex = None
        case _:
            raise Exception()

    if make_matches := [x.group() for x in clause_all_regex.finditer(query_string)]:
        return make_matches

    check_clause_spelling(query_string, clause)

    return None
