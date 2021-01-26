import pytest
from pgtonic.pg13.grant import TEMPLATES
from pgtonic.spec.parse.parse import parse

@pytest.mark.parametrize("template", TEMPLATES)
def test_parse_grant(template) -> None:
    assert parse(template)


