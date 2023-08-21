from json import load
from typing import Generator

import pytest

from testing import TEST_DBMS_FOLDER_PATH
from wiggle_shell.core.select_dbms.select_index_file import (
    create_new_indexes_file,
    get_existing_indexes_file_path,
)


class TestRelationshipIndex:
    def test_create_new_relationship_index(
        self, wigsh_setup_databases: Generator
    ) -> None:
        dbms_name = "foo2"
        # Check that the rel index does not exit

        test_ri_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            f"{dbms_name}/indexes_{dbms_name}.json"
        )
        assert test_ri_fp.is_file() is False

        # Create the rel index file
        test_after = create_new_indexes_file(
            dbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )
        assert test_after == test_ri_fp
        assert test_after.is_file() is True

        # Check to see if the file has noe indexes
        with open(test_after, "r") as file:
            data = load(file)

        assert data == {"relationships": {}, "node_labels": []}

        # Create the rel index file again
        with pytest.raises(ValueError):
            create_new_indexes_file(
                dbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )

    def test_get_existing_relationship_index_file_path(self) -> None:
        exp_indexes_fp = TEST_DBMS_FOLDER_PATH.joinpath(
            "sample_dbms/indexes_sample_dbms.json"
        )
        test_db_fp = get_existing_indexes_file_path(
            dbms_name="sample_dbms", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
        )

        assert exp_indexes_fp == test_db_fp

        with pytest.raises(FileNotFoundError):
            get_existing_indexes_file_path(
                dbms_name="NOT A rel index", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
            )
