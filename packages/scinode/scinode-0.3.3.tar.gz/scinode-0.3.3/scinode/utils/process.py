def read_pid(pidfile: str) -> int or None:
    """Read a pid file and return the pid."""
    try:
        with open(pidfile, "r") as f:
            pid = int(f.read().strip())
        return pid
    except IOError:
        return None


def is_pid_running(pid: int) -> bool:
    """Check the status of a pid, return True if the process is running"""
    import psutil

    if psutil.pid_exists(pid):
        return True
    else:
        return False


def is_process_running(pidfile: str) -> bool:
    """Check if the process is running by reading the pid file"""
    pid = read_pid(pidfile)
    if pid:
        return is_pid_running(pid)
    else:
        return False


def stop_process(pid: int) -> bool:
    """Stop the process by pid"""
    import os
    import signal

    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    pid = read_pid("~/.scinode/web.pid")
    print("pid: ", pid)
