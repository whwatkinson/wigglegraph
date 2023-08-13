from models.wql import (
    ParsedMake,
    Node,
    Relationship,
    Clause,
    NodePre,
    RelationshipPre,
    MakePre,
    WiggleGraphMetalData,
    EmitNode,
    EmitNodes,
)
from models.wigsh import DbmsFilePath

from wiggle_query_language.clauses.make.parse_make.make_properties import (
    make_properties,
)
from wiggle_query_language.graph.state.wiggle_number import (
    get_current_wiggle_number,
    update_wiggle_number,
)


def make_node(emit_pre: EmitNode) -> Node:
    """
    Makes the Node object for a node.
    :param emit_pre: The pre-processed node.
    :return: A WiggleGraph Node.
    """
    node_pre = emit_pre.node_pre
    node_metadata = WiggleGraphMetalData(wn=node_pre.wn)
    node_label = node_pre.node_label
    properties = make_properties(node_pre.props_string)
    relations = [
        make_relationship(relationship_pre)
        for relationship_pre in emit_pre.relationship_pre
    ]

    return Node(
        node_metadata=node_metadata,
        node_label=node_label,
        properties=properties,
        relations=relations,
    )


def make_relationship(relationship_pre: RelationshipPre) -> Relationship:
    """
    Makes the relationship object for a node.
    :param relationship_pre: The pre-processed Relationship
    :return: A WiggleGraph Relationship.
    """
    rel_metadata = WiggleGraphMetalData(wn=relationship_pre.wn)

    properties = make_properties(relationship_pre.props_string)

    return Relationship(
        rel_metadata=rel_metadata,
        relationship_name=relationship_pre.rel_name,
        wn_from_node=relationship_pre.wn_from_node,
        wn_to_node=relationship_pre.wn_to_node,
        properties=properties,
    )


def add_nodes_tp_graph(
    nodes_list: list[Node],
    # relationships_list: list[Relationship],
    current_wiggle_number: int,
    dbms_file_path: DbmsFilePath,
) -> bool:
    # Add Nodes

    # nodes_to_add = [node.export_node() for node in nodes_list]

    # Update WiggleNumber
    update_wiggle_number(dbms_file_path.wiggle_number_file_path, current_wiggle_number)

    return True


def relationship_is_left_to_right(parsed_relationship_pattern: str) -> bool:
    """
    Checks the direction of the relationship.
    :param parsed_relationship_pattern: The extracted relationship expression.
    :return: Ture if LTR, False if RTL.
    """
    return True if parsed_relationship_pattern[-1] == ">" else False


def process_parsed_make(
    parsed_make: ParsedMake, dbms_file_path: DbmsFilePath, current_wiggle_number: int
) -> MakePre:
    pass


def process_parsed_make_list(
    parsed_make_list: list[ParsedMake], current_wiggle_number: int
) -> tuple[int, list[EmitNodes]]:
    emit_nodes_list = []

    for parsed_make in parsed_make_list:
        if parsed_make.clause is not Clause.MAKE:
            raise Exception(f"Expecting MAKE but got {parsed_make.clause}")

        for parsed_pattern in parsed_make.parsed_pattern_list:
            make_pre = MakePre()

            # Left Node
            if parsed_pattern.left_node:
                left_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.left_node_label,
                    node_handle=parsed_pattern.left_node_handle,
                    props_string=parsed_pattern.left_node_props,
                )
                make_pre.left_node = left_node
                current_wiggle_number += 1

            # Middle Node
            if parsed_pattern.middle_node:
                middle_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.middle_node_label,
                    node_handle=parsed_pattern.middle_node_handle,
                    props_string=parsed_pattern.middle_node_props,
                )
                make_pre.middle_node = middle_node
                current_wiggle_number += 1

            # Right Node
            if parsed_pattern.right_node:
                right_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.right_node_label,
                    node_handle=parsed_pattern.right_node_handle,
                    props_string=parsed_pattern.right_node_props,
                )
                make_pre.right_node = right_node
                current_wiggle_number += 1

            # LeftMiddle Relationship
            if left_middle_rel := parsed_pattern.left_middle_rel:
                lm_rel_dir = relationship_is_left_to_right(left_middle_rel)

                if lm_rel_dir:
                    wn_from_node = make_pre.left_node.wn
                    wn_to_node = make_pre.middle_node.wn
                else:
                    wn_from_node = make_pre.middle_node.wn
                    wn_to_node = make_pre.left_node.wn

                left_middle_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                    rel_handle=parsed_pattern.left_middle_rel_handle,
                    props_string=parsed_pattern.left_middle_rel_props,
                    wn_from_node=wn_from_node,
                    wn_to_node=wn_to_node,
                )
                make_pre.left_middle_relationship = left_middle_relationship
                current_wiggle_number += 1

            # MiddleRight Relationship
            if right_middle_rel := parsed_pattern.middle_right_rel:
                mr_rel_dir = relationship_is_left_to_right(right_middle_rel)

                if mr_rel_dir:
                    wn_from_node = make_pre.middle_node.wn
                    wn_to_node = make_pre.right_node.wn
                else:
                    wn_from_node = make_pre.right_node.wn
                    wn_to_node = make_pre.middle_node.wn

                middle_right_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                    rel_handle=parsed_pattern.middle_right_rel_handle,
                    props_string=parsed_pattern.middle_right_rel_props,
                    wn_from_node=wn_from_node,
                    wn_to_node=wn_to_node,
                )
                make_pre.middle_right_relationship = middle_right_relationship

                current_wiggle_number += 1

            emit_nodes_pre = make_pre.emit_nodes()
            emit_nodes_list.append(emit_nodes_pre)

    return current_wiggle_number, emit_nodes_list


def make(parsed_make_list: list[ParsedMake], dbms_file_path: DbmsFilePath) -> bool:
    """

    :param parsed_make_list:
    :param dbms_file_path:
    :return:
    """
    current_wiggle_number = get_current_wiggle_number(
        dbms_file_path.wiggle_number_file_path
    )
    # create NodePre and RelationshipPre
    current_wiggle_number, emit_nodes_list = process_parsed_make_list(
        parsed_make_list=parsed_make_list, current_wiggle_number=current_wiggle_number
    )

    # create Nodes and Relationship
    # print(emit_nodes_list)
    nodes_list_pre = [x.nodes_from_creation() for x in emit_nodes_list]
    nodes_list = [item for sublist in nodes_list_pre for item in sublist]

    # Commit if not errors
    add_nodes_tp_graph(
        nodes_list=nodes_list,
        # relationships_list=relationships_list,
        current_wiggle_number=current_wiggle_number,
        dbms_file_path=dbms_file_path,
    )

    return True
