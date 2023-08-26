import pytest

from testing.test_helpers import does_not_raise
from wiggle_query_language.clauses.find.short_circuits.nodes import (
    node_label_is_in_index,
)


class TestFindNodeShortCircuits:
    @pytest.fixture()
    def node_labels_index(self):
        yield {"foo", "bar", "baz"}

    @pytest.mark.parametrize(
        "test_node_labels, expected_result, exception",
        [
            pytest.param({"foo"}, True, does_not_raise(), id="EXP PASS: In index"),
            pytest.param({"a"}, False, does_not_raise(), id="EXP PASS: Not in index"),
        ],
    )
    def test_node_label_is_in_index(
        self,
        test_node_labels: set[str],
        expected_result: bool,
        exception,
        node_labels_index: set[str],
    ) -> None:
        with exception:
            test = node_label_is_in_index(test_node_labels, node_labels_index)
            assert test is expected_result
