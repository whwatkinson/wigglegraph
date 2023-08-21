import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.find.short_circuits.relationships import (
    relationship_name_is_in_index,
)


class TestFindNodeShortCircuits:
    @pytest.fixture()
    def relationship_names_index(self):
        yield {"FOO", "BAR", "BAZ"}

    @pytest.mark.parametrize(
        "test_relationship_names, expected_result, exception",
        [pytest.param({"A"}, True, does_not_raise(), id="EXP PASS: Not in index")],
    )
    def test_relationship_name_is_in_index(
        self,
        test_relationship_names: set[str],
        expected_result: bool,
        exception,
        relationship_names_index: set[str],
    ) -> None:
        with exception:
            test = relationship_name_is_in_index(
                test_relationship_names, relationship_names_index
            )
            assert test is expected_result
