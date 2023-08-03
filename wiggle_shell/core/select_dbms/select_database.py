from pathlib import Path


from wiggle_shell import DBMS_FOLDER


def create_new_database(db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER) -> Path:
    """
    Creates a new database with
    :param db_name:
    :param path_to_dbms_dir:
    :return:
    """

    new_db_file_path = path_to_dbms_dir.joinpath(f"{db_name}/database_{db_name}.json")

    if new_db_file_path.is_file():
        raise ValueError("Name in use")

    path_to_dbms_dir.joinpath(f"{db_name}").mkdir(parents=True, exist_ok=True)
    new_db_folder = path_to_dbms_dir.joinpath(f"{db_name}")
    path_touch_db = new_db_folder.joinpath(f"database_{db_name}.json")
    path_touch_db.touch()

    return path_touch_db


def get_existing_db_file_path(
    db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    db_file_path = path_to_dbms_dir.joinpath(f"{db_name}/database_{db_name}.json")
    if not db_file_path.is_file():
        raise FileNotFoundError()
    return db_file_path
