from typing import Generator

import pytest


from state.wiggle_number import get_current_wiggle_number, update_wiggle_number


TEST_WIGGLE_NUMBER_FILE_PATH = "state/tests/test_wiggle_number.txt"


class TestState:
    @pytest.fixture
    def clear_txt_file(self):

        with open(TEST_WIGGLE_NUMBER_FILE_PATH, "w") as file_handle:
            file_handle.write("0")

        yield None

        with open(TEST_WIGGLE_NUMBER_FILE_PATH, "w") as file_handle:
            file_handle.write("0")

    def test_get_get_current_wiggle_number(self, clear_txt_file) -> None:

        test = get_current_wiggle_number(TEST_WIGGLE_NUMBER_FILE_PATH)

        assert test == 0

    @pytest.mark.parametrize("calls, expected_result", [(10, 10), (64, 64)])
    def test_update_wiggle_number(
        self, calls: int, expected_result: int, clear_txt_file: Generator
    ) -> None:

        wiggle_number = get_current_wiggle_number(TEST_WIGGLE_NUMBER_FILE_PATH)

        for _ in range(calls):
            wiggle_number += 1

        update_wiggle_number(TEST_WIGGLE_NUMBER_FILE_PATH, wiggle_number)

        test = get_current_wiggle_number(TEST_WIGGLE_NUMBER_FILE_PATH)

        assert test == expected_result
