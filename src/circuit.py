import numpy

from src.car.acceleration import Acceleration
from src.car.car import Car
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


def graph_from_circuit(circuits_file):
    circuit = read_circuit(circuits_file)
    costs = determine_circuit_costs(circuits_file)

    graph = Graph(True)

    line_pos = 0
    for line in circuit:
        for column in range(len(line) - 1):
            node_1 = Node(circuit[line_pos][column], line_pos, column)
            node_2 = Node(circuit[line_pos][column + 1], line_pos, column + 1)
            graph.add_edge(node_1, node_2, costs)
        line_pos += 1

    line_pos = 0  # Reset the counter
    for line_a in circuit:
        if line_pos == len(circuit) - 1:
            break

        for column_a in range(len(line_a)):
            node_a = Node(circuit[line_pos][column_a], line_pos, column_a)
            node_b = Node(circuit[line_pos + 1][column_a], line_pos + 1, column_a)
            graph.add_edge(node_a, node_b, costs)
        line_pos += 1

    for line in reversed(range(len(circuit))):
        for column in range(len(circuit[0])):
            node_c = Node(circuit[line][column], line, column)
            node_d = Node(circuit[line - 1][column], line - 1, column)
            graph.add_edge(node_c, node_d, costs)

        if line - 1 == 0:
            break

    return graph


def process_race(race_data, car_registration, destiny_node):
    race_path = race_data[0]

    car = Car(car_registration)
    for position in range(1, len(race_path) - 1):
        car.set_velocity(Acceleration.POSITIVE.value)

    car.set_line(destiny_node.get_line())
    car.set_column(destiny_node.get_column())
    return car
