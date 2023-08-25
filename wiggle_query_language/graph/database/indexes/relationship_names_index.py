from pathlib import Path


from wiggle_query_language.graph.database.indexes.index_helpers import (
    add_items_set_to_index_by_name,
    load_index_set_by_name,
    wipe_index_set_by_name,
)
from wiggle_query_language.graph.database.indexes import RELATIONSHIP_NAMES_INDEX_NAME


def add_items_to_relationship_names_index(
    indexes_file_path: Path, items_to_add: set[str]
) -> bool:
    """
    Adds the data to the database.
    :param indexes_file_path: The file path to the Indexes file.
    :param items_to_add: The items to be added to the relationship_names index.
    :return: A bool.
    """
    return add_items_set_to_index_by_name(
        indexes_file_path=indexes_file_path,
        items_to_add=items_to_add,
        index_name=RELATIONSHIP_NAMES_INDEX_NAME,
    )


def load_relationship_names_index(indexes_file_path: Path) -> set:
    """
    Loads the relationship_name indexes into memory.
    :param indexes_file_path: The file path to the Indexes file.
    :return: A database dict.
    """

    return load_index_set_by_name(
        indexes_file_path=indexes_file_path, index_name=RELATIONSHIP_NAMES_INDEX_NAME
    )


def wipe_relationship_names_index(
    indexes_file_path: Path, im_sure: bool = False
) -> bool:
    """
    Wipes the relationship_names index, must set im_sure to true.
    :param indexes_file_path: The file path to the Indexes file.
    :param im_sure: Flag for making sure.
    :return:
    """
    return wipe_index_set_by_name(
        indexes_file_path=indexes_file_path,
        index_name=RELATIONSHIP_NAMES_INDEX_NAME,
        im_sure=im_sure,
    )


if __name__ == "__main__":
    from testing import INDEXES_TEST_FILE_PATH

    items = {"foo", "bar", "baz"}
    wipe_relationship_names_index(INDEXES_TEST_FILE_PATH, True)
    add_items_to_relationship_names_index(INDEXES_TEST_FILE_PATH, items)
    load_relationship_names_index(INDEXES_TEST_FILE_PATH)
