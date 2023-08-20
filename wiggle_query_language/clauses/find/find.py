from typing import Optional

from models.wigish import DbmsFilePath
from models.wql import ParsedFind, ParsedCriteria
from wiggle_query_language.clauses.find.transform.find_pre import (
    process_parsed_find_list,
)


def find(
    parsed_find_list: list[ParsedFind],
    dbms_file_path: DbmsFilePath,
    parsed_criteria_list: Optional[list[ParsedCriteria]] = None,
) -> bool:
    foo = process_parsed_find_list(
        parsed_find_list=parsed_find_list, parsed_criteria_list=parsed_criteria_list
    )
    print(foo)
