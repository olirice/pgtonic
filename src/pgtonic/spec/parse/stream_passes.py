from flupy import flu
from typing import List
from pgtonic.spec.lex.types import Part, Token


def filter_whitespace(stream: List[Part]) -> List[Part]:
    """Remove whitespace tokens"""
    return flu(stream).filter(lambda x: x.token != Token.WHITESPACE).collect()
