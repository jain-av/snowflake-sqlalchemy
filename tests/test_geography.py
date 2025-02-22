#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from json import loads

from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy import select
from sqlalchemy.sql import text

from snowflake.sqlalchemy import GEOGRAPHY


def test_create_table_geography_datatypes(engine_testaccount):
    """
    Create table including geography data types
    """

    metadata = MetaData()
    table_name = "test_geography0"
    test_geography = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("geo", GEOGRAPHY),
    )
    metadata.create_all(engine_testaccount)
    try:
        assert test_geography is not None
    finally:
        test_geography.drop(engine_testaccount)


def test_inspect_geography_datatypes(engine_testaccount):
    """
    Create table including geography data types
    """
    metadata = MetaData()
    table_name = "test_geography0"
    test_geography = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("geo1", GEOGRAPHY),
        Column("geo2", GEOGRAPHY),
    )
    metadata.create_all(engine_testaccount)

    try:
        with engine_testaccount.connect() as conn:
            test_point = "POINT(-122.35 37.55)"
            test_point1 = '{"coordinates": [-122.35,37.55],"type": "Point"}'

            ins = test_geography.insert().values(
                id=1, geo1=test_point, geo2=test_point1
            )

            with conn.begin():
                results = conn.execute(ins)

                s = select(test_geography)
                results = conn.execute(s)
                row = results.fetchone()
                assert row[0] == 1
                assert row[1] == row[2]
                assert loads(row[2]) == loads(test_point1)
    finally:
        test_geography.drop(engine_testaccount)
