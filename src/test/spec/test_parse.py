import pytest

from pgtonic.pg13.grant import TEMPLATES


@pytest.mark.parametrize("template", TEMPLATES)
def test_parse_grant(template) -> None:
    assert template.ast
