from queue import Queue
from node import Node
import networkx as nx
import matplotlib.pyplot as plt
import math


class Graph:
    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}  # Dictionary to store the nodes and edges
        self.m_heuristics = {}  # Dictionary to store the heuristics for each node: informed search

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
            else:
                return None

    def print_edge(self):
        edge_attributes = ""
        lista = self.m_graph.keys()

        for nodo in lista:
            for (node, cost) in self.m_graph[nodo]:
                edge_attributes = edge_attributes + nodo + " ->" + node + " cost:" + str(cost) + "\n"
        return edge_attributes

    def add_edge(self, node1, node2, weight):  # Add an edge to the graph
        n1 = Node(node1)
        n2 = Node(node2)

        if n1 not in self.m_nodes:
            self.m_nodes.append(n1)
            self.m_graph[node1] = list()
        else:
            n1 = self.get_node_by_name(node1)

        if n2 not in self.m_nodes:
            self.m_nodes.append(n2)
            self.m_graph[node2] = list()
        else:
            n2 = self.get_node_by_name(node2)

        self.m_graph[node1].append((node2, weight))

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    def get_nodes(self):  # Gel all nodes of the graph
        return self.m_nodes

    def get_arc_cost(self, node1, node2):  # Get the edge cost
        total_cost = math.inf
        a = self.m_graph[node1]  # List of edges for that node

        for (nodo, cost) in a:
            if nodo == node2:
                total_cost = cost
        return total_cost

    def calculate_cost(self, path):  # Given a certain path, this function calculates his overall cost
        # "path" is a list of nodes
        aux = path  # Auxiliary variable
        cost = 0
        i = 0

        while i + 1 < len(aux):
            cost = cost + self.get_arc_cost(aux[i], aux[i + 1])
            i += 1
        return cost

    def get_neighbours(self, nodo):  # Returns the neighbours of the given node
        lista = []
        for (neighbor, peso) in self.m_graph[nodo]:
            lista.append((neighbor, peso))
        return lista

    def plot(self):  # Plot the graph
        lista_v = self.m_nodes  # Create a list of vertices
        graph = nx.Graph()

        for nodo in lista_v:
            n = nodo.set_name()
            graph.add_node(n)
            for (neighbour, peso) in self.m_graph[n]:
                lista = (n, neighbour)
                # lista_a.append(lista)
                graph.add_edge(n, neighbour, weight=peso)

        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def add_heuristic(self, node, estimate):  # Defines the heuristic for each node
        n1 = Node(node)
        if n1 in self.m_nodes:
            self.m_heuristics[node] = estimate

    def heuristic(self):
        nodes = self.m_graph.keys
        for node in nodes:
            self.m_heuristics[node] = 1  # Define the heuristic for each node (Default value: 1)
        return True

    def calculate_estimate(self, estimate):
        estimate_keys_list = list(estimate.keys())
        min_estimate = estimate[estimate_keys_list[0]]
        node = estimate_keys_list[0]

        for key, value in estimate.items():
            if value < min_estimate:
                min_estimate = value
                node = key
        return node

    def get_heuristic(self, node):  # Returns the node's heuristic
        if node not in self.m_heuristics.keys():
            return 1000
        else:
            return self.m_heuristics[node]

    def DFS_search(self, start, end, path=None, visited=None):  # Depth-First Search
        if path is None:
            path = []
        if visited is None:
            visited = set()

        path.append(start)
        visited.add(start)

        if start == end:  # Stop condition
            total_cost = self.calculate_cost(path)
            return path, total_cost

        for (neighbour, weight) in self.m_graph[start]:
            if neighbour not in visited:
                result = self.DFS_search(neighbour, end, path, visited)
                if result is not None:
                    return result

        path.pop()  # If It doesn't find it then remove whose on the path
        return None

    def BFS_search(self, start, end):  # Breadth-First search
        visited = set()  # Define a set of the visited nodes in order to avoid loops
        queue = Queue()

        # Add the start node the initial queue & the visited set
        queue.put(start)
        visited.add(start)

        parent = dict()  # Ensure that the start node is orphan
        parent[start] = None

        path_found = False
        while not queue.empty() and path_found is False:
            actual_node = queue.get()

            if actual_node == end:
                path_found = True
            else:
                for (neighbour, weight) in self.m_graph[actual_node]:
                    if neighbour not in visited:
                        queue.put(neighbour)
                        parent[neighbour] = actual_node
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
        open_set = {start}
        closed_list = set([])
        parents = {start: start}  # Dictionary that stores the previous node of a node, starts with the node 'start'

        while len(open_set) > 0:
            node = None

            # Find the node with the lowest heuristic
            for visited_node in open_set:
                if node is None or self.m_heuristics[visited_node] < self.m_heuristics[node]:
                    node = visited_node

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

            for (neighbor, weight) in self.get_neighbours(node):  # For all neighbours of the current node
                """
                    If the current node isn't on the open_set and neither on the closed list
                    then add it to the open_set and stamp the previous node. 
                """
                if neighbor not in open_set and neighbor not in closed_list:
                    open_set.add(neighbor)
                    parents[neighbor] = node

            """
                Remove the node from the set "open" and add it to the closed_list
                because all his neighbors have been inspected.
            """
            open_set.remove(node)
            closed_list.add(node)

        print('Path does not exist!')
        return None

    def A_star_search(self, start, end):
        """
            open_set is a set of nodes which have been visited, but who's neighbors
            haven't all been inspected, starts off with the start node.

            closed_set is a set of nodes which have been visited and who's neighbors
            have been inspected.
        """
        open_set = {start}
        closed_set = set([])

        """
            node_distances contains current distances from start_node to all other nodes.
            The default value (if it's not found in the map) is + infinity.
        """
        node_distances = {start: 0}
        parents = {start: start}  # Parents contain an adjacency map of all nodes
        node = None

        while len(open_set) > 0:
            # Find a node with the lowest value of f() - evaluation function
            calculate_heuristic = {}
            flag = 0

            for neighbor in open_set:
                if node is None:
                    node = neighbor
                else:
                    flag = 1
                    calculate_heuristic[neighbor] = node_distances[neighbor] + self.get_heuristic(neighbor)
            if flag == 1:
                minimum_estimate = self.calculate_estimate(calculate_heuristic)
                node = minimum_estimate
            if node is None:
                print('Path does not exist!')
                return None

            """
                If the current node is the stop_node then
                whe begin the rebuild of the path from it til the start_node.
            """
            if node == end:
                rebuild_path = []

                while parents[node] != node:
                    rebuild_path.append(node)
                    node = parents[node]

                rebuild_path.append(start)
                rebuild_path.reverse()

                # print('Path found: {}'.format(reconst_path))
                return rebuild_path, self.calculate_cost(rebuild_path)

            # For all neighbors of the current node do
            for (neighbor, weight) in self.get_neighbours(node):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.add(neighbor)
                    parents[neighbor] = node
                    node_distances[neighbor] = node_distances[node] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if node_distances[neighbor] > node_distances[node] + weight:
                        node_distances[neighbor] = node_distances[node] + weight
                        parents[neighbor] = node

                        if neighbor in closed_set:
                            closed_set.remove(neighbor)
                            open_set.add(neighbor)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_set.remove(node)
            closed_set.add(node)

        print('Path does not exist!')
        return None

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
            return out
