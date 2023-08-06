from random import choice


class LBStrategy:
    """
    集群读连接池的负载均衡器
    """

    def get_server(self):
        pass


class RandomLBStrategy(LBStrategy):
    """
    随机选取节点
    """

    def __init__(self, servers: list):
        self._servers = servers

    def get_server(self):
        if self._servers and len(self._servers) > 0:
            return choice(self._servers)
        return None
