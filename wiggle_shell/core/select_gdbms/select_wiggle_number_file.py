from pathlib import Path

from project_root import get_project_root

DBMS_FOLDER = Path(f"{get_project_root()}/dbms/")
INPUT_PROMPT_SPACING = " " * 5


def create_new_wiggle_number_file(
    dbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Create a new Wiggle number file.
    :param dbms_name The name of the database.
    :param path_to_dbms_dir The directory of the DBMS folder.
    :return The path to the new Wiggle number file.
    """
    path_to_dbms_dir.joinpath(f"{dbms_name}").mkdir(parents=True, exist_ok=True)
    new_wn_state_file_path = path_to_dbms_dir.joinpath(
        f"{dbms_name}/wiggle_number_{dbms_name}.txt"
    )
    if new_wn_state_file_path.is_file():
        raise ValueError("A WiggleNUmber file already exists")

    new_wn_state_file_path.touch()

    with open(new_wn_state_file_path, "w") as file:
        file.write("0")

    return new_wn_state_file_path


def get_existing_wn_file_path(
    gdbms_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """
    Gets the filepath of an existing wiggle number file.
    :param gdbms_name: The name of the DBMS.
    :param path_to_dbms_dir: The directory of the DBMS folder.
    :return: The path to the Wiggle number file for a given database.
    """
    wn_file_path = path_to_dbms_dir.joinpath(
        f"{gdbms_name}/wiggle_number_{gdbms_name}.txt"
    )
    if not wn_file_path.is_file():
        raise FileNotFoundError()
    return wn_file_path
