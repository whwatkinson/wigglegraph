from typing import Optional
from pathlib import Path
from string import ascii_uppercase

from pydantic import BaseModel

from project_root import get_project_root


STATE_FOLDER = Path(f"{get_project_root()}/state/")
DBMS_FOLDER = Path(f"{get_project_root()}/dbms/")
INPUT_PROMPT_SPACING = " " * 5


class DbWnFilePaths(BaseModel):
    db: Path
    wn: Path


def get_existing_databases(skips: Optional[set[str]] = None) -> list[str]:
    """
    Lists the subdirectories in the database folder
    :param skips:
    :return: A set names of the subdirectories
    """

    if not skips:
        skips = set()
    existing_databases = [
        x.name for x in DBMS_FOLDER.iterdir() if x.is_dir() and x.name not in skips
    ]

    return existing_databases


def display_available_database() -> dict[str, str]:

    skips = {"tests", "__pycache__"}
    existing_databases = get_existing_databases(skips)
    # Zip does the shorter of the two iterables
    letter_db_dict = {
        char: x
        for char, x in zip(ascii_uppercase, existing_databases)
        if x not in skips
    }
    print("\nLetter      db_name")
    for key, value in letter_db_dict.items():
        print(f"{key}           {value}")
    print("\n")
    return letter_db_dict


def create_new_database(db_name: str) -> Path:
    """
    Creates a new database with
    :param db_name:
    :return:
    """
    existing_databases = get_existing_databases()

    if db_name in existing_databases:
        raise ValueError("Name taken")
    DBMS_FOLDER.joinpath(f"{db_name}").mkdir(parents=True, exist_ok=True)
    new_db_folder = DBMS_FOLDER.joinpath(f"{db_name}")
    path_touch_db = new_db_folder.joinpath(f"database_{db_name}.json")
    path_touch_db.touch()

    return path_touch_db


def create_new_wiggle_number_file(db_name: str) -> Path:

    # todo check that this does not exist
    new_wn_state_file_path = DBMS_FOLDER.joinpath(
        f"{db_name}/wiggle_number_{db_name}.txt"
    )
    new_wn_state_file_path.touch()

    return new_wn_state_file_path


def new_database() -> DbWnFilePaths:
    """

    :return:
    """
    while True:
        new_db_name = input(f"Please enter a new db name:{INPUT_PROMPT_SPACING}")
        try:
            # todo cancel operation
            db_path = create_new_database(new_db_name)
            wn_path = create_new_wiggle_number_file(new_db_name)
            print(f"Using {new_db_name}")
            return DbWnFilePaths(db=db_path, wn=wn_path)
        except ValueError:
            print(f"{new_db_name} is already taken, please choose another name.")
            continue


def get_existing_wn_file(db_name: str) -> Path:
    wn_file = DBMS_FOLDER.joinpath(f"{db_name}/wiggle_number_{db_name}.txt")
    return wn_file


def get_existing_db_file(db_name: str) -> Path:
    wn_file = DBMS_FOLDER.joinpath(f"{db_name}/database_{db_name}.json")
    return wn_file


def get_existing_database() -> DbWnFilePaths:
    """

    :return:
    """
    while True:
        choices = display_available_database()

        if not choices:
            print("There are no databases, please create a new database.")
            db_path = new_database()
            return db_path
        db_selected = input(
            f"Please select a database to use (Letter):{INPUT_PROMPT_SPACING}"
        )
        try:
            db_name = choices[db_selected]
            # TODO make sure that this exists
            db_path = get_existing_db_file(db_name)
            wn_path = get_existing_wn_file(db_name)
            return DbWnFilePaths(db=db_path, wn=wn_path)
        except KeyError:
            print("Nope try again...")
            continue


def select_databases() -> DbWnFilePaths:
    """
    Select the databases to be used.
    :return: A path to the correct DB.
    """
    print("**********************")
    print("Welcome to WiggleGraph")
    print("**********************\n")

    db_choice = input(f"Use existing db (y/n):{INPUT_PROMPT_SPACING}")
    match db_choice:
        case "y":
            db_path = get_existing_database()
        case _:
            db_path = new_database()

    return db_path


def wiggle_shell():

    while True:
        path_to_db = select_databases()
        print(path_to_db)
        break


if __name__ == "__main__":
    wiggle_shell()
