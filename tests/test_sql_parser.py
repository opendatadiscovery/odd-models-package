from odd_models.sql_parser import SqlStatement


def test_parse_ddl():
    statement = SqlStatement("SELECT price, hd, ram FROM pc")
    assert statement.inputs == ["pc"]
    assert statement.columns == ["price", "hd", "ram"]


def test_parse_cte():
    statement = SqlStatement(
        """
    WITH cte AS (
    SELECT array_agg(id order by id desc) AS field_ids, --comment
    array_agg(dataset_version_id)  AS dsv_ids
    FROM dataset_field
    GROUP BY oddrn, type
    ORDER BY oddrn
    )
    SELECT * from cte;
    """
    )

    assert ["dataset_field"] == statement.inputs
    assert ["id", "dataset_version_id", "oddrn"] == statement.columns
    assert [] == statement.outputs


def test_parse_cte_with_wildcards():
    statement = SqlStatement(
        """
    WITH cte AS (
    SELECT array_agg(id order by id desc) AS field_ids, --comment
    array_agg(dataset_version_id)  AS dsv_ids
    FROM dataset_field
    GROUP BY oddrn, type
    ORDER BY oddrn
    )
    SELECT * from cte;
    """,
        skip_wc=False,
    )

    assert ["dataset_field"] == statement.inputs
    assert ["id", "dataset_version_id", "oddrn", "*"] == statement.columns
    assert [] == statement.outputs


def test_parse_multiple_cte():
    statement = SqlStatement(
        """\
    with cte as
    (
    select
    dbo.Cable.*,
    row_number() over(partition by dbo.Cable.TagNo order by dbo.Cable.CableRevision desc) as rn
    from dbo.Cable
    where (dbo.Cable.CableRevision = @CoreRevision )
    ),
    cte2 as (
    select
    dbo.Cable.TagNo,dbo.Core.*,
    row_number() over(partition by dbo.Core.CoreNo order by dbo.Core.CoreRevision desc) as rn
    from dbo.Core INNER JOIN
    dbo.Cable ON dbo.Cable.Id = dbo.Core.CableId
    where  (dbo.Core.CoreRevision <= @CoreRevision  )
    )
    select *
    from cte
    join cte2 on cte1.TagNo = cte2.TagNo
    where cte.rn = 1 and cte2.rn = 1;
    """
    )

    assert ["dbo.Cable", "dbo.Core"] == statement.inputs
    assert [
        "dbo.Cable.TagNo",
        "dbo.Cable.CableRevision",
        "@CoreRevision",
        "dbo.Core.CoreNo",
        "dbo.Core.CoreRevision",
        "dbo.Cable.Id",
        "dbo.Core.CableId",
        "cte1.TagNo",
    ] == statement.columns
    assert [] == statement.outputs


def test_parse_dml():
    statement = SqlStatement(
        "INSERT INTO employees (employee_name,employee_id,age,gender) VALUES ('SAM',01,31,'M');"
    )
    assert ["employees"] == statement.outputs
    assert ["employee_name", "employee_id", "age", "gender"] == statement.columns
    assert [] == statement.inputs
