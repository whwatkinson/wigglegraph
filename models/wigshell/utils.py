from pathlib import Path

from pydantic import BaseModel


class DbmsFilePath(BaseModel):
    db: Path
    wn: Path
