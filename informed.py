"""
# Informed Search — informed.py

1. Greedy Best-First Search
2. A* Search
"""



import heapq
import math
import json

#------------------------------------------------------------
#Load city coordinates
#------------------------------------------------------------

with open("map_data.json", "r") as f:
    map_data = json.load(f)

coordinates = map_data["coordinates"]

#------------------------------------------------------------
#Heuristic: straight-line distance
#------------------------------------------------------------

def heuristic(city: str, goal: str) -> float:
    """
    Calculate the straight-line distance between two cities
    using the Haversine formula.

    Returns:
        Distance in kilometers.
    """

    if city not in coordinates:
        raise ValueError(f"Coordinates not found for city: {city}")

    if goal not in coordinates:
        raise ValueError(f"Coordinates not found for city: {goal}")

    lat1, lon1 = map(float, coordinates[city])
    lat2, lon2 = map(float, coordinates[goal])

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Earth's radius in kilometers
    earth_radius = 6371.0

    return earth_radius * c

#------------------------------------------------------------
#Helper: compute total path cost
#------------------------------------------------------------

def compute_path_cost(graph: dict, path: list[str]) -> float:
    """
    Calculate the total road distance of a path.
    """

    total = 0.0

    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]

        found = False

        for neighbor, cost in graph.get(current, []):
            if neighbor == next_city:
                total += cost
                found = True
                break

        # Support undirected graphs
        if not found:
            for neighbor, cost in graph.get(next_city, []):
                if neighbor == current:
                    total += cost
                    found = True
                    break

        if not found:
            raise ValueError(
                f"Edge {current}-{next_city} not found in graph"
            )

    return total

#------------------------------------------------------------
#1. Greedy Best-First Search
#------------------------------------------------------------

def greedy(graph: dict, start: str, goal: str) -> tuple:
    """
    Greedy Best-First Search.

    Uses only the heuristic h(n) to decide which node to explore.

        f(n) = h(n)

    It chooses the city that appears closest to the goal
    based on straight-line distance.

    It does NOT guarantee the shortest road-distance path.

    Returns:
        (path, total_cost)

    If no path exists:
        (None, inf)
    """

    if start == goal:
        return [start], 0

    # Priority queue:
    # (heuristic, city, path)
    pq = []

    heapq.heappush(
        pq,
        (heuristic(start, goal), start, [start])
    )

    visited = set()

    while pq:

        h, city, path = heapq.heappop(pq)

        if city in visited:
            continue

        visited.add(city)

        # Goal test
        if city == goal:
            total_cost = compute_path_cost(graph, path)
            return path, total_cost

        # Expand neighbors
        for neighbor, _ in graph.get(city, []):

            if neighbor not in visited:

                h_value = heuristic(neighbor, goal)

                heapq.heappush(
                    pq,
                    (
                        h_value,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, float("inf")

#------------------------------------------------------------
#2. A* Search
#------------------------------------------------------------

def a_star(graph: dict, start: str, goal: str) -> tuple:
    """
    A* Search.

    Uses:

        f(n) = g(n) + h(n)

    where:

        g(n) = actual road distance from start to n
        h(n) = estimated straight-line distance from n to goal

    With a consistent/admissible heuristic, A* guarantees
    the shortest path by road distance.

    Returns:
        (path, total_cost)

    If no path exists:
        (None, inf)
    """

    if start == goal:
        return [start], 0

    # Priority queue:
    # (f_score, g_score, city, path)
    pq = []

    start_h = heuristic(start, goal)

    heapq.heappush(
        pq,
        (
            start_h,       # f = g + h, where g = 0
            0,             # g
            start,
            [start]
        )
    )

    # Best known g-cost for each city
    best_cost = {
        start: 0
    }

    while pq:

        f, cost, city, path = heapq.heappop(pq)

        # Ignore outdated queue entries
        if cost > best_cost.get(city, float("inf")):
            continue

        # Goal test
        if city == goal:
            return path, cost

        # Expand neighbors
        for neighbor, edge_cost in graph.get(city, []):

            new_cost = cost + edge_cost

            # If this is a better route to neighbor
            if new_cost < best_cost.get(
                neighbor,
                float("inf")
            ):

                best_cost[neighbor] = new_cost

                h = heuristic(neighbor, goal)

                f = new_cost + h

                heapq.heappush(
                    pq,
                    (
                        f,
                        new_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, float("inf")