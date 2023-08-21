from json import dump, load
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional

from graph_logger.graph_logger import graph_logger


def json_to_dict(
    rel_indexes: dict, wn_of_nodes: Optional[set[int]] = None
) -> dict[int, set[int]]:
    return {k: set(v) for k, v in rel_indexes.items()}


def dict_to_json(rel_indexes: dict) -> dict[int, list[int]]:
    return {k: list(v) for k, v in rel_indexes.items()}


def add_items_to_node_relationship_index(
    indexes_file_path: Path, items_to_add: dict[str, set[int]]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the relationship index file.
    :return: A bool.
    """

    with open(indexes_file_path, "r+") as file_handle:
        indexes_dict = load(file_handle)
        rel_indexes_dict = indexes_dict["node_relationships"]

        for node_wn, new_rels_wn_set in items_to_add.items():
            if node_wn in rel_indexes_dict:
                existing_rels = set(rel_indexes_dict[node_wn])
                new_set = existing_rels.union(new_rels_wn_set)
                rel_indexes_dict[node_wn] = list(new_set)
            else:
                rel_indexes_dict[node_wn] = list(new_rels_wn_set)

            file_handle.seek(0)

        indexes_dict["node_relationships"] = rel_indexes_dict

        dump(indexes_dict, file_handle, indent=4)
        file_handle.truncate()

    return True


def load_node_relationship_index(
    indexes_file_path: Path, wn_of_nodes: Optional[set[int]] = None
) -> dict[int, set[int]]:
    """
    Loads the relationship indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :param wn_of_nodes:
    :return: A database dict.
    """
    graph_logger.info("Attempting to loading Relationship indexes")
    try:
        with open(indexes_file_path, "r") as file_handle:
            indexes = load(file_handle)

            rel_indexes_json = indexes["node_relationships"]
            graph_logger.info("Successfully loaded node_relationships index")

            rel_indexes_python = json_to_dict(rel_indexes_json, wn_of_nodes)

            return rel_indexes_python

    except JSONDecodeError:
        graph_logger.exception("Empty relationship indexes,returning a new one")
        return {}


def wipe_node_relationship_index(
    indexes_file_path: Path, im_sure: bool = False
) -> bool:
    """
    Wipes the node_relationships index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return:
    """
    if im_sure:
        graph_logger.info("Dropping relationship indexes")
        with open(indexes_file_path, "r+") as file_handle:
            indexes_dict = load(file_handle)
            indexes_dict["node_relationships"] = {}
            file_handle.seek(0)
            dump(indexes_dict, file_handle, indent=4)
            file_handle.truncate()

        graph_logger.info("Relationship indexes successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop relationship indexes as {im_sure=}")


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    wipe_node_relationship_index(INDEXES_TEST_FILE_PATH, True)

    # add_items_to_relationship_index(
    #     INDEXES_TEST_FILE_PATH,
    #     {
    #         "56": {
    #             57,
    #             55,
    #             1,
    #             2,
    #             3,
    #             4,
    #             5,
    #             6,
    #             7,
    #         },
    #         "54": {1, 2, 3},
    #     },
    # )
