from pathlib import Path

from project_root import get_project_root


DBMS_FOLDER = Path(f"{get_project_root()}/dbms/")
INPUT_PROMPT_SPACING = " " * 5


def create_new_wiggle_number_file(
    db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """

    :param db_name:
    :param path_to_dbms_dir:
    :return:
    """
    new_wn_state_file_path = path_to_dbms_dir.joinpath(
        f"{db_name}/wiggle_number_{db_name}.txt"
    )
    if new_wn_state_file_path.is_file():
        raise ValueError("A wiggle file already exists")

    new_wn_state_file_path.touch()

    with open(new_wn_state_file_path, "w") as file:
        file.write("0")

    return new_wn_state_file_path


def get_existing_wn_file_path(
    db_name: str, path_to_dbms_dir: Path = DBMS_FOLDER
) -> Path:
    """

    :param db_name:
    :param path_to_dbms_dir:
    :return:
    """
    wn_file_path = path_to_dbms_dir.joinpath(f"{db_name}/wiggle_number_{db_name}.txt")
    if not wn_file_path.is_file():
        raise FileNotFoundError()
    return wn_file_path
