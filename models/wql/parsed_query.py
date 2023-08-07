from typing import Optional

from pydantic import BaseModel, Field

from models.wql.enums.clauses import Clause
from wiggle_query_language.clauses.regexes.make import MAKE_STATEMENT_ALL


class Node(BaseModel):
    node_handle: Optional[str]
    node_label: Optional[str]
    node_props: Optional[str]


class MakeRel(BaseModel):
    rel_handle: Optional[str]
    rel_label: Optional[str]
    rel_props: Optional[str]


class ParsedPattern(BaseModel):
    # TODO simplify this with the above
    left_node: Optional[str]
    left_node_handle: Optional[str]
    left_node_label: Optional[str]
    left_node_props: Optional[str]
    left_middle_rel: Optional[str]
    left_middle_rel_handle: Optional[str]
    left_middle_rel_label: Optional[str]
    left_middle_rel_props: Optional[str]
    middle_node: Optional[str]
    middle_node_handle: Optional[str]
    middle_node_label: Optional[str]
    middle_node_props: Optional[str]
    middle_right_rel: Optional[str]
    middle_right_rel_handle: Optional[str]
    middle_right_rel_label: Optional[str]
    middle_right_rel_props: Optional[str]
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
