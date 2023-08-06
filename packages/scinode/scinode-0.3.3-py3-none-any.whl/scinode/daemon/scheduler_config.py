from scinode.database.client import scinodedb
import datetime


def init_scheduler():
    """Init scheduler"""
    from scinode.utils.db import insert_one

    if scinodedb["scheduler"].find_one({"name": "scheduler"}) is None:
        data = {
            "name": "scheduler",
            "sleep": 0.01,
            "pid": -1,
            "lastUpdate": datetime.datetime.utcnow(),
        }
        insert_one(data, scinodedb["scheduler"])
