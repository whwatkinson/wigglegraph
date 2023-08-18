import pytest

from wiggle_query_language.clauses.regexes.patterns.patterns import (
    NODES_RELS_PATTERN_REGEX,
)

from wiggle_query_language.clauses.regexes.patterns.tests.cases_for_test_nodes_regex import (
    cases_for_test_nodes_rel_pattern,
)


class TestNodesRegex:
    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception", cases_for_test_nodes_rel_pattern
    )
    def test_nodes_rel_pattern_regex(
        self, test_pattern: str, expected_result: dict, exception
    ) -> None:
        test = [
            x.groupdict()
            for x in NODES_RELS_PATTERN_REGEX.finditer(test_pattern)
            if x.group()
        ]

        assert test == expected_result
