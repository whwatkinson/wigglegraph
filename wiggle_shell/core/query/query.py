from pathlib import Path

from project_root import get_project_root
from models.wql.raw_query import RawQuery
from wiggle_query_language.clauses.make.make import extract_make_statement_from_query


def parse_query_string(query_string: str) -> RawQuery:

    make = extract_make_statement_from_query(query_string)
    find = None
    criteria = None
    report = None

    query_parsed = RawQuery(make=make, find=find, criteria=criteria, report=report)

    return query_parsed


if __name__ == "__main__":
    sample_query_fp = Path(
        f"{get_project_root()}/wiggle_query_language/example_queries/make.wql"
    )

    with open(sample_query_fp, "r") as file:
        qry = file.read()

    print(parse_query_string(qry))
