from pathlib import Path


from wiggle_query_language.graph.database.indexes.index_helpers import (
    add_items_set_to_index_by_name,
    load_index_set_by_name,
    wipe_index_set_by_name,
)
from wiggle_query_language.graph.database.indexes import NODE_LABELS_INDEX_NAME


def add_items_to_node_labels_index(
    indexes_file_path: Path, items_to_add: set[str]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the node_labels index file.
    :return: A bool.
    """

    return add_items_set_to_index_by_name(
        indexes_file_path=indexes_file_path,
        items_to_add=items_to_add,
        index_name=NODE_LABELS_INDEX_NAME,
    )


def load_node_labels_index(indexes_file_path: Path) -> set:
    """
    Loads the node_labels indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :return: A database dict.
    """
    return load_index_set_by_name(
        indexes_file_path=indexes_file_path, index_name=NODE_LABELS_INDEX_NAME
    )


def wipe_node_labels_index(indexes_file_path: Path, im_sure: bool = False) -> bool:
    """
    Wipes the node_labels index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return: A bool.
    """

    return wipe_index_set_by_name(
        indexes_file_path=indexes_file_path,
        index_name=NODE_LABELS_INDEX_NAME,
        im_sure=im_sure,
    )


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    items = {"foo", "bar", "baz"}

    add_items_to_node_labels_index(INDEXES_TEST_FILE_PATH, items)
    load_node_labels_index(INDEXES_TEST_FILE_PATH)
