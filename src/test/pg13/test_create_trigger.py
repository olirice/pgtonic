import pytest

from pgtonic.pg13.create_trigger import TEMPLATES


@pytest.mark.parametrize(
    "sql,is_match",
    [
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func ()", True),
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func ( param1 )", True),
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func( param1 )", True),
        ("CREATE CONSTRAINT TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func( param1)", True),
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func(param1 )", True),
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func(param1,param2 )", True),
        ("CREATE TRIGGER my_trig AFTER INSERT ON api.account EXECUTE FUNCTION oli.func(param1, param2 )", True),
        (
            "CREATE TRIGGER my_trig BEFORE INSERT OR DELETE OR UPDATE ON public.book EXECUTE PROCEDURE somefunc( param1 )",
            True,
        ),
    ],
)
def test_pg13_grant(sql: str, is_match: bool) -> None:
    assert any([x.is_match(sql) for x in TEMPLATES]) == is_match
