from typing import Optional

from models.wigish import DbmsFilePath
from models.wql import ParsedFind, ParsedCriteria
from wiggle_query_language.clauses.find.transform.find_pre import (
    process_parsed_find,
)


def find(
    parsed_find: ParsedFind,
    dbms_file_path: DbmsFilePath,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> bool:
    foo = process_parsed_find(parsed_find=parsed_find, parsed_criteria=parsed_criteria)
    print(foo)

    return True
