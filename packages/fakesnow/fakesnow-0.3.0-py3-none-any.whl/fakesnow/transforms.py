from __future__ import annotations

from typing import cast

import sqlglot
from sqlglot import exp

MISSING_DATABASE = "missing_database"
SUCCESS_NOP = sqlglot.parse_one("SELECT 'Statement executed successfully.'")


def as_describe(expression: exp.Expression) -> exp.Expression:
    """Prepend describe to the expression.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT name FROM CUSTOMERS").transform(as_describe).sql()
        'describe SELECT name FROM CUSTOMERS'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    return exp.Describe(this=expression)


# TODO: move this into a Dialect as a transpilation
def create_database(expression: exp.Expression) -> exp.Expression:
    """Transform create database to attach database.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("CREATE database foo").transform(create_database).sql()
        'ATTACH DATABASE ':memory:' as foo'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression, with the database name stored in the create_db_name arg.
    """

    if isinstance(expression, exp.Create) and str(expression.args.get("kind")).upper() == "DATABASE":
        assert (ident := expression.find(exp.Identifier)), f"No identifier in {expression.sql}"
        db_name = ident.this
        return exp.Command(
            this="ATTACH",
            expression=exp.Literal(this=f"DATABASE ':memory:' AS {db_name}", is_string=True),
            create_db_name=db_name,
        )

    return expression


def drop_schema_cascade(expression: exp.Expression) -> exp.Expression:
    """Drop schema cascade.

    By default duckdb won't delete a schema if it contains tables, whereas snowflake will.
    So we add the cascade keyword to mimic snowflake's behaviour.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("DROP SCHEMA schema1").transform(remove_comment).sql()
        'DROP SCHEMA schema1 cascade'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if (
        not isinstance(expression, exp.Drop)
        or not (kind := expression.args.get("kind"))
        or not isinstance(kind, str)
        or kind.upper() != "SCHEMA"
    ):
        return expression

    new = expression.copy()
    new.args["cascade"] = True
    return new


def extract_comment(expression: exp.Expression) -> exp.Expression:
    """Extract table comment, removing it from the Expression.

    duckdb doesn't support comments. So we remove them from the expression and store them in the table_comment arg.
    We also replace the transform the expression to NOP if the statement can't be executed by duckdb.

    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression, with any comment stored in the new 'table_comment' arg.
    """

    if isinstance(expression, exp.Create) and (table := expression.find(exp.Table)):
        comment = None
        if props := cast(exp.Properties, expression.args.get("properties")):
            other_props = []
            for p in props.expressions:
                if isinstance(p, exp.SchemaCommentProperty) and (isinstance(p.this, (exp.Literal, exp.Identifier))):
                    comment = p.this.this
                else:
                    other_props.append(p)

            new = expression.copy()
            new_props: exp.Properties = new.args["properties"]
            new_props.set("expressions", other_props)
            new.args["table_comment"] = (table, comment)
            return new
    elif (
        isinstance(expression, exp.Comment)
        and (cexp := expression.args.get("expression"))
        and isinstance(cexp, exp.Literal)
        and (table := expression.find(exp.Table))
    ):
        new = SUCCESS_NOP.copy()
        new.args["table_comment"] = (table, cexp.this)
        return new
    elif (
        isinstance(expression, exp.AlterTable)
        and (sexp := expression.find(exp.Set))
        and not sexp.args["tag"]
        and (eq := sexp.find(exp.EQ))
        and (id := eq.find(exp.Identifier))
        and isinstance(id.this, str)
        and id.this.upper() == "COMMENT"
        and (lit := eq.find(exp.Literal))
        and (table := expression.find(exp.Table))
    ):
        new = SUCCESS_NOP.copy()
        new.args["table_comment"] = (table, lit.this)
        return new

    return expression


def extract_text_length(expression: exp.Expression) -> exp.Expression:
    """Extract length of text columns.

    duckdb doesn't have fixed-sized text types. So we capture the size of text types and store that in the
    character_maximum_length arg.

    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The original expression, with any comment stored in the new 'table_comment' arg.
    """

    if isinstance(expression, (exp.Create, exp.AlterTable)):
        text_lengths = []
        for dt in expression.find_all(exp.DataType):
            if dt.this in (exp.DataType.Type.VARCHAR, exp.DataType.Type.TEXT):
                col_name = dt.parent and dt.parent.this and dt.parent.this.this
                if dt_size := dt.find(exp.DataTypeSize):
                    size = (
                        isinstance(dt_size.this, exp.Literal)
                        and isinstance(dt_size.this.this, str)
                        and int(dt_size.this.this)
                    )
                else:
                    size = 16777216
                text_lengths.append((col_name, size))

        if text_lengths:
            expression.args["text_lengths"] = text_lengths

    return expression


