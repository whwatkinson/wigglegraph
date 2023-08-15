import pytest

from exceptions.wql.data import NodeHasUnrelatedRelationship
from models.wql.data.node import Node
from models.wql.data.relationship import Relationship
from models.wql.data.wiggle_metadata import WiggleGraphMetalData
from testing.test_helpers import does_not_raise


class TestNodeModel:
    @pytest.mark.parametrize(
        "test_rel_dict, expected_result, exception",
        [
            pytest.param(
                {"wn_from_node": 2, "wn_to_node": 3},
                None,
                does_not_raise(),
                id="EXP PASS: No errors",
            ),
            pytest.param(
                {"wn_from_node": 6, "wn_to_node": 7},
                None,
                pytest.raises(NodeHasUnrelatedRelationship),
                id="EXP EXEC: Rels not from this node",
            ),
        ],
    )
    def test_validate_from_to_wn(
        self, test_rel_dict: dict, expected_result: None, exception
    ):
        with exception:
            rel_wm = WiggleGraphMetalData(wn=1)
            rel = Relationship(relationship_metadata=rel_wm, **test_rel_dict)

            # Create the node and check
            test_node_wm = WiggleGraphMetalData(wn=2)
            test_node = Node(
                node_metadata=test_node_wm, node_label="foo", relations=[rel]
            )

            assert len(test_node.relations) == 1
