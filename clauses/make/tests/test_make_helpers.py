from contextlib import contextmanager
from typing import Optional

import pytest

from clauses.make.make_helpers import (
    build_properties_from_string,
    parse_node,
    find_nodes_from_statement,
)
from exceptions.statements.statements import (
    IllegalNodePropertyType,
    MissingNodeLabel,
    StatementError,
)
from models.enums.statement import Statement


@contextmanager
def does_not_raise():
    yield


class TestMakeHelpers:
    @pytest.mark.parametrize(
        "test_statement, expected_result, exception",
        [
            # fmt: off
            pytest.param("MAKE (node:NodeLabel)", (Statement.MAKE, 'node', 'NodeLabel', None), does_not_raise(), id='EXP PASS: Simple case'),
            pytest.param("MAKE (:NodeLabel)", (Statement.MAKE, None, 'NodeLabel', None), does_not_raise(), id='EXP PASS: Simple case, no handle'),
            pytest.param("MAKE (node:NodeLabel{name:'Name'})", (Statement.MAKE, 'node', 'NodeLabel', {'name': 'Name'}), does_not_raise(), id='EXP PASS: Simple dict params'),
            pytest.param("MAKE (:NodeLabel{uuid: '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'})", (Statement.MAKE, None, 'NodeLabel', {'uuid': '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'}), does_not_raise(), id='EXP PASS: simple case'),
            # pytest.param("MAKeeE (node:NodeLabel)", None, pytest.raises(StatementError), id='EXP EXCEPTION: Statement Error'),
            pytest.param("MAKE (node:)", None, pytest.raises(MissingNodeLabel), id='EXP EXCEPTION: Missing node label'),
        ],
    )
    def test_parse_node(
        self,
        test_statement: str,
        expected_result: tuple,
        exception: Optional[Exception],
    ) -> None:

        with exception:
            test = parse_node(test_statement)
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

    @pytest.mark.parametrize(
        "test_statement, expected_result, exception",
        [
            pytest.param(
                "MAKE (node:NodeLabel)", 1, does_not_raise(), id="EXP PASS: single case"
            ),
            pytest.param(
                "MAKE (node:NodeLabel)-[:rel]->(node2:NodeLabel)",
                2,
                does_not_raise(),
                id="EXP PASS: two nodes",
            ),
            pytest.param(
                "MAKE (node:NodeLabel)-[:cat)]->(node:NodeLabel{name:'Name'})-[:cat)]->(node:NodeLabel{uuid: '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'})",
                3,
                does_not_raise(),
                id="EXP PASS: three nodes",
            ),
            pytest.param(
                "MAKE ", 0, pytest.raises(Exception), id="EXP EXCEPTION: No nodes"
            ),
            pytest.param(
                "MAKeeE (node:NodeLabel)",
                0,
                pytest.raises(StatementError),
                id="EXP EXCEPTION: Statement Error",
            ),
        ],
    )
    def test_find_nodes_from_statement(
        self, test_statement: str, expected_result: int, exception: Optional[Exception]
    ) -> None:

        with exception:
            test = find_nodes_from_statement(test_statement)
            assert len(test) == expected_result
