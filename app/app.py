from flask import Flask, jsonify, request
tasks = {}
next_id = 1

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(list(tasks.values()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)