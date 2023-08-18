from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.make.make_patterns import (
    ILLEGAL_CHARS_REGEX,
    MAKE_STATEMENT_ALL_REGEX,
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
)
from wiggle_query_language.clauses.regexes.patterns.patterns_helpers import (
    get_nodes_rels_pattern_regex,
)


class TestMakeRePatterns:
    def test_get_pattern_regex(self) -> None:
        # regression test
        exp_pattern = r"\s*(?P<left_node>\(\s*(?P<left_node_handle>\w*)\s*:\s*(?P<left_node_label>\w+)\s*(?P<left_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<left_middle_rel><?-*\[\s*(?P<left_middle_rel_handle>\w*)\s*:?\s*(?P<left_middle_rel_label>\w*)\s*(?P<left_middle_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]-*>?\s*)?\s*(?P<middle_node>\(\s*(?P<middle_node_handle>\w*)\s*:\s*(?P<middle_node_label>\w+)\s*(?P<middle_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<middle_right_rel><?-*\[\s*(?P<middle_right_rel_handle>\w*)\s*:?\s*(?P<middle_right_rel_label>\w*)\s*(?P<middle_right_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]-*>?\s*)?\s*(?P<right_node>\(\s*(?P<right_node_handle>\w*)\s*:\s*(?P<right_node_label>\w+)\s*(?P<right_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?"
        test_pattern = rf"{get_nodes_rels_pattern_regex()}"

        assert test_pattern == exp_pattern

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
