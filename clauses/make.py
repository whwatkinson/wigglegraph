from re import match, search
from typing import Optional

from pydantic import BaseModel

from enums.statement import Statement
from exceptions.statements import IllegalParameterType, StatementError


class ParsedStatement(BaseModel):
    clause: Statement
    handle: Optional[str]
    node_label: str
    params: Optional[dict]


pattern = r"""(?P<clause>MAKE|make)\s?\((?P<handle>\w+)?\s?:(?P<node_label>\w+)\)?(?P<params>\{[\w:'\s-]+\})?"""


def parse_make_statment(input_string: str) -> ParsedStatement:

    # validate that the correct statement is called

    make_pattern = r"""(?P<clause>MAKE|make)"""

    if not match(make_pattern, input_string):
        raise StatementError(input_string)

    if matches := search(pattern, input_string):

        handle = matches.group("handle")
        node_label = matches.group("node_label")
        params = matches.group("params")

        return ParsedStatement(
            clause=Statement.MAKE, handle=handle, node_label=node_label, params=params
        )

    raise Exception()


def build_params_from_string(params_string: str) -> dict:

    raise IllegalParameterType(params_string)
