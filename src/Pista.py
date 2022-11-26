import math
import numpy as np
import sys

import networkx as nx
# Biblioteca de tratamento de grafos necessária para desenhar graficamente o grafo
import matplotlib.pyplot as plt
from node import Node

sys.setrecursionlimit(1000000)


class pista:

    def __init__(self, directed=True):
        self.nodes = []  # lista de nodos(classe) do grafo
        self.directed = directed  # se o grafo é direcionado ou nao
        self.graph = {}  # dicionario para armazenar os nodos, arestas e pesos
        self.heuristica = {}  # dicionário para armazenar heuristica para cada nodo

    def __str__(self):
        out = ""
        for key in self.graph.keys():
            out = out + "node " + str(key) + ": " + str(self.graph[key]) + "\n"
        return out

    ###
    # funcao para ler o circuito e guardar em listas
    ###
    def get_pista(self):
        file_name = "circuito.txt"
        array2Dpista = []

        with open(file_name, "r") as file_reader:
            # Ler caracter 1 a 1
            # Se "X" -> parede, "-" -> Percurso. "P" -> Partida, "F" -> Final

            for line in file_reader.readlines():
                array2Dpista.append(line.strip().split(' '))

            print(np.matrix(array2Dpista))
            print("\n")

        return array2Dpista

    #
    # funcao para obter print do circuito com pesos
    #
    def get_pistaCusto(self):
        file_name = "circuito.txt"
        array2Dpista = []

        with open(file_name, "r") as file_reader:
            # Ler caracter 1 a 1
            # Se "X" -> parede, "-" -> Percurso. "P" -> Partida, "F" -> Final

            for line in file_reader:
                for word in line:
                    if word == 'X':
                        word = 25
                    elif word == 'P':
                        word = 0
                    elif word == '-':
                        word = 1
                    elif word == 'F':
                        word = 10

                    print(word, end=' ')

        print("\n")
        return array2Dpista

    #
    # funcao para adicionar arestas ao grafo da pista
    #
    def criaGraphPista(self, array_pista, p):

        for linha in range(7):  # range(7 linhas)
            for coluna in range(9):  # range(9 colunas)
                node1 = node(array_pista[linha][coluna], linha, coluna)  # cria nodo1
                node2 = node(array_pista[linha][coluna + 1], linha, coluna + 1)  # cria nodo2 (coluna asseguir ao node1)

                p.adicionar_aresta(node1, node2)

        for coluna in range(10):  # range(10 colunas)
            for linha in range(6):  # range(6 linhas)

                node3 = node(array_pista[linha][coluna], linha, coluna)  # cria nodo1
                node4 = node(array_pista[linha + 1][coluna], linha + 1, coluna)  # cria nodo2 (coluna asseguir ao node1)

                p.adicionar_aresta(node3, node4)

        return p

    def adicionar_aresta(self, n1, n2):

        if n1 not in self.nodes:
            self.nodes.append(n1)  # guarda no dicionario "nodes" o nodo criado
            self.graph[n1.getName()] = set()  # guarda no dicionario graph o name do n1
        else:
            nodo1 = self.verificaNodeExiste(n1)

        if n2 not in self.nodes:
            self.nodes.append(n2)  # guarda no dicionario "nodes" o nodo criado
            self.graph[n2.getName()] = set()  # guarda no dicionario graph o name do n2
        else:
            nodo2 = self.verificaNodeExiste(n2)

        n2 = self.setPeso_from_Tipo(n2)  # setPeso pelo Tipo
        self.add_heuristica(n2, n2.getPeso())  # adiciona o valor da heuristica ao nodo

        self.graph[n1.getName()].add((n2.getName(),
                                      n2.getPeso()))  # guarda no dicionario graph o (name, peso) do node asseguir ao n1

        n1 = self.setPeso_from_Tipo(n1)  # setPeso pelo Tipo
        self.add_heuristica(n1, n1.getPeso())  # adiciona o valor da heuristica ao nodo

        if self.directed:  # se o grafo for direcionado
            self.graph[n2.getName()].add((n1.getName(), n1.getPeso()))

        return self.graph

    def setPeso_from_Tipo(self, nodo):

        if nodo.getTipo() == 'X':  # funçao if caso proximo nodo da aresta seja obstaculo
            nodo.setPeso(25)
        elif nodo.getTipo() == 'P':  # funçao if caso proximo nodo da aresta seja Partida
            nodo.setPeso(0)
        elif nodo.getTipo() == 'F':  # funçao if caso proximo nodo da aresta seja Final
            nodo.setPeso(10)
        else:
            nodo.setPeso(1)  # funçao if caso proximo nodo da aresta seja "-"

        return nodo

    # função que dá return da heuristica do nodo
    def getHeuristica(self, h):
        return self.heuristica[h]

    # funçao para adicionar valor da heurisica ao nodo
    def add_heuristica(self, nodo, valor_heuristica):

        if nodo in self.nodes:
            self.heuristica[nodo] = valor_heuristica

        # procura o nodo pela posicao

    def verificaNodeExiste(self, nodo_de_procura):
        for nodo in self.nodes:
            if nodo == nodo_de_procura:
                return nodo
            else:
                return None

    # procura o nodo pela linha e pela coluna
    def getNodebyPosition(self, linha, coluna):
        if linha < 8 and coluna < 10:
            for nodo in self.graph.keys():
                for nodo2 in self.graph[nodo]:
                    if nodo2.getLinha == linha and nodo2.getColuna == coluna:
                        return nodo2.getName()

        return f"Node not found"

    # imprime as arestas todos guardadas no dicionario graph
    def imprime_aresta(self):
        listaA = ""
        for nodo in self.graph.keys():
            listaA = listaA + "\n"
            for nodo2 in self.graph[nodo]:
                listaA = listaA + nodo + " -> " + nodo2[0] + " com Peso: " + str(nodo2[1]) + "; "

        return listaA

    # funcao que devovle a possicao inicial do circuito, o "P"
    def getPosicaoInicial(self):
        posicao_inicial = 0
        for nodo in self.graph.keys():
            if nodo.getTipo() == 'P':
                posicao_inicial = nodo.getPosition()

        return posicao_inicial

    # desenha o grafo com o import networkx
    def desenhar_grafo(self):

        plt.figure(figsize=(7, 10))
        graph = nx.Graph()

        graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
        positions = {0: [0, 0], 1: [1, 0], 2: [1, 1], 3: [0, 1]}
        nx.draw_networkx(graph, pos=positions)

        plt.draw()
        plt.show()

        return None

    def get_arc_cost(self, node1, node2):
        custo_total = math.inf
        neighbours = self.graph[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in neighbours:
            if nodo == node2:
                custo_total = custo

        return custo_total

    def calcula_custo_total(self, caminho):
        # caminho é uma lista de nomes de nodos
        custo = 0
        i = 0
        while i + 1 < len(caminho):
            custo = custo + self.get_arc_cost(caminho[i], caminho[i + 1])
            i = i + 1
        return custo

    def getNodeByName(self, name):
        for nodo in self.nodes:
            if nodo.getName() == name:
                return nodo

        return f"Nodo com nome {name} nao encontrado"

    # dado o nodo, devolve os seus vizinhos
    def getVizinhos(self, nodo):
        lista = []

        for n, peso in self.graph[nodo]:
            lista.append((n, peso))

        return lista

    #
    # Função que dado um nodo, encontra o seu Vizinho mais a direite, para chegar mais rapidamente ao resultado
    # 
    def get_vizinho_mais_a_direita(self, nodo):
        coluna = 0  # variavel com o maior valor da coluna já lido
        temp = None # varivel tempraria para armazenar o nodo
        vizinho_mais_direita = None    # variavel tempraria para armazenar o vizinho mais a direita
        
        for adjacente, peso in self.graph[nodo]:    # precorre todos os vizinhos do nodo
            temp = self.getNodeByName(adjacente)
            
            if peso < 25 and coluna < temp.getColuna():
                coluna = temp.getColuna()
                vizinho_mais_direita = temp.getName()

        return vizinho_mais_direita

    #############################################
    # Pesquisa DFS
    #############################################
    def procura_DFS(self, start, end, caminho=[], visited=set()):
        caminho.append(start)
        visited.add(start)

        resultado = []

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custo_total = self.calcula_custo_total(caminho)
            return caminho, custo_total

        adjacente = self.get_vizinho_mais_a_direita(start)  # procura o vizinho mais a direita
        if adjacente not in visited:
            resultado = self.procura_DFS(adjacente, end, caminho, visited)  # faz a procura_DFS com o vizinho
            if resultado is not None:
                return resultado

        caminho.pop()  # se nao encontra remover o que está no caminho......

        return None

    #############################################
    # Pesquisa gulosa
    #############################################
    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = {start}
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {start: start}

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for list_index in open_list:
                if n is None or self.heuristica[self.getNodeByName(list_index)] < self.heuristica[
                    self.getNodeByName(n)]:
                    n = list_index

            if n is None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return reconst_path, self.calcula_custo_total(reconst_path)

            # para todos os vizinhos  do nodo corrente
            for (neighbour, weight) in self.getVizinhos(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if neighbour not in open_list and neighbour not in closed_list:
                    open_list.add(neighbour)
                    parents[neighbour] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')

        return None

    #############################################
    # Pesquisa A*
    #############################################
    def A_star(self, start, end):

        open_list = {start}
        closed_list = set([])

        g = {start: 0}

        parents = {start: start}

        while len(open_list) > 0:
            n = None

            # encontra o nodo com a menor heuristica
            for list_index in open_list:
                if n is None or g[list_index] + self.getHeuristica(self.getNodeByName(list_index)) < g[
                    list_index] + self.getHeuristica(self.getNodeByName(list_index)):
                    n = list_index

            if n is None:
                print('Path does not exist!')
                return None

        if n == end:
            reconst_path = []

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start)
            reconst_path.reverse()

            print("Path found: {}".format(reconst_path))
            return reconst_path, self.calcula_custo_total(reconst_path)

        if m not in open_list and m not in closed_list:
            open_list.add(m)
            parents[m] = n
            g[m] = g[n] + weight



        else:

            if g[m] > g[n] + weight:
                g[m] = g[n] + weight
                parents[m] = n

                if m in closed_list:
                    closed_list.remove(m)
                    open_list.add(m)

        open_list.remove(n)
        closed_list(n)

        return None


"""vizinhos_do_nodo = self.getVizinhos(adjacente)
                for nodo in vizinhos_do_nodo:
                    n = self.getNodeByName(nodo)
                    if n.getTipo() != "X":
                        if n.getColuna() >= tamanho_coluna:
                            tamanho_coluna = n.getColuna()
                            name = n.getName()"""


"""for (adjacente, peso) in self.graph[start]:
    if peso < 25:
        if adjacente not in visited:
            resultado = self.procura_DFS(adjacente, end, caminho, visited)  # TODO Perguntar ao professor
            if resultado is not None:
                return resultado"""