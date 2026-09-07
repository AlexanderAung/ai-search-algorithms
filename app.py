from flask import Flask, render_template, request

from uninformed import bfs

app = Flask(__name__)


# Dummy graph for testing
graph = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1)],
}


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
