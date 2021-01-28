from pgtonic.spec.template import Template

ROLE_SPEC = Template("{ [ GROUP ] UNQUALIFIED_NAME | PUBLIC | CURRENT_USER | SESSION_USER }")

TEMPLATES = [
    Template(
        """
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
[, ...] | ALL [ PRIVILEGES ] }
ON { [ TABLE ] table_name [, ...]
     | ALL TABLES IN SCHEMA schema_name [, ...] }
TO role_specification [, ...] [ WITH GRANT OPTION ]
    """,
        where={
            "table_name": Template("{ NAME }"),
            "schema_name": Template("{ UNQUALIFIED_NAME }"),
            "role_specification": ROLE_SPEC,
        },
    ),
]
