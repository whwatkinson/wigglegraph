from contextlib import contextmanager
from typing import Optional

import pytest

from clauses.make.make import build_properties_from_string, parse_make_statment
from exceptions.statements import (
    IllegalNodePropertyType,
    MissingNodeLabel,
    StatementError,
)
from models.enums.statement import Statement


@contextmanager
def does_not_raise():
    yield


class TestMake:
    @pytest.mark.parametrize(
        "test_statement, expected_result, exception",
        [
            # fmt: off
            pytest.param("MAKE (node:NodeLabel)", (Statement.MAKE, 'node', 'NodeLabel', None), does_not_raise(), id='EXP PASS: Simple case'),
            pytest.param("MAKE (:NodeLabel)", (Statement.MAKE, None, 'NodeLabel', None), does_not_raise(), id='EXP PASS: Simple case, no handle'),
            pytest.param("MAKE (node:NodeLabel{name:'Name'})", (Statement.MAKE, 'node', 'NodeLabel', {'name': 'Name'}), does_not_raise(), id='EXP PASS: Simple dict params'),
            pytest.param("MAKE (:NodeLabel{uuid: '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'})", (Statement.MAKE, None, 'NodeLabel', {'uuid': '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'}), does_not_raise(), id='EXP PASS: simple case'),
            pytest.param("MAKeeE (node:NodeLabel)", None, pytest.raises(StatementError), id='EXP EXCEPTION: Statement Error'),
            pytest.param("MAKE (node:)", None, pytest.raises(MissingNodeLabel), id='EXP EXCEPTION: Missing node label'),
        ],
    )
    def test_make(
        self,
        test_statement: str,
        expected_result: tuple,
        exception: Optional[Exception],
    ) -> None:

        with exception:
            test = parse_make_statment(test_statement)
            clause, handle, node_label, params = expected_result

            assert test.clause == clause
            assert test.handle == handle
            assert test.node_label == node_label
            assert test.belongings == params
            assert test.statement_string == test_statement

    @pytest.mark.parametrize(
        "params_string, expected_result, exception",
        [
            pytest.param(
                "foo: 'Bar'",
                {"foo": "Bar"},
                does_not_raise(),
                id="EXP PASS: string to string",
            ),
            pytest.param(
                "{foo: 6}", {"foo": 6}, does_not_raise(), id="EXP PASS: string to int"
            ),
            pytest.param(
                "foo: 3.14159",
                {"foo": 3.14159},
                does_not_raise(),
                id="EXP PASS: string to float",
            ),
            pytest.param(
                "foo: True",
                {"foo": True},
                does_not_raise(),
                id="EXP PASS: string to bool",
            ),
            pytest.param(
                "foo: ['bar', 'baz']",
                {"foo": ["bar", "baz"]},
                does_not_raise(),
                id="EXP PASS: string to list",
            ),
            pytest.param(
                "foo: 'Bar' | foo2: 6 | foo3: 3.14159 | foo4: True | foo5: ['bar', 'baz']",
                {
                    "foo": "Bar",
                    "foo2": 6,
                    "foo3": 3.14159,
                    "foo4": True,
                    "foo5": ["bar", "baz"],
                },
                does_not_raise(),
                id="EXP PASS: all supported datatypes",
            ),
            pytest.param(
                "foo: {foo: 'Bar}",
                None,
                pytest.raises(IllegalNodePropertyType),
                id="EXP EXCEPTION: Not allowed a nested data structure",
            ),
        ],
    )
    def test_build_properties_from_string(
        self, params_string: str, expected_result: dict, exception: Optional[Exception]
    ) -> None:
        with exception:
            test = build_properties_from_string(params_string)
            assert test == expected_result
