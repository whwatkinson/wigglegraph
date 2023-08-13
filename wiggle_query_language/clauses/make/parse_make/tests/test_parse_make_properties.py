import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_properties import (
    make_properties,
    string_to_correct_data_type,
    string_to_list_data_type,
)


class TestParseMakeProperties:
    @pytest.mark.parametrize(
        "test_stmt, expected_value, exception",
        [
            pytest.param("", "", does_not_raise(), id="EXP PASS: "),
        ],
    )
    def test_make_properties(
        self, test_stmt: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = make_properties(test_stmt)
            assert test == expected_value

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
