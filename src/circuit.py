import numpy
from src.graph import Graph
from src.node import Node


def read_circuit(circuits_file):
    try:
        with open(circuits_file) as file_stream:
            circuit = []

            for line in file_stream.readlines():
                line_formatted = line.strip().split(' ')
                circuit.append(line_formatted)

            file_stream.close()
            return circuit
    except OSError:
        print(f"Failed to open {circuits_file} file.")


def print_circuits(circuits_file):
    circuit = read_circuit(circuits_file)
    print(numpy.mat(circuit))


def print_circuits_graphs(graph):
    print(f"Graph: ")
    print(graph.print_edges())


def plot_circuit_graph(graph):
    graph.plot()


def determine_circuit_costs(circuits_file):
    circuit = read_circuit(circuits_file)
    costs = [[0] * len(line) for line in circuit]
    line_pos = 0

    for line in circuit:
        for column in range(len(line)):  # Num. of columns = length of the line
            match line[column]:
                case 'P':
                    costs[line_pos][column] = 0
                case '-':
                    costs[line_pos][column] = 1
                case 'X':
                    costs[line_pos][column] = 25
                case 'F':
                    costs[line_pos][column] = 10
        line_pos += 1
    return costs


def graph_from_circuit(circuits_file):  # TODO: Debug this function
    circuit = read_circuit(circuits_file)
    costs = determine_circuit_costs(circuits_file)

    graph = Graph()
    line_pos = 0

    for line in circuit:
        for column in range(len(line) - 1):
            node_1 = Node(circuit[line_pos][column], line_pos, column)
            node_2 = Node(circuit[line_pos][column + 1], line_pos, column + 1)
            graph.add_edge(node_1, node_2, costs[line_pos][column + 1])
        line_pos += 1

    line_pos = 0

    for column in range(len(circuit[0]) - 1):
        for line in circuit:
            node_1 = Node(circuit[line_pos][column], line_pos, column)
            node_2 = Node(circuit[line_pos + 1][column], line_pos + 1, column)
            graph.add_edge(node_1, node_2, costs[line_pos + 1][column])

    return graph
