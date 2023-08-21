from pathlib import Path
from typing import Optional


def add_items_to_node_labels_index(
    indexes_file_path: Path, items_to_add: set[str]
) -> bool:
    return True


def load_node_labels_index(
    indexes_file_path: Path, wn_of_nodes: Optional[set[int]] = None
) -> set:
    return set()


def wipe_node_labels_index(indexes_file_path: Path, im_sure: bool = False) -> bool:
    if im_sure:
        return True
