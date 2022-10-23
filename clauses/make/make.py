from models.enums.statement import Statement
from models.statement import ParsedStatement
from nodes.node import Node
from state.wiggle_number import get_current_wiggle_number, update_wiggle_number


def make_node(parsed_statement: ParsedStatement, wiggle_nuber_file_path: str) -> Node:

    if parsed_statement.clause is not Statement.MAKE:
        raise Exception

    wiggle_number = get_current_wiggle_number(wiggle_nuber_file_path)

    node = Node(
        wiggle_number=wiggle_number,
        node_label=parsed_statement.node_label,
        belongings=parsed_statement.belongings,
        relations=parsed_statement.relations,
    )
    wiggle_number += 1

    update_wiggle_number(wiggle_nuber_file_path, wiggle_number)

    return node
