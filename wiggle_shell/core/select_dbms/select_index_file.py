from pathlib import Path

from wiggle_shell import DBMS_FOLDER


def create_new_relationship_index(
    dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Creates a new database file.
    :param dbms_name: The name of the database.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return : The path to the new database file.
    """

    new_rel_idx_file_path = path_to_dbms_dir.joinpath(
        f"{dbms_name}/indexes_{dbms_name}.json"
    )

    if new_rel_idx_file_path.is_file():
        raise ValueError("Name in use")

    path_to_dbms_dir.joinpath(f"{dbms_name}").mkdir(parents=True, exist_ok=True)
    new_db_folder = path_to_dbms_dir.joinpath(f"{dbms_name}")
    path_touch_db = new_db_folder.joinpath(f"indexes_{dbms_name}.json")
    path_touch_db.touch()

    with open(f"{dbms_name}/indexes_{dbms_name}.json", "r") as file_handle:
        file_handle.write("""{"relationships": null}""")

    return path_touch_db


def get_existing_relationship_index_file_path(
    dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Gets the filepath of an existing wiggle number file.
    :param dbms_name: The name of the database.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return:
    """
    rel_idx_file_path = path_to_dbms_dir.joinpath(
        f"{dbms_name}/indexes_{dbms_name}.json"
    )
    if not rel_idx_file_path.is_file():
        raise FileNotFoundError()
    return rel_idx_file_path


if __name__ == "__main__":
    create_new_relationship_index("foo")
