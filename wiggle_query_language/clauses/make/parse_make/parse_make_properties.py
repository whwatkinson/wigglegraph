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

    if not params_string:
        return None

    # Handle primitive properties first
    primitive_property_dictionary = parse_primitive_properties(params_string)

    # Then attempt the list
    list_property_dictionary = parse_list_property(params_string)

    return primitive_property_dictionary | list_property_dictionary


def parse_primitive_properties(params_string: str) -> dict:
    primitive_property_dictionary = dict()
    if props_primitive := ALL_PARAMS_KEY_VALUE_REGEX.finditer(params_string):
        for match in props_primitive:
            make_primitive_property = MakePrimitiveProperty(**match.groupdict())
            if match.group("property_value").strip() == "":
                raise MakeIllegalPropertyValue(
                    f"Error for setting property in {params_string} {make_primitive_property.property_name} was empty a value must be supplied"
                )
            try:
                value_parsed = handle_extracted_primitive_property(
                    make_primitive_property
                )
            except MakeIllegalPropertyValue as e:
                raise e

            primitive_property_dictionary[
                make_primitive_property.property_name
            ] = value_parsed

    return primitive_property_dictionary


def parse_list_property(params_string: str) -> dict:
    list_property_dictionary = dict()

    if props_list := LIST_KEY_VALUE_REGEX.finditer(params_string):
        for match in props_list:
            make_list_property = MakeListProperty(**match.groupdict())
            try:
                list_parsed = handle_list_property(make_list_property.property_value)
            except MakeIllegalPropertyValue as e:
                raise e
            list_property_dictionary[make_list_property.property_name] = list_parsed

    return list_property_dictionary


def handle_extracted_primitive_property(make_property: MakePrimitiveProperty):
    extracted_property = make_property.yield_extracted_param()

    for property_type, extracted_property in extracted_property.items():
        striped_value = extracted_property.strip('"').strip("'").strip()

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
        raise MakeIllegalPropertyValue(
            f"Value must be null: provided value was {value} "
        )

    return None


def handle_bool_property(value: str) -> bool:
    match value:
        case "true":
            bool_found = True
        case "True":
            raise MakeIllegalPropertyValue(
                f"{value} should be lowercase. Boolean property example {{foo: true}}"
            )
        case "false":
            bool_found = False
        case "False":
            raise MakeIllegalPropertyValue(
                f"{value} should be lowercase. Boolean property example {{foo: false}}"
            )
        case _:
            raise MakeIllegalPropertyValue(f"{value} is not a boolean")
    graph_logger.debug(f"{value} was determined to be {bool_found}")
    return bool_found


def handle_float_property(value: str) -> float:
    if "." not in value:
        raise MakeIllegalPropertyValue(
            f"{value} missing a period please add, e.g {{foo: 3.14}}"
        )
    try:
        found_float = float(value)
        graph_logger.debug(f"{value} was determined to be a float: {found_float}")
        return found_float
    except (TypeError, ValueError):
        raise MakeIllegalPropertyValue(
            f"{value} was mot a decimal. Float property example: {{foo: 3.14}}"
        )


def handle_int_property(value: str) -> int:
    if "." in value:
        raise MakeIllegalPropertyValue(
            f"{value} has a period, please remove, e.g {{foo: 6}}"
        )
    try:
        found_int = int(value)
        graph_logger.debug(f"{value} was determined to be an int: {found_int}")
        return found_int
    except (ValueError, TypeError):
        raise MakeIllegalPropertyValue(
            f"{value} was mot an integer. Integer property example: {{foo: 3.14}}"
        )


def handle_string_property(value: str) -> str:
    if value in {"Null", "None", "none"}:
        raise MakeIllegalPropertyValue(
            f"Cannot use {value} as a string, please use the null type for example {{foo: null}}"
        )

    # catch all.. todo make this better
    found_str = str(value)
    graph_logger.debug(f"{value} was determined to be a string: {found_str}")
    return found_str


def handle_list_property(value_in: str) -> list[TYPES_ALLOWED]:
    # TODO change to it iterate ove the list.
    value = value_in.replace("true", "True").replace("false", "False")
    try:
        found_list = literal_eval(value)
    except SyntaxError:
        raise MakeIllegalPropertyValue(f"{value_in} contained an Error.")
    graph_logger.debug(f"{value_in} was determined to be a list: {found_list}")
    return found_list


if __name__ == "__main__":
    s = """{int: 1, float: 3.14, bool: true, none: None, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"], list2: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]}"""

    make_properties(s)
