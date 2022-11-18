from src.graph import Graph


def read_circuits(circuits_file):
    try:
        with open(circuits_file) as file_stream:
            # In the "circuits.txt" file the circuits are separated by a $.
            stream = file_stream.read().strip().split('$')
            file_stream.close()
            return stream
    except OSError:
        print(f"Failed to open {circuits_file} file.")


def print_circuits(circuits_file):
    circuits = read_circuits(circuits_file)
    circuit_index = 1

    for circuit in circuits:
        print(f"Circuit {circuit_index}:")
        print(f"{circuit}")
        circuit_index += 1


def print_circuits_graphs(graphs):
    if graphs is None:
        return

    graph_index = 1
    for graph in graphs:
        print(f"Graph {graph_index}: ")
        print(graph.print_edges())
        graph_index += 1


def plot_circuit_graph(graph):
    graph.plot()


def format_circuits(circuits):
    formatted_circuits = list()

    for circuit in circuits:
        formatted_circuit = circuit.replace(' ', '').replace('\n', '')
        formatted_circuit_to_list = [char for char in formatted_circuit]
        formatted_circuits.append(formatted_circuit_to_list)
    return formatted_circuits


def circuits_graphs(circuits_file):
    circuits = format_circuits(read_circuits(circuits_file))
    graphs = list()

    for circuit in circuits:
        graph = Graph()

        for i in range(len(circuit)):
            if i + 1 == len(circuit):
                break

            current_char = circuit.__getitem__(i)
            next_char = circuit.__getitem__(i + 1)

            if current_char == '-' and next_char == 'X':
                graph.add_edge(f"-{i}", f"X{i + 1}", 25)
            if current_char == '-' and next_char == '-':
                graph.add_edge(f"-{i}", f"-{i + 1}", 1)
            if current_char == '-' and next_char == 'F':
                graph.add_edge(f"-{i}", f"F{i + 1}", 1)

            if current_char == 'P' and next_char == 'X':
                graph.add_edge(f"P{i}", f"X{i + 1}", 25)
            if current_char == 'P' and next_char == '-':
                graph.add_edge(f"P{i}", f"-{i + 1}", 1)

            # TODO: Change the velocity & the acceleration of the vehicle
            if current_char == 'X' and next_char == 'X':
                graph.add_edge(f"X{i}", f"X{i + 1}", 25)
            if current_char == 'X' and next_char == '-':
                graph.add_edge(f"X{i}", f"-{i + 1}", 13)
            if current_char == 'X' and next_char == 'F':
                graph.add_edge(f"X{i}", f"F{i + 1}", 25)

        graphs.append(graph)
    return graphs