def float_to_double(expression: exp.Expression) -> exp.Expression:
    """Convert float to double for 64 bit precision.

    Snowflake floats are all 64 bit (ie: double)
    see https://docs.snowflake.com/en/sql-reference/data-types-numeric#float-float4-float8
    """

    if isinstance(expression, exp.DataType) and expression.this == exp.DataType.Type.FLOAT:
        # TODO don't copy!
        new = expression.copy()
        new.args["this"] = exp.DataType.Type.DOUBLE
        return new

    return expression


def indices_to_array(expression: exp.Expression) -> exp.Expression:
    """Convert to 1-based list indices.

    Snowflake uses 0-based array indexing, whereas duckdb using 1-based list indexing.

    See https://docs.snowflake.com/en/sql-reference/data-types-semistructured#accessing-elements-of-an-array-by-index-or-by-slice

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT myarray[0] FROM table1").transform(indices_to_array).sql()
        'SELECT myarray[1] FROM table1'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """
    if (
        isinstance(expression, exp.Bracket)
        and len(expression.expressions) == 1
        and (index := expression.expressions[0])
        and isinstance(index, exp.Literal)
        and index.this
        and not index.is_string
    ):
        new = expression.copy()
        new.expressions[0] = exp.Literal(this=str(int(index.this) + 1), is_string=False)
        return new
    return expression


def indices_to_object(expression: exp.Expression) -> exp.Expression:
    """Convert object indices to JSON extraction.

    Supports Snowflake object indices, see
    https://docs.snowflake.com/en/sql-reference/data-types-semistructured#accessing-elements-of-an-object-by-key

    Duckdb uses the -> operator, or the json_extract function, see
    https://duckdb.org/docs/extensions/json#json-extraction-functions

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("select name['k'] from semi").transform(indices_to_object).sql()
        'SELECT name -> '$.k' FROM semi'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """
    if (
        isinstance(expression, exp.Bracket)
        and len(expression.expressions) == 1
        and (index := expression.expressions[0])
        and isinstance(index, exp.Literal)
        and index.this
        and index.is_string
        and (ident := expression.find(exp.Identifier))
    ):
        # use sql() to handle quoting
        ident_sql = ident.sql()
        return sqlglot.parse_one(f"{ident_sql} -> '$.{index.this}'", read="duckdb")
    return expression


def information_schema_columns_snowflake(expression: exp.Expression) -> exp.Expression:
    """Redirect to the information_schema.columns_snowflake view which has metadata that matches snowflake.

    Because duckdb doesn't store character_maximum_length or character_octet_length.
    """

    if (
        isinstance(expression, exp.Select)
        and (tbl_exp := expression.find(exp.Table))
        and tbl_exp.name.upper() == "COLUMNS"
        and tbl_exp.db.upper() == "INFORMATION_SCHEMA"
    ):
        tbl_exp.set("this", exp.Identifier(this="COLUMNS_SNOWFLAKE", quoted=False))

    return expression


def information_schema_tables_ext(expression: exp.Expression) -> exp.Expression:
    """Join to information_schema.tables_ext to access additional metadata columns (eg: comment)."""

    if (
        isinstance(expression, exp.Select)
        and (tbl_exp := expression.find(exp.Table))
        and tbl_exp.name.upper() == "TABLES"
        and tbl_exp.db.upper() == "INFORMATION_SCHEMA"
    ):
        return expression.join(
            "information_schema.tables_ext",
            on=(
                """
                tables.table_catalog = tables_ext.ext_table_catalog AND
                tables.table_schema = tables_ext.ext_table_schema AND
                tables.table_name = tables_ext.ext_table_name
                """
            ),
            join_type="left",
        )

    return expression


def integer_precision(expression: exp.Expression) -> exp.Expression:
    """Snowflake integers are 38 digits.

    See https://docs.snowflake.com/en/sql-reference/data-types-numeric
    """

    decimal_38_0 = exp.DataType(
        this=exp.DataType.Type.DECIMAL,
        expressions=[
            exp.DataTypeSize(this=exp.Literal(this="38", is_string=False)),
            exp.DataTypeSize(this=exp.Literal(this="0", is_string=False)),
        ],
        nested=False,
        prefix=False,
    )

    if (
        isinstance(expression, exp.DataType)
        and (expression.this == exp.DataType.Type.DECIMAL and not expression.expressions)
        or expression.this
        in (exp.DataType.Type.BIGINT, exp.DataType.Type.INT, exp.DataType.Type.SMALLINT, exp.DataType.Type.TINYINT)
    ):
        return decimal_38_0

    return expression


