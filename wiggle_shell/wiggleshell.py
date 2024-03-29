from core.query.query import query
from core.select_gdbms.select_gdbms import select_gdbms

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
        gdbms_file_path = select_gdbms()
        print(f"Using {gdbms_file_path}\n")
        break

    # Interact with the DB
    while True:
        query_string = input(
            f"Please enter a query (q to exit): {INPUT_PROMPT_SPACING}"
        )
        print(query_string, "\n")

        if query_string == "q":
            print("Good Bye!")
            break

        if "help" in query_string.lower():
            print("A helpful guide is on the way!\n")
            continue

        # query(query_string=query_string, gdbms_file_path=dbms_file_path)

        try:
            query(query_string=query_string, gdbms_file_path=gdbms_file_path)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    start_wiggle_shell()
