from models.wigshell.query import ParsedQuery


def parse_raw_query(query_string: str) -> ParsedQuery:

    print(query_string)

    make = None
    find = None
    criteria = None
    report = None

    query_parsed = ParsedQuery(make=make, find=find, criteria=criteria, report=report)

    return query_parsed
