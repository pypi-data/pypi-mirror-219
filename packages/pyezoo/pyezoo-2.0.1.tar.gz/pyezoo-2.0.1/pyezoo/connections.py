from pyezoo.config import *
from pyezoo.error import NotSupportedError, ParamCheckError
from pyezoo.ezoo_log import logger
from pyezoo.pool import *


class Connection(EZooClient):
    """
    Representation of a thrift connection with a ezoo-server.

    The proper way to get an instance of this class is to call
    connect().

    Establish a connection to the ezoo graph database. Accepts several
    arguments:
    :param host: Host where the database server is located.
    :param port: port
    :param auth: need auth
    :param user: Username to log in as.
    :param password: Password to use.
    :param timeout: socket timeout, -1 represents not set socket timeout
    :param ssl_open: ssl open
    :param scheme_url: connect url e.g. ezoodb://192.168.1.99:9090,192.168.1.100:9090

    other params:
    if enable ssl: next params need be input. example:
         ssl_cert_common_name="ezoodb.com"
         ca_certs="/tmp/ezoodb/keys/CA.pem"
         client_cert="/tmp/ezoodb/keys/client.crt"
         client_key="/tmp/ezoodb/keys/client.key"
    """

    def __init__(self, user=None, password=None, auth=True, host=None, port=0, scheme_url=None,
                 timeout=-1, ssl_open=False, manage=False, *args, **kwargs):
        if host and port:
            server = ServerAddress(host, port)
        elif scheme_url:
            result = Parser.parser(scheme_url)
            if len(result["servers"]) == 1:
                server = result["servers"][0]
            else:
                logger.error("only support standalone! " + scheme_url)
                raise ParamCheckError
        else:
            raise ParamCheckError
        super().__init__(server, user, password, auth, timeout, ssl_open, manage, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def close(self):
        """
        Close the connection now (rather than whenever .__del__() is called).
        The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any
        operation is attempted with the connection. The same applies to all cursor objects trying to use the connection.
        Note that closing a connection without committing the changes first will cause an implicit rollback to be
        performed.
        """
        super().close()

    def commit(self):
        """
        Commit any pending transaction to the database.
        Note that if the database supports an auto-commit feature, this must be initially off. An interface method may
        be provided to turn it back on.
        Database modules that do not support transactions should implement this method with void functionality.
        """
        pass

    def rollback(self):
        """
        This method is optional since not all databases provide transaction support.
        In case a database does provide transactions this method causes the database to roll back to the start of any
        pending transaction. Closing a connection without committing the changes first will cause an implicit rollback
        to be performed.
        """
        pass

    def cursor(self):
        """
        Return a new Cursor Object using the connection.
        If the database does not provide a direct cursor concept, the module will have to emulate cursors using other
        means to the extent needed by this specification.
        """
        raise NotSupportedError

    def get_client(self):
        return self.client

    def ping(self):
        return self.check_valid()
