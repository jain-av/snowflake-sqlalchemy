#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from sqlalchemy import Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, Sequence("user_id_seq"), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)


def test_insert_table(engine_testaccount):
    metadata = MetaData()
    users = User.__table__
    users.metadata.create_all(engine_testaccount)

    data = [
        {
            "id": 1,
            "name": "testname1",
            "fullname": "fulltestname1",
        },
        {
            "id": 2,
            "name": "testname2",
            "fullname": "fulltestname2",
        },
    ]
    try:
        with engine_testaccount.connect() as conn:
            # using multivalue insert
            with conn.begin():
                conn.execute(users.insert().values(data))
                results = conn.execute(select(users).order_by("id"))
                row = results.fetchone()
                assert row._mapping["name"] == "testname1"

    finally:
        users.drop(engine_testaccount)
