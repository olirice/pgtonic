import re

import pytest

from pgtonic.spec.regex import ENTITY_NAME, NAME, SCHEMA_NAME


@pytest.mark.parametrize(
    "schema_name,is_match",
    [
        ("public", True),
        ("oli_ver", True),
        ("_dkjle_adb", True),
        ("dkj8le_adb", True),
        ("aaAa", True),
        ("A_aaAa", True),
        ('"A_aaAa"', True),
        ('"A_$aaAa"', True),
        ('"%ab_$^&c"', True),
        ("8aaa", False),
        ("aa a", False),
        ("aa$a", False),
        ('"a"a"', False),
    ],
)
def test_schema_name(schema_name: str, is_match: bool) -> None:
    assert (re.match("^" + SCHEMA_NAME + "$", schema_name) is not None) == is_match


@pytest.mark.parametrize(
    "entity_name,is_match",
    [
        ("public", True),
        ("oli_ver", True),
        ("_dkjle_adb", True),
        ("dkj8le_adb", True),
        ("aaAa", True),
        ("A_aaAa", True),
        ('"A_aaAa"', True),
        ('"A_$aaAa"', True),
        ('"%ab_$^&c"', True),
        ("8aaa", False),
        ("aa a", False),
        ("aa$a", False),
        ('"a"a"', False),
    ],
)
def test_entity_name(entity_name: str, is_match: bool) -> None:
    assert (re.match("^" + ENTITY_NAME + "$", entity_name) is not None) == is_match


@pytest.mark.parametrize(
    "name,is_match",
    [
        # Name does not have to be schema qualified
        ("public", True),
        ("oli_ver", True),
        ("_dkjle_adb", True),
        ("dkj8le_adb", True),
        ("aaAa", True),
        ("A_aaAa", True),
        ('"A_aaAa"', True),
        ('"A_$aaAa"', True),
        ('"%ab_$^&c"', True),
        ("8aaa", False),
        ("aa a", False),
        ("aa$a", False),
        ('"a"a"', False),
        ('a"a', False),
        # Name may be schema qualified
        ("public.account", True),
        ("public.ac_ount", True),
        ("api_v3._abcded1", True),
        ('"api$_v3"."_abc8dAed1"', True),
        ('"ap"3"."_abc8dAed1"', False),
        ('ap"3._abc8dAed1', False),
    ],
)
def test_name(name: str, is_match: bool) -> None:
    assert (re.match("^" + NAME + "$", name) is not None) == is_match
