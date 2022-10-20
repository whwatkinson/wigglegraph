# import re
#
# from re import search
#
# pattern = r"""(?P<clause>[MmAa
# KkEe]{4})\s?\((?P<handle>\w+)\s?:(?P<node_label>\w+)\)"""
#
# string = "MAKE (node:NodeLabel)"
#
#
# def make(input_string: str):
#     pass
#
#
# def parse_make_statement(input_string: str):
#
#     if match := re.search(pattern, input_string):
#         clause = match.group("clause")
#         if clause.upper() != "MAKE":
#             raise Exception
#
#         handle = match.group("handle")
#         node_label = match.group("node_label")
#
#         return clause, handle, node_label
#
#     raise Exception
