from metro.topology import STATION_REGISTRY, LINE_REGISTRY
from metro.network import MetroNetwork
from metro.station import Station

def show_map():
    pass

def plan_trip():
    """
    Prompts user for a starting station and a destination station, 
    then finds and displays a path between them.

    The user can choose to use either Depth-First Search (DFS) or Breadth-First Search (BFS) for pathfinding.
    """
    pass

def ride_metro():
    """
    Prompts user for a starting station and simulates riding the metro.
    At each destination, the user can choose to continue to the next station or exit the ride.

    At the end of the ride, the program displays the total number of stations visited and the path taken.
    """

    pass

def init_network():
    """
    Initializes the metro network by creating Station objects for each station in the STATION_REGISTRY.
    """
    network = MetroNetwork()
    for line_id, stations in LINE_REGISTRY.items():
        network.add_line(line_id, stations)

    return network

def main_loop():

    network = init_network()

    while True:
        print("Welcome to the Metro System!")
        print("1. View network map")
        print("2. Plan your trip")
        print("3. Ride the metro")

        print("Exit with any other key.")

        choice = input("Enter your choice: ")
        if choice == "1":
            show_map()
        elif choice == "2":
            plan_trip()
        elif choice == "3":
            ride_metro()
        else:
            break
