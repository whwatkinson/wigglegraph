from core.select_dbms.select_dbms import select_dbms
from core.query.query import parse_raw_query

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
        print(dbms_file_path)
        break

    # Interact with the DB
    while True:
        query_string = input(f"Please enter a query (q) to exit{INPUT_PROMPT_SPACING}")
        print(query_string)

        try:
            query_parsed = parse_raw_query(query_string)
            print(query_parsed)
        except Exception:
            continue


if __name__ == "__main__":
    start_wiggle_shell()
