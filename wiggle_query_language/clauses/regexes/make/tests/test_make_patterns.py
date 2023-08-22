from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.make.make_patterns import (
    MAKE_STATEMENT_ALL_REGEX,
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)


class TestMakePatterns:
    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                "MAKE (:NodeLabel{})-[:]->(foo:NodeLabel {} );",
                ["MAKE (:NodeLabel{})-[:]->(foo:NodeLabel {} );"],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                "FIND (:NodeLabel{})-[:]->(foo:NodeLabel {} );",
                [],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_make_statement_all_regex(
        self,
        test_pattern: str,
        expected_result: Optional[list[str]],
        exception,
    ) -> None:
        with exception:
            test = MAKE_STATEMENT_ALL_REGEX.findall(test_pattern)
            if test:
                assert test == expected_result

    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                "AKME (:NodeLabel{})-[:]->(foo:NodeLabel {} );",
                ["AKME"],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                "REPORT (:NodeLabel{})-[:]->(foo:NodeLabel {} );",
                [],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_make_statement_check_clause_syntax_regex(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX.findall(test_pattern)
            assert test == expected_result
