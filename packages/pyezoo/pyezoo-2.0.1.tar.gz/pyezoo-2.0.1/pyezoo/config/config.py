import re

from pyezoo.error import ParserSchemeError


class ServerAddress:
    """
    ip and port
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __eq__(self, other):
        if type(other) == type(self) and self.ip == other.ip and self.port == other.port:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.ip + ":" + self.port)

    def __str__(self):
        return self.ip + ":" + self.port


class Parser:
    """
    parser scheme
    """

    @staticmethod
    def parser(scheme: str) -> map:
        if not scheme:
            raise ParserSchemeError
        res = {
            "username": None,
            "password": None,
            "servers": None
        }
        obj = re.match(r'^ezoodb://([a-zA-Z]+:[a-zA-Z]+@)?([0-9.:,]+)(/[\-a-zA-Z0-9_\u4e00-\u9fa5]+)?$', scheme)
        if obj:
            secret = obj.group(1)
            server = obj.group(2)
            database = obj.group(3)
            if secret:
                user_pwd = secret.split(':')
                if len(user_pwd) != 2:
                    raise ParserSchemeError
                res["username"] = user_pwd[0]
                res["password"] = user_pwd[1]
            res["database"] = database
            servers = server.split(',')
            serveraddrs = []
            for one in servers:
                ip_port = one.split(':')
                if len(ip_port) != 2:
                    raise ParserSchemeError
                serveraddr = ServerAddress(ip_port[0], ip_port[1])
                serveraddrs.append(serveraddr)
            res["servers"] = serveraddrs
            return res
        else:
            raise ParserSchemeError


class EZooPooledConfig:
    """
    ezoo connection pool's config
    :param user 用户名
    :param password 密码
    :param scheme_url ezoo-server的scheme_url，入参指定的user、password、database的优先级大于scheme_url解析后的
           v2.0.0，传入controller节点的ip和对外rpc端口
           e.g. ezoodb://192.168.1.99:9090,192.168.1.100:9090
    :param database 数据库名 暂未使用
    :param maxconnections: 连接池允许的最大连接数，0和None表示不限制连接数, 使用PooledDistribute时表示写池的最大连接数
    :param mincached: 初始化时，链接池中至少创建的空闲的链接，0表示不创建, 使用PooledDistribute时表示写池的初始连接数
    :param maxcached: 链接池中最多闲置的链接，0和None不限制, 使用PooledDistribute时表示写池的最多闲置连接
    :param read_maxconnections: 仅用于PooledDistribute，且read_slave_ok=True时有效，表示读池的最大连接数
    :param read_mincached: 仅用于PooledDistribute，且read_slave_ok=True时有效，表示读池的初始连接数
    :param read_maxcached: 仅用于PooledDistribute，且read_slave_ok=True时有效，表示读池的最多闲置连接
    :param blocking: 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    :param maxusage: 一个链接最多被重复使用的次数，None表示无限制
    :param connect_timeout: timeout for get a connection in milliseconds (default: 10000)
    :param read_slave_ok 从库是否可读
    :param read_write_separate
    :param ssl_open: ssl open
    :param auth: need auth
    :param timeout: query timeout in milliseconds (default: None - no timeout)

    other params:
    if enable ssl: next params need be input. example:
         ssl_cert_common_name="ezoodb.com"
         ca_certs="/tmp/ezoodb/keys/CA.pem"
         client_cert="/tmp/ezoodb/keys/client.crt"
         client_key="/tmp/ezoodb/keys/client.key"
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
                 maxusage=None,
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
        self.scheme_url = scheme_url
        result = Parser.parser(scheme_url)
        self.servers = result["servers"]
        self.user = user if user else result["username"]
        self.password = password if password else result["password"]
        self.database = database if database else result["database"]
        self.min_cached = mincached if mincached else 0
        self.max_cached = maxcached if maxcached else 0
        self.max_connections = maxconnections if maxconnections else 0
        self.read_min_cached = read_mincached if read_mincached else 0
        self.read_max_cached = read_maxcached if read_maxcached else 0
        self.read_max_connections = read_maxconnections if read_maxconnections else 0
        self.blocking = blocking
        self.max_usage = maxusage
        self.connect_timeout = connect_timeout
        self.read_slave_ok = read_slave_ok
        self.read_write_separate = read_write_separate
        self.auth = auth
        self.ssl_open = ssl_open
        self.ssl_cert_common_name = ssl_cert_common_name
        self.ca_certs = ca_certs
        self.client_cert = client_cert
        self.client_key = client_key
        self.timeout = timeout
