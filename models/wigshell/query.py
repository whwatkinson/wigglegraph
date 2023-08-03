from typing import Optional

from pydantic import BaseModel


class ParsedQuery(BaseModel):
    make: Optional[dict]
    find: Optional[dict]
    criteria: Optional[dict]
    report: Optional[dict]
