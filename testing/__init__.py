from pathlib import Path

from project_root import get_project_root

DATABASE_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/sample_dbms/database_sample_dbms.json"
)
WIGGLE_NUMBER_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/sample_dbms/wiggle_number_sample_dbms.txt"
)

TEST_DBMS_FOLDER_PATH = Path(f"{get_project_root()}/testing/test_dbms/")
