import json

from flask import Flask, render_template, request

from informed import a_star, greedy
from uninformed import bfs, dfs, ids, ucs

app = Flask(__name__)

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
    cities = map_graph["cities"]
    return render_template("index.html", cities=cities)


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
