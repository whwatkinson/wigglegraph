from typing import Generator

import pytest

from models.wql import FindNodePre
from testing import TEST_GDBMS
from wiggle_query_language.graph.indexes.node_labels_index import (
    add_items_to_node_labels_index,
)
from wiggle_query_language.graph.indexes.relationship_names_index import (
    add_items_to_relationship_names_index,
)
from wiggle_query_language.graph.indexes.node_relationships_index import (
    add_items_to_node_relationships_index,
)
from wiggle_query_language.graph.database.database import add_item_to_database
from wiggle_query_language.clauses.find.find import find_node


class TestFind:
    @pytest.fixture
    def setup_test_gdbms(self, clear_dbms_test: Generator) -> Generator:
        items_to_add = {
            "0": {
                "node_metadata": {
                    "wn": 0,
                    "created_at": 1693304388.099026,
                    "updated_at": None,
                },
                "node_label": "Foo",
                "properties": {"none": None, "int": 1},
                "relations": [
                    {
                        "relationship_metadata": {
                            "wn": 3,
                            "created_at": 1693304388.099026,
                            "updated_at": None,
                        },
                        "relationship_name": "REL1",
                        "wn_from_node": 0,
                        "wn_to_node": 1,
                        "properties": {"float": 3.14},
                    }
                ],
            },
            "1": {
                "node_metadata": {
                    "wn": 1,
                    "created_at": 1693304388.099026,
                    "updated_at": None,
                },
                "node_label": "Foo",
                "properties": {"str": "2", "str2": "2_4"},
                "relations": [
                    {
                        "relationship_metadata": {
                            "wn": 4,
                            "created_at": 1693304388.099026,
                            "updated_at": None,
                        },
                        "relationship_name": "REL2",
                        "wn_from_node": 1,
                        "wn_to_node": 2,
                        "properties": {"list": [1, "2", "2_4", "3 4", 3.14]},
                    }
                ],
            },
            "2": {
                "node_metadata": {
                    "wn": 2,
                    "created_at": 1693304388.099026,
                    "updated_at": None,
                },
                "node_label": "Bar",
                "properties": {"bool": True, "bool2": False},
                "relations": None,
            },
        }
        rel_indexes_to_add_dict = {"0": {3}, "1": {4}}
        node_labels_to_add = {"Foo": {0, 1}, "Bar": {2}}
        relationship_names_set_to_add = {"REL2", "REL1"}

        add_item_to_database(TEST_GDBMS.database_file_path, items_to_add=items_to_add)

        add_items_to_node_relationships_index(
            TEST_GDBMS.indexes_file_path, rel_indexes_to_add_dict
        )
        add_items_to_node_labels_index(TEST_GDBMS.indexes_file_path, node_labels_to_add)
        add_items_to_relationship_names_index(
            TEST_GDBMS.indexes_file_path, relationship_names_set_to_add
        )
        yield None

    def test_find_node__single_node(self, setup_test_gdbms: Generator) -> None:
        # Finding a single Node with matching props
        node_pre = FindNodePre(
            node_label="Foo", props_dict_yes={"none": None, "int": 1}
        )
        test = find_node(node_pre=node_pre, gdbms_file_path=TEST_GDBMS)

        assert len(test) == 1
        node = test[0]
        assert node.node_label == "Foo"
        assert node.properties == {"none": None, "int": 1}

        # Add lookup params resulting in no matches
        node_pre = FindNodePre(
            node_label="Foo", props_dict_yes={"none": None, "int": 1, "str": "2"}
        )
        test = find_node(node_pre=node_pre, gdbms_file_path=TEST_GDBMS)
        assert len(test) == 0

        # Using props_dict_no
        node_pre = FindNodePre(
            node_label="Foo",
            props_dict_no={"myvar": 1234, "albert": True, "str22": "2342"},
        )
        test = find_node(node_pre=node_pre, gdbms_file_path=TEST_GDBMS)
        assert len(test) == 2
