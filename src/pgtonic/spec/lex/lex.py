from typing import List

from pgtonic.exceptions import LexFailureException
from pgtonic.spec.lex.types import Part, Token
from pgtonic.spec.lex.utils import build_consumer

TOKEN_MAP = {
    Token.REPEATING: build_consumer(["[, ...]"]),
    Token.WHITESPACE: build_consumer([" ", "\n", "\t"]),
    Token.LITERAL: build_consumer(list(" ABCDEFGHIJKLMNOPQRSTUVWZYZ")),
    Token.ARG: build_consumer(list("_abcdefghijklmnopqrstuvwxyz")),
    Token.L_PAREN: build_consumer(["("]),
    Token.R_PAREN: build_consumer([")"]),
    Token.L_BRACKET: build_consumer(["["]),
    Token.R_BRACKET: build_consumer(["]"]),
    Token.L_BRACE: build_consumer(["{"]),
    Token.R_BRACE: build_consumer(["}"]),
    Token.PIPE: build_consumer(["|"]),
}


def lex(text: str) -> Part:
    """Parse input text according to the mapping of token to callable"""
    token_stream: List[Part] = []
    remaining_text = text

    while remaining_text != "":
        for token, consumer in TOKEN_MAP.items():
            parsed, remaining = consumer(remaining_text)
            if parsed != "":
                remaining_text = remaining
                instance = Part(token, parsed.strip())
                token_stream.append(instance)
                break
        else:
            raise LexFailureException("Could not match {}".format(remaining_text))

    return token_stream
