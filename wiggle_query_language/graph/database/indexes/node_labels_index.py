from json import load, dump
from pathlib import Path
from typing import Optional


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


def load_node_labels_index(
    indexes_file_path: Path, wn_of_nodes: Optional[set[int]] = None
) -> set:
    return set()


def wipe_node_labels_index(indexes_file_path: Path, im_sure: bool = False) -> bool:
    if im_sure:
        return True


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    items = {"foo", "bar", "baz"}

    add_items_to_node_labels_index(INDEXES_TEST_FILE_PATH, items)
