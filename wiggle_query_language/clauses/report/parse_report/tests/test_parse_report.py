from typing import Optional

import pytest

from exceptions.wql.clauses import MultipleClauseStatementsError
from exceptions.wql.report import FindReportHandleMissmatch
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.report.parse_report.parse_report_statement import (
    parse_report_statement_from_query_string,
)


class TestParseReport:
    @pytest.mark.parametrize(
        "test_report_stmt, test_find_handles, expected_value, exception",
        [
            pytest.param("REPORT *;", None, 1, does_not_raise(), id="EXP PASS: *"),
            pytest.param(
                "REPORT foo;", {"foo"}, 1, does_not_raise(), id="EXP PASS: Single label"
            ),
            pytest.param(
                "REPORT foo.bar;",
                {"foo"},
                1,
                does_not_raise(),
                id="EXP PASS: Single label with prop",
            ),
            pytest.param(
                "REPORT foo.bar, foo.baz, foo.qux;",
                {"foo"},
                1,
                does_not_raise(),
                id="EXP PASS: Single label with multiple props",
            ),
            pytest.param(
                "REPORT r;", {"r"}, 1, does_not_raise(), id="EXP PASS: Rel label"
            ),
            pytest.param(
                "REPORT r.bar;",
                {"r"},
                1,
                does_not_raise(),
                id="EXP PASS: Rel label with single prop",
            ),
            pytest.param(
                "REPORT r.bar, r.baz, r.qux;",
                {"r"},
                1,
                does_not_raise(),
                id="EXP PASS: Rel label with multiple props",
            ),
            pytest.param(
                "REPORT foo.bar, foo.baz, foo.qux, r.bar, r.baz, r.qux;",
                {"foo", "r"},
                1,
                does_not_raise(),
                id="EXP PASS: Mix of Node and rels with props",
            ),
            pytest.param(
                """
                FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
                CRITERIA p.name = "Bar" or q.name = "Bar;
                REPORT p, r2, q;
                """,
                {"p", "r2", "q"},
                1,
                does_not_raise(),
                id="EXP PASS: Mix of Node and rels with props",
            ),
            pytest.param(
                "REPORT bar;",
                {"foo"},
                0,
                pytest.raises(FindReportHandleMissmatch),
                id="EXP EXEC: Missmatch handles",
            ),
            pytest.param(
                "REPORT bar;\nREPORT bar;",
                {"foo"},
                0,
                pytest.raises(MultipleClauseStatementsError),
                id="EXP EXEC: Multiple REPORTS",
            ),
        ],
    )
    def test_parse_report_statement_from_query_string(
        self,
        test_report_stmt: str,
        test_find_handles: Optional[set[str]],
        expected_value: None,
        exception,
    ) -> None:
        with exception:
            test = parse_report_statement_from_query_string(
                test_report_stmt, test_find_handles
            )
            if test:
                assert len(test) == expected_value
            else:
                assert test is None
