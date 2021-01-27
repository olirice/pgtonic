import re
from typing import List

import pytest

from pgtonic.pg13.grant import TEMPLATES
from pgtonic.spec.parse.parse import parse

REGEXES: List[str] = [parse(x.spec).to_regex() for x in TEMPLATES]


@pytest.mark.parametrize(
    "sql,is_match",
    [
        ("GRANT UPDATE ON TABLE public.account TO oliver;", True),
        ("GRANT UPDATE ON public.account TO oliver WITH GRANT OPTION", True),
        ("GRANT UPDATE ON TABLE public.account TO oliver WITH", False),
        ("GRANT UPDATE (full_name) ON account TO GROUP oliver_u", True),
        ("GRANT ALL PRIVILEGES ON SEQUENCE xyz.account_seq TO PUBLIC, GROUP anon_user", True),
        ("GRANT TEMP,CONNECT, CREATE ON DATABASE tonicdb TO oli WITH GRANT OPTION", True),
        ("GRANT ALL ON FOREIGN DATA WRAPPER my_fdw TO PUBLIC;", True),
        ('GRANT USAGE ON FOREIGN SERVER my_server, my_other_server TO "ec$ho_rw";', True),
        ("GRANT EXECUTE ON FUNCTION api_v2.to_upper () TO oliver", True),
        ("GRANT EXECUTE ON FUNCTION api_v2.to_upper ( text ) TO oliver", True),
    ],
)
def test_pg13_grant(sql: str, is_match: bool) -> None:
    assert any([re.match("^" + regex + "$", sql) for regex in REGEXES]) == is_match
