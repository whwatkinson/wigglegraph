from typing import Optional

from pydantic import BaseModel, Field

from wiggle_query_language.clauses.make.make_patterns import MAKE_STATEMENT_ALL


class RawMake(BaseModel):
    statement: str = Field(regex=MAKE_STATEMENT_ALL.pattern)


class RawQuery(BaseModel):
    make: Optional[list[RawMake]]
    find: Optional[dict] = None
    criteria: Optional[dict] = None
    report: Optional[dict] = None
