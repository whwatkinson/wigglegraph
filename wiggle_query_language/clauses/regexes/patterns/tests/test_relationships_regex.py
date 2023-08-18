from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.patterns.relationships import (
    RELATIONSHIP_DIR_CHECK_REGEX,
)


class TestRelationshipRegex:
    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                """MAKE (:NodeLabel)-[f:REL]->(foo:NodeLabel);""",
                [("-[f:REL]->", "REL")],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                """MAKE (:NodeLabel)---[f:REL]--->(foo:NodeLabel);""",
                [("---[f:REL]--->", "REL")],
                does_not_raise(),
                id="EXP PASS: 1 Match, long rel",
            ),
            pytest.param(
                """MAKE (:NodeLabel)-[]-(foo:NodeLabel);""",
                [("-[]-", "")],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                """MAKE (:NodeLabel)----[]---(foo:NodeLabel);""",
                [("----[]---", "")],
                does_not_raise(),
                id="EXP PASS: 1 Match, long rel not symmetrical",
            ),
            pytest.param(
                """MAKE (:NodeLabel)<-[f:FOO]->(foo:NodeLabel);""",
                [("<-[f:FOO]->", "FOO")],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                "REPORT (:NodeLabel);",
                [],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_relationship_dir_check_regex(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = RELATIONSHIP_DIR_CHECK_REGEX.findall(test_pattern)
            assert test == expected_result
