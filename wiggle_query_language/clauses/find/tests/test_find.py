from typing import Generator

import pytest

from testing import TEST_GDBMS
from wiggle_query_language.graph.database.indexes.node_labels_index import (
    add_items_to_node_labels_index,
)


class TestFind:
    @pytest.fixture
    def setup_test_gdbms(self, clear_dbms_test: Generator) -> Generator:
        add_items_to_node_labels_index(TEST_GDBMS.indexes_file_path, {"NodeLabel"})
        yield None

    def test_find_single_node(self, setup_test_gdbms: Generator) -> None:
        assert True
