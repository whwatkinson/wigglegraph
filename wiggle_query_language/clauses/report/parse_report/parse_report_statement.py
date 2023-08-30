from typing import Optional

from exceptions.wql.clauses import MultipleClauseStatementsError
from exceptions.wql.report import FindReportHandleMissmatch
from models.wql import Clause, ParsedReport
from wiggle_query_language.clauses.parsing_helpers.extract_statements import (
    extract_all_statements,
)


def check_find_report_handles(find_handles: set[str], extracted_report: str) -> True:
    if find_handles:
        for find_handle in find_handles:
            if find_handle not in extracted_report:
                raise FindReportHandleMissmatch(
                    f"FIND handle {find_handle} was not found not in the ---> {extracted_report} <---"
                )

    return True


def validate_report_statement(find_handles: set[str], extracted_report: str) -> True:
    check_find_report_handles(find_handles, extracted_report)

    return True


def parse_report_statement_from_query_string(
    query_string: str,
    find_handles: Optional[set[str]] = None,
) -> Optional[ParsedReport]:
    """
    Take the raw query and parse it.
    :param query_string: The query from the User.
    :param find_handles: The handles from the parsed FIND statement.
    :return: A parsed query.
    """

    report_matches = extract_all_statements(query_string, Clause.REPORT)
    if not report_matches:
        return None
    if len(report_matches) > 1:
        raise MultipleClauseStatementsError(
            f"Only one {Clause.REPORT} clause is allowed per query"
        )

    extracted_report = report_matches[0]

    if not validate_report_statement(find_handles, extracted_report):
        raise Exception()

    return ParsedReport(
        raw_statement=extracted_report, extracted_report=extracted_report
    )


if __name__ == "__main__":
    q = """
        FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
        CRITERIA p.name = "Bar" or q.name = "Bar;
        REPORT p, r2, q;
    """

    parse_report_statement_from_query_string(q, {"p", "r2", "q"})
