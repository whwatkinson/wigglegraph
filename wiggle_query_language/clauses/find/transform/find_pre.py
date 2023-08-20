from typing import Optional

from models.wql import ParsedFind, MakePre, Clause
from models.wql.clauses.find.find_pre import NodeFindPre
from wiggle_query_language.clauses.parsing_helpers.parse_properties import (
    get_property_dict,
)


def process_parsed_find_list(
    parsed_find_list: list[ParsedFind], parsed_criteria_list: Optional[list] = None
):
    for parsed_find in parsed_find_list:
        if parsed_find.clause is not Clause.FIND:
            raise Exception(f"Expecting FIND but got {parsed_find.clause}")

        for parsed_pattern in parsed_find.parsed_pattern_list:
            mp = MakePre()

            # TODO consider criteria
            print(parsed_criteria_list)

            # FOR ONE NODE
            # Left Node
            left_handle = parsed_pattern.left_node_handle
            left_node_label = parsed_pattern.left_node_label
            left_props_dict = get_property_dict(parsed_pattern.left_node_props)

            left = NodeFindPre(
                node_handle=left_handle,
                node_label=left_node_label,
                props_dict=left_props_dict,
            )
            mp.left_node = left
            # Middle Node
            if parsed_pattern.middle_node:
                pass


if __name__ == "__main__":
    from wiggle_query_language.clauses.find.parse_find.parse_find_statement import (
        parse_find_statement_from_query_string,
    )

    # Just doing Onde node for now then will build it up...
    query_string = """"FIND (left_node_handle:LeftNodeLabel { int: 1, str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    # query_string = """"FIND (left_node_handle:LeftNodeLabel);"""

    finds = parse_find_statement_from_query_string(query_string)

    process_parsed_find_list(finds)

    a = 1
