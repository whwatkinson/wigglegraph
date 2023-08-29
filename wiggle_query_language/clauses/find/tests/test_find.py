from typing import Generator

import pytest

from testing import TEST_GDBMS
from wiggle_query_language.graph.indexes.node_labels_index import (
    add_items_to_node_labels_index,
)
from wiggle_query_language.graph.database.database import add_item_to_database


class TestFind:
    @pytest.fixture
    def setup_test_gdbms_single_node(self, clear_dbms_test: Generator) -> Generator:
        add_items_to_node_labels_index(TEST_GDBMS.indexes_file_path, {"NodeLabel"})

        single_node = {
            "0": {
                "node_metadata": {
                    "wn": 0,
                    "created_at": 1693303669.511471,
                    "updated_at": None,
                },
                "node_label": "NodeLabel",
                "properties": {
                    "none": None,
                    "int": 1,
                    "str": "2",
                    "str2": "2_4",
                    "float": 3.14,
                    "list": [1, "2", "2_4", "3 4", 3.14],
                },
                "relations": None,
            }
        }
        add_item_to_database(TEST_GDBMS.database_file_path, single_node)

        yield None

    def test_find_single_node(self, setup_test_gdbms_single_node: Generator) -> None:
        assert True
