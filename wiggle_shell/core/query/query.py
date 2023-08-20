from pathlib import Path

from exceptions.wiggleshell.query import NotAValidQueryError
from models.wigish import DbmsFilePath
from models.wql import ParsedQuery
from project_root import get_project_root
from wiggle_query_language.clauses.make import (
    make,
    parse_make_statement_from_query_string,
)
from wiggle_query_language.clauses.find import (
    find,
    parse_find_statement_from_query_string,
)


#  todo docstrings


def parse_query_string(query_string: str) -> ParsedQuery:
    """
    Take the raw query and parse it.
    :param query_string: The query from the User.
    :return: A parsed query.
    """

    make_parsed = parse_make_statement_from_query_string(query_string)
    find_parsed = parse_find_statement_from_query_string(query_string)
    criteria_parsed = None
    report_parsed = None

    query_parsed = ParsedQuery(
        make_parsed=make_parsed,
        find_parsed=find_parsed,
        criteria_parsed=criteria_parsed,
        report_parsed=report_parsed,
    )

    return query_parsed


def execute_query(parsed_query: ParsedQuery, dbms_file_path: DbmsFilePath) -> bool:
    if query_make := parsed_query.make_parsed:
        make(parsed_make_list=query_make, dbms_file_path=dbms_file_path)

    if query_find := parsed_query.find_parsed:
        find(
            parsed_find_list=query_find,
            dbms_file_path=dbms_file_path,
            parsed_criteria_list=parsed_query.criteria_parsed,
        )

    return True


def valid_query(query_string) -> bool:
    valid_query_set = {"make", "find", "adjust", "criteria", "report", "using"}
    query_string_set = set(query_string.lower().split(" "))

    return bool(valid_query_set.intersection(query_string_set))


def query(query_string: str, dbms_file_path: DbmsFilePath) -> bool:
    # todo remove \n and split on :
    # query_string.replace('\n', '').split(';')
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

    qry = """
    FIND (:NodeLabel{str: '2'})<-[]-(:NodeLabel{str2:"2_4"})-[rel2:REL2{float: 3.14}]->(:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]});
    """

    # qry = """
    #
    # MAKE (:NodeLabel{int: 1})<-[rel1:REL{str: '2'}]-(:NodeLabel{str2:"2_4"})-[rel1:REL{str: '2'}]->(:NodeLabel{str2:"2_4"});
    # """
    #
    # qry = """MAKE (c:NodeLabel {int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"], list2: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]});"""

    # qry = """
    #     MAKE (:NodeLabel1), (:NodeLabel2);
    #     MAKE (:NodeLabel3);
    #     """

    query(qry, TEST_DBMS)
