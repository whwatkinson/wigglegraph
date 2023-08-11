from pathlib import Path


from exceptions.wiggleshell.query import NotAValidQueryError
from models.wql import ParsedMake, ParsedQuery
from models.wigshell import DbmsFilePath
from project_root import get_project_root
from wiggle_query_language.clauses.make.parse_make import (
    parse_make_statement_from_query_string,
)
from wiggle_query_language.clauses.make import make


def parse_query_string(query_string: str) -> ParsedQuery:
    """
    Take the raw query and parse it.
    :param query_string: The query from the User.
    :return: A parsed query.
    """

    make_parsed = parse_make_statement_from_query_string(query_string)
    find_parsed = None
    criteria_parsed = None
    report_parsed = None

    query_parsed = ParsedQuery(
        make_parsed=make_parsed,
        find_parsed=find_parsed,
        criteria_parsed=criteria_parsed,
        report_parsed=report_parsed,
    )

    return query_parsed


def handle_make(raw_query_make: list[ParsedMake], dbms_file_path: DbmsFilePath) -> bool:
    make(raw_query_make, dbms_file_path)

    return True


def execute_query(raw_query: ParsedQuery, dbms_file_path: DbmsFilePath) -> None:
    if raw_query_make := raw_query.make_parsed:
        handle_make(raw_query_make, dbms_file_path)

    return None


def valid_query(query_string) -> bool:
    valid_query_set = {"make", "find", "adjust", "criteria", "report", "using"}
    query_string_set = set(query_string.lower().split(" "))

    return bool(valid_query_set.intersection(query_string_set))


def query(query_string: str, dbms_file_path: DbmsFilePath) -> bool:
    if not valid_query(query_string) and False:
        raise NotAValidQueryError(
            "Query must contain MAKE, FIND, ADJUST, CRITERIA, REPORT, USING\n"
        )

    raw_query = parse_query_string(query_string)

    execute_query(raw_query, dbms_file_path)

    return True


if __name__ == "__main__":
    from testing import TEST_DBMS

    sample_query_fp = Path(
        f"{get_project_root()}/wiggle_query_language/example_queries/make_long.wql"
    )

    # with open(sample_query_fp, "r") as file:
    #     qry = file.read()

    qry = """MAKE (:NodeLabel{int: 1})-[rel1:REL{str: '2'}]->(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->(:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]}});"""

    query(qry, TEST_DBMS)
