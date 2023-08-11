from typing import Optional

from pydantic import BaseModel, Field

from models.wql.enums.clauses import Clause
from wiggle_query_language.clauses.regexes.make_patterns import MAKE_STATEMENT_ALL_REGEX


class Node(BaseModel):
    node_handle: Optional[str]
    node_label: Optional[str]
    node_props: Optional[str]


class Rel(BaseModel):
    rel_handle: Optional[str]
    rel_label: Optional[str]
    rel_props: Optional[str]


class ParsedPattern(BaseModel):
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

    @property
    def number_of_nodes(self) -> int:
        """
        Number of nodes in this ParsedPattern.
        :return: An integer.
        """

        return bool(self.left_node) + bool(self.middle_node) + bool(self.right_node)

    @property
    def number_of_relationships(self) -> int:
        """
        Number of relationships in this ParsedPattern.
        :return: An integer.
        """
        return bool(self.left_middle_rel) + bool(self.middle_right_rel)

    def __repr__(self) -> str:
        return f"|{self.__class__.__name__}| Nodes: {self.number_of_nodes}, Rels: {self.number_of_relationships}"


class ParsedMake(BaseModel):
    raw_statement: str = Field(regex=MAKE_STATEMENT_ALL_REGEX.pattern)
    clause: Clause = Clause.MAKE
    parsed_pattern_list: list[ParsedPattern]


class ParsedQuery(BaseModel):
    make: Optional[list[ParsedMake]]
    find: Optional[dict] = None
    criteria: Optional[dict] = None
    report: Optional[dict] = None
