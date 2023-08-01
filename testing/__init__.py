from pathlib import Path

from project_root import get_project_root


TEST_DATABASE_FILE_PATH = Path(f"{get_project_root()}/test_database.json")
TEST_WIGGLE_NUMBER_STATE_FILE_PATH = Path(
    f"{get_project_root()}testing/test_wiggle_number_state.txt"
)
