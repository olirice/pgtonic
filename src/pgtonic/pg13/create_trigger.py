from pgtonic.spec.template import Template

COLUMN_NAME_SPEC = Template("{ UNQUALIFIED_NAME }")

TEMPLATES = [
    Template(
        original="""
CREATE [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE { FUNCTION | PROCEDURE } function_name ( arguments )
    """,
        where={
            "name": Template("{ UNQUALIFIED_NAME }"),
            "event": Template(
                "{ INSERT | UPDATE [ OF column_name [, ...] ] | DELETE | TRUNCATE }",
                where={"column_name": COLUMN_NAME_SPEC},
            ),
            "table_name": Template("{ NAME }"),
            "referenced_table_name": Template("{ NAME }"),
            # TODO
            "transition_relation_name": Template("{ NAME }"),
            # TODO
            "condition": Template("{ NAME }"),
            # TODO
            "function_name": Template("{ NAME }"),
            # TODO
            # An optional comma-separated list of arguments to be provided to the function when the trigger is executed. The arguments are literal string constants. Simple names and numeric constants can be written here, too, but they will all be converted to strings. Please check the description of the implementation language of the trigger function to find out how these arguments can be accessed within the function; it might be different from normal function arguments.
            "arguments": Template("{ UNQUALIFIED_NAME [, ...] }"),
        },
    )
]
