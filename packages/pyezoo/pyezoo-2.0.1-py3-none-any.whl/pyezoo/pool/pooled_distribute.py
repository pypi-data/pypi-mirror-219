"""
PooledDB - pooling for DB-API 2 connections.
support replicaset db
"""

import copy
import time
from threading import Condition
from threading import Lock
from threading import Thread
from time import sleep

from pyezoo.gen.ezootypes.ttypes import srv_status_enum

import pyezoo
from pyezoo.config import EZooPooledConfig
from pyezoo.connections import Connection
from pyezoo.error import ParameterError
from pyezoo.ezoo_log import logger
from pyezoo.loadbalance.strategy import RandomLBStrategy
from pyezoo.pool.pooled_db import (
    NotSupportedError, TooManyConnections, PooledDedicatedDBConnection, ConnectionTimeout, ParamInvalid
)
from .steady_db import connect


class RoutingTable:

    def __init__(self, workers: list, graph_group: dict, group_distributed_infos: dict):
        self._workers = workers
        self._graph_group = graph_group
        self._distributed_infos = group_distributed_infos


class EZooDataSource:
    """
    manage distribute cluster connections
    """

    def __init__(self, servers: list, config: EZooPooledConfig):
        self._servers = servers
        self._lock = Lock()
        self._condition_lock = Condition()
        self._username = config.user
        self._password = config.password
        self._read_slave_ok = config.read_slave_ok
        self._read_write_separate = config.read_write_separate
        self._timeout = config.timeout
        self._config = config
        self._graph_name = config.database
        self._controller_leader = self._find_controller_leader()
        self._graph_leader, self._graph_follower = self._find_graph_leader()
        self._graph_available_follower = []
        for one in self._graph_follower:
            if one.srv_status == srv_status_enum.connected:
                self._graph_available_follower.append(one)

        # 开启线程去更新从库的信息, 因为当获取到的server拿不到连接时会降级，同时依靠该线程来，检测降级后的连接是否重新可用
        Thread(target=self._check_follower, args=(), daemon=True).start()

    def fresh(self):
        if self._lock.acquire():
            try:
                self._controller_leader = self._find_controller_leader()
                if self._controller_leader:
                    self._graph_leader, self._graph_follower = self._find_graph_leader()
                    if self._graph_leader:
                        self._graph_available_follower = []
                        for one in self._graph_follower:
                            if one.srv_status == srv_status_enum.connected:
                                self._graph_available_follower.append(one)
            except Exception as e:
                logger.error("background thread check follower error: " + str(e))
            self._lock.release()

    def _check_follower(self):
        while True:
            self.fresh()
            with self._condition_lock:
                if self._controller_leader and self._graph_leader:
                    self._condition_lock.wait()
                else:
                    sleep(2)

    def _find_controller_leader(self):
        for server in self._servers:
            try:
                conn = Connection(host=server.ip, port=server.port, timeout=self._timeout,
                                  user=self._config.user, password=self._config.password, auth=self._config.auth,
                                  ssl_open=self._config.ssl_open,
                                  manage=True,
                                  ssl_cert_common_name=self._config.ssl_cert_common_name,
                                  ca_certs=self._config.ca_certs,
                                  client_cert=self._config.client_cert,
                                  client_key=self._config.client_key)
                parameters = {"is_all": "true"}
                response = conn.client.get_status(parameters)
                graph_groups = response.graph_groups
                group_distributed_infos = response.group_distributed_infos
                if graph_groups and "admin" in graph_groups and group_distributed_infos:
                    admin_gid = graph_groups["admin"]
                    for shard in group_distributed_infos[admin_gid]:
                        # follower = 0x1, candidate = 0x2, leader = 0x3
                        if shard.role == 0x03:
                            return shard
                else:
                    logger.error("please check config, maybe not a distribute cluster.")
                conn.close()
            except Exception as e:
                logger.error("get_status invoke error! " + str(e))
        logger.error("can not find controller leader!")
        return None

    def _get_routing_table(self):
        if not self._controller_leader:
            logger.error("controller leader is None!")
            return None, None, None
        try:
            conn = Connection(host=self._controller_leader.ip, port=self._controller_leader.service_port,
                              timeout=self._timeout,
                              user=self._config.user, password=self._config.password, auth=self._config.auth,
                              ssl_open=self._config.ssl_open,
                              manage=True,
                              ssl_cert_common_name=self._config.ssl_cert_common_name,
                              ca_certs=self._config.ca_certs,
                              client_cert=self._config.client_cert,
                              client_key=self._config.client_key)
            parameters = {"is_all": "true"}
            response = conn.client.get_status(parameters)
            graph_groups = response.graph_groups
            group_distributed_infos = response.group_distributed_infos
            if graph_groups and "admin" in graph_groups and group_distributed_infos:
                admin_gid = graph_groups["admin"]
                for shard in group_distributed_infos[admin_gid]:
                    # follower = 0x1, candidate = 0x2, leader = 0x3
                    if shard.role == 0x03 and self._controller_leader.server_id == shard.server_id:
                        return response.graph_groups, response.group_distributed_infos, response.servers
                    elif shard.role == 0x03:
                        self._controller_leader = shard
            else:
                logger.error("please check config, maybe not a distribute cluster.")
            conn.close()

        except Exception as e:
            logger.error("get_routing_table invoke error! " + str(e))
        return None, None, None

    def _find_graph_leader(self):
        leader = None
        follower = []
        try:
            graph_groups, group_distributed_infos, servers = self._get_routing_table()
            if graph_groups and self._graph_name in graph_groups and group_distributed_infos:
                gid = graph_groups[self._graph_name]
                shards = group_distributed_infos[gid]
                if not shards:
                    return leader, follower
                for one in shards:
                    if one.role == 0x03:
                        leader = one
                    else:
                        if servers[one.server_id]:
                            follower.append(servers[one.server_id])
        except Exception as e:
            logger.warn("not find graph info! " + str(e))
        if not leader:
            with self._condition_lock:
                self._condition_lock.notify_all()
        return leader, follower

    def reset_graph_leader(self):
        if self._lock.acquire():
            try:
                self._graph_leader, self._graph_follower = self._find_graph_leader()
                if self._graph_leader:
                    logger.info("find a new leader: " + str(self._graph_leader.ip))
                    self._graph_available_follower = []
                    for one in self._graph_follower:
                        if one.srv_status == srv_status_enum.connected:
                            self._graph_available_follower.append(one)
            except Exception as e:
                logger.error("reset graph leader error: " + str(e))
            self._lock.release()

    def write_connection(self, manage=False):
        if not manage:
            if self._graph_leader:
                try:
                    conn = Connection(host=self._graph_leader.ip, port=self._graph_leader.service_port,
                                      timeout=self._timeout,
                                      user=self._config.user, password=self._config.password, auth=self._config.auth,
                                      ssl_open=self._config.ssl_open,
                                      manage=manage,
                                      ssl_cert_common_name=self._config.ssl_cert_common_name,
                                      ca_certs=self._config.ca_certs,
                                      client_cert=self._config.client_cert,
                                      client_key=self._config.client_key
                                      )
                    if not conn.isClosed:
                        return conn
                except Exception:
                    pass
        else:
            if self._controller_leader:
                try:
                    conn = Connection(host=self._controller_leader.ip, port=self._controller_leader.service_port,
                                      timeout=self._timeout,
                                      user=self._config.user, password=self._config.password, auth=self._config.auth,
                                      ssl_open=self._config.ssl_open,
                                      manage=manage,
                                      ssl_cert_common_name=self._config.ssl_cert_common_name,
                                      ca_certs=self._config.ca_certs,
                                      client_cert=self._config.client_cert,
                                      client_key=self._config.client_key
                                      )
                    if not conn.isClosed:
                        return conn
                except Exception:
                    pass
        # reset when not get one connection
        try:
            self.reset_graph_leader()
        except Exception:
            pass
        return None

    def read_connection(self, manage=False):
        if not self._read_slave_ok:
            return self.write_connection(manage)
        else:
            # manage thread
            if manage:
                return self.write_connection(manage)

            # graph
            for_select_set = []
            if self._lock.acquire():
                for_select_set = copy.deepcopy(self._graph_available_follower)
                self._lock.release()

            # 是否读写分离
            if not self._read_write_separate:
                for_select_set.append(self._graph_leader)

            need_reset = False
            if len(for_select_set) != 0:
                server = RandomLBStrategy(for_select_set).get_server()
                try:
                    conn = Connection(host=server.ip, port=server.service_port, timeout=self._timeout,
                                      user=self._config.user, password=self._config.password, auth=self._config.auth,
                                      ssl_open=self._config.ssl_open,
                                      manage=manage,
                                      ssl_cert_common_name=self._config.ssl_cert_common_name,
                                      ca_certs=self._config.ca_certs,
                                      client_cert=self._config.client_cert,
                                      client_key=self._config.client_key
                                      )
                    if not conn.isClosed:
                        return conn
                except Exception:
                    if server.server_id != self._graph_leader.server_id:
                        self._update_follower(server)
                    else:
                        need_reset = True

            else:
                need_reset = True

            if need_reset:
                # 尝试重新连接
                try:
                    self.reset_graph_leader()
                except Exception:
                    pass
        return None

    def connection(self, manage=False):
        return self.write_connection(manage)

    def _update_follower(self, server):
        if self._lock.acquire():
            for x in self._graph_available_follower:
                if x.server_id == server.server_id:
                    self._graph_available_follower.remove(x)
                    break
            self._lock.release()


