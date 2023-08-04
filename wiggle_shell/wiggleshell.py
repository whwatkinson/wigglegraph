from core.select_dbms.select_dbms import select_dbms
from core.query.query import query

from wiggle_shell import INPUT_PROMPT_SPACING


def start_wiggle_shell() -> None:
    """
    Interactive shell for the Wiggle shell
    :return: None
    """

    print("**********************")
    print("Welcome to WiggleGraph")
    print("**********************\n")

    # Create/Use an existing DBMS
    while True:
        dbms_file_path = select_dbms()
        print(f"Using {dbms_file_path}")
        break

    # Interact with the DB
    while True:
        query_string = input(f"Please enter a query (q) to exit{INPUT_PROMPT_SPACING}")
        print(query_string)

        if query_string == "q":
            print("Good Bye!")
            break

        try:
            query(query_string)
        except Exception:
            continue


if __name__ == "__main__":
    start_wiggle_shell()
