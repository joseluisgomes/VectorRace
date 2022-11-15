from queue import Queue


def calculate_cost(self, path):  # Given a certain path, this function calculates his overall cost
    # "path" is a list of nodes
    aux = path  # Auxiliary variable
    cost = 0
    i = 0

    while i + 1 < len(aux):
        cost = cost + self.get_arc_cost(aux[i], aux[i + 1])
        i += 1
    return cost


def BFS_search(self, start, end):  # Breadth-First search
    visited = set()  # Define a set of the visited nodes in order to avoid loops
    queue = Queue()

    # Add the start node the initial queue & the visited set
    queue.put(start)
    visited.add(start)

    parent = dict()  # Ensure that the start node is orphan
    parent[start] = None

    path_found = False
    while not queue.empty() and path_found == False:
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
        cost = calculate_cost(path)
    return path, cost


def DFS_search(self, start, end, path=None, visited=None):  # Depth-First Search
    if path is None:
        path = []
    if visited is None:
        visited = set()

    path.append(start)
    visited.add(start)

    if start == end:  # Stop condition
        total_cost = calculate_cost(path)
        return path, total_cost

    for (neighbour, weight) in self.m_graph[start]:
        if neighbour not in visited:
            result = self.DFS_search(neighbour, end, path, visited)
            if result is not None:
                return result

    path.pop()  # If It doesn't find it then remove whose on the path
    return None
