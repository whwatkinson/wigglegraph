from typing import Optional
from pathlib import Path
from string import ascii_uppercase

from project_root import get_project_root


DATABASES_FOLDER = Path(f"{get_project_root()}/database/")
INPUT_PROMPT_SPACING = " " * 5


def databases_sub_directories(skips: Optional[set[str]] = None) -> set[str]:
    """
    Lists the subdirectories in the database folder
    :param skips:
    :return: A set names of the subdirectories
    """

    if not skips:
        skips = set()

    subdirectories = {
        x.name for x in DATABASES_FOLDER.iterdir() if x.is_dir() and x.name not in skips
    }

    return subdirectories


def display_available_database() -> dict[str, str]:

    skips = {"tests", "__pycache__"}
    database_sub_directories = databases_sub_directories(skips)
    # Zip does the shorter of the two iterables
    letter_db_dict = {
        char: x
        for char, x in zip(ascii_uppercase, database_sub_directories)
        if x not in skips
    }
    for key, value in letter_db_dict.items():
        print(f"{key}   {value}")
    return letter_db_dict


def create_new_database(db_name: str) -> Path:
    """
    Creates a new database with
    :param db_name:
    :return:
    """
    database_sub_directories = databases_sub_directories()

    if db_name in database_sub_directories:
        raise Exception("Name taken")
    DATABASES_FOLDER.joinpath(f"{db_name}").mkdir(parents=True, exist_ok=True)
    new_db_folder = DATABASES_FOLDER.joinpath(f"{db_name}")
    path_touch_db = new_db_folder.joinpath(f"database_{db_name}.json")
    path_touch_db.touch()

    return path_touch_db


def handle_new_databse() -> Path:
    while True:
        new_db_name = input(f"Please enter a new db name:{INPUT_PROMPT_SPACING}")
        try:
            db_path = create_new_database(new_db_name)
            print(f"using {new_db_name}")
            return db_path
        except Exception:
            print(f"{new_db_name} is already taken, please choose another name")
            continue


def handle_existing_databse() -> Path:
    while True:
        choices = display_available_database()

        if not choices:
            print("There are no databases, creating new")
            db_path = handle_new_databse()
            return db_path
        db_selected = input(f"Please select a database to use{INPUT_PROMPT_SPACING}")
        try:
            db_name = choices[db_selected]
            # TODO make sure that this exists
            db_path = Path(f"database/{db_name}/{db_name}database.json")
            return db_path
        except KeyError:
            print("Nope try again...")
            continue


def select_databases() -> Path:
    """
    Select the databases to be used.
    :return: A path to the correct DB.
    """
    print("Welcome to WiggleGraph\n")

    new_db = input(f"Use existing db (y/n):{INPUT_PROMPT_SPACING}")
    if new_db != "y":
        db_path = handle_new_databse()
    else:
        db_path = handle_existing_databse()

    return db_path


def wiggle_shell():

    while True:
        path_to_db = select_databases()
        print(path_to_db)
        break


if __name__ == "__main__":
    wiggle_shell()
