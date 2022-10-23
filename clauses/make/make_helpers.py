from ast import literal_eval
from re import search
from typing import Union

from exceptions.statements.statements import (
    IllegalNodePropertyType,
    MissingNodeLabel,
    StatementError,
)
from models.enums.statement import Statement
from models.statement import ParsedStatement
from graph_logger.graph_logger import graph_logger


def parse_make_statment(statement_string: str) -> ParsedStatement:
    graph_logger.debug(statement_string)
    # validate that the correct statement is called

    statement = None
    handle = None
    params = None

    make_statement_pattern = r"""(?P<clause>MAKE|make)"""
    statement_search = search(make_statement_pattern, statement_string)

    if not statement_search:
        raise StatementError(statement_string)

    statement = Statement[statement_search.group("clause").upper()]

    node_label_pattern = r""":\s*(?P<node_label>\w+)"""
    node_label_search = search(node_label_pattern, statement_string)

    if not node_label_search:
        raise MissingNodeLabel(statement_string)

    node_label = node_label_search.group("node_label")

    handle_pattern = r"""\(\s*(?P<handle>[a-zA-Z0-9]+)\:"""

    if handle_search := search(handle_pattern, statement_string):
        handle = handle_search.group("handle")

    params_pattern = r"""\s*?(?P<params>[\w\'\:\|\s\-\.\,\[\]]+)?\s*}\s*\)"""
    if params_search := search(params_pattern, statement_string):

        params_string = params_search.group("params")

        if params_string:
            params = build_properties_from_string(params_string)

        else:
            params = None

    return ParsedStatement(
        clause=statement,
        handle=handle,
        node_label=node_label,
        belongings=params,
        statement_string=statement_string,
    )


def build_properties_from_string(params_string: str) -> dict:

    params_dict = dict()
    params_list = params_string.split("|")
    key_value_pattern = r"""(?P<key>[\w]+):\s?(?P<value>[\[\]\s\,'\w\d\-\.]+)"""

    for param in params_list:

        param = param.strip()

        if match := search(key_value_pattern, param):

            key = match.group("key")
            value = match.group("value")

            if value.strip() == "":
                raise IllegalNodePropertyType(param)

            value_parsed = string_to_correct_data_type(value)

            params_dict[key] = value_parsed

    return params_dict


def string_to_correct_data_type(value: str) -> Union[float, int, str, list]:

    value = value.strip('"')
    value = value.strip("'")

    # bool
    if value in {"True", "False"}:

        match value:
            case "False":
                return False
            case "false":
                return False
            case "True":
                return True
            case "true":
                return True

    #  float
    if "." in value:
        try:
            value_parsed = float(value)
            return value_parsed
        except (TypeError, ValueError):
            pass

    #  int
    try:
        value_parsed = int(value)
        return value_parsed
    except (ValueError, TypeError):
        pass

    # list
    if "[" in value and "]" in value:
        return literal_eval(value)

    # dict
    if "{" in value and "}" in value:
        raise IllegalNodePropertyType(value)

    # string
    try:
        value_parsed = str(value)
        return value_parsed
    except Exception:
        pass
