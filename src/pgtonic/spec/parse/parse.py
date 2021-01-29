from functools import lru_cache
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
    Name,
    Pipe,
    QualifiedName,
    RepeatComma,
    RepeatNone,
    RepeatOr,
    UnqualifiedName,
)


@lru_cache()
def parse(sql: str) -> Base:
    tstream0 = lex(sql)
    tstream1 = filter_whitespace(tstream0)
    nodes = _parse(tstream1)  # type: ignore

    if isinstance(nodes, list):
        return Group(nodes)
    return nodes


def handle_pipes(x):
    grouped = (
        flu(x)
        .group_by(lambda x: isinstance(x, Pipe), sort=False)
        .filter(lambda x: not x[0])
        .map(lambda x: x[1].collect())
        .map(lambda x: Group(x) if len(x) > 1 else x[0])
        .collect()
    )
    if len(grouped) == 1:
        return grouped[0]
    return Choice(grouped)


def _parse(stream: Iterable[Part]) -> Union[List, Base]:  # type: ignore
    out: List = []  # type: ignore

    stream_once = flu(stream)

    for p in stream_once:

        if p.token == Token.R_BRACKET:
            if len(out) > 1:
                maybe_choice = handle_pipes(out)
                if isinstance(maybe_choice, Choice):
                    return Maybe(maybe_choice)
                return Maybe(Group(out))
            return Maybe(out[0])

        elif p.token == Token.R_PAREN:
            return InParens(out)

        elif p.token == Token.R_BRACE:
            # Braces always contain pipes
            return handle_pipes(out)

        elif p.token in (Token.L_BRACE, Token.L_BRACKET, Token.L_PAREN):
            out.append(_parse(stream_once))

        elif p.token == Token.ARG:
            out.append(Argument(p.text))

        elif p.token == Token.DELIMITED_COMMA:
            out[-1] = RepeatComma(out[-1])

        elif p.token == Token.DELIMITED_OR:
            out[-1] = RepeatOr(out[-1])

        elif p.token == Token.DELIMITED_NONE:
            out[-1] = RepeatNone(out[-1])

        elif p.token in (Token.LITERAL, Token.STAR):
            out.append(Literal(p.text))

        elif p.token == Token.PIPE:
            out.append(Pipe(p.text))

        elif p.token == Token.NAME:
            out.append(Name(p.text))

        elif p.token == Token.QUALIFIED_NAME:
            out.append(QualifiedName(p.text))

        elif p.token == Token.UNQUALIFIED_NAME:
            out.append(UnqualifiedName(p.text))

        else:
            assert "Unhandled Token: {}".format(p.token)

    return out
