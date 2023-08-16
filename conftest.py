from typing import Generator

import pytest

from testing import (
    DATABASE_TEST_FILE_PATH,
    INDEXES_TEST_FILE_PATH,
    WIGGLE_NUMBER_TEST_FILE_PATH,
)
from wiggle_query_language.graph.database.database import wipe_database
from wiggle_query_language.graph.database.relationship_index import (
    wipe_relationship_index,
)


@pytest.fixture
def clear_database_test() -> Generator:
    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)

    yield None

    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)


@pytest.fixture
def clear_relationship_index_test() -> Generator:
    wipe_relationship_index(INDEXES_TEST_FILE_PATH, im_sure=True)

    yield None

    wipe_relationship_index(INDEXES_TEST_FILE_PATH, im_sure=True)


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
    wipe_relationship_index(INDEXES_TEST_FILE_PATH, im_sure=True)
    with open(WIGGLE_NUMBER_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")

    yield None

    wipe_database(DATABASE_TEST_FILE_PATH, im_sure=True)
    wipe_relationship_index(WIGGLE_NUMBER_TEST_FILE_PATH, im_sure=True)
    with open(INDEXES_TEST_FILE_PATH, "w") as file_handle:
        file_handle.write("0")
