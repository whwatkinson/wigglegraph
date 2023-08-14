import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_properties import (
    make_properties,
    string_to_correct_data_type,
    string_to_list_data_type,
)


class TestParseMakeProperties:
    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_stmt, expected_value, exception",
        [
            pytest.param("""""", None, does_not_raise(), id="EXP PASS: No properties"),
            pytest.param(
                """{int: 1}""", {"int": 1}, does_not_raise(), id="EXP PASS: int"
            ),
            pytest.param(
                """{int: 1, str: '2'}""",
                {"int": 1, "str": "2"},
                does_not_raise(),
                id="EXP PASS: int, str",
            ),
            pytest.param(
                """{int: 1, str: '2', str2:"2_4"}""",
                {"int": 1, "str": "2", "str3": "2_4"},
                does_not_raise(),
                id="EXP PASS: No properties",
            ),
            pytest.param(
                """{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14], email: 'foo@bar.net}""",
                None,
                does_not_raise(),
                id="EXP PASS: No properties",
            ),
            pytest.param(
                """{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14], email: 'foo@bar.net}""",
                None,
                does_not_raise(),
                id="EXP PASS: No properties",
            ),
            pytest.param(
                """{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14], email: 'foo@bar.net}""",
                None,
                does_not_raise(),
                id="EXP PASS: No properties",
            ),
        ],
    )
    def test_make_properties(
        self, test_stmt: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = make_properties(test_stmt)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_stmt, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_string_to_correct_data_type(
        self, test_stmt: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = string_to_correct_data_type(test_stmt)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_stmt, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_string_to_list_data_type(
        self, test_stmt: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = string_to_list_data_type(test_stmt)
            assert test == expected_value
