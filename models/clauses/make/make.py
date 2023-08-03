from typing import Optional

from pydantic import BaseModel


class MakeNodeParsed(BaseModel):
    wiggle_number: int
    statement_string: str
    node_label: str
    handle: Optional[str]
    belongings: Optional[dict]
    relations: Optional[dict]


class MakeStatementParsed(BaseModel):

    left_node: MakeNodeParsed
    right_node: Optional[MakeNodeParsed]
