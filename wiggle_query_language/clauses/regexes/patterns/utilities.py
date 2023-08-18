from re import IGNORECASE, compile

from wiggle_query_language.clauses.regexes import ILLEGAL_CHARS

# #%&*
ILLEGAL_CHARS_REGEX = compile(pattern=rf"[{ILLEGAL_CHARS}]", flags=IGNORECASE)
