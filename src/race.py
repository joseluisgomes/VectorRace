import colorama
import pyfiglet
import circuit

from colorama import Fore


def race():
    circuits_file = "circuits.txt"
    circuit_graphs = circuit.graph_from_circuit(circuits_file)
    status = -1

    while status != 0:
        print(Fore.YELLOW + pyfiglet.figlet_format("Vector Race"))
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
                destiny_node = circuit_graphs.get_node_by_name(end_node)
                car_settings = circuit.process_race(DFS_result, "AAA-BBB-CCC", destiny_node)

                print(f"DFS result: {DFS_result})")
                print(f"{car_settings}")
                print("\nPress Enter to continue")
            case 6:
                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                BFS_result = circuit_graphs.BFS_search(start_node, end_node)
                destiny_node = circuit_graphs.get_node_by_name(end_node)
                car_settings = circuit.process_race(BFS_result, "AAA-BBB-CCC", destiny_node)

                print(f"BFS result: {BFS_result})")
                print(f"{car_settings}")
                print("\nPress Enter to continue")
            case 7:
                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                greedy_result = circuit_graphs.greedy_search(start_node, end_node)
                destiny_node = circuit_graphs.get_node_by_name(end_node)
                car_settings = circuit.process_race(greedy_result, "AAA-BBB-CCC", destiny_node)

                print(f"Greedy result: {greedy_result})")
                print(f"{car_settings}")
                print("\nPress Enter to continue")
            case 8:
                start_node = input("Start node-> ")
                end_node = input("Destiny node-> ")

                a_star_result = circuit_graphs.A_star_search(start_node, end_node)
                destiny_node = circuit_graphs.get_node_by_name(end_node)
                car_settings = circuit.process_race(a_star_result, "AAA-BBB-CCC", destiny_node)

                print(f"A Star result: {a_star_result})")
                print(f"{car_settings}")
                print("\nPress Enter to continue")
            case _:
                print("Invalid option...")
                print("Press Enter to continue")


colorama.init(autoreset=True)
race()
