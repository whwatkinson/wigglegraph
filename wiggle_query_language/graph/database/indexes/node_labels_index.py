from json import dump, load
from json.decoder import JSONDecodeError
from pathlib import Path

from graph_logger.graph_logger import graph_logger


def add_items_to_node_labels_index(
    indexes_file_path: Path, items_to_add: set[str]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the relationship index file.
    :return: A bool.
    """
    index_name = "node_labels"
    with open(indexes_file_path, "r+") as file_handle:
        indexes_dict = load(file_handle)
        node_label_indexes = set(indexes_dict[index_name])
        updated_index = node_label_indexes.union(items_to_add)
        file_handle.seek(0)
        indexes_dict[index_name] = list(updated_index)
        dump(indexes_dict, file_handle, indent=4)
        file_handle.truncate()

    return True


def load_node_labels_index(indexes_file_path: Path) -> set:
    """
    Loads the relationship indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :return: A database dict.
    """
    index_name = "node_labels"
    graph_logger.info("Attempting to loading Relationship indexes")
    try:
        with open(indexes_file_path, "r") as file_handle:
            indexes = load(file_handle)
            rel_indexes_json = indexes[index_name]
            graph_logger.info("Successfully loaded node_labels index")
            rel_indexes_python = set(rel_indexes_json)

            return rel_indexes_python

    except JSONDecodeError:
        graph_logger.exception("Empty node_labels indexes, returning a new one")

    return set()


def wipe_node_labels_index(indexes_file_path: Path, im_sure: bool = False) -> bool:
    """
    Wipes the node_labels index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return:
    """
    index_name = "node_labels"
    if im_sure:
        graph_logger.info("Dropping node_labels indexes")
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

    add_items_to_node_labels_index(INDEXES_TEST_FILE_PATH, items)
    load_node_labels_index(INDEXES_TEST_FILE_PATH)
