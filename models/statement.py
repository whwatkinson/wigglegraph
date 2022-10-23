from typing import Optional

from pydantic import BaseModel

from models.enums.statement import Statement


class ParsedStatement(BaseModel):
    clause: Statement
    handle: Optional[str]
    node_label: str
    params: Optional[dict]
    statement_string: str
