import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.report.parse_report.parse_report_statement import (
    parse_report_statement_from_query_string,
)


class TestParseReport:
    @pytest.mark.parametrize(
        "test_make_stmt, expected_value, exception",
        [pytest.param("""""", 1, does_not_raise())],
    )
    def test_parse_report_statement_from_query_string(
        self, test_make_stmt: str, expected_value: None, exception
    ) -> None:
        with exception:
            test = parse_report_statement_from_query_string(test_make_stmt)
            if test:
                assert len(test) == expected_value
            else:
                assert test is None
