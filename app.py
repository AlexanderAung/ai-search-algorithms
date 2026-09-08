from flask import Flask, render_template, request
import json
from uninformed import bfs

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
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    start = request.form["start"]
    goal = request.form["goal"]

    path, cost = bfs(graph, start, goal)

    return render_template("index.html", path=path, cost=cost)


if __name__ == "__main__":
    app.run(debug=True)
