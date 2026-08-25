from commuter.cost import TripDistanceCalculator, TripDurationCalculator
from commuter.planner import Plan, TripPlanner
from commuter.roads import MapService

source = "b1"
destination = "f6"

street_names_map = {
    "a": "Apple St.",
    "b": "Birch St.",
    "c": "Cucumber St.",
    "d": "Diamond Av.",
    "e": "Echo St.",
    "f": "Fox St.",
    "g": "Garden St.",
    "1": "1st St.",
    "2": "2nd St.",
    "3": "3rd St.",
    "4": "4th St.",
    "5": "5th St.",
    "6": "6th St.",
    "7": "7th St.",
}

local_roads_only = ["b1", "b2", "b3", "b4", "b5", "c5", "d5", "e5", "f5", "f6"]
arterial = [
    "b1",
    "c1",
    "d1",
    "xd",
    "x7",
    "g7",
    "f7",
    "f6",
]
balanced = ["b1", "c1", "d1", "d3", "d5", "e5", "f5", "f6"]


def compare_routes(routes):
    for r, n in zip(routes, ["Local Roads only", "Proritize Arterial", "Balanced"]):
        print(n)
        mins = TripDurationCalculator(MapService()).get_cost(r)
        kms = TripDistanceCalculator(MapService()).get_cost(r)
        print("Route:", " -> ".join(r))
        print(f"{kms} km, {mins} mins")

        print("\n")


def node_to_display_name(node: str):
    if node == "xd":
        return "Route 42 - Exit 1 (Diamond)"
    if node == "x7":
        return "Route 42 - Exit 2 (7th)"

    return f"{street_names_map[node[0]]} & {street_names_map[node[1]]}"


def prompt_option(prompt: str, options: list[str]) -> str:
    """
    Prompts the user to select an option from a list of options.
    Returns the selected option.
    """
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def plan_trip_dist(source: str, destination: str) -> Plan:
    map_service = MapService()
    planner = TripPlanner(map_service, TripDistanceCalculator(map_service))
    return planner.plan_route(source, destination)


def plan_trip_time(source: str, destination: str) -> Plan:
    map_service = MapService()
    planner = TripPlanner(map_service, TripDurationCalculator(map_service))
    return planner.plan_route(source, destination)


def display_plan(plan: Plan, unit: str):
    print("Route:", " -> ".join(plan.route))
    print(f"Cost: {plan.cost} {unit}")


def main():
    print(
        f"Eric lives in {node_to_display_name(source)} and works in {node_to_display_name(destination)}"
    )

    option = prompt_option(
        "What do you want to do today?",
        [
            "Compare routes",
            "See how much distance he will travel",
            "See how much time he will spend traveling",
            "Exit",
        ],
    )
    print("\n")
    match option:
        case "Compare routes":
            compare_routes([local_roads_only, arterial, balanced])
            return
        case "See how much distance he will travel":
            display_plan(plan_trip_dist(source, destination), "km")
        case "See how much time he will spend traveling":
            display_plan(plan_trip_time(source, destination), "mins")
        case _:
            print("Exiting the program.")
            return


if __name__ == "__main__":
    main()
