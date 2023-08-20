from typing import Optional

from exceptions.wql.find import MultipleFindStatementsError
from models.wql import ParsedFind, Clause
from wiggle_query_language.clauses.parsing_helpers.parse_statement_checks import (
    validate_statement,
)

from wiggle_query_language.clauses.regexes.patterns.patterns import (
    NODES_RELS_PATTERN_REGEX,
)
from wiggle_query_language.clauses.parsing_helpers.extract_statements import (
    extract_all_statements,
)


def build_parsed_find(statement: str) -> ParsedFind:
    """
    Handles building of the ParsedMake.
    :param statement: The raw FIND statement.
    :return: A ParsedFind Object.
    """
    parsed_pattern_dict = [
        x.groupdict() for x in NODES_RELS_PATTERN_REGEX.finditer(statement) if x.group()
    ]

    parsed_make = ParsedFind(
        raw_statement=statement, parsed_pattern_list=parsed_pattern_dict[0]
    )

    return parsed_make


def parse_find_statement_from_query_string(
    query_string: str,
) -> Optional[ParsedFind]:
    """
    Extracts the FIND statement from the query body.
    :param query_string: The raw query.
    :return: A list of ParsedFind.
    """
    find_matches = extract_all_statements(query_string, Clause.FIND)
    if not find_matches:
        return None
    if len(find_matches) > 1:
        raise MultipleFindStatementsError(
            "Only one FIND clause is allowed per statement"
        )
    if not validate_statement(find_matches):
        raise Exception("find_matches says no")

    if find_matches:
        return build_parsed_find(statement=find_matches[0])
    else:
        return None


if __name__ == "__main__":
    qs = """"FIND (left_node_handle:LeftNodeLabel { int: 1   , str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    # qs = "FIND (:NodeLabel{int: 1})-[:]->(foo:NodeLabel);"
    #
    # qs = """
    #     FIND (n:NodeLabel)-[r:REL]->(m:NodeLabel);
    #     FIND (n:NodeLabel2)-[r:REL]->(m:NodeLabel2);
    #     ADJUST n.name = "h" and m.name = "Wig";
    #     FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
    #     CRITERIA p.name = "Bar" or q.name = "Bar;
    #     REPORT wn(p), wn(q);
    #
    # """

    s = parse_find_statement_from_query_string(qs)
    a = 1
