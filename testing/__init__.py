from pathlib import Path

from project_root import get_project_root


DATABASE_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/database_test.json"
)
WIGGLE_NUMBER_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/wiggle_number_test.txt"
)
