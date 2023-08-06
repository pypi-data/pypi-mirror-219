from scinode.database.db import ScinodeDB
from scinode.config.profile import ProfileConfig
import pandas as pd
from scinode.common.log import logging

logger = logging.getLogger("database")

pd.set_option("display.max_rows", 200)


class WorkerClient(ScinodeDB):
    """Class used to query and manipulate the database."""

    def __init__(self) -> None:
        super().__init__()
        self.profile = ProfileConfig()
        self.current_profile = self.profile.get_current_profile()

    def get_data(self, query={}):
        data = list(self.db["worker"].find(query, {"_id": 0}))
        if data is None:
            data = []
        return data

    def get_worker(self, name, computer):
        """Get worker data by name"""
        data = self.get_data()
        for d in data:
            if d["name"] == name and d["computer"] == computer:
                return d
        return None

    def list(self, query={}):
        """List worker"""
        data = self.get_data(query)
        df = pd.DataFrame(data)
        if df.empty:
            print(
                "index",
                "name",
                "computer",
                "workdir",
                "pid",
                "worker",
            )
        else:
            print(
                df[
                    [
                        "index",
                        "name",
                        "computer",
                        "workdir",
                        "pid",
                        "worker",
                    ]
                ]
            )

    def show(self, query={}):
        from scinode.utils.formater import print_key_value, cyan

        data = self.db["worker"].find_one(query)
        if data is None:
            print("Worker with query: {} does not exist".format(query))
            return
        print("")
        print_key_value("Name", cyan(data["name"]))
        print_key_value("Computer", cyan(data["computer"]))
        print_key_value("Concurrency", cyan(data["worker"]))
        print_key_value("Sleep", cyan(data["sleep"]))
        print_key_value("Work Dir", cyan(data["workdir"]))

    def get_status(self, query={}):
        from scinode.utils.daemon import inspect_daemon_status_builtin

        data = self.get_data(query=query)
        if self.current_profile is not None and self.current_profile[
            "engine"
        ].upper() in ["CELERY", "DASK"]:
            from scinode.engine.celery.tasks import app

            reply = app.control.inspect()
            active = reply.active()
            # print(active)
            for d in data:
                worker_name = f"{d['name']}@worker"
                if active is not None and worker_name in active:
                    d["running"] = True
                else:
                    d["running"] = False
        else:
            for d in data:
                running = inspect_daemon_status_builtin(d["name"], d["sleep"])
                d["running"] = running
        return data

    def print_status(self, query={}):
        """Get worker status.
        - First send a message to mq to check the worker status.
        - Daemon recieve the message and update the lastUpdate field in the database.
        - Wait sleep time.
        - Get the lastUpdate time
        """
        from colorama import Fore, Style
        from scinode.utils.emoji import emoji

        print(
            # "{:10s} {:5s} {:5s} {:10s}".format("name", "sleep", "lastUpdate", "running")
            "{:10s} {:10s}".format("name", "running")
        )
        data = self.get_status(query)
        for d in data:
            if d["running"]:
                state_emoji = emoji["check_mark"]
                d["running"] = Fore.GREEN + str(d["running"]) + Style.RESET_ALL
            else:
                state_emoji = emoji["cross_mark"]
                d["running"] = Fore.RED + str(d["running"]) + Style.RESET_ALL
            print(
                "{:10s}".format(d["name"]),
                # "{:5.1f}".format(d["sleep"]),
                # "{:10s}".format(str(d["lastUpdate"])),
                "{:5s}".format(str(d["running"]) + state_emoji),
            )


if __name__ == "__main__":
    d = WorkerClient()
    d.list()
    d.show({"index": 1})
