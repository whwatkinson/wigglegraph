from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.make_patterns import (
    ALL_PARAMS_KEY_VALUE_REGEX,
    ILLEGAL_CHARS_REGEX,
    MAKE_STATEMENT_ALL_REGEX,
    MAKE_STATEMENT_CHECK_CLAUSE_SYNTAX_REGEX,
    MAKE_STATEMENT_CHECK_PARAMS_SYNTAX_REGEX,
    NODES_RELS_PATTERN_REGEX,
    PARAM_LIST_VALUE_REGEX,
    RELATIONSHIP_DIR_CHECK_REGEX,
)
from wiggle_query_language.clauses.regexes.make_patterns_helpers import (
    get_nodes_rels_pattern_regex,
)
from wiggle_query_language.clauses.regexes.tests.cases_for_test_re import (
    cases_for_test_nodes_rel_pattern,
)


class TestMakeRePatterns:
    def test_get_pattern_regex(self) -> None:
        # regression test
        exp_pattern = r"\s*(?P<left_node>\(\s*(?P<left_node_handle>\w*)\s*:\s*(?P<left_node_label>\w+)\s*(?P<left_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<left_middle_rel><?-*\[\s*(?P<left_middle_rel_handle>\w*)\s*:\s*(?P<left_middle_rel_label>\w*)\s*(?P<left_middle_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]-*>?\s*)?\s*(?P<middle_node>\(\s*(?P<middle_node_handle>\w*)\s*:\s*(?P<middle_node_label>\w+)\s*(?P<middle_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?\s*(?P<middle_right_rel><?-*\[\s*(?P<middle_right_rel_handle>\w*)\s*:\s*(?P<middle_right_rel_label>\w*)\s*(?P<middle_right_rel_props>[{}\w:\s,'\"\.\[\]@]+)?\s*]-*>?\s*)?\s*(?P<right_node>\(\s*(?P<right_node_handle>\w*)\s*:\s*(?P<right_node_label>\w+)\s*(?P<right_node_props>[{}\w:\s,'\"\.\[\]@]+)?\s*\)\s*)?"
        test_pattern = rf"{get_nodes_rels_pattern_regex()}"

        assert test_pattern == exp_pattern

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
                """MAKE (:NodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14]});""",
                [
                    """{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14]}"""
                ],
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
    def test_make_statement_check_params_syntax(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = MAKE_STATEMENT_CHECK_PARAMS_SYNTAX_REGEX.findall(test_pattern)
            assert test == expected_result

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

    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                """{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, none: null, list: [1, '2', "2_4", "3 4", 3.14]}""",
                ['[1, \'2\', "2_4", "3 4", 3.14]'],
                does_not_raise(),
                id="EXP PASS: 1 Match",
            ),
            pytest.param(
                """{int: 1, str: '2', str2:"2_4", float: 3.14, none: null, bool: false]}""",
                [],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_param_list_value_regex(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = PARAM_LIST_VALUE_REGEX.findall(test_pattern)
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

    @pytest.mark.parametrize(
        "test_pattern, expected_result, exception",
        [
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net', pn: '+447541254566', list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net", "+447541254566"]}""",
                [
                    ("int", "1", "", "", "", "1", "", ""),
                    ("float", "3.14", "", "", "3.14", "", "", ""),
                    ("bool", "true", "", "true", "", "", "", ""),
                    ("bool2", "false", "", "false", "", "", "", ""),
                    ("none", "null", "null", "", "", "", "", ""),
                    ("str", "'2'", "", "", "", "", "", "'2'"),
                    ("str2", '"2_4"', "", "", "", "", "", '"2_4"'),
                    ("str3", '"3 4 5"', "", "", "", "", "", '"3 4 5"'),
                    ("email", "'foo@bar.net'", "", "", "", "", "", "'foo@bar.net'"),
                    ("pn", "'+447541254566'", "", "", "", "", "", "'+447541254566'"),
                    (
                        "list",
                        '[1, 3.14, true, false, \'2\', "2_4", "3 4", "foo@bar.net", "+447541254566"]',
                        "",
                        "",
                        "",
                        "",
                        '[1, 3.14, true, false, \'2\', "2_4", "3 4", "foo@bar.net", "+447541254566"]',
                        "",
                    ),
                ],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
            pytest.param(
                "{int: 1}",
                [("int", "1", "", "", "", "1", "", "")],
                does_not_raise(),
                id="EXP PASS: No Match",
            ),
        ],
    )
    def test_all_params_key_value_regex(
        self, test_pattern: str, expected_result: Optional[list[str]], exception
    ) -> None:
        with exception:
            test = ALL_PARAMS_KEY_VALUE_REGEX.findall(test_pattern)
            assert test == expected_result
