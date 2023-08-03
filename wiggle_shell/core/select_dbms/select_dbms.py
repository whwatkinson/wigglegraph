import os
from glob import glob
from pathlib import Path
from string import ascii_uppercase
from typing import Optional

from models.wigshell.paths import DbmsFilePath
from wiggle_shell import INPUT_PROMPT_SPACING, DBMS_FOLDER
from wiggle_shell.core.select_dbms import (
    create_new_database,
    get_existing_db_file_path,
    create_new_wiggle_number_file,
    get_existing_wn_file_path,
)


def list_existing_dbms(
    skips: Optional[set[str]] = None, path_to_dbms_dir: Path = DBMS_FOLDER
) -> list[str]:
    """
    Lists the subdirectories in the database folder
    :param skips: A list of folder to ignore
    :param path_to_dbms_dir:
    :return: A set names of the subdirectories
    """

    if not skips:
        skips = set()
    existing_databases = [
        x.name for x in path_to_dbms_dir.iterdir() if x.is_dir() and x.name not in skips
    ]

    return existing_databases


def get_and_display_available_dbms(
    path_to_dbms_dir: Path = DBMS_FOLDER,
) -> dict[str, str]:
    skips = {"tests", "__pycache__"}
    existing_databases = list_existing_dbms(skips, path_to_dbms_dir)
    # Zip does the shorter of the two iterables
    letter_db_dict = {
        char: x
        for char, x in zip(ascii_uppercase, existing_databases)
        if x not in skips
    }
    # todo refactor this
    print("\nLetter      db_name")
    for key, value in letter_db_dict.items():
        print(f"{key}           {value}")
    print("\n")
    return letter_db_dict


def create_new_dbms(path_to_dbms_dir: Path = DBMS_FOLDER) -> DbmsFilePath:
    """

    :return:
    """
    while True:
        new_db_name = input(f"Please enter a new db name:{INPUT_PROMPT_SPACING}")
        try:
            return get_new_dbms_file_paths(
                new_db_name=new_db_name, path_to_dbms_dir=path_to_dbms_dir
            )
        except ValueError:
            print(f"{new_db_name} is already taken, please choose another name.")
            continue


def get_new_dbms_file_paths(
    new_db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> DbmsFilePath:
    """
    Creates a new DBMS
    :param new_db_name: The name of the new dbms
    :param path_to_dbms_dir: The path ot the DBMS directory
    :return:
    """

    try:
        # todo cancel operation
        db_path = create_new_database(new_db_name, path_to_dbms_dir)
        wn_path = create_new_wiggle_number_file(new_db_name, path_to_dbms_dir)
        print(f"Using {new_db_name}")
        return DbmsFilePath(database_file_path=db_path, wiggle_number_file_path=wn_path)
    except ValueError:
        print(f"{new_db_name} is already taken, please choose another name.")
        raise


def get_existing_dbms(path_to_dbms_dir: Path = DBMS_FOLDER) -> DbmsFilePath:
    """

    :return:
    """
    # todo test for this and break up
    while True:
        choices = get_and_display_available_dbms()

        if not choices:
            print("There are no databases, please create a new database.")
            db_path = create_new_dbms(path_to_dbms_dir=path_to_dbms_dir)
            return db_path
        db_selected = input(
            f"Please select a database to use (Letter):{INPUT_PROMPT_SPACING}"
        )
        try:
            existing_db_name = choices[db_selected]

        except KeyError:
            print(f"{db_selected} does not exist, please select an existing DB")
            continue

        try:
            db_path = get_existing_db_file_path(
                db_name=existing_db_name, path_to_dbms_dir=path_to_dbms_dir
            )
            wn_path = get_existing_wn_file_path(
                db_name=existing_db_name, path_to_dbms_dir=path_to_dbms_dir
            )
            return DbmsFilePath(
                database_file_path=db_path, wiggle_number_file_path=wn_path
            )
        except FileNotFoundError as e:
            print(f"Database files could not be found {e}")
            continue


def get_existing_dbms_file_paths(
    existing_db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> DbmsFilePath:
    pass


def delete_dbms(db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER) -> int:

    db_path = path_to_dbms_dir.joinpath(f"{db_name}/")

    if not db_path.is_dir():
        raise Exception()

    files = glob(f"{db_path}/*")
    if files:
        for file in files:
            os.remove(file)

    db_path.rmdir()

    return 0


def select_dbms() -> DbmsFilePath:
    """
    Select the databases to be used.
    :return: A path to the correct DB.
    """

    db_choice = input(f"Use existing db (y/n):{INPUT_PROMPT_SPACING}")
    match db_choice:
        case "y":
            db_path = get_existing_dbms()
        case _:
            db_path = create_new_dbms()

    return db_path