def object_construct(expression: exp.Expression) -> exp.Expression:
    """Convert object_construct to return a json string

    Because internally snowflake stores OBJECT types as a json string.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT OBJECT_CONSTRUCT('a',1,'b','BBBB', 'c',null)", read="snowflake").transform(object_construct).sql(dialect="duckdb")
        "SELECT TO_JSON({'a': 1, 'b': 'BBBB', 'c': NULL})"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """  # noqa: E501

    if isinstance(expression, exp.Struct):
        return exp.Anonymous(this="TO_JSON", expressions=[expression])

    return expression


def parse_json(expression: exp.Expression) -> exp.Expression:
    """Convert parse_json() to json().

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("insert into table1 (name) select parse_json('{}')").transform(parse_json).sql()
        "CREATE TABLE table1 (name JSON)"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if (
        isinstance(expression, exp.Anonymous)
        and isinstance(expression.this, str)
        and expression.this.upper() == "PARSE_JSON"
    ):
        new = expression.copy()
        new.args["this"] = "JSON"
        return new

    return expression


def regex(expression: exp.Expression) -> exp.Expression:
    """Transform regex expressions from snowflake to duckdb.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT regexp_replace('abc123', '\\\\D', '')").transform(tag).sql()
        "SELECT regexp_replace('abc123', '\\D', '', 'g')"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if (
        isinstance(expression, exp.Anonymous)
        and isinstance(expression.this, str)
        and "REGEXP_REPLACE" == expression.this.upper()
    ):
        new = expression.copy()
        new_args = new.expressions

        if len(new_args) > 3:
            # see https://docs.snowflake.com/en/sql-reference/functions/regexp_replace
            raise NotImplementedError(
                "REGEXP_REPLACE with additional parameters (eg: <position>, <occurrence>, <parameters>) not supported"
            )

        # snowflake requires escaping backslashes in single-quoted string constants, but duckdb doesn't
        # see https://docs.snowflake.com/en/sql-reference/functions-regexp#label-regexp-escape-character-caveats
        new_args[1].args["this"] = new_args[1].this.replace("\\\\", "\\")

        if len(new_args) == 2:
            # if no replacement string, the snowflake default is ''
            new_args.append(exp.Literal(this="", is_string=True))

        # snowflake regex replacements are global
        new_args.append(exp.Literal(this="g", is_string=True))

        new.set("expressions", new_args)

        return new

    return expression


# TODO: move this into a Dialect as a transpilation
def set_schema(expression: exp.Expression, current_database: str | None) -> exp.Expression:
    """Transform USE SCHEMA/DATABASE to SET schema.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("USE SCHEMA bar").transform(set_schema, current_database="foo").sql()
        "SET schema = 'foo.bar'"
        >>> sqlglot.parse_one("USE SCHEMA foo.bar").transform(set_schema).sql()
        "SET schema = 'foo.bar'"
        >>> sqlglot.parse_one("USE DATABASE marts").transform(set_schema).sql()
        "SET schema = 'marts.main'"

        See tests for more examples.
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: A SET schema expression if the input is a USE
            expression, otherwise expression is returned as-is.
    """

    if (
        isinstance(expression, exp.Use)
        and (kind := expression.args.get("kind"))
        and isinstance(kind, exp.Var)
        and kind.name
        and kind.name.upper() in ["SCHEMA", "DATABASE"]
    ):
        assert expression.this, f"No identifier for USE expression {expression}"

        if kind.name.upper() == "DATABASE":
            # duckdb's default schema is main
            name = f"{expression.this.name}.main"
        else:
            # SCHEMA
            if db := expression.this.args.get("db"):
                db_name = db.name
            else:
                # isn't qualified with a database
                db_name = current_database or MISSING_DATABASE

            name = f"{db_name}.{expression.this.name}"

        return exp.Command(this="SET", expression=exp.Literal.string(f"schema = '{name}'"))

    return expression


