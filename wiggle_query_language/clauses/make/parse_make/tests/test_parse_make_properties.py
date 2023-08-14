import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.make.parse_make.parse_make_properties import (
    make_properties,
    handle_null_property,
    handle_bool_property,
    handle_float_property,
    handle_int_property,
    handle_string_property,
    handle_list_property,
)


class TestParseMakeProperties:
    @pytest.mark.parametrize(
        "test_params_string, expected_value, exception",
        [
            pytest.param("", None, does_not_raise(), id="EXP PASS: No properties"),
            pytest.param(
                """{int: 1}""", {"int": 1}, does_not_raise(), id="EXP PASS: int"
            ),
            pytest.param(
                """{int: 1, float: 3.14}""",
                {"int": 1, "float": 3.14},
                does_not_raise(),
                id="EXP PASS: int, float",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true}""",
                {"int": 1, "float": 3.14, "bool": True},
                does_not_raise(),
                id="EXP PASS: int, float, bool",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false}""",
                {"int": 1, "float": 3.14, "bool": True, "bool2": False},
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null}""",
                {"int": 1, "float": 3.14, "bool": True, "bool2": False, "none": None},
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2'}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4"}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                    "str2": "2_4",
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str, str2",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5"}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                    "str2": "2_4",
                    "str3": "3 4 5",
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str, str2, str3",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net'}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                    "str2": "2_4",
                    "str3": "3 4 5",
                    "email": "foo@bar.net",
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str, str2, str3, email",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                    "str2": "2_4",
                    "str3": "3 4 5",
                    "email": "foo@bar.net",
                    "list": [1, 3.14, True, False, "2", "2_4", "3 4", "foo@bar.net"],
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str, str2, str3, email, list",
            ),
            pytest.param(
                """{int: 1, float: 3.14, bool: true, bool2: false, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"], list2: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]}""",
                {
                    "int": 1,
                    "float": 3.14,
                    "bool": True,
                    "bool2": False,
                    "none": None,
                    "str": "2",
                    "str2": "2_4",
                    "str3": "3 4 5",
                    "email": "foo@bar.net",
                    "list": [1, 3.14, True, False, "2", "2_4", "3 4", "foo@bar.net"],
                    "list2": [1, 3.14, True, False, "2", "2_4", "3 4", "foo@bar.net"],
                },
                does_not_raise(),
                id="EXP PASS: int, float, bool, bool2, none, str, str2, str3, email, list, list2",
            ),
        ],
    )
    def test_make_properties(
        self, test_params_string: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = make_properties(test_params_string)
            assert test == expected_value

    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("null", None, does_not_raise(), id="EXP PASS: Simple case")],
    )
    def test_handle_null_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_null_property(test_wg_property)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_handle_bool_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_bool_property(test_wg_property)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_handle_float_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_float_property(test_wg_property)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_handle_int_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_int_property(test_wg_property)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_handle_string_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_string_property(test_wg_property)
            assert test == expected_value

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "test_wg_property, expected_value, exception",
        [pytest.param("", "", does_not_raise(), id="EXP PASS: ")],
    )
    def test_handle_list_property(
        self, test_wg_property: str, expected_value: dict, exception
    ) -> None:
        with exception:
            test = handle_list_property(test_wg_property)
            assert test == expected_value
