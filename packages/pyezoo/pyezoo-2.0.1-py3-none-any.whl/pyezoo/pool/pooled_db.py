"""
PooledDB - pooling for DB-API 2 connections.
"""

import time
from threading import Condition

from pyezoo.ezoo_log import logger
from .steady_db import connect


class PooledDBError(Exception):
    """General PooledDB error."""


class InvalidConnection(PooledDBError):
    """Database connection is invalid."""


class NotSupportedError(PooledDBError):
    """DB-API module not supported by PooledDB."""


class TooManyConnections(PooledDBError):
    """Too many database connections were opened."""


class ConnectionTimeout(PooledDBError):
    """get connect timeout."""


class ParamInvalid(PooledDBError):
    """get connect timeout."""


class PooledDB:
    """Pool for DB-API 2 connections.

    After you have created the connection pool, you can use
    connection() to get pooled, steady DB-API 2 connections.
    """

    def __init__(
            self, creator, mincached=0, maxcached=5,
            maxshared=0, maxconnections=10, blocking=False,
            connect_timeout=5000,
            maxusage=None, setsession=None, reset=True,
            failures=None, ping=1,
            *args, **kwargs):
        """Set up the DB-API 2 connection pool.

        creator: either an arbitrary function returning new DB-API 2
            connection objects or a DB-API 2 compliant database module
        mincached: initial number of idle connections in the pool
            (0 means no connections are made at startup)
        maxcached: maximum number of idle connections in the pool
            (0 or None means unlimited pool size)
        maxshared: maximum number of shared connections
            (0 or None means all connections are dedicated)
            When this maximum number is reached, connections are
            shared if they have been requested as shareable.
        maxconnections: maximum number of connections generally allowed
            (0 or None means an arbitrary number of connections)
        blocking: determines behavior when exceeding the maximum
            (if this is set to true, block and wait until the number of
            connections decreases, otherwise an error will be reported)
        maxusage: maximum number of reuses of a single connection
            (0 or None means unlimited reuse)
            When this maximum usage number of the connection is reached,
            the connection is automatically reset (closed and reopened).
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        reset: how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        failures: an optional exception class or a tuple of exception classes
            for which the connection failover mechanism shall be applied,
            if the default (OperationalError, InterfaceError, InternalError)
            is not adequate for the used database module
        ping: determines when the connection should be checked with ping()
            (0 = None = never, 1 = default = whenever fetched from the pool,
            2 = when a cursor is created, 4 = when a query is executed,
            7 = always, and all other bit combinations of these values)
        args, kwargs: the parameters that shall be passed to the creator
            function or the connection constructor of the DB-API 2 module
        """
        try:
            threadsafety = creator.threadsafety
        except AttributeError:
            try:
                if not callable(creator.connect):
                    raise AttributeError
            except AttributeError:
                threadsafety = 2
            else:
                threadsafety = 0
        if not threadsafety:
            raise NotSupportedError("Database module is not thread-safe.")
        self._creator = creator
        self._args, self._kwargs = args, kwargs
        self._blocking = blocking
        self._maxusage = maxusage
        self._setsession = setsession
        self._reset = reset
        self._failures = failures
        self._ping = ping
        if mincached is None:
            mincached = 0
        if maxcached is None:
            maxcached = 0
        if maxconnections is None:
            maxconnections = 0
        if maxcached:
            if maxcached < mincached:
                maxcached = mincached
            self._maxcached = maxcached
        else:
            self._maxcached = 0
        if threadsafety > 1 and maxshared:
            self._maxshared = maxshared
            self._shared_cache = []  # the cache for shared connections
        else:
            self._maxshared = 0
        if maxconnections:
            if maxconnections < maxcached:
                maxconnections = maxcached
            if maxconnections < maxshared:
                maxconnections = maxshared
            self._maxconnections = maxconnections
        else:
            self._maxconnections = 0
        self._idle_cache = []  # the actual pool of idle connections
        self._lock = Condition()
        self._connections = 0
        self._connection_timeout = connect_timeout
        # Establish an initial number of idle database connections with thread
        idle = [self.dedicated_connection() for i in range(mincached)]
        while idle:
            idle.pop().close()

    def steady_connection(self):
        """Get a steady, unpooled DB-API 2 connection."""
        return connect(
            self._creator, None, self._maxusage, self._setsession, True, None,
            self._failures, self._ping, True, *self._args, **self._kwargs)

    def connection(self):
        """Get a steady, cached DB-API 2 connection from the pool.

        If shareable is set and the underlying DB-API 2 allows it,
        then the connection may be shared with other threads.
        """
        with self._lock:
            start = int(round(time.time() * 1000))
            timeout = self._connection_timeout
            while timeout > 0:
                has_get = False
                while self._maxconnections and self._connections >= self._maxconnections:
                    self._wait_lock()
                try:  # first try to get it from the idle cache
                    # connection limit not reached, get a dedicated connection
                    while len(self._idle_cache) > 0:
                        con = self._idle_cache.pop(0)
                        if con.check_maxusage():
                            has_get = True
                            break
                    if not has_get:
                        con = self.steady_connection()
                        has_get = True
                except Exception:
                    pass
                if has_get and con._ping_check():  # check connection
                    # generate proxy connection
                    con = PooledDedicatedDBConnection(self, con)
                    self._connections += 1
                    return con
                end = int(round(time.time() * 1000))
                timeout = self._connection_timeout - (end - start)
        logger.error("get connection timeout!")
        raise ConnectionTimeout

    def dedicated_connection(self):
        """Alias for connection(shareable=False)."""
        return self.connection()

    def unshare(self, con):
        """Decrease the share of a connection in the shared cache."""
        with self._lock:
            con.unshare()
            shared = con.shared
            if not shared:  # connection is idle,
                try:  # so try to remove it
                    self._shared_cache.remove(con)  # from shared cache
                except ValueError:
                    pass  # pool has already been closed
        if not shared:  # connection has become idle,
            self.cache(con.con)  # so add it to the idle cache

    def cache(self, con):
        """Put a dedicated connection back into the idle cache."""
        with self._lock:
            if not self._maxcached or len(self._idle_cache) < self._maxcached:
                con._reset(force=self._reset)  # rollback possible transaction
                # the idle cache is not full, so put it there
                self._idle_cache.append(con)  # append it to the idle cache
            else:  # if the idle cache is already full,
                con.close()  # then close the connection
            self._connections -= 1
            self._lock.notify()

    def close(self):
        """Close all connections in the pool."""
        with self._lock:
            while self._idle_cache:  # close all idle connections
                con = self._idle_cache.pop(0)
                try:
                    con.close()
                except Exception:
                    pass
            if self._maxshared:  # close all shared connections
                while self._shared_cache:
                    con = self._shared_cache.pop(0).con
                    try:
                        con.close()
                    except Exception:
                        pass
                    self._connections -= 1
            self._lock.notify_all()

    def __del__(self):
        """Delete the pool."""
        try:
            self.close()
        except:  # builtin Exceptions might not exist any more
            pass

    def _wait_lock(self):
        """Wait until notified or report an error."""
        if not self._blocking:
            raise TooManyConnections
        self._lock.wait()


