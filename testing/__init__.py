from pathlib import Path

from models.wigsh import DbmsFilePath
from project_root import get_project_root

DATABASE_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/sample_dbms/database_sample_dbms.json"
)

RELATIONSHIP_INDEX_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/sample_dbms/relationship_index_sample_dbms.json"
)

WIGGLE_NUMBER_TEST_FILE_PATH = Path(
    f"{get_project_root()}/testing/test_dbms/sample_dbms/wiggle_number_sample_dbms.txt"
)

TEST_DBMS_FOLDER_PATH = Path(f"{get_project_root()}/testing/test_dbms/")

TEST_DBMS = DbmsFilePath(
    database_file_path=DATABASE_TEST_FILE_PATH,
    relationship_index_file_path=RELATIONSHIP_INDEX_FILE_PATH,
    wiggle_number_file_path=WIGGLE_NUMBER_TEST_FILE_PATH,
)
