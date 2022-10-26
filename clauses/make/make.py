from models.enums.statement import Statement
from models.statement import ParsedStatement
from nodes.node import Node
from state.wiggle_number import get_current_wiggle_number, update_wiggle_number
from graph_logger.graph_logger import graph_logger


def make_node(parsed_statement: ParsedStatement, wiggle_number_file_path: str) -> Node:
    """
    Takes a parsed statement and adds the record to the graph
    :param parsed_statement: A prepared input from the user
    :param wiggle_nuber_file_path: A file path to the Wiggle number
    :return: A node really to be added to the database
    """
    graph_logger.debug("Starting make node")
    if parsed_statement.clause is not Statement.MAKE:
        # todo is this useful?
        raise Exception

    wiggle_number = get_current_wiggle_number(wiggle_number_file_path)

    node = Node(
        wn=wiggle_number,
        node_label=parsed_statement.node_label,
        belongings=parsed_statement.belongings,
        relations=parsed_statement.relations,
    )
    graph_logger.info("Created new node")
    wiggle_number += 1

    update_wiggle_number(wiggle_number_file_path, wiggle_number)

    return node


def make(nodes, edges):
    pass
