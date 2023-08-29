from typing import Optional, Union


from models.wql.data.node import Node
from models.wigish import GDBMSFilePath
from models.wql import ParsedCriteria, ParsedFind, FindNodePre
from wiggle_query_language.clauses.find.transform.find_pre import process_parsed_find
from wiggle_query_language.clauses.find.short_circuits.find_short_circuits import (
    find_short_circuit,
)

DATABASE_SHAPE = dict[int, dict[str, Union[dict, list, str]]]


def find_node(node_pre: FindNodePre, database: DATABASE_SHAPE) -> Optional[list[Node]]:
    matches = []

    # for wn, nodes in database.items():
    #
    #     pass

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
