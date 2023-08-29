from typing import Generator

from testing import INDEXES_TEST_FILE_PATH
from wiggle_query_language.graph.indexes.node_labels_index import (
    add_items_to_node_labels_index,
    load_node_labels_index,
)


class TestNodeLabelsIndex:
    def test_node_labels_index(self, clear_node_labels_index_test: Generator) -> None:
        # Check the indexes is empty
        test_before = load_node_labels_index(indexes_file_path=INDEXES_TEST_FILE_PATH)

        assert len(test_before) == 0

        # Insert some records
        items = {"Foo": {0, 1}, "Bar": {2}}
        test_add = add_items_to_node_labels_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add is True

        test_load1 = load_node_labels_index(indexes_file_path=INDEXES_TEST_FILE_PATH)
        assert len(test_load1) == 2
        assert test_load1["Foo"] == {0, 1}
        assert test_load1["Bar"] == {2}

        # JSON has no set but a list
        assert type(test_load1) is dict

        # Insert a some more labels

        items = {"Foo": {4}, "Bar": {5}, "Baz": {7, 8, 9}}

        test_add_again = add_items_to_node_labels_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add_again is True

        test_load2 = load_node_labels_index(indexes_file_path=INDEXES_TEST_FILE_PATH)
        assert len(test_load2) == 3
        assert test_load2["Foo"] == {0, 1, 4}
        assert test_load2["Bar"] == {2, 5}
        assert test_load2["Baz"] == {7, 8, 9}
        assert type(test_load2) is dict
