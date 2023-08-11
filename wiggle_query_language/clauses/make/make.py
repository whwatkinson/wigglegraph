from models.wql import (
    ParsedMake,
    Node,
    Relationship,
    Clause,
    NodePre,
    RelationshipPre,
    MakePre,
)
from models.wigshell import DbmsFilePath

from wiggle_query_language.graph.state.wiggle_number import get_current_wiggle_number


def make_node(node_pre: NodePre) -> Node:
    return Node(wn=node_pre.wn, node_label=node_pre.node_label)


def make_relationship(relationship_pre: RelationshipPre) -> Relationship:
    return Relationship(wn=relationship_pre.wn, rel_name=relationship_pre.rel_name)


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
                    wn=current_wiggle_number, node_label=parsed_pattern.left_node_label
                )
                make_pre.left_node = left_node
                current_wiggle_number += 1

            # Middle Node
            if parsed_pattern.middle_node:
                middle_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=parsed_pattern.middle_node_label,
                )
                make_pre.middle_node = middle_node
                current_wiggle_number += 1

            # Right Node
            if parsed_pattern.right_node:
                right_node = NodePre(
                    wn=current_wiggle_number, node_label=parsed_pattern.right_node_label
                )
                make_pre.right_node = right_node
                current_wiggle_number += 1

            # LeftMiddle Relationship
            if left_middle_rel := parsed_pattern.left_middle_rel:
                left_middle_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                )
                make_pre.left_middle_relationship = left_middle_relationship

                lm_rel_dir = relationship_is_left_to_right(left_middle_rel)

                if lm_rel_dir:
                    make_pre.left_node.rel_to = make_pre.middle_node.wn
                else:
                    make_pre.middle_node.rel_to = make_pre.left_node.wn

                current_wiggle_number += 1

            # MiddleRight Relationship
            if right_middle_rel := parsed_pattern.middle_right_rel:
                middle_right_relationship = RelationshipPre(
                    wn=current_wiggle_number,
                    rel_name=parsed_pattern.left_middle_rel_label,
                )
                make_pre.middle_right_relationship = middle_right_relationship

                lm_rel_dir = relationship_is_left_to_right(right_middle_rel)
                if lm_rel_dir:
                    make_pre.middle_node.rel_to = make_pre.right_node.wn
                else:
                    make_pre.right_node.rel_to = make_pre.middle_node.wn

                current_wiggle_number += 1

            # Commit at the end.

            print(current_wiggle_number)

            # nodes_list = [make_node(node_pre) for node_pre in nodes_pre_list]
            # relationships_list = [
            #     make_relationship(rel_pre) for rel_pre in relationships_pre_list
            # ]

            # commit(nodes_list, relationships_list, current_wiggle_number)
