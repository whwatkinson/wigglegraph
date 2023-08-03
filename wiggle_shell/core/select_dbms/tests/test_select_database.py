from typing import Generator

import pytest

from wiggle_shell.core.select_dbms import (
    # create_new_database,
    get_existing_db_file_path,
)
from testing import TEST_DBMS_FOLDER_PATH


class TestSelectDatabase:
    @pytest.mark.skip
    def test_create_new_database(self, setup_databases: Generator) -> None:
        # TODO rewrite removing dbms functions use path
        pass
        # db_name = "foo2"
        # # Check that the db does not exit
        # test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        #
        # assert len(test) == 2
        # assert db_name not in test
        # assert "test" in test
        #
        # # Create the database file
        # create_new_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        #
        # test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        #
        # assert len(test) == 3
        # assert db_name in test
        #
        # # Create the database file again
        # with pytest.raises(ValueError):
        #     create_new_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        #
        # # Check that there are still 3 dbs
        # test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        # assert len(test) == 3
        # assert db_name in test

    def test_get_existing_db_file(self) -> None:
        exp_db_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            "sample_dbms/database_sample_dbms.json"
        )
        test_db_fp = get_existing_db_file_path(
            db_name="sample_dbms", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert exp_db_fp == test_db_fp

        with pytest.raises(FileNotFoundError):
            get_existing_db_file_path(
                db_name="NOT A WN", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )
