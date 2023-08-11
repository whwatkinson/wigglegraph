from typing import Generator

import pytest

from wiggle_query_language.graph.database.database import wipe_database
from testing import DATABASE_TEST_FILE_PATH, WIGGLE_NUMBER_TEST_FILE_PATH


@pytest.fixture
def clear_database_test() -> Generator:
    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)

    yield None

    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)


@pytest.fixture
def clear_wiggle_number_test() -> Generator:
    with open(WIGGLE_NUMBER_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")

    yield None

    with open(WIGGLE_NUMBER_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")


@pytest.fixture
def clear_dbms_test() -> Generator:
    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)
    with open(WIGGLE_NUMBER_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")

    yield None

    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)
    with open(WIGGLE_NUMBER_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")
