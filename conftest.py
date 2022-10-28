import pytest

from database.database import wipe_database
from testing import TEST_DATABASE_FILE_PATH, TEST_WIGGLE_NUMBER_STATE_FILE_PATH


@pytest.fixture
def clear_database():
    wipe_database(TEST_DATABASE_FILE_PATH, im_sure=True)
    yield None
    wipe_database(TEST_DATABASE_FILE_PATH, im_sure=True)


@pytest.fixture
def clear_wiggle_number_state_file():

    with open(TEST_WIGGLE_NUMBER_STATE_FILE_PATH, "w") as file_handle:
        file_handle.write("0")

    yield None

    with open(TEST_WIGGLE_NUMBER_STATE_FILE_PATH, "w") as file_handle:
        file_handle.write("0")
