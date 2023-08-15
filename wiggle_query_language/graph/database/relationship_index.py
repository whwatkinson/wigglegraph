# from typing import Optional
# from json import dump, load
# from json.decoder import JSONDecodeError
# from pathlib import Path
#
# from graph_logger.graph_logger import graph_logger
# from testing import DATABASE_TEST_FILE_PATH
#
#
# def json_to_dict(rel_indexes: dict, wn_of_nodes: Optional[set[int]] = None) -> dict[int, set[int]]:
#     return {k: list(v) for k, v in rel_indexes.items()}
#
#
# def dict_to_json(rel_indexes: dict) -> dict[int, list[int]]:
#     return {k: set(v) for k, v in rel_indexes.items()}
#
#
# def load_relationship_index(relationship_index_file_path: Path, wn_of_nodes: Optional[set[int]]=None) -> dict[int: set[int]]:
#     """
#     Loads the relationship indexes into memory.
#     :param relationship_index_file_path: The file path to the Wiggle number file.
#     :param wn_of_nodes:
#     :return: A database dict.
#     """
#     graph_logger.info("Attempting to loading Relationship indexes")
#     try:
#         with open(relationship_index_file_path, "r") as file_handle:
#             rel_indexes = load(file_handle)
#             graph_logger.info("Successfully loaded database")
#
#             rel_indexes_py = json_to_dict(rel_indexes, wn_of_nodes)
#
#             return rel_indexes_py
#
#     except JSONDecodeError:
#         graph_logger.exception("Empty relationship indexes,returning a new one")
#         return {}
#
#
#
#
# def add_items_to_relationship_index(relationship_index_file_path: Path, items_to_add: dict[int, set[int]]) -> bool:
#     """
#     Adds the data to the database.
#     :param relationship_index_file_path: The file path to the Relationship Index file.
#     :param items_to_add: The items to be added to the relationship index file.
#     :return: A bool.
#     """
#
#
#
#     # load the existing data
#
#     rel_indexes = load_relationship_index(relationship_index_file_path)
#     rel_indexes_keys = rel_indexes.keys()
#
#     # upsert the new data
#
#     for node_wn, rels_wn_set in items_to_add.items():
#         if node_wn in rel_indexes_keys:
#             new_rels = rels_wn_set.intersection()
#
#     # prepare pydict to json
#     json_to_add = dict_to_json(items_to_add)
#
#     # save
#
#
#     return True
#
#
# def wipe_relationship_index(relationship_index_file_path: Path, im_sure: bool = False) -> bool:
#     """
#     Wipes the database, must set im_sure to true.
#     :param relationship_index_file_path: The file path to the Wiggle number file.
#     :param im_sure: Flag for making sure.
#     :return:
#     """
#     if im_sure:
#         graph_logger.info("Dropping relationship indexes")
#         with open(relationship_index_file_path, "w") as file_handle:
#             file_handle.write("")
#         graph_logger.info("Relationship indexes successfully dropped.")
#         return True
#     graph_logger.debug(f"Did not drop relationship indexes as {im_sure=}")
#
#
#
# if __name__ == "__main__":
#     wipe_relationship_index(DATABASE_TEST_FILE_PATH, True)
