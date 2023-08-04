from pathlib import Path

from project_root import get_project_root
from models.wql.raw_query import RawQuery, RawMake
from wiggle_query_language.clauses.make.make import extract_make_statement_from_query


def parse_query_string(query_string: str) -> RawQuery:
    """
    Take the raw query
    :param query_string:
    :return:
    """

    make = extract_make_statement_from_query(query_string)
    find = None
    criteria = None
    report = None

    query_parsed = RawQuery(make=make, find=find, criteria=criteria, report=report)

    return query_parsed


def handle_make(raw_query_make: list[RawMake]):
    print(raw_query_make)


def execute_query(raw_query: RawQuery) -> None:

    if raw_query_make := raw_query.make:
        handle_make(raw_query_make)

    return None


def valid_query(query_string) -> bool:
    valid_query_set = {"make", "find", "adjust", "criteria", "Report"}
    query_string_set = set(query_string.lower().split(" "))

    return bool(valid_query_set.intersection(query_string_set))


def query(query_string: str) -> None:

    if not valid_query(query_string):
        # todo make this an exception
        print("Please enter a valid query..\n")
        return None

    raw_query = parse_query_string(query_string)

    execute_query(raw_query)


if __name__ == "__main__":
    sample_query_fp = Path(
        f"{get_project_root()}/wiggle_query_language/example_queries/make.wql"
    )

    with open(sample_query_fp, "r") as file:
        qry = file.read()

    qry = "MAKE (n:Person);MAKE (n:Person);"

    print(parse_query_string(qry))
