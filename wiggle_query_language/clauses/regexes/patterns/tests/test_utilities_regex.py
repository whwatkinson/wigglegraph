from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.patterns.utilities import ILLEGAL_CHARS_REGEX


class TestUtilitiesRegex:
    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                """MAKE (:NodeLabel$)-[#:%]->(foo:NodeLabel*);""",
                ["$", "#", "%", "*"],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                """MAKE (:NodeLabel)-[:]->(foo:NodeLabel);""",
                [],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_illegal_chars_regex(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = ILLEGAL_CHARS_REGEX.findall(test_pattern)
            assert test == expected_result
