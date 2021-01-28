from dataclasses import dataclass
from enum import Enum


class Token(str, Enum):
    LITERAL = "LITERAL"
    ARG = "ARG"
    WHITESPACE = "WHITESPACE"
    DELIMITED_OR = "DELIMITED_OR"
    DELIMITED_COMMA = "DELIMITED_COMMA"
    DELIMITED_NONE = "DELIMITED_NONE"
    L_PAREN = "L_PAREN"
    R_PAREN = "R_PAREN"
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    L_BRACE = "L_BRACE"
    R_BRACE = "R_BRACE"
    PIPE = "PIPE"
    STAR = "STAR"
    COMMA = "COMMA"
    # mytable
    UNQUALIFIED_NAME = "UNQUALIFIED_NAME"
    # public.mytable
    QUALIFIED_NAME = "QUALIFIED_NAME"
    # qualified or unqualified
    NAME = "NAME"

    def __str__(self) -> str:
        return str.__str__(self)

    def __repr__(self) -> str:
        return str.__str__(self)


@dataclass
class Part:
    token: Token
    text: str
