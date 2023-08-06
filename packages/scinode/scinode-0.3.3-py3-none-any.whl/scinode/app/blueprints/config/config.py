from flask import Blueprint, render_template, request
from scinode.app.db import db

config_bp = Blueprint("config_bp", __name__, template_folder="templates")


# =================================
# componetns
# =================================
@config_bp.route("/")
def configs():
    return render_template("config.html", title="Configuration")


@config_bp.route("/workers/logfile/<name>")
def worker_logfile(name):
    from scinode.daemon.worker import DaemonWorker

    worker = DaemonWorker(name=name)
    with open(worker.logfile) as f:
        log_data = f.readlines()
    return render_template("worker_logfile.html", title="Logfile", log_data=log_data)


@config_bp.route("/api/worker_data")
def worker_data():
    from scinode.database.worker import WorkerClient

    worker_client = WorkerClient()
    data = worker_client.get_status()
    print("worker: ", data)
    # response
    return {
        "data": data,
        "recordsFiltered": 0,
        "recordsTotal": 0,
        "draw": request.args.get("draw", type=int),
    }


@config_bp.route("/api/worker_add", methods=["POST"])
def worker_add():
    from scinode.config import DaemonConfig

    json = request.json
    config = DaemonConfig()
    print("worker: ", json)
    if json["name"] == "":
        return {"message": "Name is empty. Please input a value"}
    elif json["workdir"] == "":
        return {"message": "Work directory is empty. Please input a value"}
    else:
        config.insert_one(json)
    return {"message": "Add worker {} successfully".format(json["name"])}


@config_bp.route("/api/worker_action", methods=["POST"])
def worker_action():
    import os

    json = request.json
    print("worker action: ", json)
    query = {}
    name = json.get("name")
    action = json.get("action")
    if name:
        query["name"] = name
    if action.upper() == "DELETE":
        os.system("scinode worker delete --name {}".format(name))
        # config.delete(query)
        return {"message": "Delete {} successfully".format(name)}
    elif action.upper() == "STOP":
        print("Stop worker {}".format(name))
        os.system("scinode worker stop {}".format(name))
        return {"message": "Stop {} successfully".format(name)}
    elif action.upper() == "START":
        print("Start worker {}".format(name))
        os.system("scinode worker start {}".format(name))
        return {"message": "Start {} successfully".format(name)}
    elif action.upper() == "RESTART":
        os.system("scinode worker restart {}".format(name))
        return {"message": "Restart {} successfully".format(name)}
    # response
    return {"message": "None"}
