from pathlib import Path

from wiggle_shell import DBMS_FOLDER


def create_new_database(dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER) -> Path:
    """
    Creates a new database file.
    :param dbms_name: The name of the database.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return : The path to the new database file.
    """

    path_to_dbms_dir.joinpath(f"{dbms_name}").mkdir(parents=True, exist_ok=True)
    new_database_file_path = path_to_dbms_dir.joinpath(
        f"{dbms_name}/database_{dbms_name}.json"
    )

    if new_database_file_path.is_file():
        raise ValueError("A Database file already exists")

    new_database_file_path.touch()

    return new_database_file_path


def get_existing_db_file_path(
    dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Gets the filepath of an existing wiggle number file.
    :param dbms_name: The name of the database.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return:
    """
    db_file_path = path_to_dbms_dir.joinpath(f"{dbms_name}/database_{dbms_name}.json")
    if not db_file_path.is_file():
        raise FileNotFoundError()
    return db_file_path
