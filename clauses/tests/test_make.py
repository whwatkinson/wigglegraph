from contextlib import contextmanager

import pytest


@contextmanager
def does_not_raise():
    yield


class TestMake:
    @pytest.mark.parametrize(
        "test_statement, expected_result, exception",
        [
            ("MAKE (node:NodeLabel)", None, does_not_raise()),
            ("MAKE (:NodeLabel)", None, does_not_raise()),
            ("MAKE (:NodeLabel{name:'Name'})", None, does_not_raise()),
            (
                "MAKE (:NodeLabel{uuid: '7e48f6ae-b25a-4634-91af-b1fb67b90ad9'})",
                None,
                does_not_raise(),
            ),
            # ("MAKE (:NodeLabel)", None, does_not_raise()),
            # ("MAKE (:NodeLabel)", None, does_not_raise()),
        ],
    )
    def test_make(self, test_statement: str, expected_result, exception):

        with exception:
            pass
