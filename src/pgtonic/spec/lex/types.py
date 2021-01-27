from dataclasses import dataclass
from enum import Enum


class Token(str, Enum):
    LITERAL = "LITERAL"
    ARG = "ARG"
    WHITESPACE = "WHITESPACE"
    # The clause is repeatable, but most appear at least once
    REPEATING_REQUIRED = "REPEATING_REQUIRED"
    # The clause is repeatable, but not required
    REPEATING_OPTIONAL = "REPEATING_OPTIONAL"
    L_PAREN = "L_PAREN"
    R_PAREN = "R_PAREN"
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    L_BRACE = "L_BRACE"
    R_BRACE = "R_BRACE"
    PIPE = "PIPE"
    STAR = "STAR"

    def __str__(self) -> str:
        return str.__str__(self)

    def __repr__(self) -> str:
        return str.__str__(self)


@dataclass
class Part:
    token: Token
    text: str
