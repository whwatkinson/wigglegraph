import os
from glob import glob
from pathlib import Path
from string import ascii_uppercase
from typing import Optional

from models.wigish import GDBMSFilePath
from wiggle_shell import DBMS_FOLDER, INPUT_PROMPT_SPACING
from wiggle_shell.core.select_gdbms.select_database_file import (
    create_new_database,
    get_existing_db_file_path,
)
from wiggle_shell.core.select_gdbms.select_index_file import (
    create_new_indexes_file,
    get_existing_indexes_file_path,
)
from wiggle_shell.core.select_gdbms.select_wiggle_number_file import (
    create_new_wiggle_number_file,
    get_existing_wn_file_path,
)


def list_existing_dbms(
    skips: Optional[set[str]] = None, path_to_dbms_dir: Path = DBMS_FOLDER
) -> list[str]:
    """
    Lists the subdirectories in the database folder.
    :param: skips: A list of folders to ignore.
    :param: path_to_dbms_dir: The directory of the DBMS folder.
    :return: A list names of the subdirectories, ordered alphabetically..
    """

    if not skips:
        skips = set()
    existing_databases = [
        x.name for x in path_to_dbms_dir.iterdir() if x.is_dir() and x.name not in skips
    ]

    existing_databases_sorted = sorted(existing_databases)

    return existing_databases_sorted


def get_and_display_available_dbms(
    path_to_dbms_dir: Path = DBMS_FOLDER,
) -> Optional[dict[str, str]]:
    """
    Lists the available DBMS's to the User to select.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return: A mapping of Letter: DBMS.
    """
    skips = {"tests", "__pycache__"}
    if not (existing_databases := list_existing_dbms(skips, path_to_dbms_dir)):
        return None
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


def create_new_dbms(path_to_dbms_dir: Path = DBMS_FOLDER) -> GDBMSFilePath:
    """
    Handles creation of a new DBMS.
    :param path_to_dbms_dir The directory of the DBMS folder.
    :return: A filepath for both the db and wn.
    """
    while True:
        new_db_name = input(f"Please enter a new db name:{INPUT_PROMPT_SPACING}")
        try:
            return get_new_gdbms_file_paths(
                new_gdbms_name=new_db_name, path_to_dbms_dir=path_to_dbms_dir
            )
        except ValueError:
            print(f"{new_db_name} is already taken, please choose another name.")
            continue


def get_new_gdbms_file_paths(
    new_gdbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> GDBMSFilePath:
    """
    Creates a new DBMS.
    :param new_gdbms_name: The name of the new dbms.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return: A filepath for both the db and wn.
    """

    try:
        # todo cancel operation
        db_path = create_new_database(new_gdbms_name, path_to_dbms_dir)
        indexes_path = create_new_indexes_file(new_gdbms_name, path_to_dbms_dir)
        wn_path = create_new_wiggle_number_file(new_gdbms_name, path_to_dbms_dir)
        print(f"Using {new_gdbms_name}")
        return GDBMSFilePath(
            database_file_path=db_path,
            indexes_file_path=indexes_path,
            wiggle_number_file_path=wn_path,
        )
    except ValueError:
        print(f"{new_gdbms_name} is already taken, please choose another name.")
        raise


def get_existing_gdbms(path_to_gdbms_dir: Path = DBMS_FOLDER) -> GDBMSFilePath:
    """
    Gets and existing DBMS by name
    :param path_to_gdbms_dir: The directory of the DBMS folder.
    :return: A filepath for both the db and wn.
    """
    # todo test for this and break up
    while True:
        choices = get_and_display_available_dbms()

        if not choices:
            print("There are no databases, please create a new database.")
            dbms_path = create_new_dbms(path_to_dbms_dir=path_to_gdbms_dir)
            return dbms_path
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
                gdbms_name=existing_db_name, path_to_dbms_dir=path_to_gdbms_dir
            )
            indexes_path = get_existing_indexes_file_path(
                gdbms_name=existing_db_name, path_to_dbms_dir=path_to_gdbms_dir
            )
            wn_path = get_existing_wn_file_path(
                gdbms_name=existing_db_name, path_to_dbms_dir=path_to_gdbms_dir
            )
            return GDBMSFilePath(
                database_file_path=db_path,
                indexes_file_path=indexes_path,
                wiggle_number_file_path=wn_path,
            )
        except FileNotFoundError as e:
            print(f"Database files could not be found {e}")
            continue


def get_existing_gdbms_file_paths(
    existing_db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> GDBMSFilePath:
    pass


def delete_gdbms(gdbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER) -> int:
    """
    Deletes an existing DBMS
    :param gdbms_name The name of the DBMS.
    :param path_to_dbms_dir The directory of the DBMS folder.
    :return: An integer.
    """

    db_path = path_to_dbms_dir.joinpath(f"{gdbms_name}/")

    if not db_path.is_dir():
        raise Exception()

    files = glob(f"{db_path}/*")
    if files:
        for file in files:
            os.remove(file)

    db_path.rmdir()

    return 0


def select_gdbms() -> GDBMSFilePath:
    """
    Select the DBMS to be used.
    :return: A filepath for both the db and wn.
    """
    # TODO index.json and query_log

    db_choice = input(f"Use existing dbms (y/n):{INPUT_PROMPT_SPACING}")
    match db_choice:
        case "y" | "yes":
            db_path = get_existing_gdbms()
        case _:
            db_path = create_new_dbms()

    return db_path
