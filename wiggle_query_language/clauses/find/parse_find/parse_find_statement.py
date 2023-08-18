# from typing import Optional
#
# from models.wql import ParsedFind
# from wiggle_query_language.clauses.parsing_helpers.parse_statement_checks import (
#     validate_statement,
#     check_make_clause_spelling,
# )
#
#
# def build_parsed_find(statement: str) -> ParsedFind:
#     """
#     Handles building of the ParsedFind.
#     :param statement: The raw find statement.
#     :return: A ParsedMake Object.
#     """
#     parsed_pattern_dict = [
#         x.groupdict() for x in NODES_RELS_PATTERN_REGEX.finditer(statement) if x.group()
#     ]
#
#     parsed_make = ParsedFind(
#         raw_statement=statement, parsed_pattern_list=parsed_pattern_dict
#     )
#
#     return parsed_make
#
#
# def extract_all_find_statements(query_string: str) -> Optional[list[str]]:
#     """
#     Extracts the FIND statement from the query body.
#     :param query_string: The raw query.
#     :return: A list of FIND statements.
#     """
#
#     if make_matches := [
#         x.group() for x in MAKE_STATEMENT_ALL_REGEX.finditer(query_string)
#     ]:
#         return make_matches
#
#     check_make_clause_spelling(query_string)
#
#     return None
#
#
# def parse_find_statement_from_query_string(
#     query_string: str,
# ) -> Optional[list[ParsedFind]]:
#     """
#     Extracts the FIND statement from the query body.
#     :param query_string: The raw query.
#     :return: A list of FIND statements.
#     """
#     make_matches = extract_all_find_statements(query_string)
#     if not make_matches:
#         return None
#     if not validate_statement(make_matches):
#         raise Exception("make_matches says no")
#
#     if make_matches:
#         return [build_parsed_find(statement=stmt) for stmt in make_matches]
#     else:
#         return None