def tag(expression: exp.Expression) -> exp.Expression:
    """Handle tags. Transfer tags into upserts of the tag table.

    duckdb doesn't support tags. In lieu of a full implementation, for now we make it a NOP.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("ALTER TABLE table1 SET TAG foo='bar'").transform(tag).sql()
        "SELECT 'Statement executed successfully.'"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if isinstance(expression, exp.AlterTable) and (actions := expression.args.get("actions")):
        for a in actions:
            if isinstance(a, exp.Set) and a.args["tag"]:
                return SUCCESS_NOP
    elif (
        isinstance(expression, exp.Command)
        and (cexp := expression.args.get("expression"))
        and isinstance(cexp, str)
        and "SET TAG" in cexp.upper()
    ):
        # alter table modify column set tag
        return SUCCESS_NOP

    return expression


def to_date(expression: exp.Expression) -> exp.Expression:
    """Convert to_date() to a cast.

    See https://docs.snowflake.com/en/sql-reference/functions/to_date

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT to_date(to_timestamp(0))").transform(to_date).sql()
        "SELECT CAST(DATE_TRUNC('day', TO_TIMESTAMP(0)) AS DATE)"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if (
        isinstance(expression, exp.Anonymous)
        and isinstance(expression.this, str)
        and expression.this.upper() == "TO_DATE"
    ):
        return exp.Cast(
            # add datetrunc to handle timestamp_ns (aka timestamp(9)) columns
            # and avoid https://github.com/duckdb/duckdb/issues/7672
            this=exp.DateTrunc(unit=exp.Literal(this="day", is_string=True), this=expression.expressions[0]),
            to=exp.DataType(this=exp.DataType.Type.DATE, nested=False, prefix=False),
        )
    return expression


def timestamp_ntz_ns(expression: exp.Expression) -> exp.Expression:
    """Convert timestamp_ntz(9) to timestamp_ntz.

    To compensate for https://github.com/duckdb/duckdb/issues/7980
    """

    if (
        isinstance(expression, exp.DataType)
        and expression.this == exp.DataType.Type.TIMESTAMP
        and exp.DataTypeSize(this=exp.Literal(this="9", is_string=False)) in expression.expressions
    ):
        new = expression.copy()
        del new.args["expressions"]
        return new

    return expression


# sqlglot.parse_one("create table example(date TIMESTAMP_NTZ(9));", read="snowflake")
def semi_structured_types(expression: exp.Expression) -> exp.Expression:
    """Convert OBJECT, ARRAY, and VARIANT types to duckdb compatible types.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("CREATE TABLE table1 (name object)").transform(semi_structured_types).sql()
        "CREATE TABLE table1 (name JSON)"
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if isinstance(expression, exp.DataType):
        if expression.this in [exp.DataType.Type.OBJECT, exp.DataType.Type.VARIANT]:
            new = expression.copy()
            new.args["this"] = exp.DataType.Type.JSON
            return new
        elif expression.this == exp.DataType.Type.ARRAY:
            new = expression.copy()
            new.set("expressions", [exp.DataType(this=exp.DataType.Type.JSON)])
            return new

    return expression


def upper_case_unquoted_identifiers(expression: exp.Expression) -> exp.Expression:
    """Upper case unquoted identifiers.

    Snowflake represents case-insensitivity using upper-case identifiers in cursor results.
    duckdb uses lowercase. We convert all unquoted identifiers to uppercase to match snowflake.

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("select name, name as fname from table1").transform(upper_case_unquoted_identifiers).sql()
        'SELECT NAME, NAME AS FNAME FROM TABLE1'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if isinstance(expression, exp.Identifier) and not expression.quoted and isinstance(expression.this, str):
        new = expression.copy()
        new.set("this", expression.this.upper())
        return new

    return expression


def values_columns(expression: exp.Expression) -> exp.Expression:
    """Support column1, column2 expressions in VALUES.

    Snowflake uses column1, column2 .. for unnamed columns in VALUES. Whereas duckdb uses col0, col1 ..
    See https://docs.snowflake.com/en/sql-reference/constructs/values#examples

    Example:
        >>> import sqlglot
        >>> sqlglot.parse_one("SELECT * FROM VALUES ('Amsterdam', 1)").transform(values_columns).sql()
        'SELECT * FROM (VALUES ('Amsterdam', 1)) AS _("column1", "column2")'
    Args:
        expression (exp.Expression): the expression that will be transformed.

    Returns:
        exp.Expression: The transformed expression.
    """

    if (
        isinstance(expression, exp.Values)
        and not expression.alias
        and expression.find_ancestor(exp.Select)
        and (values := expression.find(exp.Tuple))
    ):
        new = expression.copy()
        num_columns = len(values.expressions)
        columns = [exp.Identifier(this=f"column{i + 1}", quoted=True) for i in range(num_columns)]
        new.set("alias", exp.TableAlias(this=exp.Identifier(this="_", quoted=False), columns=columns))
        return new

    return expression
