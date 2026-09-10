import json

from flask import Flask, render_template, request

from informed import a_star, greedy
from uninformed import bfs, dfs, ids, ucs

app = Flask(__name__)


positions = {
"Yangon": (150, 550),
"Bago": (250, 500),
"Naypyidaw": (400, 400),
"Mawlamyine": (300, 600),
"Hpa-an": (400, 600),
"Dawei": (450, 680),
"Myeik": (550, 680),

"Pathein": (50, 500),
"Pyay": (200, 350),
"Magway": (350, 300),
"Sittwe": (100, 100),
"Hakha": (50, 50),

"Mandalay": (500, 250),
"Monywa": (400, 150),
"Sagaing": (500, 100),
"Pakokku": (350, 200),

"Meiktila": (500, 350),
"Taunggyi": (650, 350),
"Loikaw": (700, 450),
"Lashio": (700, 200),
"Bhamo": (750, 100),
"Myitkyina": (850, 50),

}

def get_path_edges(path):
    if not path:
        return set()

    edges = set()

    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]

        # Sort so A-B and B-A are considered the same edge
        edges.add(tuple(sorted([a, b])))

    return edges


with open("map_data.json", "r") as f:
    map_graph = json.load(f)


def build_graph(map_data):
    graph = {}

    for city, neighbors in map_data["connections"].items():
        graph[city] = []

        for neighbor in neighbors:
            # Distance keys can be in either direction
            key1 = f"{city}-{neighbor}"
            key2 = f"{neighbor}-{city}"

            if key1 in map_data["distances"]:
                distance = map_data["distances"][key1]
            elif key2 in map_data["distances"]:
                distance = map_data["distances"][key2]
            else:
                distance = 0

            graph[city].append((neighbor, distance))

    return graph


graph = build_graph(map_graph)


@app.route("/")
def home():
    return render_template(
        "index.html",
        cities=map_graph["cities"],
        graph=graph,
        positions=positions,
        start="Yangon",
        goal="Mandalay",
        algorithm="bfs",
        path=None,
        cost=None,
        path_edges=set()
    )


@app.route("/search", methods=["POST"])
def search():
    start = request.form["start"]
    goal = request.form["goal"]
    algo = request.form["algorithm"]

    if algo == "bfs":
        path, cost = bfs(graph, start, goal)

    if algo == "dfs":
        path, cost = dfs(graph, start, goal)

    if algo == "ucs":
        path, cost = ucs(graph, start, goal)

    if algo == "ids":
        path, cost = ids(graph, start, goal)

    if algo == "a_star":
        path, cost = a_star(graph, start, goal)

    if algo == "greedy":
        path, cost = greedy(graph, start, goal)

    return render_template(
        "index.html", cities=map_graph["cities"], path=path, cost=cost
    )


if __name__ == "__main__":
    app.run(debug=True)
