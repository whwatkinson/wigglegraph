from re import compile


s = compile(
    r"""(?P<clause>[MmAaKkEe]{4})\s?\(
(?P<handle>\w+)\s?:(?P<node_label>\w+)\)"""
)

"""
MAKE (node:NodeLable)

"""


def make():
    pass
