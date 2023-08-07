from typing import Optional

from pydantic import BaseModel, Field

from models.wql.enums.clauses import Clause
from wiggle_query_language.clauses.make.make_patterns import MAKE_STATEMENT_ALL


class ParsedPattern(BaseModel):
    left_node: Optional[str]
    left_node_handle: Optional[str]
    left_node_label: Optional[str]
    left_node_props: Optional[str]
    rel_left_middle: Optional[str]
    rel_left_middle_handle: Optional[str]
    rel_left_middle_label: Optional[str]
    rel_lm_props: Optional[str]
    middle_node: Optional[str]
    middle_node_handle: Optional[str]
    middle_node_label: Optional[str]
    middle_node_props: Optional[str]
    rel_middle_right: Optional[str]
    rel_middle_right_handle: Optional[str]
    rel_middle_right_label: Optional[str]
    rel_mr_props: Optional[str]
    right_node: Optional[str]
    right_node_handle: Optional[str]
    right_node_label: Optional[str]
    right_node_props: Optional[str]


class ParsedMake(BaseModel):
    raw_statement: str = Field(regex=MAKE_STATEMENT_ALL.pattern)
    clause: Clause = Clause.MAKE
    parsed_pattern_list: list[ParsedPattern]


class ParsedQuery(BaseModel):
    make: Optional[list[ParsedMake]]
    find: Optional[dict] = None
    criteria: Optional[dict] = None
    report: Optional[dict] = None
