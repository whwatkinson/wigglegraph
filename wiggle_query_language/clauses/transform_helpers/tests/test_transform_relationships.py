import pytest

from exceptions.wql.parsing import NonDirectedRelationshipError
from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.transform_helpers.relationships import (
    relationship_is_left_to_right,
)


class TestTransformRelationships:
    @pytest.mark.parametrize(
        "test_rel, expected_result, exception",
        [
            pytest.param("-[:]->", True, does_not_raise(), id="EXP PASS: LTR"),
            pytest.param("<-[:]-", False, does_not_raise(), id="EXP PASS: RTL"),
            pytest.param(
                "<-[:]->",
                False,
                pytest.raises(NonDirectedRelationshipError),
                id="EXP EXEC: Non-directed relationship",
            ),
        ],
    )
    def test_relationship_is_left_to_right(
        self, test_rel: str, expected_result: bool, exception
    ) -> None:
        with exception:
            test = relationship_is_left_to_right(test_rel)
            assert test is expected_result
