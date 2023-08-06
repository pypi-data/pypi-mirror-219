#!/usr/bin/env python
#
# Embedded code in thrift gen-py.
# Non-essential component of the eZoo-Python-SDK.
#

import sys
from thrift.transport import TTransport, TSocket, TSSLSocket, THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from pyezoo.ezoo_log import logger
import inspect

from pyezoo.gen.ezooapi_algorithm import ezooapi_algorithm
from pyezoo.gen.ezooapi_auth import ezooapi_auth
from pyezoo.gen.ezooapi_base import ezooapi_base
from pyezoo.gen.ezooapi_data import ezooapi_data
from pyezoo.gen.ezooapi_client import ezooapi_client


class EZooInterface:

    def __init__(self, protocol, pool, manage):
        self._pool = pool
        self._manage = manage
        # ezooapi_algorithm client
        ezooapi_algorithm_protocol = TMultiplexedProtocol(protocol, "ezooapi_algorithm")
        self.cli_ezooapi_algorithm = ezooapi_algorithm.Client(ezooapi_algorithm_protocol)
        # ezooapi_auth client
        ezooapi_auth_protocol = TMultiplexedProtocol(protocol, "ezooapi_auth")
        self.cli_ezooapi_auth = ezooapi_auth.Client(ezooapi_auth_protocol)
        # ezooapi_base client
        ezooapi_base_protocol = TMultiplexedProtocol(protocol, "ezooapi_base")
        self.cli_ezooapi_base = ezooapi_base.Client(ezooapi_base_protocol)
        # ezooapi_data client
        ezooapi_data_protocol = TMultiplexedProtocol(protocol, "ezooapi_data")
        self.cli_ezooapi_data = ezooapi_data.Client(ezooapi_data_protocol)
        # ezooapi_client client
        ezooapi_client_protocol = TMultiplexedProtocol(protocol, "ezooapi_client")
        self.cli_ezooapi_client = ezooapi_client.Client(ezooapi_client_protocol)

    def set_connection_pool(self, pool):
        self._pool = pool


    # pyezoo.gen.ezooapi_algorithm.Iface

    def check_connectivity(self, db_name, src_node_id, dest_node_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.check_connectivity(db_name, src_node_id, dest_node_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def count_neighbour_with_prop_filter(self, db_name, start_node, edge, end_node_type, end_node_order_prop_name, search_direction, k_min, k_max, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.count_neighbour_with_prop_filter(db_name, start_node, edge, end_node_type, end_node_order_prop_name, search_direction, k_min, k_max)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def count_one_neighbour_relations_top_k(self, db_name, start_node_type, edge_type_set, end_node_type_set, search_direction, output_prop, top_k, is_desc, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.count_one_neighbour_relations_top_k(db_name, start_node_type, edge_type_set, end_node_type_set, search_direction, output_prop, top_k, is_desc)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_subgraph_with_neighbour(self, db_name, node_id, k_min, k_max, search_direction, condition, new_db_name, readonly, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.create_subgraph_with_neighbour(db_name, node_id, k_min, k_max, search_direction, condition, new_db_name, readonly)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_subgraph_with_node(self, db_name, ids, new_db_name, readonly, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.create_subgraph_with_node(db_name, ids, new_db_name, readonly)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_subgraph_with_node_neighbour(self, db_name, ids, search_direction, k, new_db_name, readonly, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.create_subgraph_with_node_neighbour(db_name, ids, search_direction, k, new_db_name, readonly)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_subgraph_with_type(self, db_name, node_type_list, edge_type_list, new_db_name, readonly, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.create_subgraph_with_type(db_name, node_type_list, edge_type_list, new_db_name, readonly)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_betcentrality(self, db_name, search_direction, hop, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_betcentrality(db_name, search_direction, hop)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_clocentrality(self, db_name, if_WF, hop, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_clocentrality(db_name, if_WF, hop)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_cluster_for_studio(self, db_name, node_list, edge_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_cluster_for_studio(db_name, node_list, edge_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_neighbour(self, db_name, ids, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_neighbour(db_name, ids, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_neighbour_for_studio(self, db_name, ids, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_neighbour_for_studio(db_name, ids, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_neighbour_with_few_relations(self, db_name, ids, k_min, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_neighbour_with_few_relations(db_name, ids, k_min, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_neighbour_with_limit(self, db_name, ids, k_min, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_neighbour_with_limit(db_name, ids, k_min, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_neighbour_without_relations(self, db_name, ids, k_min, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_neighbour_without_relations(db_name, ids, k_min, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_relation(self, db_name, node_list, k_max, search_direction, distinct, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_relation(db_name, node_list, k_max, search_direction, distinct, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_common_simple_neighbour(self, db_name, ids, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_common_simple_neighbour(db_name, ids, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_cosine_similarity_neighborhoods_single_source(self, db_name, node_id, e_type, weight, top_k, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_cosine_similarity_neighborhoods_single_source(db_name, node_id, e_type, weight, top_k)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_difference_neighbour(self, db_name, A, B, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_difference_neighbour(db_name, A, B, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_dijkstra(self, db_name, src_node_id, dest_node_id, search_direction, edge_type, edge_props_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_dijkstra(db_name, src_node_id, dest_node_id, search_direction, edge_type, edge_props_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_euclidean_distance(self, db_name, A, B, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_euclidean_distance(db_name, A, B)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_full_path(self, db_name, src_node_id, dest_node_id, k_max, search_direction, condition, max_size, distinct, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_full_path(db_name, src_node_id, dest_node_id, k_max, search_direction, condition, max_size, distinct)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_full_path_with_set(self, db_name, src_node_id_set, dest_node_id_set, k_max, search_direction, condition, max_size, distinct, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_full_path_with_set(db_name, src_node_id_set, dest_node_id_set, k_max, search_direction, condition, max_size, distinct)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_greedy_graph_coloring(self, db_name, node_type_set, edge_type_set, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_greedy_graph_coloring(db_name, node_type_set, edge_type_set)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_jaccard_similarity(self, db_name, A, B, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_jaccard_similarity(db_name, A, B)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_jaccard_similarity_between_two_node(self, db_name, A, B, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_jaccard_similarity_between_two_node(db_name, A, B)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_k_core(self, db_name, k_max, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_k_core(db_name, k_max)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_knn_cosine_single_source(self, db_name, node_id, e_type, weight, top_k, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_knn_cosine_single_source(db_name, node_id, e_type, weight, top_k)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_local_clustering_coefficient(self, db_name, node_type_set, edge_type_set, top_k, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_local_clustering_coefficient(db_name, node_type_set, edge_type_set, top_k)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_louvain(self, db_name, edge_type, edge_props_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_louvain(db_name, edge_type, edge_props_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_lpa(self, db_name, epoch_limit, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_lpa(db_name, epoch_limit)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_lpa_sync(self, db_name, epoch_limit, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_lpa_sync(db_name, epoch_limit)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_money_flow(self, db_name, start_node, start_time, end_time, money_percent, time_window, edge_type, time_props, money_props, mode, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_money_flow(db_name, start_node, start_time, end_time, money_percent, time_window, edge_type, time_props, money_props, mode)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour(self, db_name, node_id, k_min, k_max, search_direction, condition, return_relations, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour(db_name, node_id, k_min, k_max, search_direction, condition, return_relations)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_count(self, db_name, node_id, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_count(db_name, node_id, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_for_studio(self, db_name, node_id, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_for_studio(db_name, node_id, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_path_for_studio(self, db_name, search_direction, condition, nodes, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_path_for_studio(db_name, search_direction, condition, nodes)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_with_edge_filter(self, db_name, start_node, edge_type, is_valid_edge, end_node, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_with_edge_filter(db_name, start_node, edge_type, is_valid_edge, end_node, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_with_limit(self, db_name, node_id, k_min, k_max, search_direction, condition, return_relations, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_with_limit(db_name, node_id, k_min, k_max, search_direction, condition, return_relations, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_with_multi_edge_filter(self, db_name, start_node, edge_type_list, end_node, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_with_multi_edge_filter(db_name, start_node, edge_type_list, end_node, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_neighbour_with_prop_filter(self, db_name, start_node, edge, end_node, search_direction, k_min, k_max, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_neighbour_with_prop_filter(db_name, start_node, edge, end_node, search_direction, k_min, k_max)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_one_neighbour(self, db_name, node_id, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_one_neighbour(db_name, node_id, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_overlap_similarity(self, db_name, A, B, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_overlap_similarity(db_name, A, B)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_pagerank(self, db_name, damping_factor, epoch_limit, max_convergence_error, vertex_init_value, edge_type, edge_props_name, bidirection, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_pagerank(db_name, damping_factor, epoch_limit, max_convergence_error, vertex_init_value, edge_type, edge_props_name, bidirection)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_pagerank_top_k(self, db_name, damping_factor, epoch_limit, max_convergence_error, vertex_init_value, edge_type, edge_props_name, bidirection, top_k, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_pagerank_top_k(db_name, damping_factor, epoch_limit, max_convergence_error, vertex_init_value, edge_type, edge_props_name, bidirection, top_k)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_path(self, db_name, src_node_id, dest_node_id, k_min, k_max, search_direction, condition, max_size, query_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_path(db_name, src_node_id, dest_node_id, k_min, k_max, search_direction, condition, max_size, query_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_path_for_studio(self, db_name, src_node_id, dest_node_id, k_min, k_max, search_direction, condition, max_size, query_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_path_for_studio(db_name, src_node_id, dest_node_id, k_min, k_max, search_direction, condition, max_size, query_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_path_with_prop_filter(self, db_name, start_node, edge, end_node, search_direction, k_min, k_max, distinct, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_path_with_prop_filter(db_name, start_node, edge, end_node, search_direction, k_min, k_max, distinct, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_pearson_similarity(self, db_name, A, B, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_pearson_similarity(db_name, A, B)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_prop_cluster(self, db_name, node_list, edge_list, type_prop, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_prop_cluster(db_name, node_list, edge_list, type_prop)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_random_walk_sub(self, db_name, node_id, length, num_walks, p, q, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_random_walk_sub(db_name, node_id, length, num_walks, p, q, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_scc(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_scc(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_shortest_path(self, db_name, a_node_id, b_node_id, condition, k_max, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_shortest_path(db_name, a_node_id, b_node_id, condition, k_max, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_shortest_path_limit(self, db_name, a_node_id, b_node_id, condition, k_max, search_direction, limit, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_shortest_path_limit(db_name, a_node_id, b_node_id, condition, k_max, search_direction, limit)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_shortest_path_limit_v2(self, db_name, a_node_id, b_node_id, condition, k_max, search_direction, limit, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_shortest_path_limit_v2(db_name, a_node_id, b_node_id, condition, k_max, search_direction, limit)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_simple_neighbour(self, db_name, node_id, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_simple_neighbour(db_name, node_id, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_simple_neighbour_limit(self, db_name, node_id, k_min, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_simple_neighbour_limit(db_name, node_id, k_min, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_simple_path(self, db_name, src_node_id, dest_node_id, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_simple_path(db_name, src_node_id, dest_node_id, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_single_source_shortest_path_unweighted(self, db_name, node_id, node_type_set, edge_type_set, k_min, k_max, search_direction, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_single_source_shortest_path_unweighted(db_name, node_id, node_type_set, edge_type_set, k_min, k_max, search_direction, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_slpa(self, db_name, node_type_set, edge_type_set, threshold, max_iter, output_limit, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_slpa(db_name, node_type_set, edge_type_set, threshold, max_iter, output_limit)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_standard_difference_neighbour(self, db_name, A, B, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_standard_difference_neighbour(db_name, A, B, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_by_neighbour_for_studio(self, db_name, node_id, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_by_neighbour_for_studio(db_name, node_id, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_by_node_for_studio(self, db_name, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_by_node_for_studio(db_name, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_with_neighbour(self, db_name, node_id, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_with_neighbour(db_name, node_id, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_with_neighbour_limit(self, db_name, node_id, k_min, k_max, search_direction, condition, max_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_with_neighbour_limit(db_name, node_id, k_min, k_max, search_direction, condition, max_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_with_node(self, db_name, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_with_node(db_name, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_with_node_neighbour(self, db_name, ids, search_direction, k, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_with_node_neighbour(db_name, ids, search_direction, k)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_subgraph_with_type(self, db_name, node_type_list, edge_type_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_subgraph_with_type(db_name, node_type_list, edge_type_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_total_neighbour(self, db_name, ids, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_total_neighbour(db_name, ids, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_triangle_count(self, db_name, node_type_set, edge_type_set, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_triangle_count(db_name, node_type_set, edge_type_set)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_union_neighbour(self, db_name, ids, k_min, k_max, search_direction, condition, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_union_neighbour(db_name, ids, k_min, k_max, search_direction, condition)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def query_wcc(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_algorithm.query_wcc(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret



    # pyezoo.gen.ezooapi_auth.Iface

    def auth(self, username, password, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.auth(username, password)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def cancel_grant_roles(self, username, graph, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.cancel_grant_roles(username, graph)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def change_password(self, old_password, password, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.change_password(old_password, password)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def check_is_need_auth(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.check_is_need_auth()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_user(self, username, password, graph, roles, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.create_user(username, password, graph, roles)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_user(self, username, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.drop_user(username)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def grant_roles(self, username, graph, roles, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.grant_roles(username, graph, roles)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def reset_password(self, username, password, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.reset_password(username, password)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def view_all_users(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.view_all_users()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def view_roles(self, username, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.view_roles(username)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def view_users(self, graph, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_auth.view_users(graph)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret



    # pyezoo.gen.ezooapi_base.Iface

    def close_graph(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.close_graph(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def copy_graph(self, src_graph_name, dst_graph_name, readonly, auto_load, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.copy_graph(src_graph_name, dst_graph_name, readonly, auto_load)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.create(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_by_json(self, db_name, schema_json, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.create_by_json(db_name, schema_json)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.drop(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def export_graph(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.export_graph(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_active_graph_list(self, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_active_graph_list(parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_client_details(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_client_details()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_list(self, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_graph_list(parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_schema_list(self, db_name_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_graph_schema_list(db_name_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_server_infos(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_server_infos()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_status(self, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.get_status(parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def gnn_infer(self, file_id, db_name, gnn_typ, input_params, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.gnn_infer(file_id, db_name, gnn_typ, input_params)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def gnn_list_resources(self, directory, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.gnn_list_resources(directory)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def gnn_upload_resources(self, file_id, content, option, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.gnn_upload_resources(file_id, content, option)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def hello(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.hello()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def invoke_python(self, db_name, py_path, py_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.invoke_python(db_name, py_path, py_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def open_graph(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.open_graph(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def ping(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_base.ping()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret



    # pyezoo.gen.ezooapi_data.Iface

    def add_edge(self, db_name, edge_type, src_node_index_list, dest_node_index_list, edge_props_list, model, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_edge(db_name, edge_type, src_node_index_list, dest_node_index_list, edge_props_list, model)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_edge_by_id(self, db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_edge_by_id(db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_edge_property(self, db_name, edge_type, name, type, default_value, cache_level, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_edge_property(db_name, edge_type, name, type, default_value, cache_level)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_node(self, db_name, node_type, node_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_node(db_name, node_type, node_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_node_property(self, db_name, node_type, name, type, default_value, cache_level, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_node_property(db_name, node_type, name, type, default_value, cache_level)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_or_update_edge(self, db_name, edge_type, src_node_index_list, dest_node_index_list, edge_props_list, model, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_or_update_edge(db_name, edge_type, src_node_index_list, dest_node_index_list, edge_props_list, model)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_or_update_edge_with_id(self, db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_or_update_edge_with_id(db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add_or_update_node(self, db_name, node_type, node_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.add_or_update_node(db_name, node_type, node_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def commit_transaction(self, db_name, transaction_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.commit_transaction(db_name, transaction_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_edge_index(self, db_name, edge_type, index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.create_edge_index(db_name, edge_type, index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_edge_type(self, db_name, edge_type, indexes, props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.create_edge_type(db_name, edge_type, indexes, props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_node_index(self, db_name, node_type, index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.create_node_index(db_name, node_type, index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_node_type(self, db_name, node_type, indexes, props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.create_node_type(db_name, node_type, indexes, props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def create_single_edge_type(self, db_name, edge_type, indexes, props, single_mode, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.create_single_edge_type(db_name, edge_type, indexes, props, single_mode)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_connected_component_cache(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.drop_connected_component_cache(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_edge_index(self, db_name, edge_type, index_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.drop_edge_index(db_name, edge_type, index_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_edge_type(self, db_name, edge_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.drop_edge_type(db_name, edge_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_node_index(self, db_name, node_type, index_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.drop_node_index(db_name, node_type, index_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drop_node_type(self, db_name, node_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.drop_node_type(db_name, node_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_all_edge(self, db_name, src_node_id, dest_node_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_all_edge(db_name, src_node_id, dest_node_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_basic_graph(self, db_name, src_id, count, src_ids, if_order, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_basic_graph(db_name, src_id, count, src_ids, if_order)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_black_node_id(self, db_name, is_sorted, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_black_node_id(db_name, is_sorted)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_edge(self, db_name, edge_index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_edge(db_name, edge_index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_edge_with_basic_id(self, db_name, edge_basic_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_edge_with_basic_id(db_name, edge_basic_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_edges_with_basic_ids(self, db_name, edge_basic_ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_edges_with_basic_ids(db_name, edge_basic_ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_edges_with_props(self, db_name, type, props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_edges_with_props(db_name, type, props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_all_edge_size(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_graph_all_edge_size(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_all_node_size(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_graph_all_node_size(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_edge_size(self, db_name, edge_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_graph_edge_size(db_name, edge_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_graph_node_size(self, db_name, node_type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_graph_node_size(db_name, node_type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node(self, db_name, node_index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node(db_name, node_index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node_index_by_id(self, db_name, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node_index_by_id(db_name, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node_s_batch(self, db_name, src_id, count, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node_s_batch(db_name, src_id, count)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node_tag_with_ids(self, db_name, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node_tag_with_ids(db_name, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node_tag_with_tags(self, db_name, tags, absolutely_equal, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node_tag_with_tags(db_name, tags, absolutely_equal)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_node_with_id(self, db_name, id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_node_with_id(db_name, id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_degree(self, db_name, type_list, min_degree, max_degree, search_direction, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_degree(db_name, type_list, min_degree, max_degree, search_direction)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_ids(self, db_name, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_ids(db_name, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_prop_range(self, db_name, type, prop_name, min_data, min_inclusive, max_data, max_inclusive, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_prop_range(db_name, type, prop_name, min_data, min_inclusive, max_data, max_inclusive)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_props(self, db_name, type, props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_props(db_name, type, props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_type(self, db_name, type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_type(db_name, type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_nodes_with_type_and_page(self, db_name, type, page_num, page_size, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_nodes_with_type_and_page(db_name, type, page_num, page_size)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def get_rel_graph(self, db_name, src_id, count, src_ids, if_order, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.get_rel_graph(db_name, src_id, count, src_ids, if_order)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def import_edge_from_data(self, db_name, config, table, safe_mode, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.import_edge_from_data(db_name, config, table, safe_mode)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def import_node_from_data(self, db_name, config, table, safe_mode, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.import_node_from_data(db_name, config, table, safe_mode)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def rebuild_adj_table(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.rebuild_adj_table(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def refresh_connected_component_cache(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.refresh_connected_component_cache(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_all_edge(self, db_name, src_node_id, dest_node_id, type, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_all_edge(db_name, src_node_id, dest_node_id, type)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_all_edge_with_node_index(self, db_name, src_node_index_list, dest_node_index_list, type_list, model, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_all_edge_with_node_index(db_name, src_node_index_list, dest_node_index_list, type_list, model)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_edge(self, db_name, edge_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_edge(db_name, edge_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_edge_property(self, db_name, edge_type, name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_edge_property(db_name, edge_type, name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_node(self, db_name, id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_node(db_name, id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_node_property(self, db_name, node_type, name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_node_property(db_name, node_type, name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_node_tag(self, db_name, tags, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_node_tag(db_name, tags)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_node_tag_with_specific(self, db_name, id2tags, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_node_tag_with_specific(db_name, id2tags)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove_nodes(self, db_name, node_index_list, model, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.remove_nodes(db_name, node_index_list, model)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def rollback_transaction(self, db_name, transaction_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.rollback_transaction(db_name, transaction_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def set_node_tag(self, db_name, tag, ids, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.set_node_tag(db_name, tag, ids)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def start_transaction(self, db_name, level, timeout_seconds, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.start_transaction(db_name, level, timeout_seconds)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def stat_graph_global_view(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.stat_graph_global_view(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def stat_inout_degree(self, db_name, search_direction, top_k, is_desc, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.stat_inout_degree(db_name, search_direction, top_k, is_desc)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_edge(self, db_name, edge_index, edge_props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_edge(db_name, edge_index, edge_props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_edge_index(self, db_name, edge_type, index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_edge_index(db_name, edge_type, index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_edge_with_id(self, db_name, edge_id, edge_props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_edge_with_id(db_name, edge_id, edge_props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_edges(self, db_name, edge_index_list, edge_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_edges(db_name, edge_index_list, edge_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_edges_with_ids(self, db_name, edge_id_list, edge_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_edges_with_ids(db_name, edge_id_list, edge_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_graph_schema(self, db_name, parameters, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_graph_schema(db_name, parameters)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_node(self, db_name, node_index, node_props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_node(db_name, node_index, node_props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_node_index(self, db_name, node_type, index, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_node_index(db_name, node_type, index)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_node_with_id(self, db_name, id, node_props, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_node_with_id(db_name, id, node_props)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_nodes(self, db_name, node_index_list, node_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_nodes(db_name, node_index_list, node_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def update_nodes_with_ids(self, db_name, ids, node_props_list, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.update_nodes_with_ids(db_name, ids, node_props_list)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def view_node_tag(self, db_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_data.view_node_tag(db_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret



    # pyezoo.gen.ezooapi_client.Iface

    def QL(self, db_name, query, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.QL(db_name, query)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def add(self, ip, port, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.add(ip, port)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def drain(self, server_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.drain(server_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def dump(self, path, db_name, skips, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.dump(path, db_name, skips)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def init(self, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.init()

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def rebalance_graph(self, graph_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.rebalance_graph(graph_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def remove(self, server_id, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.remove(server_id)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def restore(self, uri, db_name, tmp_path, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.restore(uri, db_name, tmp_path)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret


    def yield_leadership(self, graph_name, retry=True):
        params_map = locals()
        ret = self.cli_ezooapi_client.yield_leadership(graph_name)

        if retry and hasattr(ret, "status") and ret.status == 50 and self._pool:
            func_name = sys._getframe().f_code.co_name
            logger.info("re-invoke function " + func_name)
            self._pool.fresh()
            new_conn = self._pool.connection(self._manage)
            if hasattr(new_conn.client, func_name):
                func = getattr(new_conn.client, func_name)
                func_sig_list = list(inspect.signature(func).parameters)
                params = []
                for param_name in func_sig_list:
                    params.append(params_map[param_name])
                params[-1] = False
                return func(*params)
        return ret

