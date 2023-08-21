from itertools import chain

from models.wigish import DbmsFilePath
from models.wql import (
    EmitNode,
    EmitNodes,
    Node,
    ParsedMake,
    Relationship,
    RelationshipPre,
    WiggleGraphMetalData,
)
from wiggle_query_language.clauses.make.transform.make_pre import (
    process_parsed_make_list,
)
from wiggle_query_language.clauses.parsing_helpers.parse_properties import (
    get_property_dict,
)
from wiggle_query_language.graph.database.database import add_item_to_database
from wiggle_query_language.graph.database.indexes.node_relationship_index import (
    add_items_to_node_relationship_index,
)
from wiggle_query_language.graph.database.indexes.node_labels_index import (
    add_items_to_node_labels_index,
)
from wiggle_query_language.graph.database.indexes.relationship_names_index import (
    add_items_to_relationship_names_index,
)
from wiggle_query_language.graph.state.wiggle_number import (
    get_current_wiggle_number,
    update_wiggle_number,
)


def make_nodes(emit_node: EmitNodes) -> list[Node]:
    """
    Handles the creation of the nodes.
    :param emit_node: The pre-processed Node
    :return: A list of Nodes for loading onto the graph.
    """
    # Will always be a left node in a MAKE
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
    properties = get_property_dict(node_pre.props_string)
    if emit_node.relationship_pre:
        relations = [
            make_relationship(relationship_pre)
            for relationship_pre in emit_node.relationship_pre
            if relationship_pre
        ]
    else:
        relations = None
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

    properties = get_property_dict(relationship_pre.props_string)

    return Relationship(
        relationship_metadata=rel_metadata,
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
    """
    Adds the Nodes to the graph.
    :param nodes_list: The list of constructed Nodes.
    :param current_wiggle_number: The most recent WiggleNumber.
    :param dbms_file_path: The path to the DBMS.
    :return: A bool.
    """
    # Export Nodes and Rels
    nodes_to_add_dict = {str(node.wn): node.dict() for node in nodes_list}

    # Write data to the database
    add_item_to_database(dbms_file_path.database_file_path, nodes_to_add_dict)

    # Add indexes
    rel_indexes_to_add_dict = {
        str(node.wn): {rel.wn for rel in node.relations}
        for node in nodes_list
        if node.relations
    }

    node_labels_set_to_add = {node.node_label for node in nodes_list}

    foo = [node.node_relationship_names() for node in nodes_list if node.relations]
    relationship_names_set_to_add = set(chain.from_iterable(foo))

    add_items_to_node_relationship_index(
        dbms_file_path.indexes_file_path, rel_indexes_to_add_dict
    )
    add_items_to_node_labels_index(
        dbms_file_path.indexes_file_path, node_labels_set_to_add
    )
    add_items_to_relationship_names_index(
        dbms_file_path.indexes_file_path, relationship_names_set_to_add
    )

    # Update WiggleNumber
    update_wiggle_number(dbms_file_path.wiggle_number_file_path, current_wiggle_number)

    return True


def make(parsed_make_list: list[ParsedMake], dbms_file_path: DbmsFilePath) -> bool:
    """
    Handles the loading from stmt to putting data in the DB.
    :param parsed_make_list: The list of parsed MAKE statements.
    :param dbms_file_path: The path to the DBMS.
    :return: A bool.
    """
    # Get the next available WN
    current_wiggle_number = get_current_wiggle_number(
        dbms_file_path.wiggle_number_file_path
    )
    # create NodePre and RelationshipPre
    current_wiggle_number, emit_nodes_list = process_parsed_make_list(
        parsed_make_list=parsed_make_list, current_wiggle_number=current_wiggle_number
    )

    # create Nodes and Relationship
    nodes_list = [make_nodes(emit_nodes) for emit_nodes in emit_nodes_list]
    nodes_list_flat = [item for sublist in nodes_list for item in sublist]

    # Commit if only not errors
    add_nodes_to_graph(
        nodes_list=nodes_list_flat,
        current_wiggle_number=current_wiggle_number,
        dbms_file_path=dbms_file_path,
    )

    return True
