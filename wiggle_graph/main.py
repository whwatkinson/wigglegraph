from state.wiggle_number import (
    WIGGLE_NUMBER_FILE_PATH,
)
from database.database import DATABASE_FILE_PATH, add_item_to_database

from clauses.make.make_helpers import parse_make_statment
from clauses.make.make import make_node


def main(statement: str):
    parsed_statement = parse_make_statment(statement)
    node = make_node(parsed_statement, WIGGLE_NUMBER_FILE_PATH)
    add_item_to_database(DATABASE_FILE_PATH, node.export_node())


if __name__ == "__main__":
    statement = input("qry: ")

    main(statement)
