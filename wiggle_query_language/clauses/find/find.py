from typing import Optional

from models.wigish import GDBMSFilePath
from models.wql import ParsedCriteria, ParsedFind
from wiggle_query_language.clauses.find.transform.find_pre import process_parsed_find


def find(
    parsed_find: ParsedFind,
    dbms_file_path: GDBMSFilePath,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> bool:
    who_what_where = process_parsed_find(
        parsed_find=parsed_find, parsed_criteria=parsed_criteria
    )

    # Short Circuits!

    print(who_what_where)

    return True