class PooledDatasource:
    """Pool for DB-API 2 connections.

    After you have created the connection pool, you can use
    read_connection() or write_connection() to get pooled, steady DB-API 2 connections.
    In this class we will use datasource to get connection.

    :param creator: either an arbitrary function returning new DB-API 2
        connection objects or a DB-API 2 compliant database module
    :param datasource: class EZooDataSource, generate connection
    :param mincached: initial number of idle connections in the pool
        (0 means no connections are made at startup)
    :param maxcached: maximum number of idle connections in the pool
        (0 or None means unlimited pool size)
    :param maxshared: maximum number of shared connections
        (0 or None means all connections are dedicated)
        When this maximum number is reached, connections are
        shared if they have been requested as shareable.
    :param maxconnections: maximum number of connections generally allowed
        (0 or None means an arbitrary number of connections)
    :param blocking: determines behavior when exceeding the maximum
        (if this is set to true, block and wait until the number of
        connections decreases, otherwise an error will be reported)
    :param maxusage: maximum number of reuses of a single connection
        (0 or None means unlimited reuse)
        When this maximum usage number of the connection is reached,
        the connection is automatically reset (closed and reopened).
    :param args, kwargs: the parameters that shall be passed to the creator
        function or the connection constructor of the DB-API 2 module
    """

    def __init__(self, creator, datasource, mincached=0, maxcached=0, maxconnections=0,
                 blocking=False, maxusage=None, connect_timeout=5000, readonly=None, *args, **kwargs):
        """
        Set up the DB-API 2 connection pool.
        """
        try:
            threadsafety = creator.threadsafety
        except AttributeError:
            threadsafety = 0
        if not threadsafety:
            raise NotSupportedError("Database module is not thread-safe.")
        if not datasource:
            raise ParamInvalid
        self._creator = creator
        self._args, self._kwargs = args, kwargs
        self._blocking = blocking
        self._maxusage = maxusage
        self._setsession = None
        self._reset = True
        self._failures = None
        self._ping = 1
        self._datasource = datasource
        self._readonly = readonly
        # pool
        if maxcached:
            if maxcached < mincached:
                maxcached = mincached
            self._maxcached = maxcached
        else:
            self._maxcached = 0
        if maxconnections:
            if maxconnections < maxcached:
                maxconnections = maxcached
            self._maxconnections = maxconnections
        else:
            self._maxconnections = 0
        self._idle_cache = []  # the actual write pool of idle connections
        self._lock = Condition()
        self._connections = 0
        self._connection_timeout = connect_timeout
        # Establish an initial number of idle database connections with thread
        # idle = [self.dedicated_connection() for i in range(mincached)]
        # while idle:
        #     idle.pop().close()

    def steady_connection(self, manage, write=True):
        """Get a steady, unpooled DB-API 2 connection."""
        return connect(
            self._creator, self._datasource, self._maxusage, self._setsession, False, manage, write,
            self._failures, self._ping, True, *self._args, **self._kwargs)

    def connection(self, manage: bool):
        """Get a steady, cached DB-API 2 connection from the pool. support with PooledDatasource

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
                try:
                    # manage thread not join in pool
                    if not manage:
                        # first try to get it from the idle cache
                        # connection limit not reached, get a dedicated connection
                        while len(self._idle_cache) > 0:
                            con = self._idle_cache.pop(0)
                            if con.check_maxusage():
                                has_get = True
                                break
                    if not has_get:
                        if self._readonly:
                            con = self.steady_connection(manage, write=False)
                        else:
                            con = self.steady_connection(manage, write=True)
                        has_get = True
                except Exception:
                    pass
                # check connection
                if has_get and con._ping_check():
                    # generate proxy connection
                    con = PooledDedicatedDBConnection(self, con)
                    if not manage:
                        self._connections += 1
                    return con
                end = int(round(time.time() * 1000))
                timeout = self._connection_timeout - (end - start)
        logger.error("get connection timeout!")
        raise ConnectionTimeout

    def dedicated_connection(self):
        """Alias for connection(shareable=False)."""
        return self.connection(manage=False)

    def cache(self, con):
        """
        Put a dedicated connection back into the idle cache.
        """
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
            self._lock.notify_all()

    def fresh(self):
        if self._datasource:
            self._datasource.fresh()

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


class PooledDistribute:
    """
    线程池，同时支持读、写
    """

    def __init__(self,
                 user=None,
                 password=None,
                 scheme_url=None,
                 database=None,
                 mincached=0,
                 maxcached=10,
                 maxconnections=10,
                 read_mincached=0,
                 read_maxcached=30,
                 read_maxconnections=30,
                 blocking=False,
                 maxusage=20,
                 connect_timeout=10000,
                 read_slave_ok=False,
                 read_write_separate=False,
                 timeout=-1,
                 auth=True,
                 ssl_open=False,
                 ssl_cert_common_name=None,
                 ca_certs=None,
                 client_cert=None,
                 client_key=None
                 ):
        if not database or not scheme_url:
            raise ParameterError
        self.pooled_config = EZooPooledConfig(user, password, scheme_url, database, mincached, maxcached,
                                              maxconnections, read_mincached, read_maxcached, read_maxconnections,
                                              blocking, maxusage, connect_timeout, read_slave_ok, read_write_separate,
                                              timeout, auth, ssl_open, ssl_cert_common_name, ca_certs,
                                              client_cert, client_key
                                              )
        self.datasource = EZooDataSource(self.pooled_config.servers, self.pooled_config)
        self._read_slave_ok = self.pooled_config.read_slave_ok
        # write pool
        self._write_pool = PooledDatasource(
            pyezoo,
            self.datasource,
            mincached=self.pooled_config.min_cached,
            maxcached=self.pooled_config.max_cached,
            maxconnections=self.pooled_config.max_connections,
            blocking=self.pooled_config.blocking,
            maxusage=self.pooled_config.max_usage,
            connect_timeout=self.pooled_config.connect_timeout
        )
        # read pool
        if self._read_slave_ok:
            self._read_pool = PooledDatasource(
                pyezoo,
                self.datasource,
                mincached=self.pooled_config.read_min_cached,
                maxcached=self.pooled_config.read_max_cached,
                maxconnections=self.pooled_config.read_max_connections,
                blocking=self.pooled_config.blocking,
                maxusage=self.pooled_config.max_usage,
                connect_timeout=self.pooled_config.connect_timeout,
                readonly=True
            )

    def read_connection(self, manage=False):
        return self._read_pool.connection(manage) if self._read_slave_ok else self._write_pool.connection(manage)

    def write_connection(self, manage=False):
        return self._write_pool.connection(manage)

    def connection(self, manage=False):
        return self._write_pool.connection(manage)

    def fresh(self):
        self._write_pool.fresh()
        if self._read_slave_ok:
            self._read_pool.fresh()

    def close(self):
        self._write_pool.close()
        if self._read_slave_ok:
            self._read_pool.close()

    def __del__(self):
        """Delete the pool."""
        try:
            self.close()
        except Exception:
            pass
