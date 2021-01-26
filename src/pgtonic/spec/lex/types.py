from typing import Tuple, List, Dict, Callable
from enum import Enum
from dataclasses import dataclass


class Token(str, Enum):
    LITERAL = 'LITERAL'
    ARG = 'ARG'
    WHITESPACE = 'WHITESPACE'
    REPEATING = 'REPEATING'
    L_PAREN = 'L_PAREN'
    R_PAREN = 'R_PAREN'
    L_BRACKET = "L_BRACKET"
    R_BRACKET = "R_BRACKET"
    L_BRACE = "L_BRACE"
    R_BRACE = "R_BRACE"
    PIPE = "PIPE"

    def __str__(self):
        return str.__str__(self)
    
    def __repr__(self):
        return str.__str__(self)   


@dataclass
class Part:
    token: Token
    text: str




