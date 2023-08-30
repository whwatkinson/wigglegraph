from json import dump, load
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any

from exceptions.wql.database import NodeExistsError
from testing import DATABASE_TEST_FILE_PATH
from wiggle_graph_logger.graph_logger import graph_logger

DATABASE_SHAPE = dict[int, dict[str, Any]]


def load_database(database_file_path: Path) -> DATABASE_SHAPE:
    """
    Loads the database into memory.
    :param database_file_path: The file path to the Wiggle number file.
    :return: A database dict.
    """
    graph_logger.info("Attempting to loading database")
    try:
        with open(database_file_path, "r") as file_handle:
            database = load(file_handle)
            database = {int(k): v for k, v in database.items()}
            graph_logger.info("Successfully loaded database")
            return database

    except JSONDecodeError:
        graph_logger.exception("Empty database, returning a new one")
        return {}


def add_item_to_database(
    database_file_path: Path, items_to_add: DATABASE_SHAPE
) -> bool:
    """
    Adds the data to the database.
    :param database_file_path: The file path to the Database file.
    :param items_to_add: The items to be added to the Database file.
    :return: A bool.
    """

    with open(database_file_path, "r+") as file_handle:
        database = load(file_handle)
        graph_logger.info("writing to db")
        for wiggle_number_to_add, node in items_to_add.items():
            if wiggle_number_to_add in database:
                raise NodeExistsError(
                    message=f"Node {wiggle_number_to_add} already exists did you mean to update"
                )
            else:
                database[wiggle_number_to_add] = node

        file_handle.seek(0)
        dump(database, file_handle, indent=4)

    graph_logger.info(
        f"Successfully added {len(items_to_add)} records to the database."
    )

    return True


def wipe_database(database_file_path: Path, im_sure: bool = False) -> bool:
    """
    Wipes the database, must set im_sure to true.
    :param database_file_path: The file path to the Database file.
    :param im_sure: Flag for making sure.
    :return:
    """
    if im_sure:
        graph_logger.info("Dropping database")
        with open(database_file_path, "w") as file_handle:
            database = dict()
            file_handle.seek(0)
            dump(database, file_handle, indent=4)
            file_handle.truncate()

        graph_logger.info("Database successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop database as {im_sure=}")


if __name__ == "__main__":
    # wipe_database(DATABASE_TEST_FILE_PATH, True)
    a = load_database(DATABASE_TEST_FILE_PATH)
    b = 1
