import re
from typing import List

import pytest

from pgtonic.pg13.grant import TEMPLATES
from pgtonic.spec.parse.parse import parse

REGEXES: List[str] = [parse(x).to_regex() for x in TEMPLATES]


@pytest.mark.parametrize(
    "sql,is_match",
    [
        ("GRANT UPDATE ON TABLE public.account TO oliver;", True),
        ("GRANT UPDATE ON public.account TO oliver WITH GRANT OPTION", True),
        ("GRANT UPDATE ON TABLE public.account TO oliver WITH", False),
        ("GRANT UPDATE (full_name) ON account TO GROUP oliver_u", True),
    ],
)
def test_pg13_grant(sql: str, is_match: bool) -> None:

    assert any([re.match(regex, sql) for regex in REGEXES]) == is_match
