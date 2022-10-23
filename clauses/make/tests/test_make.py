from contextlib import contextmanager
from typing import Generator, Optional

import pytest

from clauses.make.make import make_node
from clauses.make.make_helpers import parse_make_statment
from database.database import add_item_to_database, load_database
from exceptions.statements.statements import MissingNodeLabel, StatementError
from testing import TEST_DATABASE_FILE_PATH, TEST_WIGGLE_NUMBER_STATE_FILE_PATH


@contextmanager
def does_not_raise():
    yield


class TestMake:
    @pytest.mark.parametrize(
        "test_statement, expected_result_number_of_results, exception",
        [
            # fmt: off
            pytest.param("MAKE (node:NodeLabel)", 1, does_not_raise(), id='EXP PASS: Simple case'),
            pytest.param("MAKE (:NodeLabel)", 1, does_not_raise(), id='EXP PASS: Simple case, no handle'),
            pytest.param("MAKE (node:NodeLabel{name:'Name'})", 1, does_not_raise(), id='EXP PASS: Simple dict params'),
            pytest.param("MAKE (:NodeLabel{uuid: '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'})", 1, does_not_raise(), id='EXP PASS: simple case'),
            pytest.param("MAKeeE (node:NodeLabel)", None, pytest.raises(StatementError), id='EXP EXCEPTION: Statement Error'),
            pytest.param("MAKE (node:)", None, pytest.raises(MissingNodeLabel), id='EXP EXCEPTION: Missing node label'),
        ],
    )
    def test_make(
        self,
        test_statement: str,
        expected_result_number_of_results: int,
        exception: Optional[Exception],
        clear_database: Generator,
    ) -> None:
        with exception:
            parsed_statement = parse_make_statment(test_statement)
            node = make_node(parsed_statement, TEST_WIGGLE_NUMBER_STATE_FILE_PATH)
            add_item_to_database(TEST_DATABASE_FILE_PATH, node.export_node())

            test = load_database(TEST_DATABASE_FILE_PATH)

            assert len(test) == 1
