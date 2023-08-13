from models.wql import (
    ParsedMake,
    Node,
    Relationship,
    RelationshipPre,
    WiggleGraphMetalData,
    EmitNode,
    EmitNodes,
)
from models.wigsh import DbmsFilePath
from wiggle_query_language.clauses.make.makepre import process_parsed_make_list
from wiggle_query_language.clauses.make.parse_make.make_properties import (
    make_properties,
)
from wiggle_query_language.graph.state.wiggle_number import (
    get_current_wiggle_number,
    update_wiggle_number,
)


def make_nodes(emit_node: EmitNodes) -> list[Node]:
    """

    :param emit_node:
    :return:
    """
    # Will always be a left in a MAKE
    nodes = [make_node(emit_node.left)]

    if emit_node.middle:
        nodes.append(make_node(emit_node.middle))

    if emit_node.right:
        nodes.append(make_node(emit_node.right))

    return nodes


def make_node(emit_node: EmitNode) -> Node:
    """
    Makes the Node object for a node.
    :param emit_node: The pre-processed node.
    :return: A WiggleGraph Node.
    """
    node_pre = emit_node.node_pre
    node_metadata = WiggleGraphMetalData(wn=node_pre.wn)
    node_label = node_pre.node_label
    properties = make_properties(node_pre.props_string)
    relations = [
        make_relationship(relationship_pre)
        for relationship_pre in emit_node.relationship_pre
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


def add_nodes_to_graph(
    nodes_list: list[Node],
    current_wiggle_number: int,
    dbms_file_path: DbmsFilePath,
) -> bool:
    # Add Nodes

    for batch in nodes_list:
        pass

    # Update WiggleNumber
    update_wiggle_number(dbms_file_path.wiggle_number_file_path, current_wiggle_number)

    return True


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
    nodes_list = [make_nodes(emit_nodes) for emit_nodes in emit_nodes_list]
    nodes_list_flat = [item for sublist in nodes_list for item in sublist]
    # Commit if not errors
    add_nodes_to_graph(
        nodes_list=nodes_list_flat,
        current_wiggle_number=current_wiggle_number,
        dbms_file_path=dbms_file_path,
    )

    return True
