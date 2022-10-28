from typing import Generator

import pytest

from database.database import add_item_to_database, load_database
from exceptions.database import NodeExistsError
from testing import TEST_DATABASE_FILE_PATH


class TestDataBase:
    def test_database(self, clear_database: Generator) -> None:

        # Check the db is empty
        test = load_database(file_path=TEST_DATABASE_FILE_PATH)

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
        add_item_to_database(file_path=TEST_DATABASE_FILE_PATH, item=item)
        test = load_database(file_path=TEST_DATABASE_FILE_PATH)

        assert len(test) == 1

        # Insert a same record

        with pytest.raises(NodeExistsError):
            add_item_to_database(file_path=TEST_DATABASE_FILE_PATH, item=item)
