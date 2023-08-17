# from ast import literal_eval
# from typing import Optional
#
# from exceptions.wql.make import MakeIllegalPropertyValue
# from graph_logger.graph_logger import graph_logger
# from models.wql import WG_ALLOWED_TYPES, MakeProperty, PropertyType
# from wiggle_query_language.clauses.regexes.make_patterns import (
#     ALL_PARAMS_KEY_VALUE_REGEX,
# )
#
#
# def make_properties(properties_string: str) -> Optional[dict]:
#     """
#     The extracted params to be turned into a dictionary
#     :param properties_string: The raw params string.
#     :return: A parsed dictionary with correct data types
#     """
#
#     if not properties_string:
#         return None
#
#     property_dictionary = parse_properties(properties_string)
#
#     return property_dictionary
#
#
# def parse_properties(properties_string: str) -> dict:
#     """
#     Parses the properties_string to WiggleGraph types.
#     :param properties_string: The raw params string.
#     :return: A dictionary ready for export.
#     """
#     primitive_property_dictionary = dict()
#     if props_primitive := ALL_PARAMS_KEY_VALUE_REGEX.finditer(properties_string):
#         for match in props_primitive:
#             make_primitive_property = MakeProperty(**match.groupdict())
#             if match.group("property_value").strip() == "":
#                 raise MakeIllegalPropertyValue(
#                     f"Error for setting property in {properties_string} {make_primitive_property.property_name} was empty a value must be supplied"
#                 )
#             try:
#                 value_parsed = handle_extracted_property(make_primitive_property)
#             except MakeIllegalPropertyValue as e:
#                 raise e
#
#             primitive_property_dictionary[
#                 make_primitive_property.property_name
#             ] = value_parsed
#
#     return primitive_property_dictionary
#
#
# def handle_extracted_property(
#     make_property: MakeProperty,
# ) -> WG_ALLOWED_TYPES:
#     """
#     Handles the selection for parsing the extracted property.
#     :param make_property: The extracted property.
#     :return: A parsed WiggleGraph property.
#     """
#     extracted_property = make_property.yield_extracted_property()
#
#     striped_value = extracted_property.property_value.strip('"').strip("'").strip()
#
#     match extracted_property.property_type:
#         case PropertyType.NONE_TYPE:
#             return handle_null_property(striped_value)
#         case PropertyType.BOOL_TYPE:
#             return handle_bool_property(striped_value)
#         case PropertyType.FLOAT_TYPE:
#             return handle_float_property(striped_value)
#         case PropertyType.INT_TYPE:
#             return handle_int_property(striped_value)
#         case PropertyType.LIST_TYPE:
#             return handle_list_property(striped_value)
#         case PropertyType.STRING_TYPE:
#             return handle_string_property(striped_value)
#         case _:
#             raise Exception()
#
#
# def handle_null_property(value: str) -> None:
#     """
#     Handles the parsing for WiggleGraph null values.
#     :param value: The extracted property value.
#     :return: A Python None
#     """
#     if value != "null":
#         raise MakeIllegalPropertyValue(
#             f"Value must be null: provided value was {value} "
#         )
#
#     return None
#
#
# def handle_bool_property(value: str) -> bool:
#     """
#     Handles the parsing for WiggleGraph bool values.
#     :param value: The extracted property value.
#     :return: A Python bool.
#     """
#     match value:
#         case "true":
#             bool_found = True
#         case "false":
#             bool_found = False
#         case "True":
#             raise MakeIllegalPropertyValue(
#                 f"{value} should be lowercase. Boolean property example {{foo: true}}"
#             )
#         case "False":
#             raise MakeIllegalPropertyValue(
#                 f"{value} should be lowercase. Boolean property example {{foo: false}}"
#             )
#         case _:
#             raise MakeIllegalPropertyValue(f"{value} is not a boolean")
#     graph_logger.debug(f"{value} was determined to be {bool_found}")
#     return bool_found
#
#
# def handle_float_property(value: str) -> float:
#     """
#     Handles the parsing for WiggleGraph float values
#     :param value: The extracted property value.
#     :return: A Python float
#     """
#     if "." not in value:
#         raise MakeIllegalPropertyValue(
#             f"{value} missing a period. Float property example: {{foo: 3.14}}"
#         )
#     try:
#         found_float = float(value)
#         graph_logger.debug(f"{value} was determined to be a float: {found_float}")
#         return found_float
#     except (TypeError, ValueError):
#         raise MakeIllegalPropertyValue(
#             f"{value} was mot a decimal. Float property example: {{foo: 3.14}}"
#         )
#
#
# def handle_int_property(value: str) -> int:
#     """
#     Handles the parsing for WiggleGraph int values
#     :param value: The extracted property value.
#     :return: A Python int
#     """
#
#     if "." in value:
#         raise MakeIllegalPropertyValue(
#             f"{value} has a period, please remove, e.g {{foo: 6}}"
#         )
#     try:
#         found_int = int(value)
#         graph_logger.debug(f"{value} was determined to be an int: {found_int}")
#         return found_int
#     except (ValueError, TypeError):
#         raise MakeIllegalPropertyValue(
#             f"{value} was mot an integer. Integer property example: {{foo: 3.14}}"
#         )
#
#
# def handle_list_property(value_in: str) -> list[WG_ALLOWED_TYPES]:
#     """
#     Handles the parsing for WiggleGraph list values
#     :param value_in: The extracted property value.
#     :return: A Python list.
#     """
#     # params validation happens in check_make_params
#     value = value_in.replace("true", "True").replace("false", "False")
#     try:
#         found_list = literal_eval(value)
#     except SyntaxError:
#         raise MakeIllegalPropertyValue(f"{value_in} contained an Error.")
#     graph_logger.debug(f"{value_in} was determined to be a list: {found_list}")
#     return found_list
#
#
# def handle_string_property(value: str) -> str:
#     """
#     Handles the parsing for WiggleGraph string values
#     :param value: The extracted property value.
#     :return: A Python string
#     """
#     if value in {"Null", "None", "none"}:
#         raise MakeIllegalPropertyValue(
#             f"Cannot use {value} as a string, please use the null type for example {{foo: null}}"
#         )
#
#     if value in {"true", "True", "false", "False"}:
#         raise MakeIllegalPropertyValue(
#             f"Cannot use {value} as a string, please use the bool type for example {{foo: true}}"
#         )
#
#     found_str = str(value)
#     graph_logger.debug(f"{value} was determined to be a string: {found_str}")
#     return found_str
#
#
# if __name__ == "__main__":
#     s = """{int: 1, float: 3.14, bool: true, none: None, str: '2', str2:"2_4", str3: "3 4 5", email: 'foo@bar.net',  list: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"], list2: [1, 3.14, true, false, '2', "2_4", "3 4", "foo@bar.net"]}"""
#
#     make_properties(s)
