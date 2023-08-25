from pathlib import Path

from models.wigish import GDBMSFilePath
from project_root import get_project_root

DATABASE_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_gdbms/sample_gdbms/database_sample_gdbms.json"
)

INDEXES_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_gdbms/sample_gdbms/indexes_sample_gdbms.json"
)

WIGGLE_NUMBER_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_gdbms/sample_gdbms/wiggle_number_sample_gdbms.txt"
)

TEST_DBMS_FOLDER_PATH = Path(f"{get_project_root()}/testing/test_gdbms/")

TEST_DBMS = GDBMSFilePath(
    database_file_path=DATABASE_TEST_FILE_PATH,
    indexes_file_path=INDEXES_TEST_FILE_PATH,
    wiggle_number_file_path=WIGGLE_NUMBER_TEST_FILE_PATH,
)
