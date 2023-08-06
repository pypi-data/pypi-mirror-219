import os
import sys
from pathlib import Path
from scinode.daemon.daemon import BaseDaemon
from scinode.engine.mq import MQ
from scinode.config.profile import profile_datas

home = Path.home()


class DaemonScheduler(BaseDaemon):
    """Daemon for scheduler.

    name: str
        Name of the daemon.
    sleep: float
        Time interval to fetch data. Default 0.1

    """

    coll_name = "scheduler"

    def __init__(self, name, sleep=None):
        self.name = name
        self.sleep = sleep if sleep is not None else self.data["sleep"]
        logfile = os.path.join(
            home, ".scinode/scheduler-{}.log".format(profile_datas["name"])
        )
        super().__init__(logfile)
        # add sys path
        sys.path.append(os.path.join(profile_datas["config_path"], "custom_node"))

    def run(self):
        """"""
        import time
        from scinode.database.client import scinodedb
        from scinode.engine.scheduler import EngineScheduler
        from scinode.utils.emoji import logo

        print(logo)

        self.db = scinodedb
        self.update_data()
        #
        mq = MQ(name=self.name)
        es = EngineScheduler(queue=mq)
        step = 0
        while True:
            print("{} {}".format(self.name, step))
            # --------------------------------------------------
            es.consume_messages()
            # f.close()
            step += 1
            time.sleep(self.sleep)


def init_scheduler():
    """Initialize scheduler."""

    daemon = DaemonScheduler("local")
    daemon.start(daemonize=False)


if __name__ == "__main__":
    daemon = DaemonScheduler("local")
    daemon.start(daemonize=False)
