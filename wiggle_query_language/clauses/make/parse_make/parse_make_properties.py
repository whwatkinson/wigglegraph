# from ast import literal_eval
# from typing import Union
#
# from graph_logger.graph_logger import graph_logger
#
# from exceptions.wql.make import MakeIllegalNodePropertyType
# from wiggle_query_language.clauses.regexes.make_patterns import (
#     LIST_KEY_VALUE_REGEX,
#     NOT_LIST_KEY_VALUE_REGEX,
# )
#
# #
# #
# # def make_properties(params_string: str) -> dict:
# #     """
# #     The extracted params to be turned into a dictionary
# #     :param params_string: The raw params string
# #     :return: A parsed dictionary with correct data types
# #     """
# #     params_dict = dict()
# #     params_list = params_string.split("|")
# #
# #     # params of list
# #
# #     # TODO check that the names of the
# #
# #     for param in params_list:
# #         param = param.strip()
# #
# #         if match := key_value_regex.search(string=param):
# #             key = match.group("key")
# #             value = match.group("value")
# #
# #             if value.strip() == "":
# #                 raise MakeIllegalNodePropertyType(param)
# #
# #             value_parsed = string_to_correct_data_type(value)
# #
# #             params_dict[key] = value_parsed
# #
# #     return params_dict
# #
# #
# # def string_to_correct_data_type(value: str) -> Union[float, int, str, list]:
# #     """
# #     Turns a string to the correct datatype.
# #     By identifying characteristics of data types
# #     this allows for making the best guess
# #     :param value: The string to be marshalled
# #     :return: The correct data type
# #     """
# #     graph_logger.info(f"starting conversion of  string {value}")
# #     value = value.strip('"')
# #     value = value.strip("'")
# #
# #     # bool
# #     if value in {"True", "False"}:
# #         found_bool = None
# #         match value:
# #             case "False":
# #                 found_bool = False
# #             case "false":
# #                 found_bool = False
# #             case "True":
# #                 found_bool = True
# #             case "true":
# #                 found_bool = True
# #         graph_logger.debug(f"{value} was determined to be {found_bool}")
# #         return found_bool
# #
# #     #  float
# #     if "." in value:
# #         try:
# #             found_float = float(value)
# #             graph_logger.debug(f"{value} was determined to be a float: {found_float}")
# #             return found_float
# #         except (TypeError, ValueError):
# #             pass
# #
# #     #  int
# #     try:
# #         found_int = int(value)
# #         graph_logger.debug(f"{value} was determined to be an int: {found_int}")
# #         return found_int
# #     except (ValueError, TypeError):
# #         pass
# #
# #     # list
# #     if "[" in value and "]" in value:
# #         found_list = literal_eval(value)
# #         graph_logger.debug(f"{value} was determined to be a list: {found_list}")
# #         return found_list
# #
# #     # dict
# #     if "{" in value and "}" in value:
# #         graph_logger.debug(f"{value} was determined to be a dict, not allowed")
# #         raise MakeIllegalNodePropertyType(value)
# #
# #     # string
# #     try:
# #         # catch all.. todo make this better
# #         found_str = str(value)
# #         graph_logger.debug(f"{value} was determined to be a string: {found_str}")
# #         return found_str
# #     except Exception:
# #         pass
# #
#
#
# def make_properties(params_string: str) -> dict:
#     return dict()
