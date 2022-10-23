from typing import Generator

import pytest


from state.wiggle_number import get_current_wiggle_number, update_wiggle_number


WIGGLE_NUMBER_FILE_PATH_TEST = "state/tests/test_wiggle_number.txt"


class TestState:
    @pytest.fixture
    def clear_txt_file(self):

        with open(WIGGLE_NUMBER_FILE_PATH_TEST, "w") as file_handle:
            file_handle.write("0")

        yield None

        with open(WIGGLE_NUMBER_FILE_PATH_TEST, "w") as file_handle:
            file_handle.write("0")

    def test_get_get_current_wiggle_number(self, clear_txt_file) -> None:

        test = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH_TEST)

        assert test == 0

    @pytest.mark.parametrize("calls, expected_result", [(10, 10), (64, 64)])
    def test_update_wiggle_number(
        self, calls: int, expected_result: int, clear_txt_file: Generator
    ) -> None:

        wiggle_number = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH_TEST)

        for _ in range(calls):
            wiggle_number += 1

        update_wiggle_number(WIGGLE_NUMBER_FILE_PATH_TEST, wiggle_number)

        test = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH_TEST)

        assert test == expected_result
