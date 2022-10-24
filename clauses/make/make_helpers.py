from ast import literal_eval
from re import search
from typing import Union

from exceptions.statements.statements import (
    IllegalNodePropertyType,
    MissingNodeLabel,
    StatementError,
)
from graph_logger.graph_logger import graph_logger
from models.enums.statement import Statement
from models.statement import ParsedStatement


def parse_make_statment(statement_string: str) -> ParsedStatement:
    """
    Parses the input from the user to make a node
    :param statement_string: The raw input string
    :return: A parsed statement to be passed to make_node
    """
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
    """
    The extracted params to be turned into a dictionary
    :param params_string: The raw params string
    :return: A parsed dictionary with correct data types
    """
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
    """
    Turns a string to the correct datatype.
    By identifying characteristics of data types this allows for making a best guess.
    :param value: The string to be marshalled
    :return: The correct data type
    """
    graph_logger.info(f"starting conversion of  string {value}")
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
            graph_logger.debug(f"{value} was detirmined to be a float")
            return value_parsed
        except (TypeError, ValueError):
            pass

    #  int
    try:
        value_parsed = int(value)
        graph_logger.debug(f"{value} was detirmined to be an int")
        return value_parsed
    except (ValueError, TypeError):
        pass

    # list
    if "[" in value and "]" in value:
        graph_logger.debug(f"{value} was detirmined to be a list")
        return literal_eval(value)

    # dict
    if "{" in value and "}" in value:
        graph_logger.debug(f"{value} was detirmined to be a dict, not allowed")
        raise IllegalNodePropertyType(value)

    # string
    try:
        # catch all.. todo make this better
        value_parsed = str(value)
        graph_logger.debug(f"{value} was detirmined to be a string")
        return value_parsed
    except Exception:
        pass
