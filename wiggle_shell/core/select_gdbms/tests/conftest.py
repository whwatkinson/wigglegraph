from typing import Generator

import pytest

from testing import TEST_DBMS_FOLDER_PATH
from wiggle_shell.core.select_gdbms.select_gdbms import (
    create_new_database,
    delete_gdbms,
    list_existing_dbms,
)


def wigsh_clear_test_dbmss() -> None:
    skips = {"sample_gdbms"}
    existing_databases = list_existing_dbms(
        skips=skips, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
    )

    for dbms_name in existing_databases:
        delete_gdbms(gdbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)


@pytest.fixture
def wigsh_setup_databases() -> Generator:
    wigsh_clear_test_dbmss()
    create_new_database(dbms_name="test", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
    # create_new_indexes_file(dbms_name="test", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)

    yield None
    wigsh_clear_test_dbmss()
