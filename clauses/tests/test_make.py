# from typing import Generator
# from contextlib import contextmanager
#
# import pytest
#
# from clauses.make import parse_make_statement
#
# @contextmanager
# def does_not_raise():
#     yield
#
#
# class TestMake:
#
#     @pytest.mark.parametrize(
#         "input_string, expected_result, exception",
#         [
#             ("MAKE (node:NodeLabel)", (1, 2, 3), does_not_raise())
#         ]
#     )
#     def test_parse_make_statement(self, input_string:
#     str, expected_result:, exception: Generator):
#         with exception:
#
#             test = parse_make_statement(input_string)
#
#             assert t
