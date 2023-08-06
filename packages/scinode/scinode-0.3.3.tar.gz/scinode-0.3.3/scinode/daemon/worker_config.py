from scinode.database.client import scinodedb
from pathlib import Path
from uuid import uuid1
import datetime
from scinode.config import profile_datas

coll_name = "worker"
default_path = str(Path.home())
# default_path = str(Path.home() / "scinode")


class WorkerConfig:
    """Configuration for a worker."""

    def __init__(
        self,
        name="local",
        uuid=None,
        computer=None,
        workdir=default_path,
        sleep=5,
    ) -> None:
        self.name = name
        self.workdir = workdir
        self.uuid = uuid if uuid else str(uuid1())
        self.sleep = sleep
        self.computer = computer or profile_datas["computer"]

    @property
    def data(self):
        return self.get_data()

    def get_data(self):
        from scinode.database.worker import WorkerClient

        # Load datas from database
        client = WorkerClient()
        data = client.get_data(query={"name": self.name})
        if data is None:
            raise ValueError(f"Daemon {self.name} is not setup.")
        return data[0]

    def to_dict(self):
        data = {
            "name": self.name,
            "computer": self.computer,
            "uuid": self.uuid,
            "workdir": self.workdir,
            "pid": 0,
            "worker": 0,
            "sleep": self.sleep,
            "running": False,
            "lastUpdate": datetime.datetime.utcnow(),
        }
        return data

    def insert(self):
        """Insert the configuration in the database."""
        from scinode.utils.db import insert_one
        from colorama import Fore, Style

        data = scinodedb[coll_name].find_one({"name": self.name})
        if data is not None:
            print(
                Fore.RED
                + f"\n Error! \nDaemon {self.name} is already registered. Please choose another name.\n"
                + Style.RESET_ALL
            )
            return
        data = self.to_dict()
        insert_one(data, scinodedb[coll_name])

    def save(self):
        """Save the configuration in the database."""
        from scinode.utils.db import update_one

        data = self.to_dict()
        update_one(data, scinodedb[coll_name])

    @classmethod
    def from_json(cls, file):
        """Load datas from json file.

        Returns:
            list: a list of the configuration datas.
        """
        import json

        # read file
        with open(file, "r") as f:
            datas = json.load(f)
            d = cls(**datas)
            d.insert()


def init_worker():
    """_summary_"""
    # create a default worker "local" if it does not exist
    if scinodedb["worker"].find_one({"name": "local"}) is None:
        from scinode.daemon.worker_config import WorkerConfig

        config = WorkerConfig(name="local", sleep=1)
        config.insert()
