import re
from typing import List

import pytest

from pgtonic.pg13.create_trigger import TEMPLATES

REGEXES: List[str] = [x.to_regex() for x in TEMPLATES]

@pytest.mark.skip(reason="incomplete")
@pytest.mark.parametrize(
    "sql,is_match",
    [
        ("CREATE TRIGGER my_trig AFTER UPDATE ON api.account EXECUTE api.myfunc()", True),
    ],
)
def test_pg13_grant(sql: str, is_match: bool) -> None:
    assert any([re.match("^" + regex + "$", sql) for regex in REGEXES]) == is_match
