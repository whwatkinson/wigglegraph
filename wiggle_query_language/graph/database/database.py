from json import dump, load
from json.decoder import JSONDecodeError

from exceptions.wql.database import NodeExistsError
from graph_logger.graph_logger import graph_logger
from testing import DATABASE_TEST_FILE_PATH


def load_database(file_path: str) -> dict:
    graph_logger.info("Attempting to loading database")
    try:
        with open(file_path, "r") as file_handle:
            database = load(file_handle)
            graph_logger.info("Successfully loaded database")
            return database

    except JSONDecodeError:
        graph_logger.exception("Empty database, returning a new one")
        return {}


def add_item_to_database(file_path: str, item: dict):
    database = load_database(file_path)

    # todo o(n) -> o(1)
    for wiggle_number, _ in item.items():
        if str(wiggle_number) in database.keys():
            raise NodeExistsError(
                message=f"Node {wiggle_number} already exists did you mean to update"
            )

    database.update(item)

    with open(file_path, "w") as file_handle:
        graph_logger.info("writing to db")
        dump(database, file_handle, ensure_ascii=False)
        graph_logger.info("Done")


def add_item_to_database_append(file_path: str, item: dict):
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


def wipe_database(file_path: str, im_sure: bool = False):
    if im_sure:
        graph_logger.info("Dropping database")
        with open(file_path, "w") as file_handle:
            file_handle.write("")
        return None
    graph_logger.debug(f"Did not drop datbase as {im_sure=}")


if __name__ == "__main__":
    x = load_database(DATABASE_TEST_FILE_PATH)

    from random import randint

    print(x)
    wn = randint(0, 9999)

    i = {
        wn: {
            "wiggle_number": wn,
            "node_label": "NodeLabel",
            "created_at": 1666534101.384132,
            "updated_at": None,
            "belongings": {"uuid": "7e48f6ae-b25a-4634-91af-b1fb67b90ad9"},
            "relations": None,
        }
    }
    # update_database(DATABASE_TEST_FILE_PATH)
    #
    # add_item_to_database(DATABASE_TEST_FILE_PATH, i)
    add_item_to_database(DATABASE_TEST_FILE_PATH, i)

    wipe_database(DATABASE_TEST_FILE_PATH, True)
