from ast import literal_eval
from re import findall
from typing import Union

from exceptions.statements.statements import (
    IllegalNodePropertyType,
    MissingNodeLabel,
    StatementError,
)
from graph_logger.graph_logger import graph_logger
from models.enums.statement import Statement
from models.statement import ParsedStatement
from patterns.nodes import (
    make_clause_regex,
    nodes_regex,
    node_handle_regex,
    node_label_regex,
    node_params_regex,
    key_value_regex,
)


def parse_make_statement(statement_string: str) -> tuple[list[ParsedStatement], None]:

    nodes = find_nodes_from_statement(statement_string)

    node_statements = [
        parse_node(node_statement_string) for node_statement_string in nodes
    ]

    # edges = None
    # edge_statements = None

    return node_statements, None


def find_nodes_from_statement(statement_string: str) -> list[str]:
    graph_logger.debug(f"Parsing statement for nodes: {statement_string}")

    statement_search = make_clause_regex.search(statement_string)

    if not statement_search:
        raise StatementError(statement_string)

    nodes = nodes_regex.findall(statement_string)

    if not nodes:
        raise MissingNodeLabel(statement_string)

    graph_logger.debug(f"Found {len(nodes)} from {statement_string}")

    return nodes


def find_edges_from_statements(statement_string: str) -> list[str]:

    graph_logger.debug(f"Parsing statement for relationships: {statement_string}")

    # v1_rel = r"""\(.*:.+\)(?P<relationship>-\[[\w]*:.+\]->)\(.+:.+\)"""

    relationship_pattern = r"""(?P<rel>\<*-\[\s*\w*\s*:\s*\w+\s*\]-\>*)"""

    relationship_matches = findall(
        pattern=relationship_pattern, string=statement_string
    )

    if len(relationship_matches) > 2:
        # not supporting multi relationship creation atm
        raise Exception

    # lookup in parsed statement list and update


def parse_node(node_statement_string: str) -> ParsedStatement:
    """
    Parses the input from the user to make a node
    :param node_statement_string: The raw input string
    :return: A parsed statement to be passed to make_node
    """

    graph_logger.debug(f"parsing {node_statement_string}")

    # HANDLE
    if handle_search := node_handle_regex.search(string=node_statement_string):
        handle = handle_search.group("handle")
        graph_logger.debug(f"found {handle=} form {node_statement_string}")
    else:
        graph_logger.debug(f"{node_statement_string} does not have handle")
        handle = None

    # NODE LABEL
    node_label_search = node_label_regex.search(string=node_statement_string)

    if not node_label_search:
        raise MissingNodeLabel(node_statement_string)

    node_label = node_label_search.group("node_label")
    graph_logger.debug(f"Found {node_label=} from {node_statement_string}")

    params = None
    if params_search := node_params_regex.search(string=node_statement_string):

        params_string = params_search.group("params")
        graph_logger.debug(f"Found {params_string=} from {node_statement_string}")
        if params_string:
            params = build_properties_from_string(params_string)

    return ParsedStatement(
        clause=Statement.MAKE,
        handle=handle,
        node_label=node_label,
        belongings=params,
        statement_string=node_statement_string,
    )


def build_properties_from_string(params_string: str) -> dict:
    """
    The extracted params to be turned into a dictionary
    :param params_string: The raw params string
    :return: A parsed dictionary with correct data types
    """
    params_dict = dict()
    params_list = params_string.split("|")

    for param in params_list:

        param = param.strip()

        if match := key_value_regex.search(string=param):

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
    By identifying characteristics of data types
    this allows for making the best guess
    :param value: The string to be marshalled
    :return: The correct data type
    """
    graph_logger.info(f"starting conversion of  string {value}")
    value = value.strip('"')
    value = value.strip("'")

    # bool
    if value in {"True", "False"}:
        found_bool = None
        match value:
            case "False":
                found_bool = False
            case "false":
                found_bool = False
            case "True":
                found_bool = True
            case "true":
                found_bool = True
        graph_logger.debug(f"{value} was determined to be {found_bool}")
        return found_bool

    #  float
    if "." in value:
        try:
            found_float = float(value)
            graph_logger.debug(f"{value} was determined to be a float: {found_float}")
            return found_float
        except (TypeError, ValueError):
            pass

    #  int
    try:
        found_int = int(value)
        graph_logger.debug(f"{value} was determined to be an int: {found_int}")
        return found_int
    except (ValueError, TypeError):
        pass

    # list
    if "[" in value and "]" in value:
        found_list = literal_eval(value)
        graph_logger.debug(f"{value} was determined to be a list: {found_list}")
        return found_list

    # dict
    if "{" in value and "}" in value:
        graph_logger.debug(f"{value} was determined to be a dict, not allowed")
        raise IllegalNodePropertyType(value)

    # string
    try:
        # catch all.. todo make this better
        found_str = str(value)
        graph_logger.debug(f"{value} was determined to be a string: {found_str}")
        return found_str
    except Exception:
        pass
