from typing import Optional

import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.regexes.patterns.properties import (
    ALL_PARAMS_KEY_VALUE_REGEX,
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
            test = ALL_PARAMS_KEY_VALUE_REGEX.findall(test_pattern)
            assert test == expected_result
