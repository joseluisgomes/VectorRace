import circuit


def race():
    circuits_file = "circuits.txt"
    circuit_graphs = circuit.graph_from_circuit(circuits_file)
    status = -1

    while status != 0:
        print("1-Print circuits")
        print("2-Plot Graph")
        print("3-Print the nodes of the Graph")
        print("4-Print the edges of the Graph")
        print("5-DFS Search")
        print("6-BFS Search")
        print("7-Greedy Search")
        print("8-A Star Search")
        print("0-Exit")

        status = int(input("Choose your option -> "))

        match status:
            case 0:
                print("Exiting..........")
                exit(0)
            case 1:
                circuit.print_circuits(circuits_file)
                print("Press Enter to continue")
            case 2:
                circuit.plot_circuit_graph(circuit_graphs)
                print("Press Enter to continue")
            case 3:
                print(f"Graph's nodes: ")
                print(circuit_graphs.print_nodes())
                print("Press Enter to continue")
            case 4:
                print(f"Graph edges: ")
                print(circuit_graphs.print_edges())
                print("Press Enter to continue")
            case 5:
                start_node = input("Start node -> ")
                end_node = input("Destiny node -> ")

                DFS_result = circuit_graphs.DFS_search(start_node, end_node, path=[], visited=set())
                print(f"Race: {DFS_result})")
                print("Press Enter to continue")
            case 6:
                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                BFS_result = circuit_graphs.BFS_search(start_node, end_node)
                print(f"Race: {BFS_result})")
                print("Press Enter to continue")
            case 7:
                #            print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))
                #      circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                """
                    Heuristic: lowest cost between the start & the end nodes
                """
                #          print(circuit_graph.lowest_cost(start_node, end_node))
                print("Press Enter to continue")
            case 8:
                #         print(f"#Circuits: {len(circuit_graphs)}")
                graph_index = int(input("Circuit number -> "))
                #         circuit_graph = circuit_graphs.__getitem__(graph_index - 1)

                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                #                print(circuit_graph.BFS_search(start_node, end_node))
                print("Press Enter to continue")
            case _:
                print("Invalid option...")
                print("Press Enter to continue")


race()
