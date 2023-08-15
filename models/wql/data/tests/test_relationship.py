import pytest

from exceptions.wql.data import RelationshipToFromError
from models.wql.data.relationship import Relationship
from models.wql.data.wiggle_metadata import WiggleGraphMetalData
from testing.test_helpers import does_not_raise


class TestRelationshipModel:
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
                {"wn_from_node": 2, "wn_to_node": 2},
                None,
                pytest.raises(RelationshipToFromError),
                id="EXP EXEC: Same to from",
            ),
        ],
    )
    def test_validate_from_to_wn(
        self, test_rel_dict: dict, expected_result: None, exception
    ):
        with exception:
            wm = WiggleGraphMetalData(wn=1)
            test_rel = Relationship(relationship_metadata=wm, **test_rel_dict)

            assert test_rel.wn_from_node == test_rel_dict.get("wn_from_node")
            assert test_rel.wn_to_node == test_rel_dict.get("wn_to_node")
