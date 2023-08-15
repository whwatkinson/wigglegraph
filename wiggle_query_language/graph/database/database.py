from json import dump, load
from json.decoder import JSONDecodeError
from pathlib import Path

from exceptions.wql.database import NodeExistsError
from graph_logger.graph_logger import graph_logger
from testing import DATABASE_TEST_FILE_PATH


def load_database(database_file_path: Path) -> dict:
    """
    Loads the database into memory.
    :param database_file_path: The file path to the Wiggle number file.
    :return: A database dict.
    """
    graph_logger.info("Attempting to loading database")
    try:
        with open(database_file_path, "r") as file_handle:
            database = load(file_handle)
            graph_logger.info("Successfully loaded database")
            return database

    except JSONDecodeError:
        graph_logger.exception("Empty database, returning a new one")
        return {}


def add_item_to_database(database_file_path: Path, items_to_add: dict) -> bool:
    """
    Adds the data to the database.
    :param database_file_path: The file path to the Wiggle number file.
    :param items_to_add: The items to be added to the database.
    :return: A bool.
    """
    database = load_database(database_file_path)
    database_keys = database.keys()
    for wiggle_number_to_add in items_to_add:
        if wiggle_number_to_add in database_keys:
            raise NodeExistsError(
                message=f"Node {wiggle_number_to_add} already exists did you mean to update"
            )

    database.update(items_to_add)

    with open(database_file_path, "w") as file_handle:
        graph_logger.info("writing to db")
        dump(database, file_handle, ensure_ascii=False)
        graph_logger.info("Done")

    return True


def add_item_to_database_append(file_path: Path, item: dict):
    wiggle_number = None
    for key in item:
        wiggle_number = key
        if str(wiggle_number) in {1, 2, 3}:
            raise NodeExistsError(
                message=f"Node {wiggle_number} already exisits did you mean to update"
            )

    with open(file_path, "a") as file_handle:
        graph_logger.info(f"Writing Node {wiggle_number} to db")
        dump(item, file_handle, ensure_ascii=False)
        graph_logger.info(f"Succesfully wrote Node {wiggle_number} to db")


def wipe_database(database_file_path: Path, im_sure: bool = False) -> bool:
    """
    Wipes the database, must set im_sure to true.
    :param database_file_path: The file path to the Wiggle number file.
    :param im_sure: Flag for making sure.
    :return:
    """
    if im_sure:
        graph_logger.info("Dropping database")
        with open(database_file_path, "w") as file_handle:
            file_handle.write("")
        graph_logger.info("Database successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop database as {im_sure=}")


if __name__ == "__main__":
    wipe_database(DATABASE_TEST_FILE_PATH, True)
