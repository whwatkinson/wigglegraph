from json import dumps
from pathlib import Path

from wiggle_shell import DBMS_FOLDER


def create_new_indexes_file(
    dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Creates a new database file.
    :param dbms_name: The name of the database.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return : The path to the new database file.
    """

    path_to_dbms_dir.joinpath(f"{dbms_name}").mkdir(parents=True, exist_ok=True)
    new_indexes_file_path = path_to_dbms_dir.joinpath(
        f"{dbms_name}/indexes_{dbms_name}.json"
    )

    if new_indexes_file_path.is_file():
        raise ValueError("An Indexes file already exists")

    new_indexes_file_path.touch()

    new_index_dict = {
        "node_relationships": {},
        "node_labels": [],
        "relationship_names": [],
    }

    with open(new_indexes_file_path, "w") as file_handle:
        file_handle.write(dumps(new_index_dict))

    return new_indexes_file_path


def get_existing_indexes_file_path(
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
    create_new_indexes_file("foo", DBMS_FOLDER)
