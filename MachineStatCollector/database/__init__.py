"""Database layer for the project1. Contains mapping to SQLAlchemy/PostgreSQL.
"""

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import config


Base = declarative_base()
collect_engine = create_engine(
    "postgres://%s:%s@%s:%s/%s?client_encoding=utf8" % (
        config.get("database", "user"), config.get("database", "password"),
        config.get("database", "host"), config.get("database", "port"),
        config.get("database", "database")
    ), pool_size=20, max_overflow=0
)


import clients
import stats


Session = scoped_session(sessionmaker(bind=collect_engine))
Base.metadata.create_all(collect_engine)



def add_to_database(orm_class, commit=True, retries=3, **kwargs):
    """Creates a new entry for the specified ORM class.

    Can also commit with retries
    :param orm_class: The ORM class for which the entry is to be added.
    :type orm_class: sqlalchemy.ext.declarative.api.DeclarativeMeta
    :param commit: Whether to perform a DB session commit after adding the
    record. Defaults to True.
    :type commit: bool
    :param retries: The number of times to retry the DB commit. Does a
    session flush before retrying.
    :type retries: int
    :param kwargs: The values that are to be put in the new record
    :type kwargs: dict
    :return: A valid ORM object
    """
    new_record = orm_class(**kwargs)
    Session.add(new_record)
    while retries and commit:
        try:
            Session.commit()
            commit = False
        except exc.InvalidRequestError:
            retries -= 1
            Session.flush()
        if retries == 0:
            message = "Retry count exceeded for database insertion of '{}' " \
                      "record"
            print(message)
            # raise exception.Failed(message=message.format(orm_class))
    return new_record