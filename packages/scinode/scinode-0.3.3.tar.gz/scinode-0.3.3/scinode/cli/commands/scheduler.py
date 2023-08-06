import click
from pathlib import Path
from colorama import Fore, Style


def scheduler_not_exist(name, computer):
    return (
        Fore.RED
        + "Error!!! Scheduler {}@{} is not setup.\n".format(name, computer)
        + Style.RESET_ALL
    )


def start_scheduler(ctx, name, sleep=None, foreground=None):
    print(f"Start scheduler: {name}")
    if ctx.obj.engine == "CELERY":
        from scinode.engine.celery.worker import CeleryWorker

        kwargs = {}
        kwargs["queue"] = "scheduler"
        kwargs["concurrency"] = 1
        scheduler = CeleryWorker(name=name, **kwargs)
        scheduler.start()
    else:
        from scinode.daemon.scheduler import DaemonScheduler

        scheduler = DaemonScheduler(name, sleep=sleep)
        if foreground:
            scheduler.run()
        else:
            scheduler.start()


@click.group(help="CLI tool to manage Scheduler.")
def scheduler():
    pass


@scheduler.command(help="Start the scheduler.")
@click.argument("name", default="scheduler", type=str)
@click.option("--foreground", is_flag=True, default=False, help="Use foreground mode")
@click.option("-s", "--sleep", default=0.05, help="Sleep time")
@click.pass_context
def start(ctx, name, foreground, sleep):
    """Start scheduler.

    Examples
    --------

    scinode scheduler start
    """
    start_scheduler(
        ctx,
        name,
        foreground=foreground,
        sleep=sleep,
    )


@scheduler.command(help="Stop the scheduler.")
@click.argument("name", default="scheduler", type=str)
@click.pass_context
def stop(ctx, name):
    if ctx.obj.engine == "CELERY":
        ctx.obj.app.control.broadcast("shutdown", destination=[name])
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},scheduler,STOP")


@scheduler.command(help="Restart the scheduler.")
@click.argument("name", default="scheduler", type=str)
@click.pass_context
def restart(ctx, name, computer=None):
    if ctx.obj.engine == "CELERY":
        ctx.obj.app.control.broadcast("pool_restart", destination=[name])
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},scheduler,RESTART")


@scheduler.command(help="Restart the scheduler.")
@click.argument("name", default="scheduler", type=str)
@click.option("--sleep", default=0.01, help="Sleep time")
def hard_restart(name, pool, concurrency, sleep):
    from scinode.daemon.scheduler import DaemonScheduler

    scheduler = DaemonScheduler(name, pool=pool, concurrency=concurrency, sleep=sleep)
    scheduler.restart()


@scheduler.command(help="Show the log file of the scheduler.")
@click.option("--limit", help="Number of lines to be shown.", default=100, type=int)
@click.argument("name", default="scheduler", type=str)
def log(name, limit):
    from scinode.daemon.scheduler import DaemonScheduler

    scheduler = DaemonScheduler(name=name)
    scheduler.showlog(limit)


@scheduler.command(help="Show the status of the scheduler.")
@click.pass_context
def status(ctx):
    from scinode.utils.daemon import (
        inspect_daemon_status_celery,
        inspect_daemon_status_builtin,
    )

    if ctx.obj.current_profile is not None and ctx.obj.current_profile["celery"]:
        scheduler_current = inspect_daemon_status_celery("scheduler")
    else:
        scheduler_current = inspect_daemon_status_builtin(
            "scheduler", sleep=2, daemon_type="scheduler"
        )
    print("Scheduler: {}".format(scheduler_current))
