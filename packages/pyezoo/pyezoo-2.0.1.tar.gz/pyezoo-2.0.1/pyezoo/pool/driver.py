import os
import platform

from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket, TSSLSocket

from pyezoo.config import *
from pyezoo.error import ConnectError
from pyezoo.error import ParamCheckError
from pyezoo.ezoo_log import logger
from pyezoo.pool.ezooapi import EZooInterface


class EZooClient:
    """
    a simple wrapper ezoo thrift client
    """

    def __init__(self, server: ServerAddress, user, password, auth, timeout, ssl_open, manage, *args,
                 **kwargs):
        self._pool = None
        self.ip = server.ip
        self.port = server.port
        self._read_timeout = timeout
        self._ssl_open = ssl_open
        self._auth = auth
        self.user = user
        self.password = password
        self._kwargs = kwargs
        self._manage = manage

        self._transport, self._protocol = self.get_protocol(server)
        self.client = EZooInterface(self._protocol, self._pool, self._manage)
        self.open()
        self.isClosed = False

    def get_protocol(self, server):
        if platform.system().lower() == 'windows':
            keepalive = False
        else:
            keepalive = True
        if self._ssl_open:
            try:
                ca = self._kwargs["ca_certs"]
                client_cert = self._kwargs["client_cert"]
                client_key = self._kwargs["client_key"]
                server_name = self._kwargs["ssl_cert_common_name"]
                if not server_name or not os.path.exists(ca) or not os.path.exists(client_cert) \
                        or not os.path.exists(client_key):
                    raise ParamCheckError
            except Exception as e:
                logger.error("please check input params: ca_certs, client_cert, client_key", e)
                raise ParamCheckError
            # ciphers = kwargs["ciphers"] if "ciphers" in kwargs and kwargs[
            #     "ciphers"] else "ALL:!ADH:!LOW:!EXP:!MD5:@STRENGTH"
            self._socket = TSSLSocket.TSSLSocket(server.ip, server.port, validate=True, server_hostname=server_name,
                                                 keyfile=client_key, certfile=client_cert, ca_certs=ca,
                                                 socket_keepalive=keepalive)
        else:
            self._socket = TSocket.TSocket(server.ip, server.port, socket_keepalive=keepalive)

        transport = TTransport.TBufferedTransport(self._socket)
        protocol = TBinaryProtocol(transport)
        return transport, protocol

    def open(self):
        self._open(self._transport)

    def check_valid(self):
        try:
            if self._transport and not self._transport.isOpen():
                return False

            self.client.hello()
            return True
        except Exception:
            pass
        return False

    def close(self):
        if self._transport:
            self._transport.close()
        self.isClosed = True

    def is_open(self):
        return self._transport and self._transport.isOpen()

    def _open(self, transport):
        try:
            if not transport.isOpen():
                # first set connect timeout, 10s
                self._socket.setTimeout(10000)
                transport.open()
                if self._read_timeout != -1:
                    self._socket.setTimeout(self._read_timeout)
                else:
                    self._socket.setTimeout(None)
                if self._auth:
                    # deprecated
                    # salted_pwd = codec_util.key_derive(self.password)
                    rep = self.client.auth(self.user, self.password)
                    if rep.status != 0:
                        logger.error("Auth failed!")
                        raise
                self.client.hello()
        except Exception as e:
            logger.error("Not connected to server, please check server.")
            raise ConnectError

    def set_connection_pool(self, pool):
        self._pool = pool
        self.client.set_connection_pool(pool)
