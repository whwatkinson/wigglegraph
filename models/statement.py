from typing import Optional

from pydantic import BaseModel

from models.enums.statement import Statement


class ParsedStatement(BaseModel):
    statement_string: str
    node_label: str
    statement_string: str
    clause: Statement
    handle: Optional[str]
    belongings: Optional[dict]
    relations: Optional[dict]