# Auxiliary classes for pooled connections

class PooledDedicatedDBConnection:
    """
    Auxiliary proxy class for pooled dedicated connections.
    :param pool: the corresponding PooledDB instance
    :param con: the underlying SteadyDB connection
    """

    def __init__(self, pool, con):
        """
        Create a pooled dedicated connection.
        """
        # basic initialization to make finalizer work
        self._con = None
        # proper initialization of the connection
        if not con.threadsafety():
            raise NotSupportedError("Database module is not thread-safe.")
        self._pool = pool
        self._con = con
        self._con.set_connection_pool(self._pool)

    def close(self):
        """Close the pooled dedicated connection."""
        # Instead of actually closing the connection,
        # return it to the pool for future reuse if not manage connection.
        if self._con:
            if self._con.manage:
                self._con.close()
                self._con = None
            else:
                self._pool.cache(self._con)
                self._con = None

    # __getattr__ 在访问对象访问类中不存在的成员时会自动调用
    def __getattr__(self, name):
        """Proxy all members of the class."""
        if self._con:
            return getattr(self._con, name)
        raise InvalidConnection

    def __del__(self):
        """Delete the pooled connection."""
        try:
            self.close()
        except:  # builtin Exceptions might not exist any more
            pass

    def __enter__(self):
        """Enter a runtime context for the connection."""
        return self

    def __exit__(self, *exc):
        """Exit a runtime context for the connection."""
        self.close()
