from models.wql import ParsedMake, Node, Relationship
from models.wigshell import DbmsFilePath


def make_node() -> Node:
    pass


def make_relationship() -> Relationship:
    pass


def make(parsed_make: list[ParsedMake], dbms_file_path: DbmsFilePath):
    for make_foo in parsed_make:
        print(make_foo.raw_statement)
