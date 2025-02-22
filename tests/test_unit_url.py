#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import urllib.parse

from sqlalchemy.engine import make_url


def test_url():
    assert (
        str(
            make_url(
                "snowflake://admin:test@testaccount/?warehouse=testwh"
            )
        )
        == "snowflake://admin:test@testaccount/?warehouse=testwh"
    )

    assert (
        str(make_url("snowflake://admin:test@testaccount/"))
        == "snowflake://admin:test@testaccount/"
    )

    assert (
        str(
            make_url(
                "snowflake://admin:1-pass 2-pass 3-%3A 4-%40 5-%2F 6-pass@testaccount/"
            )
        )
        == "snowflake://admin:1-pass 2-pass 3-%3A 4-%40 5-%2F 6-pass@testaccount/"
    )

    quoted_password = urllib.parse.quote("kx@% jj5/g")
    assert (
        str(make_url(f"snowflake://admin:{quoted_password}@testaccount/"))
        == "snowflake://admin:kx%40%25 jj5/g@testaccount/"
    )

    assert (
        str(make_url("snowflake://admin:test@testaccount/testdb"))
        == "snowflake://admin:test@testaccount/testdb"
    )

    assert (
        str(make_url("snowflake://admin:test@testaccount/testdb/testschema"))
        == "snowflake://admin:test@testaccount/testdb/testschema"
    )

    assert (
        str(
            make_url(
                "snowflake://admin:test@testaccount/testdb/testschema?warehouse=testwh"
            )
        )
        == "snowflake://admin:test@testaccount/testdb/testschema?warehouse=testwh"
    )

    assert (
        str(
            make_url(
                "snowflake://admin:test@snowflake.reg.local:443/testdb"
                "/testschema?account=testaccount"
            )
        )
        == "snowflake://admin:test@snowflake.reg.local:443/testdb/testschema?account=testaccount"
    )

    assert str(
        make_url("snowflake://admin:test@testaccount.eu-central-1/")
    ) == ("snowflake://admin:test@testaccount.eu-central-1/")

    assert str(
        make_url("snowflake://admin:test@testaccount.eu-central-1.azure/")
    ) == ("snowflake://admin:test@testaccount.eu-central-1.azure/")

    assert str(
        make_url(
            "snowflake://admin:test@testaccount.eu-central-1"
            ".snowflakecomputing.com:443/?account=testaccount"
        )
    ) == (
        "snowflake://admin:test@testaccount.eu-central-1"
        ".snowflakecomputing.com:443/?account=testaccount"
    )

    # empty password should be acceptable in URL utility. The validation will
    # happen in Python connector anyway.
    assert str(
        make_url(
            "snowflake://admin:@testaccount.eu-central-1"
            ".snowflakecomputing.com:443/?account=testaccount"
        )
    ) == (
        "snowflake://admin:@testaccount.eu-central-1"
        ".snowflakecomputing.com:443/?account=testaccount"
    )

    # authenticator=externalbrowser doesn't require a password.
    assert str(
        make_url(
            "snowflake://admin:@testaccount.eu-central-1"
            ".snowflakecomputing.com:443/?account=testaccount"
            "&authenticator=externalbrowser"
        )
    ) == (
        "snowflake://admin:@testaccount.eu-central-1"
        ".snowflakecomputing.com:443/?account=testaccount&authenticator=externalbrowser"
    )

    # authenticator=oktaurl support
    assert str(
        make_url(
            "snowflake://testuser:test@testaccount"
            "/?authenticator=https%3A%2F%2Ftestokta.okta.com"
        )
    ) == (
        "snowflake://testuser:test@testaccount"
        "/?authenticator=https%3A%2F%2Ftestokta.okta.com"
    )
