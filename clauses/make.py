# import re
#
# from re import search
#
# from enums.statement import Statement
#
#
# pattern = r"""(?P<clause>[MmAaKkEe]{4})\s?\((?P<handle>\w+)\s?:(?P<node_label>\w+)\)"""
#
#
# string = "MAKE (node:NodeLabel)"
#
#
# def make(input_string: str):
#
#     if match := re.search(pattern, string):
#
#         clause = match.group("clause")
#
#         try:
#             clause = Statement[match.group("clause").upper()]
#
#         except KeyError:
#             raise
#
#         handle = match.group("handle")
#         node_label = match.group("node_label")
#
#     raise Exception
