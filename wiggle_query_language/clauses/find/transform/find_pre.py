from typing import Optional, Union

from models.wql import (
    Clause,
    FindNodePre,
    FindPre,
    FindRelationshipPre,
    ParsedCriteria,
    # ParsedCriteriaYesNo,
    ParsedFind,
)
from wiggle_query_language.clauses.parsing_helpers.parse_properties import (
    get_property_dict,
)
from wiggle_query_language.clauses.transform_helpers.relationships import (
    relationship_is_left_to_right,
)


def add_criteria_yes_no_props(
    find_pre_model: Union[FindNodePre, FindRelationshipPre],
    criteria: ParsedCriteria,
    handle: str,
) -> Union[FindNodePre, FindRelationshipPre]:
    """
    Handles the updating of the FIND props from CRITERIA.
    :param find_pre_model: The Node or Relationship FindPre.
    :param criteria: The CRITERIA statement lookup properties.
    :param handle: The Nore/Relationship_handle.
    :return: A combined dict.
    """

    if criteria := criteria.criteria_handle_props.get(handle, None):
        if props_dict_yes := criteria.props_dict_yes_match:
            find_pre_model.props_dict_yes.update(props_dict_yes)
        # no
        if props_dict_no := criteria.props_dict_no_match:
            find_pre_model.props_dict_no.update(props_dict_no)

    return find_pre_model


def process_parsed_find(
    parsed_find: ParsedFind,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> FindPre:
    """
    Processes the parsed find.
    :param parsed_find: The extracted FIND statement.
    :param parsed_criteria: The extracted CRITERIA statement.
    :return: A processed find pre.
    """
    if parsed_find.clause is not Clause.FIND:
        raise Exception(f"Expecting FIND but got {parsed_find.clause}")

    parsed_pattern = parsed_find.parsed_pattern_list

    # Left Node
    left_handle = parsed_pattern.left_node_handle
    left_label = parsed_pattern.left_node_label
    left_props_dict = get_property_dict(parsed_pattern.left_node_props)

    left = FindNodePre(
        node_handle=left_handle,
        node_label=left_label,
        props_dict_yes=left_props_dict,
    )
    if parsed_criteria:
        # may need to assign left to the below
        add_criteria_yes_no_props(
            find_pre_model=left, criteria=parsed_criteria, handle=left_handle
        )

    find_pre = FindPre(left_node=left)
    find_pre.node_labels.add(left_label)

    # Middle Node
    if parsed_pattern.middle_node:
        middle_handle = parsed_pattern.middle_node_handle
        middle_label = parsed_pattern.middle_node_label
        middle_props_dict = get_property_dict(parsed_pattern.middle_node_props)

        middle = FindNodePre(
            node_handle=parsed_pattern.middle_node_handle,
            node_label=middle_label,
            props_dict_yes=middle_props_dict,
        )

        if parsed_criteria:
            add_criteria_yes_no_props(
                find_pre_model=middle, criteria=parsed_criteria, handle=middle_handle
            )

        find_pre.middle_node = middle
        find_pre.node_labels.add(middle_label)

    # Right Node
    if parsed_pattern.middle_node:
        right_handle = parsed_pattern.middle_node_handle
        right_props_dict = get_property_dict(parsed_pattern.left_node_props)
        right_label = parsed_pattern.right_node_label
        if parsed_criteria:
            right_props_dict.update(
                parsed_criteria.criteria_handle_props.get(right_handle, None)
            )

        right = FindNodePre(
            node_handle=right_handle,
            node_label=right_label,
            props_dict_yes=right_props_dict,
        )

        if parsed_criteria:
            add_criteria_yes_no_props(
                find_pre_model=right, criteria=parsed_criteria, handle=right_handle
            )

        find_pre.right_node = right
        find_pre.node_labels.add(right_label)

    # LeftMiddle Relationship
    if parsed_pattern.left_middle_rel:
        left_middle_rel_handle = parsed_pattern.left_middle_rel_handle
        left_middle_rel_name = parsed_pattern.left_middle_rel_label
        props_dict = get_property_dict(parsed_pattern.left_middle_rel_props)

        left_middle_relationship = FindRelationshipPre(
            rel_handle=left_middle_rel_handle,
            rel_name=left_middle_rel_name,
            props_dict_yes=props_dict,
        )

        if parsed_criteria:
            add_criteria_yes_no_props(
                find_pre_model=left_middle_relationship,
                criteria=parsed_criteria,
                handle=left_middle_rel_handle,
            )

        if lm_rel_name := parsed_pattern.left_middle_rel_label:
            find_pre.relationship_names.add(lm_rel_name)

        if relationship_is_left_to_right(parsed_pattern.left_middle_rel):
            find_pre.left_node.relationships.append(left_middle_relationship)
        else:
            find_pre.middle_node.relationships.append(left_middle_relationship)

    # MiddleRight Relationship
    if parsed_pattern.middle_right_rel:
        middle_right_rel_handle = parsed_pattern.middle_right_rel_handle
        middle_right_rel_name = parsed_pattern.middle_right_rel_label
        props_dict = get_property_dict(parsed_pattern.middle_right_rel_props)

        middle_right_relationship = FindRelationshipPre(
            rel_handle=middle_right_rel_handle,
            rel_name=middle_right_rel_name,
            props_dict_yes=props_dict,
        )

        if parsed_criteria:
            add_criteria_yes_no_props(
                find_pre_model=middle_right_relationship,
                criteria=parsed_criteria,
                handle=middle_right_rel_handle,
            )

        if mr_rel_name := parsed_pattern.middle_right_rel_label:
            find_pre.relationship_names.add(mr_rel_name)

        if relationship_is_left_to_right(parsed_pattern.middle_right_rel):
            find_pre.middle_node.relationships.append(middle_right_relationship)
        else:
            find_pre.right_node.relationships.append(middle_right_relationship)

    find_pre.relationship_names.discard(None)

    return find_pre


if __name__ == "__main__":
    from wiggle_query_language.clauses.find.parse_find.parse_find_statement import (
        parse_find_statement_from_query_string,
    )

    # Just doing Onde node for now then will build it up...
    query_string = """"FIND (left_node_handle:LeftNodeLabel { int: 1, str: '2', str2:"2_4", float: 3.14, list: [ 1, '2', "2_4", "3 4", 3.14, true, false, null ]});"""
    # query_string = """"FIND (left_node_handle:LeftNodeLabel);"""
    query_string = """find (left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})<-[lm:RELLM{int: 1, str: '2', str2:"2_4", float: 3.14, bool: false, none: null, list: [1, '2', "2_4", "3 4", 3.14]}]-(middle_node_label:MiddleNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[rmr:RELMR{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(right_node_label:RightNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, none: null, list: [1, '2', "2_4", "3 4", 3.14]} );"""

    finds = parse_find_statement_from_query_string(query_string)

    process_parsed_find(finds)

    a = 1
