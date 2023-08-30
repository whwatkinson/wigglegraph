from typing import Optional, Union
from uuid import uuid4

from models.wql.data.node import Node
from models.wigish import GDBMSFilePath
from models.wql import ParsedCriteria, ParsedFind, FindNodePre
from wiggle_query_language.clauses.find.transform.find_pre import process_parsed_find
from wiggle_query_language.clauses.find.short_circuits.find_short_circuits import (
    find_short_circuit,
)
from wiggle_query_language.graph.indexes.node_labels_index import load_node_labels_index
from wiggle_query_language.graph.database.database import load_database

DATABASE_SHAPE = dict[int, dict[str, Union[dict, list, str]]]


def find_node(
    node_pre: FindNodePre, gdbms_file_path: GDBMSFilePath
) -> Optional[list[Node]]:
    indexes = load_node_labels_index(gdbms_file_path.indexes_file_path)

    database = load_database(gdbms_file_path.database_file_path)

    node_labels_index = indexes[node_pre.node_label]

    matches = []
    no_value = uuid4()
    for wn in node_labels_index:
        record = database[wn]
        node = Node(**record)
        node_props = node.properties

        # No
        node_found = False
        if props_dict_no := node_pre.props_dict_no:
            for property_name, property_value in props_dict_no.items():
                if node_props.get(property_name, no_value) == property_value:
                    node_found = False
                    break
                else:
                    node_found = True

        # Yes
        if props_dict_yes := node_pre.props_dict_yes:
            for property_name, property_value in props_dict_yes.items():
                if node_props.get(property_name, no_value) == property_value:
                    node_found = True
                else:
                    node_found = False
                    break

        if node_found:
            matches.append(node)

    return matches


def find(
    parsed_find: ParsedFind,
    gdbms_file_path: GDBMSFilePath,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> Optional[dict]:
    who_what_where = process_parsed_find(
        parsed_find=parsed_find, parsed_criteria=parsed_criteria
    )

    # Short Circuits!
    if not find_short_circuit(who_what_where, gdbms_file_path):
        print("\nNo results\n")
        return None

    return {True: False}
