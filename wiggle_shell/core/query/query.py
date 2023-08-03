from models.wigshell.query import ParsedQuery


from wiggle_query_language.clauses.make.make import extract_make_statement_from_query


def parse_raw_query(query_string: str) -> ParsedQuery:

    make = extract_make_statement_from_query(query_string)
    find = None
    criteria = None
    report = None

    query_parsed = ParsedQuery(make=make, find=find, criteria=criteria, report=report)

    return query_parsed
