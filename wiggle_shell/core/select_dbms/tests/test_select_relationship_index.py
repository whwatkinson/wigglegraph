from os import stat
from typing import Generator

import pytest

from testing import TEST_DBMS_FOLDER_PATH
from wiggle_shell.core.select_dbms.select_database import (
    create_new_database,
    get_existing_db_file_path,
)


class TestSelectDatabase:
    def test_create_new_database(self, setup_databases: Generator) -> None:
        dbms_name = "foo2"
        # Check that the db does not exit

        test_db_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{dbms_name}/database_{dbms_name}.json"
        )
        assert test_db_fp.is_file() is False

        # Create the database file
        test_after = create_new_database(
            dbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )
        assert test_after == test_db_fp
        assert test_after.is_file() is True

        # Check to see if the file is empty
        assert stat(test_db_fp).st_size == 0

        # Create the database file again
        with pytest.raises(ValueError):
            create_new_database(
                dbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )

    def test_get_existing_db_file(self) -> None:
        exp_db_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            "sample_dbms/database_sample_dbms.json"
        )
        test_db_fp = get_existing_db_file_path(
            dbms_name="sample_dbms", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert exp_db_fp == test_db_fp

        with pytest.raises(FileNotFoundError):
            get_existing_db_file_path(
                dbms_name="NOT A DB", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )
