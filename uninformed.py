"""
# Task 3: Implement and Explain the Search Algorithms

## Uninformed Search — uninformed.py

1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Uniform-Cost Search (UCS)
4. Iterative Deepening Search (IDS)
"""

from collections import deque
import heapq


# used code completion
def bfs(graph: dict, start: str, goal: str) -> tuple:
    """
    BFS explores nodes in layer by layer
    It guarantees the shortest path in terms of number of edges,
    but does NOT consider road distances.
    Returns (path, total_cost) or (None, inf) if no path.
    """
    if start == goal:
        return [start], 0

    # Queue holds (current_node, path_so_far)
    queue = deque()
    queue.append((start, [start]))
    visited = {start}

    while queue:
        node, path = queue.popleft()

        # Explore neighbors (ignore costs for BFS)
        for neighbor, _ in graph.get(node, []):
            if neighbor == goal:
                # Found the goal: return the complete path
                full_path = path + [neighbor]
                # Compute total distance along this path (optional)
                total_cost = compute_path_cost(graph, full_path)
                return full_path, total_cost

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    # No path found
    return None, float("inf")


def dfs(graph: dict, start: str, goal: str) -> tuple:
    """
    DFS explores as far as possible along each branch before backtracking.
    It does not consider edge costs.
    Returns (path, total_cost) or (None, inf) if no path.
    """
    if start == goal:
        return [start], 0

    # Stack holds (current_node, path_so_far)
    stack = [(start, [start])]
    visited = {start}

    while stack:
        node, path = stack.pop()

        for neighbor, _ in graph.get(node, []):
            if neighbor == goal:
                full_path = path + [neighbor]
                total_cost = compute_path_cost(graph, full_path)
                return full_path, total_cost

            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None, float("inf")


def ucs(graph: dict, start: str, goal: str) -> tuple:
    """
    UCS expands the node with the lowest cumulative cost (distance).
    It is like Dijkstra's algorithm and guarantees the shortest path
    by actual road distance.
    Returns (path, total_cost) or (None, inf) if no path.
    """
    if start == goal:
        return [start], 0

    # Priority queue: (cumulative_cost, node, path)
    pq = [(0, start, [start])]
    # visited keeps the best cost found so far for each node
    visited = {start: 0}

    while pq:
        cost, node, path = heapq.heappop(pq)

        # If we already found a better way to this node, skip
        if cost > visited.get(node, float("inf")):
            continue

        # Goal test when we pop the node (guarantees optimality)
        if node == goal:
            return path, cost

        for neighbor, edge_cost in graph.get(node, []):
            new_cost = cost + edge_cost
            # If this is a cheaper way to neighbor, or neighbor not visited
            if new_cost < visited.get(neighbor, float("inf")):
                visited[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return None, float("inf")


def ids(graph: dict, start: str, goal: str) -> tuple:
    """
    IDS repeatedly applies depth‑limited DFS with increasing depth limits.
    It combines the space efficiency of DFS with the completeness of BFS.
    Returns (path, total_cost) or (None, inf) if no path.
    """

    def dls(node, goal, depth, path, visited):
        """
        Depth‑limited DFS (recursive).
        Returns the path if goal is found within the depth limit, else None.
        """
        if node == goal:
            return path

        # If depth limit reached, stop exploring further
        if depth == 0:
            return None

        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dls(neighbor, goal, depth - 1, path + [neighbor], visited)
                if result is not None:
                    return result
                visited.remove(neighbor)
        return None

    # Increase depth limit until we find the goal
    # We use a large max limit to avoid infinite loop; in practice,
    # the graph is finite and connected, so we'll find it.
    max_depth = len(graph)  # A safe upper bound
    for depth in range(max_depth + 1):
        visited = {start}
        path = dls(start, goal, depth, [start], visited)
        if path is not None:
            total_cost = compute_path_cost(graph, path)
            return path, total_cost

    return None, float("inf")


# ------------------------------------------------------------
# Helper: compute total distance of a given path
# ------------------------------------------------------------
def compute_path_cost(graph, path):
    """
    Sum the edge costs along the path.
    Assumes the graph is undirected; for each consecutive pair (a,b),
    we look up the cost in graph[a] (or graph[b] if necessary).
    """
    total = 0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        # Find the edge cost from a to b
        found = False
        for neighbor, cost in graph.get(a, []):
            if neighbor == b:
                total += cost
                found = True
                break
        # If not found in a, try b (undirected)
        if not found:
            for neighbor, cost in graph.get(b, []):
                if neighbor == a:
                    total += cost
                    found = True
                    break
        # If still not found, raise an error (should not happen for valid paths)
        if not found:
            raise ValueError(f"Edge {a}-{b} not found in graph")
    return total


# ------------------------------------------------------------
if __name__ == "__main__":
    # test graph
    sample_graph = {
        "Yangon": [("Mingaladon", 15), ("Insein", 10), ("Dawbon", 5)],
        "Mingaladon": [("Yangon", 15), ("Hlegu", 25), ("North Okkalapa", 12)],
        "Insein": [("Yangon", 10), ("Hlaingthaya", 8)],
        "Dawbon": [("Yangon", 5), ("Thaketa", 7)],
        "Hlegu": [("Mingaladon", 25)],
        "North Okkalapa": [("Mingaladon", 12), ("Thingangyun", 6)],
        "Hlaingthaya": [("Insein", 8)],
        "Thaketa": [("Dawbon", 7)],
        "Thingangyun": [("North Okkalapa", 6)],
    }

    start, goal = "Yangon", "Hlegu"

    print("BFS:", bfs(sample_graph, start, goal))
    print("DFS:", dfs(sample_graph, start, goal))
    print("UCS:", ucs(sample_graph, start, goal))
    print("IDS:", ids(sample_graph, start, goal))
