from typing import Optional

from pydantic import BaseModel


class Make(BaseModel):
    statement: str


class RawQuery(BaseModel):
    make: Optional[list[Make]]
    find: Optional[dict]
    criteria: Optional[dict]
    report: Optional[dict]
