from pyezoo.gen.ezooapi_algorithm import *
from pyezoo.gen.ezooapi_auth import *
from pyezoo.gen.ezooapi_base import *
from pyezoo.gen.ezooapi_data import *
from thrift.protocol import TMultiplexedProtocol

AUTH = "ezooapi_auth"
ALGORITHM = "ezooapi_algorithm"
BASE = "ezooapi_base"
DATA = "ezooapi_data"


class ezoodb_client(ezooapi_auth.Iface,
                    ezooapi_base.Iface,
                    ezooapi_data.Iface,
                    ezooapi_algorithm.Iface):

    def __init__(self, iprot):
        auth_protocol = TMultiplexedProtocol.TMultiplexedProtocol(iprot, AUTH)
        self.auth_client = ezooapi_auth.Client(auth_protocol)

        base_protocol = TMultiplexedProtocol.TMultiplexedProtocol(iprot, BASE)
        self.base_client = ezooapi_base.Client(base_protocol)

        data_protocol = TMultiplexedProtocol.TMultiplexedProtocol(iprot, DATA)
        self.data_client = ezooapi_data.Client(data_protocol)

        algo_protocol = TMultiplexedProtocol.TMultiplexedProtocol(iprot, ALGORITHM)
        self.algorithm_client = ezooapi_algorithm.Client(algo_protocol)

    # auth
    def auth(self, username, password):
        return self.auth_client.auth(username, password)

    def create_user(self, username, password, graph, roles):
        return self.auth_client.create_user(username, password, graph, roles)

    def drop_user(self, username):
        return self.auth_client.drop_user(username)

    def change_password(self, username, old_password, password):
        return self.auth_client.change_password(username, old_password, password)

    def reset_password(self, username, password):
        return self.auth_client.reset_password(username, password)

    def grant_roles(self, username, graph, roles):
        return self.auth_client.grant_roles(username, graph, roles)

    def cancel_grant_roles(self, username, graph):
        return self.auth_client.cancel_grant_roles(username, graph)

    def view_roles(self, username):
        return self.auth_client.view_roles(username)

    def view_users(self, graph):
        return self.auth_client.view_users(graph)

    # base
    def ping(self):
        return self.base_client.ping()

    def hello(self):
        return self.base_client.hello()

    def create(self, db_name, parameters):
        return self.base_client.create(db_name, parameters)

    def drop(self, db_name, parameters):
        return self.base_client.drop(db_name, parameters)

    def export_graph(self, db_name, parameters):
        return self.base_client.export_graph(db_name, parameters)

    def open_graph(self, db_name, parameters):
        return self.base_client.open_graph(db_name, parameters)

    def close_graph(self, db_name, parameters):
        return self.base_client.close_graph(db_name, parameters)

    def reload_graph(self, db_name, parameters):
        return self.base_client.reload_graph(db_name, parameters)

    def get_status(self, parameters):
        return self.base_client.get_status(parameters)

    def get_graph_list(self, parameters):
        return self.base_client.get_graph_list(parameters)

    def get_active_graph_list(self, parameters):
        return self.base_client.get_active_graph_list(parameters)

    def create_graph(self, db_name, schema_path, import_conf_path):
        return self.base_client.create_graph(db_name, schema_path, import_conf_path)

    # data
    def get_graph_schema_list(self, db_name_list):
        return self.data_client.get_graph_schema_list(db_name_list)

    def add_node(self, db_name, node_type, node_props_list):
        return self.data_client.add_node(db_name, node_type, node_props_list)

    def remove_node(self, db_name, id):
        return self.data_client.remove_node(db_name, id)

    def update_node(self, db_name, id, node_props):
        return self.data_client.update_node(db_name, id, node_props)

    def get_node(self, db_name, node_id):
        return self.data_client.get_node(db_name, node_id)

    def get_node_with_id(self, db_name, id):
        return self.data_client.get_node_with_id(db_name, id)

    def get_graph_all_node_size(self, db_name):
        return self.data_client.get_graph_all_node_size(db_name)

    def get_graph_node_size(self, db_name, node_type):
        return self.data_client.get_graph_node_size(db_name, node_type)

    def add_node_property(self, db_name, node_type, name, type, default_value, cache_level):
        return self.data_client.add_node_property(db_name, node_type, name, type, default_value, cache_level)

    def remove_node_property(self, db_name, node_type, name):
        return self.data_client.remove_node_property(db_name, node_type, name)

    def add_edge(self, db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list):
        return self.data_client.add_edge(db_name, edge_type, src_node_id_list, dest_node_id_list, edge_props_list)

    def remove_edge(self, db_name, edge_id):
        return self.data_client.remove_edge(db_name, edge_id)

    def remove_all_edge(self, db_name, src_node_id, dest_node_id, type):
        return self.data_client.remove_all_edge(db_name, src_node_id, dest_node_id, type)

    def update_edge(self, db_name, edge_id, edge_props):
        return self.data_client.update_edge(db_name, edge_id, edge_props)

    def get_edge(self, db_name, edge_id):
        return self.data_client.get_edge(db_name, edge_id)

    def get_edge_with_basic_id(self, db_name, edge_basic_id):
        return self.data_client.get_edge_with_basic_id(db_name, edge_basic_id)

    def get_all_edge(self, db_name, src_node_id, dest_node_id):
        return self.data_client.get_all_edge(db_name, src_node_id, dest_node_id)

    def get_graph_all_edge_size(self, db_name):
        return self.data_client.get_graph_all_edge_size(db_name)

    def get_graph_edge_size(self, db_name, edge_type):
        return self.data_client.get_graph_edge_size(db_name, edge_type)

    def add_edge_property(self, db_name, edge_type, name, type, default_value, cache_level):
        return self.data_client.add_edge_property(db_name, edge_type, name, type, default_value, cache_level)

    def remove_edge_property(self, db_name, edge_type, name):
        return self.data_client.remove_edge_property(db_name, edge_type, name)

    def get_node_s_batch(self, db_name, src_id, count):
        return self.data_client.get_node_s_batch(db_name, src_id, count)

    def get_adj_table(self, db_name, src_id, count):
        return self.data_client.get_adj_table(db_name, src_id, count)

    def create_node_type(self, db_name, node_type, indexes, props):
        return self.data_client.create_node_type(db_name, node_type, indexes, props)

    def create_edge_type(self, db_name, edge_type, indexes, props):
        return self.data_client.create_edge_type(db_name, edge_type, indexes, props)

    def drop_node_type(self, db_name, node_type):
        return self.data_client.drop_node_type(db_name, node_type)

    def drop_edge_type(self, db_name, edge_type):
        return self.data_client.drop_edge_type(db_name, edge_type)

    def import_node_from_file(self, db_name, node_type, props, path, file_type):
        return self.data_client.import_node_from_file(db_name, node_type, props, path, file_type)

    def import_edge_from_file(self, db_name, edge_type, props, path, file_type, start_node, end_node):
        return self.data_client.import_edge_from_file(db_name, edge_type, props, path, file_type, start_node, end_node)

    # algo
    def query_neighbour_limit(self, db_name, node_id, k_min, k_max, condition, is_return_path, search_direction,
                              max_size):
        return self.algorithm_client.query_neighbour_limit(db_name, node_id, k_min, k_max, condition, is_return_path,
                                                           search_direction,
                                                           max_size)

    def query_neighbour_count(self, db_name, node_id, k_min, k_max, condition, search_direction):
        return self.algorithm_client.query_neighbour_count(db_name, node_id, k_min, k_max, condition, search_direction)

    def query_common_neighbour(self, db_name, node_ids, k_min, k_max, condition, search_direction):
        return self.algorithm_client.query_common_neighbour(db_name, node_ids, k_min, k_max, condition,
                                                            search_direction)

    def query_dijkstra(self, db_name, a_node_id, b_node_id, condition, search_direction, edge_type, edge_prop):
        return self.algorithm_client.query_dijkstra(db_name, a_node_id, b_node_id, condition, search_direction,
                                                    edge_type,
                                                    edge_prop)

    def query_pagerank(self, db_name, damping_factor, epoch_limit, max_convergence_error, vertex_init_value):
        return self.algorithm_client.query_pagerank(db_name, damping_factor, epoch_limit, max_convergence_error,
                                                    vertex_init_value)

    def query_shortest_path(self, db_name, a_node_id, b_node_id, condition, k_max, search_direction):
        return self.algorithm_client.query_shortest_path(db_name, a_node_id, b_node_id, condition, k_max,
                                                         search_direction)

    def query_betcentrality(self, db_name, search_direction, hop):
        return self.algorithm_client.query_betcentrality(db_name, search_direction, hop)

    def query_clocentrality(self, db_name, if_WF, hop):
        return self.algorithm_client.query_clocentrality(db_name, if_WF, hop)

    def query_louvain(self, db_name, edge_type, edge_props_name):
        return self.algorithm_client.query_louvain(db_name, edge_type, edge_props_name)

    def query_one_neighbour(self, db_name, node_id, search_direction):
        return self.algorithm_client.query_one_neighbour(db_name, node_id, search_direction)

    def query_neighbour(self, db_name, node_id, k_min, k_max, search_direction, condition):
        return self.algorithm_client.query_neighbour(db_name, node_id, k_min, k_max, search_direction, condition)

    def query_neighbour_path(self, db_name, search_direction, condition, nodes):
        return self.algorithm_client.query_neighbour_path(db_name, search_direction, condition, nodes)

    def query_subgraph(self, db_name, node_id, k_min, k_max, search_direction, condition):
        return self.algorithm_client.query_subgraph(db_name, node_id, k_min, k_max, search_direction, condition)

    def query_path(self, db_name, src_node_id, dest_node_id, k_max, search_direction, condition, max_size):
        return self.algorithm_client.query_path(db_name, src_node_id, dest_node_id, k_max, search_direction, condition,
                                                max_size)
