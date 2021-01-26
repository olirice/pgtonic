from typing import List

from flupy import flu

from pgtonic.spec.lex.lex import lex
from pgtonic.spec.lex.types import Part, Token
from pgtonic.spec.parse.stream_passes import filter_whitespace
from pgtonic.spec.parse.types import (
    Argument,
    Choice,
    Group,
    InParens,
    Literal,
    Maybe,
    Pipe,
    Repeat,
    Statement,
)


def parse(text: str):
    """Parse a statement into an Statement AST"""
    stream = lex(text)
    stream = filter_whitespace(stream)
    return Statement(_parse(stream))


def _parse(stream: List[Part]):
    out = []

    stream_once = flu(stream)

    for p in stream_once:

        if p.token == Token.R_BRACKET:
            if len(out) > 1:
                return Maybe(out)
            return Maybe(out[0])

        elif p.token == Token.R_PAREN:
            if len(out) > 1:
                return InParens(out)
            return InParens(out[0])

        elif p.token == Token.R_BRACE:
            # Handle pipes
            g = (
                flu(out)
                .group_by(lambda x: isinstance(x, Pipe), sort=False)
                .filter(lambda x: not x[0])
                .map(lambda x: x[1].collect())
                .map(lambda x: Group(x) if len(x) > 1 else x[0])
                .collect()
            )
            return Choice(g)

        elif p.token in (Token.L_BRACE, Token.L_BRACKET, Token.L_PAREN):
            out.append(_parse(stream_once))

        elif p.token == Token.ARG:
            out.append(Argument(p.text))

        elif p.token == Token.REPEATING:
            out[-1] = Repeat(out[-1])

        elif p.token == Token.LITERAL:
            out.append(Literal(p.text))

        elif p.token == Token.PIPE:
            out.append(Pipe(p.text))

    return out
