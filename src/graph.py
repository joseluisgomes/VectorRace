from queue import Queue

import networkx as nx
import matplotlib.pyplot as plt
import math
from node import Node


class Graph:
    def __init__(self, directed=False):
        self.nodes = []  # List of nodes of the graph
        self.is_directed = directed  # If the graph is directed or not
        self.graph = {}  # Dictionary to store the nodes, edges and weights
        self.heuristics = {}  # Dictionary to store the heuristics for each node: informed search

    def add_edge(self, node1, node2, weight):  # node1 & node 2 are the names for each node
        n1 = Node(node1)
        n2 = Node(node2)

        if n1 not in self.nodes:
            self.nodes.append(n1)
            self.graph[node1] = set()
        else:
            n1 = self.get_node_by_name(node1)

        if n2 not in self.nodes:
            self.nodes.append(n2)
            self.graph[node2] = set()
        else:
            n2 = self.get_node_by_name(node2)

        self.graph[node1].add((node2, weight))

        # If the graph is not directed then add the opposite edge
        if not self.is_directed:
            self.graph[node2].add((node1, weight))

    def get_node_by_name(self, name):
        search_node = Node(name)

        for node in self.nodes:
            if node == search_node:
                return node
            else:
                return None

    def print_edges(self):
        listaA = ""
        for nodo in self.graph.keys():
            for (nodo2, cost) in self.graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + " cost: " + str(cost) + "\n"
        return listaA

    def get_edge_cost(self, node1, node2):
        total_cost = math.inf
        node1_edges = self.graph[node1]

        for (node, cost) in node1_edges:
            if node == node2:
                total_cost = cost
        return total_cost

    def calculate_cost(self, path):  # Given a certain path, this function calculates his overall cost
        # Path is a list of the node's name
        aux = path  # Auxiliary variable
        cost = 0
        i = 0
        while i + 1 < len(aux):
            cost = cost + self.get_edge_cost(aux[i], aux[i + 1])
            i = i + 1
        return cost

    def plot(self):  # Plot the graph
        nodes = self.nodes  # Create a list of vertices
        graph = nx.Graph()

        for node in nodes:
            aux_node = node.get_name()  # Auxiliary node
            graph.add_node(aux_node)

            for (neighbour, weight) in self.graph[aux_node]:
                graph.add_edge(aux_node, neighbour, weight=weight)

        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold')

        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def add_heuristic(self, node, estimate):
        n1 = Node(node)
        if n1 in self.nodes:
            self.heuristics[node] = estimate

    # Calculates the straight distance between 2 nodes
    def lowest_cost(self, start, end):  # Greedy com heurística focada no menor custo
        start_node_position = self.node_position(start)
        end_node_position = self.node_position(end)

        keys_slice = list(self.graph)[start_node_position: end_node_position + 1]

        X_visited = list()
        visited_keys = list()
        total_cost = 0

        for index in range(len(keys_slice)):
            key = str(keys_slice.__getitem__(index))
            value = self.graph.get(key)
            keys_list = list(value)

            if visited_keys.__contains__(key):
                key = str(keys_slice.__getitem__(index + 1))
                if key == end:
                    visited_keys.append(key)
                    break

            if len(value) == 1:
                total_cost += keys_list[0][1]
                visited_keys.append(key)
            else:
                for pair in keys_list:
                    pair_to_str = str(pair[0])  # Pair converted to string

                    if not pair_to_str.__contains__('X') and not pair_to_str.__contains__('F'):
                        if not visited_keys.__contains__(pair_to_str):
                            total_cost += pair[1]
                            visited_keys.append(key if not key.__contains__('X') else pair_to_str)

                    else:  # Outers of the circuit
                        if not X_visited.__contains__(pair_to_str):
                            X_neighbours = self.get_neighbours(pair_to_str)

                            for neighbour_pair in X_neighbours:
                                neighbour_pair_str = str(neighbour_pair[0])

                                if not neighbour_pair_str.__contains__('X') and not neighbour_pair_str.__contains__('F'):
                                    if not visited_keys.__contains__(neighbour_pair_str):
                                        total_cost += neighbour_pair[1]
                                        visited_keys.append(neighbour_pair_str)
                                        break
                            X_visited.append(pair_to_str)
        return visited_keys, total_cost

    def node_position(self, node):
        graph_keys = list(self.graph)
        node_position = 0

        for key in graph_keys:
            if key == node:
                return node_position
            node_position += 1

    def get_neighbours(self, node):
        neighbours = []

        for (neighbour, weight) in self.graph[node]:
            neighbours.append((neighbour, weight))
        return neighbours

    def DFS_search(self, start, end, path=None, visited=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        path.append(start)
        visited.add(start)

        if start == end:
            total_cost = self.calculate_cost(path)
            return path, total_cost
        for (neighbour, peso) in self.graph[start]:
            if neighbour not in visited:
                result = self.DFS_search(neighbour, end, path, visited)

                if result is not None:
                    return result
        path.pop()  # If It doesn't find it then remove the one on the path
        return None

    def BFS_search(self, start, end):
        visited = set()  # Define a set of visited nodes in order to avoid loops
        fila = Queue()

        # Add the start node to the queue & the visited set
        fila.put(start)
        visited.add(start)

        # Ensure that the start node is orphan
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found is False:
            current_node = fila.get()
            if current_node == end:
                path_found = True
            else:
                for (neighbour, peso) in self.graph[current_node]:
                    if neighbour not in visited:
                        fila.put(neighbour)
                        parent[neighbour] = current_node
                        visited.add(neighbour)
        # Rebuild the path
        path = []
        if path_found:
            path.append(end)

            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            cost = self.calculate_cost(path)
        return path, cost

    def greedy_search(self, start, end):
        """
            open_list is a set of the visited nodes, but with neighbors
            that have not yet been all visited, It starts with node "start".
            closed_list is a set of the visited nodes and all their neighbors
            that have been visited too.
        """
        open_list = {start}
        closed_list = set([])

        parents = {start: start}  # Dictionary that stores the previous node of a node, starts with the node 'start'

        while len(open_list) > 0:
            node = None

            # Find the node with the lowest heuristic
            for v in open_list:
                if node is None or self.heuristics[v] < self.heuristics[node]:
                    node = v

            if node is None:
                print('Path does not exist!')
                return None

            if node == end:
                """
                    If the current node is the destiny node:
                    Rebuild the path from that node to the initial node ('start'),
                    following the previous one.
                """
                rebuild_path = []
                while parents[node] != node:
                    rebuild_path.append(node)
                    node = parents[node]

                rebuild_path.append(start)
                rebuild_path.reverse()

                return rebuild_path, self.calculate_cost(rebuild_path)

            for (m, weight) in self.get_neighbours(node):  # For all neighbours of the current node
                """
                    If the current node isn't on the open_set and neither on the closed list
                    then add it to the open_set and stamp the previous node. 
                """
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = node

            """ 
                Remove the node from the set "open" and add it to the closed_list
                because all his neighbors have been inspected.
            """
            open_list.remove(node)
            closed_list.add(node)

        print('Path does not exist!')
        return None

    def __str__(self):
        graph = ""
        for key in self.graph.keys():
            graph = graph + "node " + str(key) + ": " + str(self.graph[key]) + "\n"
        return graph
