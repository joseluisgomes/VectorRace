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


def plot_graph(graph):
    graph.plot()


def print_circuits_graphs(graphs):
    if graphs is None:
        return

    graph_index = 1
    for graph in graphs:
        print(f"Graph {graph_index}: ")
        print(graph.print_edges())
        graph_index += 1


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


def race():
    graph = Graph()
    status = -1

    while status != 0:
        print("1-Print the circuits")
        print("2-Print Graphs")
        print("3-Plot Graph")
        print("4-Print the nodes of the Graph")
        print("5-Print the edges of the Graph")
        print("6-DFS Search")
        print("7-BFS Search")
        print("8-Greedy Search")
        print("9-A Star Search")
        print("0-Exit")

        status = int(input("Choose your option -> "))

        match status:
            case 0:
                print("Exiting..........")
                exit(0)
            case 1:
                print_circuits("circuits.txt")
                print("Press Enter to continue")
            case 2:
                circuit_graphs = circuits_graphs("circuits.txt")
                print_circuits_graphs(circuit_graphs)
                print("Press Enter to continue")
            case 3:
                graph_index = int(input("Circuit number -> "))
                graph = circuits_graphs("circuits.txt").__getitem__(graph_index - 1)
                plot_graph(graph)
                print("Press Enter to continue")
            case 4:
                # Print the i + 1eys of the dictionary which represents the graph
                print(graph.graph.keys())
                print("Press Enter to continue")
            case 5:
                # Print all edges of the graph
                print(graph.print_edges())
                print("Press Enter to continue")
            case 6:
                start = input("Start node -> ")
                end = input("Destiny node -> ")
                print(graph.DFS_search(start, end, path=[], visited=set()))
                print("Press Enter to continue")
            case 7:
                start = input("Start node-> ")
                end = input("Destiny node-> ")
                print(graph.greedy_search(start, end))
                print("Press Enter to continue")
            case _:
                print("Invalid option...")
                print("Press Enter to continue")


race()
