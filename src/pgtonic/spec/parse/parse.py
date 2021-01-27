from typing import Iterable, List, Union

from flupy import flu

from pgtonic.spec.lex.lex import lex
from pgtonic.spec.lex.types import Part, Token
from pgtonic.spec.parse.stream_passes import filter_whitespace
from pgtonic.spec.parse.types import (
    Argument,
    Base,
    Choice,
    Group,
    InParens,
    Literal,
    Maybe,
    Pipe,
    Repeat,
    Spec,
)


def parse(text: str) -> Spec:
    """Parse a statement into an Statement AST"""
    stream = lex(text)
    stream = filter_whitespace(stream)
    return Spec(_parse(stream))  # type: ignore


def _parse(stream: Iterable[Part]) -> Union[List, Base]:  # type: ignore
    out: List = []  # type: ignore

    stream_once = flu(stream)

    for p in stream_once:

        if p.token == Token.R_BRACKET:
            if len(out) > 1:
                return Maybe(Group(out))
            return Maybe(out[0])

        elif p.token == Token.R_PAREN:
            return InParens(out)

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
