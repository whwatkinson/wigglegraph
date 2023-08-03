from typing import Generator

import pytest

from testing import TEST_DBMS_FOLDER_PATH
from wiggle_shell.core.select_dbms import (
    list_existing_dbms,
    delete_dbms,
    create_new_database,
)


def clear_dbmss() -> None:
    skips = {"sample_dbms"}
    existing_databases = list_existing_dbms(
        skips=skips, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH
    )

    for dbms_name in existing_databases:
        delete_dbms(dbms_name=dbms_name, path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)


@pytest.fixture
def setup_databases() -> Generator:
    clear_dbmss()
    create_new_database(dbms_name="test", path_to_dbms_dir=TEST_DBMS_FOLDER_PATH)
    yield None
    clear_dbmss()
