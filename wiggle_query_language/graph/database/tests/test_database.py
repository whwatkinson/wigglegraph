from typing import Generator

import pytest

from exceptions.wql.database import NodeExistsError
from testing import DATABASE_TEST_FILE_PATH
from wiggle_query_language.graph.database.database import (
    add_item_to_database,
    load_database,
)


@pytest.mark.skip
class TestDataBase:
    def test_database(self, clear_database_test: Generator) -> None:
        # Check the db is empty
        test = load_database(file_path=DATABASE_TEST_FILE_PATH)

        assert len(test) == 0

        # Insert a record
        item = {
            109: {
                "wiggle_number": 19,
                "node_label": "NodeLabel",
                "created_at": 1666534101.384132,
                "updated_at": None,
                "belongings": {"uuid": "7e48f6ae-b25a-4634-91af-b1fb67b90ad9"},
                "relations": None,
            }
        }
        add_item_to_database(file_path=DATABASE_TEST_FILE_PATH, item=item)
        test = load_database(file_path=DATABASE_TEST_FILE_PATH)

        assert len(test) == 1

        # Insert a same record

        with pytest.raises(NodeExistsError):
            add_item_to_database(file_path=DATABASE_TEST_FILE_PATH, item=item)
