from typing import Generator

import pytest

from wiggle_shell.core.select_database import (
    get_and_display_available_database,
    list_existing_dbms,
    create_new_database,
    delete_database,
)
from testing import TEST_DBMS_FOLDER_PATH


class TestSelectDatabase:
    @pytest.fixture
    def add_test_db(self) -> Generator:
        create_new_database(db_name="test", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        yield None

    @pytest.fixture
    def remove_test_dbs(self, add_test_db: Generator) -> Generator:

        yield None
        skips = {"sample_dbms"}
        existing_databases = list_existing_dbms(
            skips=skips, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        for db_name in existing_databases:
            delete_database(db_name=db_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

    def test_list_existing_databases(self, remove_test_dbs: Generator) -> None:
        test = list_existing_dbms(path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

        assert len(test) == 2
        assert "test" in test

    def test_get_and_display_available_database(
        self, remove_test_dbs: Generator
    ) -> None:
        test = get_and_display_available_database(
            path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert len(test) == 2
        assert test["A"] == "sample_dbms"
        assert test["B"] == "test"

    def test_create_new_database(self, remove_test_dbs: Generator) -> None:

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

    def test_create_new_wiggle_number_file(self) -> None:
        pass

    def test_new_database(self) -> None:
        pass

    def test_get_existing_wn_file(self) -> None:
        pass

    def test_get_existing_db_file(self) -> None:
        pass

    def test_get_existing_database(self) -> None:
        pass
