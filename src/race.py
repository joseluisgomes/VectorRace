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
    graph_index = 1

    for graph in graphs:
        print(f"Graph {graph_index}:")
        print(f"{graph}")
        graph_index += 1


def circuits_graphs(circuits_file):
    circuits = read_circuits(circuits_file)
    graphs = list()

    for circuit in circuits:
        graph = list()

        for index in range(0, len(circuit)):
            match circuit.__getitem__(index):
                case 'X':
                    graph.append(25)
                case '-':
                    graph.append(1)
                case 'P':
                    graph.append(0)
                case 'F':
                    graph.append(9)  # Cost of 9 equals to infinity
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
                # print(graph)
                circuit_graphs = circuits_graphs("circuits.txt")
                print_circuits_graphs(circuit_graphs)
                print("Press Enter to continue")
            case 3:
                graph.plot()
            case 4:
                # Print the keys of the dictionary which represents the graph
                print(graph.graph.keys())
                print("Press Enter to continue")
            case 5:
                # Print all edges of the graph
                print(graph.print_edges())
                print("Press Enter to continue")
            case 6:
                start = input("Start node ->")
                end = input("Destiny node ->")
                print(graph.DFS_search(start, end, path=[], visited=set()))
                print("Press Enter to continue")
            case 7:
                start = input("Start node->")
                end = input("Destiny node->")
                print(graph.greedy_search(start, end))
                print("Press Enter to continue")
            case _:
                print("Invalid option...")
                print("Press Enter to continue")


race()
