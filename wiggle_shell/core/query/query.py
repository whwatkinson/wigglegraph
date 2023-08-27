import logging
from pathlib import Path

from exceptions.wiggleshell.query import NotAValidQueryError
from wiggle_graph_logger.graph_logger import graph_logger
from models.wigish import GDBMSFilePath
from models.wql import ParsedQuery
from project_root import get_project_root
from wiggle_query_language.clauses.find import (
    find,
    parse_find_statement_from_query_string,
)
from wiggle_query_language.clauses.make import (
    make,
    parse_make_statement_from_query_string,
)
from wiggle_query_language.clauses.report import (
    report,
    parse_report_statement_from_query_string,
)

#  todo docstrings

graph_logger.setLevel(logging.WARNING)


def parse_query_string(query_string: str) -> ParsedQuery:
    """
    Take the raw query and parse it.
    :param query_string: The query from the User.
    :return: A parsed query.
    """

    make_parsed = parse_make_statement_from_query_string(query_string)
    find_parsed = parse_find_statement_from_query_string(query_string)
    criteria_parsed = None

    find_query_handles = find_parsed.parsed_pattern.pattern_handles
    report_parsed = parse_report_statement_from_query_string(
        query_string, find_handles=find_query_handles
    )

    query_parsed = ParsedQuery(
        make_parsed=make_parsed,
        find_parsed=find_parsed,
        criteria_parsed=criteria_parsed,
        report_parsed=report_parsed,
    )

    return query_parsed


def execute_query(parsed_query: ParsedQuery, gdbms_file_path: GDBMSFilePath) -> bool:
    if query_make := parsed_query.make_parsed:
        make(parsed_make_list=query_make, gdbms_file_path=gdbms_file_path)

    if query_find := parsed_query.find_parsed:
        found = find(
            parsed_find=query_find,
            gdbms_file_path=gdbms_file_path,
            parsed_criteria=parsed_query.criteria_parsed,
        )
        # when theses a FIND there is a way
        if query_report := parsed_query.report_parsed:
            report(
                parsed_report=query_report, found=found, gdbms_file_path=gdbms_file_path
            )
    else:
        raise Exception("You must provide a FIND with a RETURN! FUBAR")

    return True


def valid_query(query_string) -> bool:
    valid_query_set = {"make", "find", "adjust", "criteria", "report", "using"}
    query_string_set = set(query_string.lower().split(" "))

    return bool(valid_query_set.intersection(query_string_set))


def query(query_string: str, gdbms_file_path: GDBMSFilePath) -> bool:
    # todo remove \n and split on :
    # query_string.replace('\n', '').split(';')
    if not valid_query(query_string) and False:
        raise NotAValidQueryError(
            "Query must contain MAKE, FIND, ADJUST, CRITERIA, REPORT, USING\n"
        )

    raw_query = parse_query_string(query_string)

    execute_query(raw_query, gdbms_file_path)

    return True


if __name__ == "__main__":
    from testing import TEST_DBMS

    sample_query_fp = Path(
        f"{get_project_root()}/wiggle_query_language/example_queries/make_long.wql"
    )

    # with open(sample_query_fp, "r") as file:
    #     qry = file.read()

    qry = """
    FIND (:NodeLabel{str: '2'})<-[]-(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->(:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]});
    """

    qry = """FIND (left_node_handle:LeftNodeLabel{none: null, int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})<-[lm:{int: 1, str: '2', str2:"2_4", float: 3.14, bool: false, none: null, list: [1, '2', "2_4", "3 4", 3.14]}]-(middle_node_label:MiddleNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[rmr:RELMR{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(right_node_label:RightNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, none: null, list: [1, '2', "2_4", "3 4", 3.14]} );"""

    query(qry, TEST_DBMS)
