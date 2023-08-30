from models.wigish import GDBMSFilePath
from models.wql import FindPre
from wiggle_query_language.clauses.find.short_circuits.nodes import (
    node_label_is_in_index,
)
from wiggle_query_language.clauses.find.short_circuits.relationships import (
    relationship_name_is_in_index,
)
from wiggle_query_language.graph.indexes.node_labels_index import load_node_labels_index
from wiggle_query_language.graph.indexes.relationship_names_index import (
    load_relationship_names_index,
)


def find_short_circuit(
    find_pre: FindPre,
    gdbms_file_path: GDBMSFilePath,
) -> bool:
    node_label_index = load_node_labels_index(gdbms_file_path.indexes_file_path)
    relationship_name_index = load_relationship_names_index(
        gdbms_file_path.indexes_file_path
    )

    node_label_index_set = set(node_label_index.keys())

    if not node_label_is_in_index(find_pre.node_labels, node_label_index_set):
        return False

    if relationship_name_is_in_index(
        find_pre.relationship_names, relationship_name_index
    ):
        return False

    return True
