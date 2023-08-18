from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.patterns.properties import (
    ALL_PROPERTIES_KEY_VALUE_REGEX,
    CHECK_PROPERTIES_SYNTAX_REGEX,
    PROPERTIES_LIST_VALUE_REGEX,
)


class TestPropertiesRegex:
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
            test = ALL_PROPERTIES_KEY_VALUE_REGEX.findall(test_pattern)
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
            test = CHECK_PROPERTIES_SYNTAX_REGEX.findall(test_pattern)
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
            test = PROPERTIES_LIST_VALUE_REGEX.findall(test_pattern)
            assert test == expected_result
