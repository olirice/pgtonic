import pytest

from pgtonic.exceptions import LexFailureException
from pgtonic.pg13.grant import TEMPLATES
from pgtonic.spec.lex.lex import lex
from pgtonic.spec.lex.types import Token


@pytest.mark.parametrize("template", TEMPLATES)
def test_lex_grant(template) -> None:
    assert lex(template)


def test_lex_fails() -> None:
    with pytest.raises(LexFailureException):
        assert lex("grant usage on 123")


def test_token___str__() -> None:
    assert str(Token.LITERAL) == "LITERAL"


def test_token___repr__() -> None:
    assert repr(Token.LITERAL) == "LITERAL"
