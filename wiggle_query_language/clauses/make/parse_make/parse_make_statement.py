from typing import Optional

from models.wql import ParsedMake
from wiggle_query_language.clauses.make.parse_make.parse_make_statement_checks import (
    check_make_clause_syntax,
    validate_make_statement,
)
from wiggle_query_language.clauses.regexes.make_patterns import (
    MAKE_STATEMENT_ALL_REGEX,
    NODES_RELS_PATTERN_REGEX,
)


def build_parsed_make(statement: str) -> ParsedMake:
    """
    Handles building of the ParsedMake.
    :param statement: The raw make statement.
    :return: A ParsedMake Object.
    """
    parsed_pattern_dict = [
        x.groupdict() for x in NODES_RELS_PATTERN_REGEX.finditer(statement) if x.group()
    ]

    parsed_make = ParsedMake(
        raw_statement=statement, parsed_pattern_list=parsed_pattern_dict
    )

    return parsed_make


def extract_all_make_statements(query_string: str) -> Optional[list[str]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """

    if make_matches := [
        x.group() for x in MAKE_STATEMENT_ALL_REGEX.finditer(query_string)
    ]:
        return make_matches

    check_make_clause_syntax(query_string)

    return None


def parse_make_statement_from_query_string(
    query_string: str,
) -> Optional[list[ParsedMake]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """
    make_matches = extract_all_make_statements(query_string)
    if not make_matches:
        return None
    if not validate_make_statement(make_matches):
        raise Exception("make_matches says no")

    if make_matches:
        return [build_parsed_make(statement=stmt) for stmt in make_matches]
    else:
        return None


if __name__ == "__main__":
    qs = """"MAKE (left_node_handle:LeftNodeLabel { int: 1   , str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    # qs = "MAKE (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);"
    #
    # qs = """
    #     MAKE (n:NodeLabel)-[r:REL]->(m:NodeLabel);
    #     MAKE (n:NodeLabel2)-[r:REL]->(m:NodeLabel2);
    #     ADJUST n.name = "h" and m.name = "Wig";
    #     FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
    #     CRITERIA p.name = "Bar" or q.name = "Bar;
    #     REPORT wn(p), wn(q);
    #
    # """

    s = parse_make_statement_from_query_string(qs)
    a = 1
