import pytest

from graph.state.wiggle_number import get_current_wiggle_number, update_wiggle_number
from testing import WIGGLE_NUMBER_TEST_FILE_PATH


class TestWiggleNumber:
    def test_get_get_current_wiggle_number(self, clear_wiggle_number_test) -> None:

        test = get_current_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH)

        assert test == 0

    @pytest.mark.parametrize("calls, expected_result", [(10, 10), (64, 64)])
    def test_update_wiggle_number(
        self, calls: int, expected_result: int, clear_wiggle_number_test
    ) -> None:

        wiggle_number = get_current_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH)

        for _ in range(calls):
            wiggle_number += 1

        update_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH, wiggle_number)

        test = get_current_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH)

        assert test == expected_result
