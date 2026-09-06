from flask import Flask, render_template, request

from uninformed import bfs

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["Post"])
def search():
    start = request.form["start"]
    goal = request.form["goal"]
    algo = request.form["algorightm"]
    return "Hello from AI_Search"


if __name__ == "__main__":
    app.run(debug=True)
