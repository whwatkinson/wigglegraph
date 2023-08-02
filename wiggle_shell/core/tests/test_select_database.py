from typing import Generator

import pytest

from wiggle_shell.core.select_database import (
    get_and_display_available_database,
    list_existing_dbms,
    create_new_database,
    delete_database,
    create_new_wiggle_number_file,
    get_existing_wn_file_path,
    get_existing_db_file_path,
)
from testing import TEST_DBMS_FOLDER_PATH


class TestSelectDatabase:
    @pytest.fixture
    def setup_databases(self) -> Generator:
        skips = {"sample_dbms"}
        existing_databases = list_existing_dbms(
            skips=skips, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        for db_name in existing_databases:
            delete_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
        create_new_database(db_name="test", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        yield None
        skips = {"sample_dbms"}
        existing_databases = list_existing_dbms(
            skips=skips, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        for db_name in existing_databases:
            delete_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

    def test_list_existing_databases(self, setup_databases: Generator) -> None:
        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 2
        assert "test" in test

    def test_get_and_display_available_database(
        self, setup_databases: Generator
    ) -> None:
        test = get_and_display_available_database(
            path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

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

    def test_create_new_wiggle_number_file(self, setup_databases: Generator) -> None:
        # Check to see that there is no wiggle number file
        db_name = "test"
        wn_fp = TEST_DBMS_FOLDER_PATH.joinpath(f"test/wiggle_number_{db_name}.txt")

        test = wn_fp.is_file()
        assert test is False

        test2 = create_new_wiggle_number_file(db_name, TEST_DBMS_FOLDER_PATH)
        assert test2 == wn_fp
        assert test2.is_file()

        # Check to see that ) is in the file
        with open(test2, "r") as file:
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
            db_name="sample_dbms", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert exp_wn_fp == test_wn_fp

        with pytest.raises(FileNotFoundError):
            get_existing_wn_file_path(
                db_name="NOT A WN", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )

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

    def test_new_database(self) -> None:
        pass

    def test_get_existing_database(self) -> None:
        pass
