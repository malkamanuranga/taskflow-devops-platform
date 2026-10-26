from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
tasks = {}
next_id = 1

REQUESTS = Counter("http_requests_total", "HTTP requests", ["method", "status"])
TASKS_CREATED = Counter("tasks_created_total", "Tasks created")

@app.after_request
def count_request(response):
    REQUESTS.labels(request.method, response.status_code).inc()
    return response
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
    TASKS_CREATED.inc()
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

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)