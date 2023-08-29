from models.wigish import GDBMSFilePath
from models.wql import (
    MakePre,
    Node,
    NodePre,
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
from wiggle_query_language.graph.indexes.node_labels_index import (
    add_items_to_node_labels_index,
)
from wiggle_query_language.graph.indexes.node_relationships_index import (
    add_items_to_node_relationships_index,
)
from wiggle_query_language.graph.indexes.relationship_names_index import (
    add_items_to_relationship_names_index,
)
from wiggle_query_language.graph.state.wiggle_number import (
    get_current_wiggle_number,
    update_wiggle_number,
)


def make_nodes(make_pre: MakePre) -> list[Node]:
    """
    Handles the creation of the nodes.
    :param make_pre: The pre-processed Nodes
    :return: A list of Nodes for loading onto the graph.
    """
    # Will always be a left node in a MAKE
    nodes = [make_node(make_pre.left_node)]

    if make_pre.middle_node:
        nodes.append(make_node(make_pre.middle_node))

    if make_pre.right_node:
        nodes.append(make_node(make_pre.right_node))

    return nodes


def make_node(emit_node: NodePre) -> Node:
    """
    Makes the Node object for a node.
    :param emit_node: The pre-processed node.
    :return: A WiggleGraph Node.
    """
    node_metadata = WiggleGraphMetalData(wn=emit_node.wn)
    node_label = emit_node.node_label
    properties = get_property_dict(emit_node.props_string)
    if emit_node.relationships_pre:
        relations = [
            make_relationship(relationship_pre)
            for relationship_pre in emit_node.relationships_pre
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
    gdbms_file_path: GDBMSFilePath,
) -> bool:
    """
    Adds the Nodes to the graph.
    :param nodes_list: The list of constructed Nodes.
    :param gdbms_file_path: The path to the DBMS.
    :return: A bool.
    """
    # Export Nodes and Rels
    nodes_to_add_dict = {str(node.wn): node.dict() for node in nodes_list}

    # Write data to the database
    add_item_to_database(gdbms_file_path.database_file_path, nodes_to_add_dict)

    return True


def add_indexes(
    nodes_list: list[Node],
    emit_nodes_list: list[MakePre],
    gdbms_file_path: GDBMSFilePath,
) -> bool:
    """
    Handles adding the indexes to the Indexes file.
    :param nodes_list: The list of constructed Nodes.
    :param emit_nodes_list: The PreProcessed Node list
    :param gdbms_file_path: The path to the DBMS.
    :return: a Bool.
    """

    rel_indexes_to_add_dict = {
        str(node.wn): {rel.wn for rel in node.relations}
        for node in nodes_list
        if node.relations
    }
    node_labels_set_to_add = set()
    relationship_names_set_to_add = set()

    for make_pre in emit_nodes_list:
        node_labels_set_to_add = node_labels_set_to_add.union(make_pre.node_labels)
        relationship_names_set_to_add = relationship_names_set_to_add.union(
            make_pre.relationship_names
        )

    add_items_to_node_relationships_index(
        gdbms_file_path.indexes_file_path, rel_indexes_to_add_dict
    )
    add_items_to_node_labels_index(
        gdbms_file_path.indexes_file_path, node_labels_set_to_add
    )
    add_items_to_relationship_names_index(
        gdbms_file_path.indexes_file_path, relationship_names_set_to_add
    )

    return True


def make(parsed_make_list: list[ParsedMake], gdbms_file_path: GDBMSFilePath) -> bool:
    """
    Handles the loading from stmt to putting data in the DB.
    :param parsed_make_list: The list of parsed MAKE statements.
    :param gdbms_file_path: The path to the DBMS.
    :return: A bool.
    """
    # Get the next available WN
    current_wiggle_number = get_current_wiggle_number(
        gdbms_file_path.wiggle_number_file_path
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
        gdbms_file_path=gdbms_file_path,
    )
    # Add Indexes
    add_indexes(
        nodes_list=nodes_list_flat,
        emit_nodes_list=emit_nodes_list,
        gdbms_file_path=gdbms_file_path,
    )

    # Update WiggleNumber if no errors
    update_wiggle_number(
        new_wiggle_number=current_wiggle_number,
        file_path=gdbms_file_path.wiggle_number_file_path,
    )

    return True
