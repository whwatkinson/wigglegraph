from typing import Generator

import pytest

from testing import TEST_DBMS_FOLDER_PATH
from wiggle_shell.core.select_dbms import (
    create_new_wiggle_number_file,
    get_existing_wn_file_path,
)


class TestSelectDatabase:
    def test_create_new_wiggle_number_file(self, setup_databases: Generator) -> None:
        # Check to see that there is no wiggle number file
        db_name = "test"
        test_wn_fp = TEST_DBMS_FOLDER_PATH.joinpath(f"test/wiggle_number_{db_name}.txt")

        test_before = test_wn_fp.is_file()
        assert test_before is False

        test_after = create_new_wiggle_number_file(db_name, TEST_DBMS_FOLDER_PATH)
        assert test_after == test_wn_fp
        assert test_after.is_file() is True

        # Check to see that the file contains 0
        with open(test_after, "r") as file:
            wn = file.read()

        assert int(wn) == 0

        # Create the wn file again
        with pytest.raises(ValueError):
            create_new_wiggle_number_file(db_name, TEST_DBMS_FOLDER_PATH)

    def test_get_existing_wn_file(self, setup_databases: Generator) -> None:
        exp_wn_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            "sample_dbms/wiggle_number_sample_dbms.txt"
        )
        test_wn_fp = get_existing_wn_file_path(
            dbms_name="sample_dbms", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert exp_wn_fp == test_wn_fp

        with pytest.raises(FileNotFoundError):
            get_existing_wn_file_path(
                dbms_name="NOT A WN", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )
