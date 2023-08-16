from typing import Generator


from testing import INDEXES_TEST_FILE_PATH
from wiggle_query_language.graph.database.relationship_index import (
    add_items_to_relationship_index,
    load_relationship_index,
)


class TestRelationshipIndex:
    def test_relationship_index(self, clear_relationship_index_test: Generator) -> None:
        # Check the indexes is empty
        test_before = load_relationship_index(indexes_file_path=INDEXES_TEST_FILE_PATH)

        assert len(test_before) == 0

        # Insert some records
        items = {"500": {503}, "501": {504}}
        test_add = add_items_to_relationship_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add is True

        test_load1 = load_relationship_index(indexes_file_path=INDEXES_TEST_FILE_PATH)
        assert len(test_load1) == 2

        # JSON has no set but a list
        for k, v in test_load1.items():
            assert type(v) is set

        # Insert a updated records

        items = {"500": {503, 505}, "501": {504, 607}}

        test_add_again = add_items_to_relationship_index(
            indexes_file_path=INDEXES_TEST_FILE_PATH, items_to_add=items
        )
        assert test_add_again is True

        test_load2 = load_relationship_index(indexes_file_path=INDEXES_TEST_FILE_PATH)
        assert len(test_load2) == 2

        # JSON has no set but a list
        for k, v in test_load2.items():
            assert type(v) is set
