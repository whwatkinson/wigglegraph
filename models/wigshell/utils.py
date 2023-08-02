from pathlib import Path

from pydantic import BaseModel


class DatabaseWiggleNumberFilePaths(BaseModel):
    db: Path
    wn: Path
