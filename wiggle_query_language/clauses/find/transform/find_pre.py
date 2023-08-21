from typing import Optional

from models.wql import ParsedFind, ParsedCriteria, Clause
from models.wql.clauses.find.find_pre import FindNodePre, FindPre, FindRelationshipPre
from wiggle_query_language.clauses.parsing_helpers.parse_properties import (
    get_property_dict,
)

from wiggle_query_language.clauses.transform_helpers.relationships import (
    relationship_is_left_to_right,
)


def update_find_properties(find: dict, criteria: dict) -> dict:
    # todo implement this
    return find


def process_parsed_find(
    parsed_find: ParsedFind,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> FindPre:
    if parsed_find.clause is not Clause.FIND:
        raise Exception(f"Expecting FIND but got {parsed_find.clause}")

    parsed_pattern = parsed_find.parsed_pattern_list
    find_pre = FindPre()

    # Left Node, FOR ONE NODE FOR NOW!
    left_handle = parsed_pattern.left_node_handle
    left_props_dict = get_property_dict(parsed_pattern.left_node_props)

    if parsed_criteria:
        left_props_dict.update(
            parsed_criteria.criteria_handle_props.get(left_handle, None)
        )

    left = FindNodePre(
        node_handle=left_handle,
        node_label=parsed_pattern.left_node_label,
        props_dict=left_props_dict,
    )
    find_pre.left_node = left

    # Middle Node
    if parsed_pattern.middle_node:
        middle_handle = parsed_pattern.middle_node_handle
        middle_props_dict = get_property_dict(parsed_pattern.middle_node_props)

        if parsed_criteria:
            middle_props_dict.update(
                parsed_criteria.criteria_handle_props.get(middle_handle, None)
            )

        middle = FindNodePre(
            node_handle=parsed_pattern.middle_node_handle,
            node_label=parsed_pattern.middle_node_label,
            props_dict=middle_props_dict,
        )
        find_pre.middle_node = middle

    # Right Node
    if parsed_pattern.middle_node:
        right_handle = parsed_pattern.middle_node_handle
        right_props_dict = get_property_dict(parsed_pattern.left_node_props)

        if parsed_criteria:
            right_props_dict.update(
                parsed_criteria.criteria_handle_props.get(right_handle, None)
            )

        right = FindNodePre(
            node_handle=parsed_pattern.right_node_handle,
            node_label=parsed_pattern.right_node_label,
            props_dict=right_props_dict,
        )
        find_pre.right_node = right

    # LeftMiddle Relationship
    if parsed_pattern.left_middle_rel:
        left_middle_rel_handle = parsed_pattern.left_middle_rel_handle
        props_dict = get_property_dict(parsed_pattern.left_middle_rel_props)

        if parsed_criteria:
            props_dict.update(
                parsed_criteria.criteria_handle_props.get(left_middle_rel_handle, None)
            )

        left_middle_relationship = FindRelationshipPre(
            rel_handle=left_middle_rel_handle,
            rel_name=parsed_pattern.left_middle_rel_label,
            props_dict=props_dict,
        )

        if relationship_is_left_to_right(parsed_pattern.left_middle_rel):
            find_pre.left_node.relationships.append(left_middle_relationship)

        else:
            find_pre.middle_node.relationships.append(left_middle_relationship)

    # MiddleRight Relationship
    if parsed_pattern.middle_right_rel:
        middle_right_rel_handle = parsed_pattern.middle_right_rel_handle

        props_dict = get_property_dict(parsed_pattern.middle_right_rel_props)

        if parsed_criteria:
            props_dict.update(
                parsed_criteria.criteria_handle_props.get(middle_right_rel_handle, None)
            )

        middle_right_relationship = FindRelationshipPre(
            rel_handle=middle_right_rel_handle,
            rel_name=parsed_pattern.middle_right_rel_label,
            props_dict=props_dict,
        )

        if relationship_is_left_to_right(parsed_pattern.middle_right_rel):
            find_pre.middle_node.relationships.append(middle_right_relationship)
        else:
            find_pre.right_node.relationships.append(middle_right_relationship)

    return find_pre


if __name__ == "__main__":
    from wiggle_query_language.clauses.find.parse_find.parse_find_statement import (
        parse_find_statement_from_query_string,
    )

    # Just doing Onde node for now then will build it up...
    query_string = """"FIND (left_node_handle:LeftNodeLabel { int: 1, str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    # query_string = """"FIND (left_node_handle:LeftNodeLabel);"""
    query_string = """FIND (left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})<-[lm:RELLM{int: 1, str: '2', str2:"2_4", float: 3.14, bool: false, none: null, list: [1, '2', "2_4", "3 4", 3.14]}]-(middle_node_label:MiddleNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[rmr:RELMR{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(right_node_label:RightNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, none: null, list: [1, '2', "2_4", "3 4", 3.14]} );"""

    finds = parse_find_statement_from_query_string(query_string)

    process_parsed_find(finds)

    a = 1
