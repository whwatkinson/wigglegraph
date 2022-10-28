from models.enums.statement import Statement
from clauses.make.make import make
from state.wiggle_number import WIGGLE_NUMBER_FILE_PATH
from database.database import DATABASE_FILE_PATH


def wiggle_graph(statement: str):
    """
    Very much a v1
    :param statement: the user input
    :return:
    """
    # Break qry into clauses

    if Statement.MAKE.value in statement.upper():
        # Kick off make flow
        make(statement, WIGGLE_NUMBER_FILE_PATH, DATABASE_FILE_PATH)

    else:
        raise NotImplementedError("Your qry could not be processed")


if __name__ == "__main__":
    statement = input("qry: ")

    wiggle_graph(statement)
