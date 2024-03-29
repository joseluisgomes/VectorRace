from queue import Queue

import matplotlib.pyplot as plt
import networkx as nx
import math


class Graph:
    def __init__(self, directed=False):
        self.nodes = []  # List of nodes of the graph
        self.is_directed = directed  # If the graph is directed or not
        self.graph = {}  # Dictionary to store the nodes, edges and weights
        self.heuristics = {}  # Dictionary to store the heuristics for each node: informed search

    def add_edge(self, node1, node2, costs):  # node1 & node 2 are the names for each node
        node1_name = node1.__str__()
        node2_name = node2.__str__()

        if node1 not in self.nodes:
            self.nodes.append(node1)
            self.graph[node1_name] = set()
        else:
            n1 = self.get_node(node1)

        node_1_weight = costs[node1.get_line()][node1.get_column()]
        self.add_heuristic(node1, node_1_weight)

        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[node2_name] = set()
        else:
            n2 = self.get_node(node2)

        node_2_weight = costs[node2.get_line()][node2.get_column()]
        self.add_heuristic(node2, node_2_weight)

        self.graph[node1_name].add((node2, node_2_weight))
        if not self.is_directed:  # If the graph is not directed then add the opposite edge
            self.graph[node2_name].add((node1, node_1_weight))

    def print_edges(self):
        edges = ""
        for node in self.graph.keys():
            for pair in self.graph[node]:
                edges += f"{node} -> neighbour: ({pair[0]}), cost: {pair[1]}\n"
        return edges

    def print_nodes(self):
        nodes = ""
        for node in self.nodes:
            nodes += f"{node.__str__()}\n"

        return nodes

    def get_node(self, search_node):
        for node in self.nodes:
            if node.__eq__(search_node):
                return node
        return None

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.__str__() == name:
                return node
        return None

    def get_node_heuristics(self, target_node):
        for node in self.heuristics.keys():
            if node.__eq__(target_node):
                return self.heuristics[target_node]
        return None

    def get_edge_cost(self, node1, node2):
        total_cost = math.inf
        node1_edges = self.graph[node1]
        target_node = self.get_node_by_name(node2)

        for (neighbour, cost) in node1_edges:
            if neighbour.__eq__(target_node):
                total_cost = cost
        return total_cost

    def calculate_cost(self, path):  # Given a certain path, this function calculates his overall cost
        total_cost = 0
        i = 0

        while i + 1 < len(path):
            total_cost += self.get_edge_cost(path[i], path[i + 1])
            i = i + 1
        return total_cost

    def calculate_estimate(self, heuristics):
        keys = list(heuristics.keys())
        min_estimate = heuristics[keys[0]]
        node = keys[0]

        for key, value in heuristics.items():
            if value < min_estimate:
                min_estimate = value
                node = key
        return node

    def plot(self):  # Plot the graph
        nodes = self.nodes  # Create a list of vertices
        graph = nx.Graph()

        for node in nodes:
            node_name = node.__str__()  # Auxiliary node
            graph.add_node(node_name)

            for (neighbour, weight) in self.graph[node_name]:
                graph.add_edge(node_name, neighbour, weight=weight)

        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold')

        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def add_heuristic(self, node, estimate):
        if node in self.nodes:
            self.heuristics[node] = estimate

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
            neighbours.append((neighbour.__str__(), weight))
        return neighbours

    def get_closest_neighbour(self, node, destiny):  # Get the node's neighbour of his right
        column = 0
        right_neighbour = None

        for (neighbour, cost) in self.graph[node]:  # Loop through all the node's neighbours
            if cost < 25 and column < neighbour.get_column():  # Avoiding 'X'
                target = self.get_node_by_name(neighbour.__str__())

                if target.get_label() == 'F':
                    if target.__str__() == destiny:
                        right_neighbour = target.__str__()
                        return right_neighbour  # Destiny node founded => no more iterations are needed
                else:
                    column = neighbour.get_column()
                    right_neighbour = neighbour.__str__()
        return right_neighbour

    def DFS_search(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            total_cost = self.calculate_cost(path)
            return path, total_cost

        neighbour = self.get_closest_neighbour(start, end)

        if neighbour not in visited:
            result = self.DFS_search(neighbour, end, path, visited)
            if result is not None:
                return result
        path.pop()  # If It doesn't find it then remove the one on the path
        return None

    def BFS_search(self, start, end):
        visited = set()  # Define a set of visited nodes in order to avoid loops
        queue = Queue()

        # Add the start node to the queue & the visited set
        queue.put(start)
        visited.add(start)

        # Ensure that the start node is orphan
        parent = dict()
        parent[start] = None

        path_found = False
        while not queue.empty() and path_found is False:
            current_node = queue.get()

            if current_node == end:
                path_found = True
            else:
                column = 0
                for (neighbour, weight) in self.graph[current_node]:
                    neighbour_str = neighbour.__str__()

                    if neighbour_str not in visited:
                        if weight < 25 and column < neighbour.get_column():  # Avoiding X
                            target = self.get_node_by_name(neighbour_str)

                            if target.get_label() == 'F':
                                if target.__str__() == end:
                                    queue.put(neighbour_str)
                                    parent[neighbour_str] = current_node
                                    visited.add(neighbour_str)
                                    break  # Destiny node founded => no more iterations are needed
                            else:
                                column = neighbour.get_column()
                                queue.put(neighbour_str)
                                parent[neighbour_str] = current_node
                                visited.add(neighbour_str)

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
            node_str = None

            # Find the node with the lowest heuristic
            for visited_node_str in open_list:
                visited_node = self.get_node_by_name(visited_node_str)
                node = self.get_node_by_name(node_str)

                if node_str is None or self.heuristics[visited_node] < self.heuristics[node]:
                    node_str = visited_node_str

            if node_str is None:
                print('Path does not exist!')
                return None

            if node_str == end:
                """
                    If the current node is the destiny node:
                    Rebuild the path from that node to the initial node ('start'),
                    following the previous one.
                """
                rebuild_path = []
                while parents[node_str] != node_str:
                    rebuild_path.append(node_str)
                    node_str = parents[node_str]

                rebuild_path.append(start)
                rebuild_path.reverse()

                return rebuild_path, self.calculate_cost(rebuild_path)

            column = 0
            for (neighbour, weight) in self.get_neighbours(node_str):  # For all neighbours of the current node
                """
                    If the current node isn't on the open_set and neither on the closed list
                    then add it to the open_set and stamp the previous node. 
                """
                if neighbour not in open_list and neighbour not in closed_list:
                    target = self.get_node_by_name(neighbour)

                    if weight < 25 and column < target.get_column():  # Avoiding X
                        if target.get_label() == 'F':
                            if target.__str__() == end:
                                open_list.add(neighbour)
                                parents[neighbour] = node_str
                                break  # Destiny node founded => no more iterations are needed
                        else:
                            column = target.get_column()
                            open_list.add(neighbour)
                            parents[neighbour] = node_str
            """ 
                Remove the node from the set "open" and add it to the closed_list
                because all his neighbors have been inspected.
            """
            open_list.remove(node_str)
            closed_list.add(node_str)

        print('Path does not exist!')
        return None

    def A_star_search(self, start, end):
        """
            open_list is a list of nodes which have been visited, but who's neighbors
            haven't all been inspected, starts off with the start node
            closed_list is a list of nodes which have been visited
            and who's neighbors have been inspected .
        """
        open_list = {start}
        closed_list = set([])

        """ 
            g contains current distances from start_node to all other nodes
            the default value (if it's not found in the map) is +infinity 
        """
        g = {start: 0}
        parents = {start: start}  # Parents contains an adjacency map of all nodes
        node_str = None

        while len(open_list) > 0:
            calculate_heuristics = {}  # Find a node with the lowest value of f() - evaluation function
            flag = 0

            for visited_node_str in open_list:
                if node_str is None:
                    node_str = visited_node_str
                else:
                    flag = 1
                    visited_node = self.get_node_by_name(visited_node_str)
                    calculate_heuristics[visited_node_str] = g[visited_node_str] + \
                                                             self.get_node_heuristics(visited_node)

            if flag == 1:
                min_estimate = self.calculate_estimate(calculate_heuristics)
                node_str = min_estimate
            if node_str is None:
                print('Path does not exist!')
                return None

            """
                If the current node is the stop_node
                then we rebuild the path from it to the start_node
            """
            if node_str == end:
                rebuild_path = []

                while parents[node_str] != node_str:
                    rebuild_path.append(node_str)
                    node_str = parents[node_str]

                rebuild_path.append(start)
                rebuild_path.reverse()
                return rebuild_path, self.calculate_cost(rebuild_path)

            column = 0
            for (neighbour, weight) in self.get_neighbours(node_str):  # For all neighbors of the current node do
                """ 
                    if the current node isn't in both open_list and closed_list
                    add it to open_list and note n as it's parent 
                """
                if neighbour not in open_list and neighbour not in closed_list:
                    target = self.get_node_by_name(neighbour)

                    if weight < 25 and column < target.get_column():  # Avoiding X
                        if target.get_label() == 'F':
                            if target.__str__() == end:
                                open_list.add(neighbour)
                                parents[neighbour] = node_str
                                g[neighbour] = g[node_str] + weight
                                break  # Destiny node founded => no more iterations are needed
                        else:
                            column = target.get_column()
                            open_list.add(neighbour)
                            parents[neighbour] = node_str
                            g[neighbour] = g[node_str] + weight

                    """
                        otherwise, check if it's quicker to first visit n, then m
                        and if it is, update parent data and g data
                        and if the node was in the closed_list, move it to open_list
                    """
                else:
                    if g[neighbour] > g[node_str] + weight:
                        g[neighbour] = g[node_str] + weight
                        parents[neighbour] = node_str

                        if neighbour in closed_list:
                            closed_list.remove(neighbour)
                            open_list.add(neighbour)

            """
                Remove n from the open_list, and add it to closed_list
                because all of his neighbors were inspected
            """
            open_list.remove(node_str)
            closed_list.add(node_str)

        print('Path does not exist!')
        return None

    def __str__(self):
        graph = ""
        for key in self.graph.keys():
            graph = graph + "node " + str(key) + ": " + str(self.graph[key]) + "\n"
        return graph
