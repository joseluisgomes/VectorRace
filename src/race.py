from circuit import circuits_graphs, print_circuits, plot_circuit_graph, print_circuits_graphs
from src.car.car import Car


def race():
    circuit_graphs = circuits_graphs("circuits.txt")
    status = -1

    while status != 0:
        print("1-Print circuits")
        print("2-Print the graphs of the circuits")
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
                print_circuits_graphs(circuit_graphs)
                print("Press Enter to continue")
            case 3:
                print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))

                circuit_graph = circuits_graphs("circuits.txt").__getitem__(graph_index - 1)
                plot_circuit_graph(circuit_graph)
                print("Press Enter to continue")
            case 4:
                # Print the keys of the dictionary which represents the graph
                print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))

                print(f"Graph {graph_index}'s keys: ")
                circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                print(circuit_graph.graph.keys())
                print("Press Enter to continue")
            case 5:
                # Print all edges of the graph
                print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))

                print(f"Graph {graph_index}'s edges: ")
                circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                print(circuit_graph.print_edges())
                print("Press Enter to continue")
            case 6:
                print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))
                circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                # num_of_cars = int(input("#Cars -> "))  # Number of cars to race
                car = Car("111-111-111")

                start_node = input("Start node -> ")
                end_node = input("Destiny node -> ")

                print(circuit_graph.DFS_search(start_node, end_node, path=[], visited=set()))
                print("Press Enter to continue")
            case 7:
                print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))
                circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                print(circuit_graph.greedy_search(start_node, end_node))
                print("Press Enter to continue")
            case _:
                print("Invalid option...")
                print("Press Enter to continue")


race()
