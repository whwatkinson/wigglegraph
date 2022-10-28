# from typing import Generator
# from uuid import uuid4
#
# import pytest
#
#
# from clauses.make.make import make_node
# from clauses.make.make_helpers import parse_make_statment
# from database.database import add_item_to_database, load_database
# from exceptions.statements.statements import MissingNodeLabel, StatementError
# from testing import TEST_DATABASE_FILE_PATH, TEST_WIGGLE_NUMBER_STATE_FILE_PATH
#
#
# @pytest.mark.xfail
# class TestQueries:
#     """
#     Marked xfail as not implemented yet.
#     The prurpose of this test file is to create a
#     few sample queries and to see how the development
#     process differes from my origional thoughts...
#     """
#
#     @pytest.fixture
#     def seed_database(self):
#         qry = """
#             MAKE (n:Person{first_name:'Harry' | last_name:"Watkinson | favourite_number: 6 | favourite_color: 'green' | uuid: '2beb78d1-d4f4-48b8-a875-1014bee3daa2'})
#         """
#
#         #  todo this should just call make
#         parsed_statement = parse_make_statment(test_statement)
#         node = make_node(parsed_statement, TEST_WIGGLE_NUMBER_STATE_FILE_PATH)
#         add_item_to_database(TEST_DATABASE_FILE_PATH, node.export_node())
#
#     def test_qry_1(
#         self, clear_database: Generator, clear_wiggle_number_state_file: Generator
#     ) -> None:
#
#         qry = """
#             FIND (node:Person{first_name:'Harry})
#             RETURN node
#         """
#
#         qry_2 = """
#             FIND (node:Person)
#             WHERE node.first_name = 'Harry'
#             RETRUN node
#         """
