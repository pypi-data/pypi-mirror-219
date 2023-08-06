"""
Original from https://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
Generic linux daemon base class for python 3.x.
"""

import sys
import os
import time
import atexit
import signal
import datetime


class BaseDaemon:
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method.
    """

    coll_name = "daemon"

    def __init__(self, logfile):
        self.logfile = logfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""
        # print("Daemonize...")
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("fork #1 failed: {0}\n".format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write("fork #2 failed: {0}\n".format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.logfile, "w+")
        so = open(self.logfile, "a+")
        se = open(self.logfile, "a+")

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

    def delpid(self):
        os.remove(self.pidfile)

    def pid_exists(self):
        import psutil

        pid = self.get_pid()
        if psutil.pid_exists(pid):
            return 0
        else:
            return 1

    def start(self, daemonize=True):
        """Start the daemon."""
        status = self.pid_exists()
        if status == 0:
            message = "Daemon {} already running?\n".format(self.name)
            sys.stderr.write(message)
            sys.exit(1)
        # Start the daemon
        # print("Starting the daemon...")
        if daemonize:
            self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""
        print(f"Stop {self.name}...")
        status = self.pid_exists()
        pid = self.get_pid()
        if status != 0:
            message = "Daemon {} not running?\n".format(self.name)
            sys.stderr.write(message)
            return
        # print("Daemon running on pid: {}".format(pid))
        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") < 0:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().
        """
        pass

    def showlog(self, limit=100):
        with open(self.logfile) as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                print(line.strip())

    def update_data(self):
        """Update data in the database.
        - pid
        - sleep
        """
        from scinode.utils.db import update_one
        from scinode.database.client import scinodedb

        pid = os.getpid()
        data = {
            "name": self.name,
            "pid": pid,
            "sleep": self.sleep,
            "lastUpdate": datetime.datetime.utcnow(),
        }
        update_one(data, scinodedb[self.coll_name], key="name")

    @property
    def data(self):
        from scinode.database.client import scinodedb

        data = scinodedb[self.coll_name].find_one({"name": self.name})
        return data

    @property
    def lastUpdate(self):
        return self.get_lastUpdate()

    def get_lastUpdate(self):
        dt = (datetime.datetime.utcnow() - self.data["lastUpdate"]).total_seconds()
        return dt

    def get_pid(self):
        data = self.data
        pid = data.get("pid", 0)
        # print("name: {}, pid: {}".format(self.name, pid))
        return pid

    def inspect_status(self):
        from scinode.utils.daemon import inspect_daemon_status

        data, running = inspect_daemon_status(self.name)
        return data, running
