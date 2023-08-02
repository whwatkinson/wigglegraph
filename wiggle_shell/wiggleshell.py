from core.select_database import select_dbms


def start_wiggle_shell() -> None:

    print("**********************")
    print("Welcome to WiggleGraph")
    print("**********************\n")

    # Create/Use an existing DBMS
    while True:
        db_wn_fp = select_dbms()
        print(db_wn_fp)
        break

    # Interact with the DB
    while True:
        qry = input("Please enter a query (q)")
        print(qry)

        match qry:
            case "q":
                print("Goodbye")
                break
            case _:
                print("Sorry please try again.")


if __name__ == "__main__":
    start_wiggle_shell()
