from typing import Optional

from models.wigish import GDBMSFilePath
from models.wql import ParsedCriteria, ParsedFind
from wiggle_query_language.clauses.find.transform.find_pre import process_parsed_find
from wiggle_query_language.clauses.find.short_circuits.find_short_circuits import (
    find_short_circuit,
)


def find(
    parsed_find: ParsedFind,
    gdbms_file_path: GDBMSFilePath,
    parsed_criteria: Optional[ParsedCriteria] = None,
) -> bool:
    who_what_where = process_parsed_find(
        parsed_find=parsed_find, parsed_criteria=parsed_criteria
    )

    # Short Circuits!
    if not find_short_circuit(who_what_where, gdbms_file_path):
        raise Exception("No results")

    print(who_what_where)

    return True
