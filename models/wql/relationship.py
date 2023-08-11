from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


TYPES_ALLOWED = Union[str, int, float, list]


class Relationship(BaseModel):
    wn: int
    rel_name: str
    created_at: float = datetime.now().timestamp()
    updated_at: Optional[float] = None

    # User defined
    belongings: Optional[dict[str, TYPES_ALLOWED]] = None
