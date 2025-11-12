from flask import Flask, request, jsonify, send_from_directory
from logic import simulate_processes
import os

app = Flask(__name__)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

# Serve styles.css
@app.route("/styles.css")
def styles():
    return send_from_directory(os.getcwd(), "styles.css")

# Serve script.js
@app.route("/script.js")
def script():
    return send_from_directory(os.getcwd(), "script.js")

# Simulation API
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    processes = data.get("processes", [])
    states, gantt = simulate_processes(processes)
    return jsonify({"states": states, "gantt": gantt})

if __name__ == "__main__":
    app.run(debug=True)
