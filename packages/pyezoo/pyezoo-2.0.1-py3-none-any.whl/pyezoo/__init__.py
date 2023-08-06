import os
import sys

include_root = os.path.abspath(__file__)
include_root = os.path.dirname(include_root)

sys.path.append(os.path.join(include_root, "gen"))

from pyezoo.ezoo_log import logger
from . import connections

"""
This package contains a pure-Python eZoo client library, based on PEP 249.
So we can use DBUtils package to support connection pool.
"""

from pyezoo.constants import FIELD_TYPE
from pyezoo.error import (
    Warning,
    Error,
    InterfaceError,
    DataError,
    DatabaseError,
    OperationalError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    ProgrammingError,
    EZooError,
)

from pyezoo.times import (
    Date,
    Time,
    Timestamp,
    DateFromTicks,
    TimeFromTicks,
    TimestampFromTicks,
)

from pyezoo.pool.pooled_db import PooledDB
from pyezoo.pool.pooled_distribute import PooledDistribute


class DBAPISet(frozenset):
    def __ne__(self, other):
        if isinstance(other, set):
            return frozenset.__ne__(self, other)
        else:
            return other not in self

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return frozenset.__eq__(self, other)
        else:
            return other in self

    def __hash__(self):
        return frozenset.__hash__(self)


STRING = DBAPISet([FIELD_TYPE.ENUM, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING])
BINARY = DBAPISet(
    [
        FIELD_TYPE.BLOB,
        FIELD_TYPE.LONG_BLOB,
        FIELD_TYPE.MEDIUM_BLOB,
        FIELD_TYPE.TINY_BLOB,
    ]
)
NUMBER = DBAPISet(
    [
        FIELD_TYPE.DECIMAL,
        FIELD_TYPE.DOUBLE,
        FIELD_TYPE.FLOAT,
        FIELD_TYPE.INT24,
        FIELD_TYPE.LONG,
        FIELD_TYPE.LONGLONG,
        FIELD_TYPE.TINY,
        FIELD_TYPE.YEAR,
    ]
)
DATE = DBAPISet([FIELD_TYPE.DATE, FIELD_TYPE.NEWDATE])
TIME = DBAPISet([FIELD_TYPE.TIME])
TIMESTAMP = DBAPISet([FIELD_TYPE.TIMESTAMP, FIELD_TYPE.DATETIME])
DATETIME = TIMESTAMP
ROWID = DBAPISet()


def Binary(x):
    """Return x as a binary type."""
    return bytes(x)


NULL = "NULL"

VERSION = (0, 0, 8, None)
if VERSION[3] is not None:
    VERSION_STRING = "%d.%d.%d_%s" % VERSION
else:
    VERSION_STRING = "%d.%d.%d" % VERSION[:3]

# required by DB API.
apilevel = "2.0"
threadsafety = 1
paramstyle = "pyformat"

Connect = connect = Connection = connections.Connection


def get_client_info():
    version = VERSION
    if VERSION[3] is None:
        version = VERSION[:3]
    return ".".join(map(str, version))


__version__ = get_client_info()

__all__ = [
    "BINARY",
    "Binary",
    "Connect",
    "Connection",
    "DATE",
    "Date",
    "Time",
    "Timestamp",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",
    "DataError",
    "DatabaseError",
    "Error",
    "FIELD_TYPE",
    "IntegrityError",
    "InterfaceError",
    "InternalError",
    "EZooError",
    "NULL",
    "NUMBER",
    "NotSupportedError",
    "DBAPISet",
    "OperationalError",
    "ProgrammingError",
    "ROWID",
    "STRING",
    "TIME",
    "TIMESTAMP",
    "Warning",
    "apilevel",
    "connect",
    "connections",
    "constants",
    "cursors",
    "get_client_info",
    "paramstyle",
    "threadsafety",
    "__version__",
    "logger",
    "PooledDB",
    "PooledDistribute"
]
