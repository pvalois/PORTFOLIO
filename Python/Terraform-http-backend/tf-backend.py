#!/usr/bin/env python3
import json
import os
import uuid
import datetime
from threading import Lock
import pickle
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

FILE_LOCKS = {}    # fichier lock par projet
TF_LOCKS = {}      # verrou logique par projet
LOG_FILE = "tf-backend.log"

def log_request(project, action, payload=None):
    ts = datetime.datetime.now()
    with open(LOG_FILE, "a") as log:
        log.write(f"[{ts}] [project={project}] {action}\n")
        if payload is not None:
            try:
                size = len(json.dumps(payload).encode("utf-8"))
                log.write(f"[{ts}] Payload size: {size} bytes\n")
            except Exception as e:
                log.write(f"[{ts}] Exception encountered: {e}\n")

def get_project_info(project):
    if project not in FILE_LOCKS:
        FILE_LOCKS[project] = Lock()
    if project not in TF_LOCKS:
        TF_LOCKS[project] = False
    state_file = f"{project}.tfstate"
    if not os.path.exists(state_file):
        default_state = {
            "version": 4,
            "terraform_version": "1.5.0",
            "serial": 0,
            "lineage": str(uuid.uuid4()),
            "resources": []
        }
        with open(state_file, "w") as f:
            json.dump(default_state, f, indent=2)
        log_request(project, f"Initialized state file: {state_file}")
    return state_file, FILE_LOCKS[project], TF_LOCKS

def set_tf_lock(project, value):
    TF_LOCKS[project] = value

# -----------------------
# Endpoints dynamiques 
# -----------------------

@app.route("/v1/state/<project>", methods=["GET"])
def get_state(project):
    state_file, file_lock, _ = get_project_info(project)
    with file_lock:
        with open(state_file) as f:
            state = json.load(f)
    log_request(project, "GET state", state)
    return jsonify(state)

@app.route("/v1/state/<project>", methods=["POST", "PUT"])
def update_state(project):
    state_file, file_lock, _ = get_project_info(project)
    try:
        state = request.get_json(force=True)
    except Exception:
        abort(400, "Invalid JSON")
    with file_lock:
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
    log_request(project, "UPDATE state", state)
    return jsonify({"status": "ok"})

@app.route("/v1/lock/<project>", methods=["POST"])
def lock_state(project):
    _, _, lock = get_project_info(project)
    if TF_LOCKS[project]:
        log_request(project, "LOCK request: already locked")
        return jsonify({"locked": True}), 423
    set_tf_lock(project, True)
    log_request(project, "LOCK acquired")
    return jsonify({"locked": False})

@app.route("/v1/unlock/<project>", methods=["POST"])
def unlock_state(project):
    if TF_LOCKS.get(project, False):
        set_tf_lock(project, False)
        log_request(project, "UNLOCK released")
    else:
        log_request(project, "UNLOCK request: no lock held")
    return jsonify({"status": "unlocked"})

if __name__ == "__main__":
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.datetime.now()}] Terraform multi-project backend running on http://0.0.0.0:9961\n")
    app.run(host="0.0.0.0", port=9961, threaded=True)
