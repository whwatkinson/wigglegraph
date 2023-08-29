from typing import Generator

from testing import INDEXES_TEST_FILE_PATH
from wiggle_query_language.graph.indexes.relationship_names_index import (
    add_items_to_relationship_names_index,
    load_relationship_names_index,
)


class TestNodeLabelsIndex:
    def test_node_labels_index(
        self, clear_relationship_names_index_test: Generator
    ) -> None:
        # Check the indexes is empty
        test_before = load_relationship_names_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH
        )

        assert len(test_before) == 0

        # Insert some records
        items = {"FOO", "BAR", "BAZ"}
        test_add = add_items_to_relationship_names_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add is True

        test_load1 = load_relationship_names_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH
        )
        assert len(test_load1) == 3

        # JSON has no set but a list
        assert type(test_load1) is set

        # Insert a some more labels

        items = {"FIZZ", "BUZZ"}

        test_add_again = add_items_to_relationship_names_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add_again is True

        test_load2 = load_relationship_names_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH
        )
        assert len(test_load2) == 5
        assert type(test_load2) is set
