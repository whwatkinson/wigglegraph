from core.select_database import select_database


def start_wiggle_shell() -> None:

    print("**********************")
    print("Welcome to WiggleGraph")
    print("**********************\n")

    while True:
        path_to_db = select_database()
        print(path_to_db)

        # foo = input(f"Please write a qry:{INPUT_PROMPT_SPACING}")
        break


if __name__ == "__main__":
    start_wiggle_shell()
