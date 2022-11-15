def calculate_cost(self, path):  # Given a certain path, this function calculates his overall cost
    # "path" is a list of nodes
    aux = path  # Auxiliary variable
    cost = 0
    i = 0

    while i + 1 < len(aux):
        cost = cost + self.get_arc_cost(aux[i], aux[i + 1])
        i += 1
    return cost


def greedy_search(self, start, end):
    """
        open_list é um conjunto dos nodos visitados, mas com vizinhos
        que ainda não foram todos visitados, começa com o  start.

        closed_list é uma lista de nodos visitados
        e todos os seus vizinhos também já o foram.
    """
    open_list = {start}
    closed_list = set([])

    # Dictionary that stores the previous node of a node, starts with the node 'start'
    parents = {start: start}

    while len(open_list) > 0:
        node = None

        # Find the node with the lowest heuristic
        for visited_node in open_list:
            if node is None or self.m_h[visited_node] < self.m_h[node]:
                node = visited_node

        if node is None:
            print('Path does not exist!')
            return None

        # se o nodo corrente é o destino
        # reconstruir o caminho a partir desse nodo até ao start
        # seguindo o antecessor
        if node == end:
            reconst_path = []

            while parents[node] != node:
                reconst_path.append(node)
                node = parents[node]

            reconst_path.append(start)

            reconst_path.reverse()

            return reconst_path, self.calcula_custo(reconst_path)

        # para todos os vizinhos  do nodo corrente
        for (m, weight) in self.getNeighbours(node):
            # Se o nodo corrente nao esta na open nem na closed list
            # adiciona-lo à open_list e marcar o antecessor
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = node

        # remover n da open_list e adiciona-lo à closed_list
        # porque todos os seus vizinhos foram inspecionados
        open_list.remove(node)
        closed_list.add(node)

    print('Path does not exist!')
    return None
