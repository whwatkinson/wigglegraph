from json import load, dump
from json.decoder import JSONDecodeError
from pathlib import Path


from graph_logger.graph_logger import graph_logger


def add_items_to_relationship_names_index(
    indexes_file_path: Path, items_to_add: set[str]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the relationship_names index.
    :return: A bool.
    """
    index_name = "relationship_names"
    with open(indexes_file_path, "r+") as file_handle:
        indexes_dict = load(file_handle)
        relationship_names_indexes = set(indexes_dict[index_name])
        updated_index = relationship_names_indexes.union(items_to_add)
        file_handle.seek(0)
        indexes_dict[index_name] = list(updated_index)
        dump(indexes_dict, file_handle, indent=4)
        file_handle.truncate()

    return True


def load_relationship_names_index(indexes_file_path: Path) -> set:
    """
    Loads the relationship indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :return: A database dict.
    """
    index_name = "relationship_names"
    graph_logger.info("Attempting to loading Relationship indexes")
    try:
        with open(indexes_file_path, "r") as file_handle:
            indexes = load(file_handle)
            relationship_names_json = indexes[index_name]
            graph_logger.info("Successfully loaded relationship_names index")
            relationship_names_python = set(relationship_names_json)

            return relationship_names_python

    except JSONDecodeError:
        graph_logger.exception("Empty relationship_names indexes, returning a new one")

    return set()


def wipe_relationship_names_index(
    indexes_file_path: Path, im_sure: bool = False
) -> bool:
    """
    Wipes the relationship_names index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return:
    """
    index_name = "relationship_names"
    if im_sure:
        graph_logger.info("Dropping relationship_names indexes")
        with open(indexes_file_path, "r+") as file_handle:
            indexes_dict = load(file_handle)
            indexes_dict[index_name] = []
            file_handle.seek(0)
            dump(indexes_dict, file_handle, indent=4)
            file_handle.truncate()

        graph_logger.info("Relationship indexes successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop relationship indexes as {im_sure=}")


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    items = {"foo", "bar", "baz"}
    wipe_relationship_names_index(INDEXES_TEST_FILE_PATH, True)
    add_items_to_relationship_names_index(INDEXES_TEST_FILE_PATH, items)
    load_relationship_names_index(INDEXES_TEST_FILE_PATH)
