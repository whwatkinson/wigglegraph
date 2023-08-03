from typing import Generator

import pytest

from wiggle_shell.core.select_dbms import (
    get_and_display_available_dbms,
    list_existing_dbms,
    create_new_database,
    get_new_dbms_file_paths,
    get_existing_dbms_file_paths,
)
from testing import TEST_DBMS_FOLDER_PATH


class TestSelectDatabase:
    def test_list_existing_dbms(self, setup_databases: Generator) -> None:
        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 2
        assert "test" in test

    def test_get_and_display_available_dbms(self, setup_databases: Generator) -> None:
        test = get_and_display_available_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 2
        assert test["A"] == "sample_dbms"
        assert test["B"] == "test"

    def test_create_new_database(self, setup_databases: Generator) -> None:

        db_name = "foo2"
        # Check that the db does not exit
        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 2
        assert db_name not in test
        assert "test" in test

        # Create the database file
        create_new_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 3
        assert db_name in test

        # Create the database file again
        with pytest.raises(ValueError):
            create_new_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        # Check that there are still 3 dbs
        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        assert len(test) == 3
        assert db_name in test

    def test_get_new_dbms_file_paths(self, setup_databases: Generator) -> None:

        new_db_name = "test_foo"
        test = get_new_dbms_file_paths(new_db_name, TEST_DBMS_FOLDER_PATH)

        exp_database_file_path = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{new_db_name}/database_{new_db_name}.json"
        )
        exp_wiggle_number_file_path = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{new_db_name}/wiggle_number_{new_db_name}.txt"
        )
        assert test.database_file_path == exp_database_file_path
        assert test.wiggle_number_file_path == exp_wiggle_number_file_path

    @pytest.mark.xfail
    def test_get_existing_dbms_file_paths(self, setup_databases: Generator) -> None:
        existing_db_name = "test"
        test = get_existing_dbms_file_paths(existing_db_name, TEST_DBMS_FOLDER_PATH)

        exp_database_file_path = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{existing_db_name}/database_{existing_db_name}.json"
        )
        exp_wiggle_number_file_path = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{existing_db_name}/wiggle_number_{existing_db_name}.txt"
        )
        assert test.database_file_path == exp_database_file_path
        assert test.wiggle_number_file_path == exp_wiggle_number_file_path
