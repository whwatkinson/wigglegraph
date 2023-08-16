from pathlib import Path

from pydantic import BaseModel


class DbmsFilePath(BaseModel):
    """
    Holds the file paths for the Database and Wiggle Number
    """

    database_file_path: Path
    indexes_file_path: Path
    wiggle_number_file_path: Path
