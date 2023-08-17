import pytest

from exceptions.wql.parsing import (
    ClauseSyntaxError,
)

# from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_statement_checks import (
    check_make_clause_spelling,
)


class TestWqlMake:
    @pytest.mark.parametrize(
        "test_make_stmt, exception",
        [
            pytest.param(
                "MAEK (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "eMAk (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "EMka (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "KMAe (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
            pytest.param(
                "EKAM (node:NodeLabel);",
                pytest.raises(ClauseSyntaxError),
                id="EXP EXEC",
            ),
        ],
    )
    def test_check_make_clause_spelling(self, test_make_stmt: str, exception) -> None:
        with exception:
            test = check_make_clause_spelling(test_make_stmt)
            assert test is True
