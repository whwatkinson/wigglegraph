from typing import Optional

from models.wql import ParsedMake

from models.wql.enums.clauses import Clause
from wiggle_query_language.clauses.parsing_helpers.parse_statement_checks import (
    validate_statement,
)

from wiggle_query_language.clauses.regexes.patterns.patterns import (
    NODES_RELS_PATTERN_REGEX,
)
from wiggle_query_language.clauses.parsing_helpers.extract_statements import (
    extract_all_statements,
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


def parse_make_statement_from_query_string(
    query_string: str,
) -> Optional[list[ParsedMake]]:
    """
    Extracts the MAKE statement from the query body.
    :param query_string: The raw query.
    :return: A list of MAKE statements.
    """
    make_matches = extract_all_statements(query_string, Clause.MAKE)
    if not make_matches:
        return None
    if not validate_statement(make_matches):
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
