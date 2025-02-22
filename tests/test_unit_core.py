#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from sqlalchemy.engine.url import URL
from sqlalchemy.engine import make_url

from snowflake.sqlalchemy import base


def test_create_connect_args():
    sfdialect = base.dialect()

    test_data = [
        (
            # 0: full host name and no account
            make_url(
                "snowflake://testuser:testpassword@testaccount.snowflakecomputing.com"
            ).set_query({}),
            {
                "autocommit": False,
                "host": "testaccount.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
            },
        ),
        (
            # 1: account name only
            make_url("snowflake://testuser:testpassword@testaccount").set_query({}),
            {
                "autocommit": False,
                "host": "testaccount.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
                "port": "443",
                "account": "testaccount",
            },
        ),
        (
            # 2: account name including region
            make_url("snowflake://testuser:testpassword@testaccount.eu-central-1").set_query({}),
            {
                "autocommit": False,
                "host": "testaccount.eu-central-1.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
                "port": "443",
                "account": "testaccount",
            },
        ),
        (
            # 3: full host including region
            make_url(
                "snowflake://testuser:testpassword@testaccount.eu-central-1.snowflakecomputing.com"
            ).set_query({}),
            {
                "autocommit": False,
                "host": "testaccount.eu-central-1.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
            },
        ),
        (
            # 4: full host including region and account
            make_url(
                "snowflake://testuser:testpassword@testaccount.eu-central-1.snowflakecomputing.com"
            ).set_query({"account": "testaccount"}),
            {
                "autocommit": False,
                "host": "testaccount.eu-central-1.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
                "account": "testaccount",
            },
        ),
        (
            # 5: full host including region and account including region
            make_url(
                "snowflake://testuser:testpassword@testaccount.eu-central-1.snowflakecomputing.com"
            ).set_query({"account": "testaccount.eu-central-1"}),
            {
                "autocommit": False,
                "host": "testaccount.eu-central-1.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
                "account": "testaccount.eu-central-1",
            },
        ),
        (
            # 6: full host including region and account including region
            make_url(
                "snowflake://testuser:testpassword@snowflake.reg.local:8082"
            ).set_query({"account": "testaccount"}),
            {
                "autocommit": False,
                "host": "snowflake.reg.local",
                "password": "testpassword",
                "user": "testuser",
                "port": 8082,
                "account": "testaccount",
            },
        ),
        (
            # 7: Global URL
            make_url(
                "snowflake://testuser:testpassword@testaccount-hso894gsiuafdhsaj935.global"
            ),
            {
                "autocommit": False,
                "host": "testaccount-hso894gsiuafdhsaj935.global.snowflakecomputing.com",
                "password": "testpassword",
                "user": "testuser",
                "port": "443",
                "account": "testaccount",
            },
        ),
    ]

    for idx, ts in enumerate(test_data):
        _, opts = sfdialect.create_connect_args(ts[0])
        assert opts == ts[1], f"Failed: {idx}: {ts[0]}"


def test_denormalize_quote_join():
    sfdialect = base.dialect()

    test_data = [
        (["abc", "cde"], "abc.cde"),
        (["abc.cde", "def"], "abc.cde.def"),
        (['"Abc".cde', "def"], '"Abc".cde.def'),
        (['"Abc".cde', '"dEf"'], '"Abc".cde."dEf"'),
    ]
    for ts in test_data:
        assert sfdialect._denormalize_quote_join(*ts[0]) == ts[1]
