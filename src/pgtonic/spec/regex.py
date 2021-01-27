############
# Concepts #
############


# public, perms, api_sch
_UNQUOTED_NAME = "([A-z_][A-z0-9]*)"

# "api_V2", "sOmEaC"
_QUOTED_NAME = '("[^"]+?")'

###################
# Externally Used #
###################

SCHEMA_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"
ENTITY_NAME = f"({_UNQUOTED_NAME}|{_QUOTED_NAME})"

NAME = f"({SCHEMA_NAME}\.{ENTITY_NAME}|{ENTITY_NAME})"

OPTIONAL_WHITESPACE = "(\s*)"

SEMICOLON = ";"
OPTIONAL_SEMICOLON = f"{SEMICOLON}?"

START_OF_LINE = "$"
END_OF_LINE = "$"
