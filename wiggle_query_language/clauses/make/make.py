from models.wql import (
    ParsedMake,
    Node,
    Relationship,
    Clause,
    NodePre,
    RelationshipPre,
    MakePre,
    WiggleGraphMetalData,
)
from models.wigsh import DbmsFilePath

from wiggle_query_language.graph.state.wiggle_number import get_current_wiggle_number


def make_node(node_pre: NodePre) -> Node:
    node_metadata = WiggleGraphMetalData(wn=node_pre.wn)
    return Node(node_metadata=node_metadata, node_label=node_pre.node_label)


def make_relationship(relationship_pre: RelationshipPre) -> Relationship:
    rel_metadata = WiggleGraphMetalData(wn=relationship_pre.wn)
    return Relationship(
        rel_metadata=rel_metadata,
        relationship_name=relationship_pre.rel_name,
        wn_from_node=0,
        wn_to_node=1,
    )


def commit(
    nodes: list[Node], relationships: list[Relationship], current_wiggle_number: int
):
    pass


def relationship_is_left_to_right(parsed_relationship_pattern: str) -> bool:
    return True if parsed_relationship_pattern[-1] == ">" else False


def make(parsed_make_list: list[ParsedMake], dbms_file_path: DbmsFilePath):
    for parsed_make in parsed_make_list:
        if parsed_make.clause is not Clause.MAKE:
            raise Exception(f"Expecting MAKE but got {parsed_make.clause}")

        for parsed_pattern in parsed_make.parsed_pattern_list:
            make_pre = MakePre()

            current_wiggle_number = get_current_wiggle_number(
                dbms_file_path.wiggle_number_file_path
            )

            # Left Node
            if parsed_pattern.left_node:
                left_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.left_node_label,
                    handle=parsed_pattern.left_node_handle,
                )
                make_pre.left_node = left_node
                current_wiggle_number += 1

            # Middle Node
            if parsed_pattern.middle_node:
                middle_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.middle_node_label,
                    handle=parsed_pattern.middle_node_handle,
                )
                make_pre.middle_node = middle_node
                current_wiggle_number += 1

            # Right Node
            if parsed_pattern.right_node:
                right_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.right_node_label,
                    handle=parsed_pattern.right_node_handle,
                )
                make_pre.right_node = right_node
                current_wiggle_number += 1

            # LeftMiddle Relationship
            if left_middle_rel := parsed_pattern.left_middle_rel:
                left_middle_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                    handle=parsed_pattern.left_middle_rel_handle,
                )
                make_pre.left_middle_relationship = left_middle_relationship
                make_pre.left_middle_relationship.props_str = (
                    parsed_pattern.left_middle_rel_props
                )

                lm_rel_dir = relationship_is_left_to_right(left_middle_rel)

                if lm_rel_dir:
                    make_pre.left_node.wn_of_rel_to = make_pre.middle_node.wn
                else:
                    make_pre.middle_node.wn_of_rel_to = make_pre.left_node.wn

                current_wiggle_number += 1

            # MiddleRight Relationship
            if right_middle_rel := parsed_pattern.middle_right_rel:
                middle_right_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                    handle=parsed_pattern.middle_right_rel_handle,
                )
                make_pre.middle_right_relationship = middle_right_relationship
                make_pre.middle_right_relationship.props_str = (
                    parsed_pattern.middle_right_rel_props
                )

                lm_rel_dir = relationship_is_left_to_right(right_middle_rel)
                if lm_rel_dir:
                    make_pre.middle_node.wn_of_rel_to = make_pre.right_node.wn
                else:
                    make_pre.right_node.wn_of_rel_to = make_pre.middle_node.wn

                current_wiggle_number += 1

            # Commit at the end.

            print(current_wiggle_number)

            # nodes_list = [make_node(node_pre) for node_pre in nodes_pre_list]
            # relationships_list = [
            #     make_relationship(rel_pre) for rel_pre in relationships_pre_list
            # ]

            # commit(nodes_list, relationships_list, current_wiggle_number)
