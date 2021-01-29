import pytest

from pgtonic.pg13.grant import TEMPLATES


@pytest.mark.parametrize(
    "sql,is_match",
    [
        ("GRANT UPDATE ON TABLE public.account TO oliver", True),
        ("GRANT UPDATE ON TABLE public.account TO GROUP oliver", True),
        ("GRANT UPDATE ON TABLE public.account TO CURRENT_USER", True),
        ("GRANT UPDATE ON TABLE public.account TO oliver", True),
        ("GRANT SELECT ON TABLE public.account, book TO oliver", True),
        ("GRANT SELECT ON TABLE public.account, book, author TO oliver, anon", True),
        ("GRANT SELECT ON ALL TABLES IN SCHEMA api, public TO oliver, anon", True),
        ("GRANT SELECT ON ALL TABLES IN SCHEMA api TO oliver, anon WITH GRANT OPTION", True),
        ("GRANT ALL ON ALL TABLES IN SCHEMA api, other TO oliver, anon", True),
        ("GRANT REFERENCES ON public.account TO oliver WITH GRANT OPTION", True),
        ("GRANT TRIGGER ON public.account TO oliver, anon WITH GRANT OPTION", True),
        ("GRANT UPDATE ON TABLE public.account TO oliver WITH", False),
        ("GRANT UPDATE ON TABLE account TABLE other TO oliver WITH", False),
        ("GRANT UPDATE ON TABLE TO oliver WITH", False),
        ("GRANT UPDATE ON TABLE account TO", False),
        ("GRANT UPDATE ON TABLE account TO ", False),
        ("GRANT UPDATEON TABLE account TO oliver", False),
        ("GRANT UPDATE ON accountTO oliver", False),
        ("GRANT UPDATE ALL ON account TO oliver", False),
        ("GRANT UPDATE ALL ON account TO oliver", False),
    ],
)
def test_pg13_grant(sql: str, is_match: bool) -> None:
    assert any([x.is_match(sql) for x in TEMPLATES]) == is_match
