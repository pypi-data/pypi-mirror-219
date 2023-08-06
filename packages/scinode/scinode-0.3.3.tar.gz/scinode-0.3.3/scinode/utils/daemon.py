from scinode.database.client import scinodedb


def inspect_daemon_status_celery(name):
    from scinode.engine.celery.tasks import app

    reply = app.control.inspect()
    active = reply.active()
    # print(active)
    if active is not None and name in active:
        return True
    else:
        return False


def inspect_daemon_status_builtin(name, sleep=None, daemon_type="worker"):
    from scinode.utils.db import push_message
    import datetime
    import time

    if not sleep:
        data = scinodedb[daemon_type].find_one({"name": name}, {"_id": 0, "sleep": 1})
        sleep = data["sleep"]
    push_message(name, f"{name},{daemon_type},UPDATE")
    time.sleep(sleep)
    data = scinodedb[daemon_type].find_one({"name": name}, {"_id": 0})
    data["lastUpdate"] = int(
        (datetime.datetime.utcnow() - data["lastUpdate"]).total_seconds()
    )
    running = data["lastUpdate"] < sleep * 1.5
    return running
