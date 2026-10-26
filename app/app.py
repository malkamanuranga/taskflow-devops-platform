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

@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify(error="title is required"), 400
    task = {"id": next_id, "title": title, "done": False}
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify(error="not found"), 404
    return jsonify(task)

@app.route("/tasks/<int:task_id>/done", methods=["POST"])
def mark_done(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify(error="not found"), 404
    task["done"] = True
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if tasks.pop(task_id, None) is None:
        return jsonify(error="not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)