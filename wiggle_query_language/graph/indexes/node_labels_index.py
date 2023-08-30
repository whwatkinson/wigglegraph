from json import dump, load
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional

from wiggle_graph_logger.graph_logger import graph_logger
from wiggle_query_language.graph.indexes import NODE_LABELS_INDEX_NAME
from wiggle_query_language.graph.indexes.index_helpers import json_to_dict


def add_items_to_node_labels_index(
    indexes_file_path: Path, items_to_add: dict[str, set[int]]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the node_labels index file.
    :return: A bool.
    """

    with open(indexes_file_path, "r+") as file_handle:
        indexes_dict = load(file_handle)
        node_labels_indexes_dict = indexes_dict[NODE_LABELS_INDEX_NAME]

        for node_label, new_labels_node_wns in items_to_add.items():
            if node_label in node_labels_indexes_dict:
                existing_rels = set(node_labels_indexes_dict[node_label])
                new_set = existing_rels.union(new_labels_node_wns)
                node_labels_indexes_dict[node_label] = list(new_set)
            else:
                node_labels_indexes_dict[node_label] = list(new_labels_node_wns)

            file_handle.seek(0)

        indexes_dict[NODE_LABELS_INDEX_NAME] = node_labels_indexes_dict

        dump(indexes_dict, file_handle, indent=4)
        file_handle.truncate()

    return True


def load_node_labels_index(
    indexes_file_path: Path, wn_of_nodes: Optional[set[int]] = None
) -> dict[str, set[int]]:
    """
    Loads the node_labels indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :param wn_of_nodes:
    :return: A node_label index.
    """
    graph_logger.info("Attempting to loading node_labels indexes")
    try:
        with open(indexes_file_path, "r") as file_handle:
            indexes = load(file_handle)

            node_labels_indexes_json = indexes[NODE_LABELS_INDEX_NAME]
            graph_logger.info("Successfully loaded node_labels index")

            node_labels_indexes_python = json_to_dict(
                node_labels_indexes_json, wn_of_nodes
            )

            return node_labels_indexes_python

    except JSONDecodeError:
        graph_logger.exception("Empty node_labels, returning a new one")
        return {}


def wipe_node_labels_index(indexes_file_path: Path, im_sure: bool = False) -> bool:
    """
    Wipes the node_labels index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return: A bool.
    """

    if im_sure:
        graph_logger.info("Dropping node_labels")
        with open(indexes_file_path, "r+") as file_handle:
            indexes_dict = load(file_handle)
            indexes_dict[NODE_LABELS_INDEX_NAME] = {}
            file_handle.seek(0)
            dump(indexes_dict, file_handle, indent=4)
            file_handle.truncate()

        graph_logger.info("node_labels successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop node_labels as {im_sure=}")


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    items = {"FOO": {1, 2, 3, 4}, "FOO2": {1, 2, 3, 4}}
    # wipe_node_labels_index(INDEXES_TEST_FILE_PATH, True)
    add_items_to_node_labels_index(INDEXES_TEST_FILE_PATH, items)
    a = load_node_labels_index(INDEXES_TEST_FILE_PATH)
    b = 1
