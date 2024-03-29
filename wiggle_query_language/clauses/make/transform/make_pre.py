from models.wql import Clause, MakePre, NodePre, ParsedMake, RelationshipPre
from wiggle_query_language.clauses.transform_helpers.relationships import (
    relationship_is_left_to_right,
)


def process_parsed_make_list(
    parsed_make_list: list[ParsedMake], current_wiggle_number: int
) -> tuple[int, list[MakePre]]:
    """
    Turns a ParsedMake into a MakePre.
    :param parsed_make_list: The list of parsed make statements.
    :param current_wiggle_number: The next available WN.
    :return: The current WN and list of MakePres ready for turning into nodes.
    """
    emit_nodes_list = []

    for parsed_make in parsed_make_list:
        if parsed_make.clause is not Clause.MAKE:
            raise Exception(f"Expecting MAKE but got {parsed_make.clause}")

        for parsed_pattern in parsed_make.parsed_pattern_list:
            # Left Node
            left_node_label = parsed_pattern.left_node_label
            left_node = NodePre(
                wn=current_wiggle_number,
                node_label=left_node_label,
                node_handle=parsed_pattern.left_node_handle,
                props_string=parsed_pattern.left_node_props,
            )
            make_pre = MakePre(left_node=left_node)
            make_pre.node_labels.add(left_node_label)
            current_wiggle_number += 1

            # Middle Node
            if parsed_pattern.middle_node:
                middle_node_label = parsed_pattern.middle_node_label
                middle_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=middle_node_label,
                    node_handle=parsed_pattern.middle_node_handle,
                    props_string=parsed_pattern.middle_node_props,
                )
                make_pre.middle_node = middle_node
                make_pre.node_labels.add(middle_node_label)
                current_wiggle_number += 1

            # Right Node
            if parsed_pattern.right_node:
                right_node_label = parsed_pattern.right_node_label
                right_node = NodePre(
                    wn=current_wiggle_number,
                    node_label=right_node_label,
                    node_handle=parsed_pattern.right_node_handle,
                    props_string=parsed_pattern.right_node_props,
                )
                make_pre.right_node = right_node
                make_pre.node_labels.add(right_node_label)
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

                if lm_rel_dir:
                    make_pre.left_node.relationships_pre.append(
                        left_middle_relationship
                    )
                else:
                    make_pre.middle_node.relationships_pre.append(
                        left_middle_relationship
                    )
                if lm_rel_name := left_middle_relationship.rel_name:
                    make_pre.relationship_names.add(lm_rel_name)

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
                    rel_name=parsed_pattern.middle_right_rel_label,
                    rel_handle=parsed_pattern.middle_right_rel_handle,
                    props_string=parsed_pattern.middle_right_rel_props,
                    wn_from_node=wn_from_node,
                    wn_to_node=wn_to_node,
                )

                if mr_rel_dir:
                    make_pre.middle_node.relationships_pre.append(
                        middle_right_relationship
                    )
                else:
                    make_pre.right_node.relationships_pre.append(
                        middle_right_relationship
                    )
                if mr_rel_name := middle_right_relationship.rel_name:
                    make_pre.relationship_names.add(mr_rel_name)
                current_wiggle_number += 1

            make_pre.relationship_names.discard(None)
            emit_nodes_list.append(make_pre)

    return current_wiggle_number, emit_nodes_list
