from typing import Generator

import pytest

from exceptions.wql.database import NodeExistsError
from testing import DATABASE_TEST_FILE_PATH
from wiggle_query_language.graph.database.database import (
    add_item_to_database,
    load_database,
)


# @pytest.mark.skip
class TestDataBase:
    def test_database(self, clear_database_test: Generator) -> None:
        # Check the db is empty
        test = load_database(database_file_path=DATABASE_TEST_FILE_PATH)

        assert len(test) == 0

        # Insert some record
        item = {
            "102132": {
                "node_metadata": {
                    "wn": 102132,
                    "created_at": 1692176499.688112,
                    "updated_at": None,
                },
                "node_label": "NodeLabel",
                "properties": {"str": "2"},
                "relations": None,
            },
            "102133": {
                "node_metadata": {
                    "wn": 102133,
                    "created_at": 1692176499.688112,
                    "updated_at": None,
                },
                "node_label": "NodeLabel",
                "properties": {"str2": "2_4"},
                "relations": [
                    {
                        "relationship_metadata": {
                            "wn": 102135,
                            "created_at": 1692176499.688112,
                            "updated_at": None,
                        },
                        "relationship_name": "REL",
                        "wn_from_node": 102133,
                        "wn_to_node": 102132,
                        "properties": {"str": "2"},
                    },
                    {
                        "relationship_metadata": {
                            "wn": 102136,
                            "created_at": 1692176499.688112,
                            "updated_at": None,
                        },
                        "relationship_name": "REL",
                        "wn_from_node": 102133,
                        "wn_to_node": 102134,
                        "properties": {"float": 3.14},
                    },
                ],
            },
            "102134": {
                "node_metadata": {
                    "wn": 102134,
                    "created_at": 1692176499.688112,
                    "updated_at": None,
                },
                "node_label": "NodeLabel2",
                "properties": {"list": [1, "2", "2_4", "3 4", 3.14]},
                "relations": None,
            },
        }
        add_item_to_database(
            database_file_path=DATABASE_TEST_FILE_PATH, items_to_add=item
        )
        test = load_database(database_file_path=DATABASE_TEST_FILE_PATH)

        assert len(test) == 3

        # Insert a same record

        with pytest.raises(NodeExistsError):
            add_item_to_database(
                database_file_path=DATABASE_TEST_FILE_PATH, items_to_add=item
            )
