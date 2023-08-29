from json import dump, load
from json.decoder import JSONDecodeError
from typing import Optional, Union
from pathlib import Path

from wiggle_graph_logger.graph_logger import graph_logger


def json_to_dict(
    rel_indexes: dict, wn_of_nodes: Optional[set[int]] = None
) -> dict[Union[int, str], set[int]]:
    return {k: set(v) for k, v in rel_indexes.items()}


def dict_to_json(rel_indexes: dict) -> dict[int, list[int]]:
    return {k: list(v) for k, v in rel_indexes.items()}


def add_items_set_to_index_by_name(
    indexes_file_path: Path, items_to_add: set[str], index_name: str
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the relationship index file.
    :param index_name: The name of the index.
    :return: A bool.
    """
    with open(indexes_file_path, "r+") as file_handle:
        indexes_dict = load(file_handle)
        node_label_indexes = set(indexes_dict[index_name])
        updated_index = node_label_indexes.union(items_to_add)
        file_handle.seek(0)
        indexes_dict[index_name] = list(updated_index)
        dump(indexes_dict, file_handle, indent=4)
        file_handle.truncate()

    return True


def load_index_set_by_name(indexes_file_path: Path, index_name: str) -> set:
    """
    Loads the relationship indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :param index_name: The name of the index.
    :return: A set of items for that index.
    """
    graph_logger.info(f"Attempting to loading {index_name} indexes")
    try:
        with open(indexes_file_path, "r") as file_handle:
            indexes = load(file_handle)
            rel_indexes_json = indexes[index_name]
            graph_logger.info(f"Successfully loaded {index_name} index")
            rel_indexes_python = set(rel_indexes_json)

            return rel_indexes_python

    except JSONDecodeError:
        graph_logger.exception(f"Empty {index_name} indexes, returning a new one")

    return set()


def wipe_index_set_by_name(
    indexes_file_path: Path, index_name: str, im_sure: bool = False
) -> bool:
    """
    Wipes the index for a given index_name, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param index_name: The name of the index.
    :param im_sure: Flag for making sure.
    :return: A bool
    """
    if im_sure:
        graph_logger.info(f"Dropping {index_name} indexes")
        with open(indexes_file_path, "r+") as file_handle:
            indexes_dict = load(file_handle)
            indexes_dict[index_name] = []
            file_handle.seek(0)
            dump(indexes_dict, file_handle, indent=4)
            file_handle.truncate()

        graph_logger.info(f"{index_name} successfully dropped.")
        return True
    graph_logger.debug(f"Did not drop relationship indexes as {im_sure=}")
