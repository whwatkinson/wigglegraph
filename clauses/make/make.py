from ast import literal_eval
from re import search
from typing import Union

from models.enums.statement import Statement
from exceptions.statements import IllegalParameterType, MissingNodeLabel, StatementError
from models.statement import ParsedStatement


def parse_make_statment(statement_string: str) -> ParsedStatement:

    # validate that the correct statement is called

    make_statement_pattern = r"""(?P<clause>MAKE|make)"""

    if not search(make_statement_pattern, statement_string):
        raise StatementError(statement_string)

    node_label_pattern = r""":\s*(?P<node_label>\w+)"""

    if not search(node_label_pattern, statement_string):
        raise MissingNodeLabel(statement_string)

    parsing_pattern = rf"""{make_statement_pattern}\s*\((?P<handle>\w+)?\s*{node_label_pattern}\s*{{?(?P<params>[\w\'\:\|\s\-\.\,\[\]]+)?\s*}}?\s*\)"""

    if matches := search(parsing_pattern, statement_string):

        handle = matches.group("handle")
        node_label = matches.group("node_label")
        params_string = matches.group("params")

        if params_string:
            params = build_params_from_string(params_string)

        else:
            params = None

        return ParsedStatement(
            clause=Statement.MAKE,
            handle=handle,
            node_label=node_label,
            params=params,
            statement_string=statement_string,
        )


def build_params_from_string(params_string: str) -> dict:

    params_dict = dict()
    params_list = params_string.split("|")
    key_value_pattern = r"""(?P<key>[\w]+):\s?(?P<value>[\[\]\s\,'\w\d\-\.]+)"""

    for param in params_list:

        param = param.strip()

        if match := search(key_value_pattern, param):

            key = match.group("key")
            value = match.group("value")

            if value.strip() == "":
                raise IllegalParameterType(param)

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
        raise IllegalParameterType(value)

    # string
    try:
        value_parsed = str(value)
        return value_parsed
    except Exception:
        pass
