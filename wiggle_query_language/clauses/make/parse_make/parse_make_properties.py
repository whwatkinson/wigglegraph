from ast import literal_eval
from typing import Optional

from models.wql import TYPES_ALLOWED, MakeListProperty, MakePrimitiveProperty

from graph_logger.graph_logger import graph_logger
from exceptions.wql.make import MakeIllegalPropertyValue
from wiggle_query_language.clauses.regexes.make_patterns import (
    LIST_KEY_VALUE_REGEX,
    ALL_PARAMS_KEY_VALUE_REGEX,
)


def make_properties(params_string: str) -> Optional[dict]:
    """
    The extracted params to be turned into a dictionary
    :param params_string: The raw params string
    :return: A parsed dictionary with correct data types
    """
    property_dictionary = dict()

    if not params_string:
        return None

    # Handle non list properties
    if props_primitive := ALL_PARAMS_KEY_VALUE_REGEX.finditer(params_string):
        for match in props_primitive:
            property_name = match.group("property_name")
            property_value = match.group("property_value")
            if property_value.strip() == "":
                raise MakeIllegalPropertyValue(
                    f"Error for setting property in {params_string} {property_name} was empty a value must be supplied"
                )

            make_primitive_property = MakePrimitiveProperty(**match.groupdict())
            value_parsed = handle_extracted_property(make_primitive_property)

            property_dictionary[property_name] = value_parsed

    if props_list := LIST_KEY_VALUE_REGEX.finditer(params_string):
        for match in props_list:
            make_list_property = MakeListProperty(**match.groupdict())

            list_parsed = handle_list_property(make_list_property.property_value)

            property_dictionary[make_list_property.property_name] = list_parsed

    return property_dictionary


def handle_extracted_property(make_property: MakePrimitiveProperty):
    extracted_property = make_property.yield_extracted_param()

    for property_type, extracted_property in extracted_property.items():
        striped_value = extracted_property.strip('"').strip("'")

        match property_type:
            case "none":
                return handle_null_property(striped_value)
            case "bool":
                return handle_bool_property(striped_value)
            case "float":
                return handle_float_property(striped_value)
            case "int":
                return handle_int_property(striped_value)
            case "string":
                return handle_string_property(striped_value)
            case _:
                raise Exception()


def handle_null_property(value: str) -> None:
    if value != "null":
        raise Exception()

    return None


def handle_bool_property(value: str) -> bool:
    match value:
        case "true":
            bool_found = True
        case "false":
            bool_found = False
        case _:
            raise Exception()
    graph_logger.debug(f"{value} was determined to be {bool_found}")
    return bool_found


def handle_float_property(value: str) -> float:
    try:
        found_float = float(value)
        graph_logger.debug(f"{value} was determined to be a float: {found_float}")
        return found_float
    except (TypeError, ValueError):
        pass


def handle_int_property(value: str) -> int:
    try:
        found_int = int(value)
        graph_logger.debug(f"{value} was determined to be an int: {found_int}")
        return found_int
    except (ValueError, TypeError):
        pass


def handle_list_property(value: str) -> list[TYPES_ALLOWED]:
    # TODO change to it iterate ove the list.
    value = value.replace("true", "True").replace("false", "False")
    found_list = literal_eval(value)
    graph_logger.debug(f"{value} was determined to be a list: {found_list}")
    return found_list


def handle_string_property(value: str) -> str:
    try:
        # catch all.. todo make this better
        found_str = str(value)
        graph_logger.debug(f"{value} was determined to be a string: {found_str}")
        return found_str
    except Exception:
        pass


if __name__ == "__main__":
    s = """{int: 1, float: 3.14, bool: true, none: null, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"], list2: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]}"""

    make_properties(s)
