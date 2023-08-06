#!/usr/bin/env python
import pkg_resources
import click
from scinode.config.profile import ProfileConfig
import os


class CLIContext:
    """Context Object for the CLI."""

    def __init__(self, app=None):
        """Initialize the CLI context."""
        self.profile = ProfileConfig()
        self.current_profile = self.profile.get_current_profile()
        self.app = app
        self.engine = self.current_profile["engine"].upper()
        if self.engine == "CELERY":
            from scinode.engine.celery.tasks import app

            self.app = app


@click.group(help="CLI tool to manage SciNode")
@click.pass_context
def scinode(ctx):
    ctx.obj = CLIContext()


@scinode.command(help="Start the services.")
@click.option("--web", is_flag=True, default=True, help="Start web service")
@click.pass_context
def start(ctx, web):
    """Start scinode services.

    Examples
    --------

    scinode start
    """
    import os
    from scinode.config import init_scinode_configuration
    from scinode.daemon.worker_config import init_worker
    from scinode.daemon.scheduler_config import init_scheduler
    from scinode.utils.emoji import logo
    from scinode.version import __version__
    from scinode.utils.formater import green, red, cyan

    print(logo)
    print("Version: {}".format(__version__))
    print("Engine: {}\n".format(ctx.obj.engine))
    print("Initializing configuration")
    init_scinode_configuration()
    print("Initializing scheduler")
    init_scheduler()
    print("Initializing worker\n")
    init_worker()
    print("Starting Scinode Services:")
    os.system("scinode scheduler start")
    os.system("scinode worker start local")
    if web:
        print("Starting Web App:")
        os.system(
            "nohup scinode web start > ~/.scinode/web.log & echo $! > ~/.scinode/web.pid &"
        )
    print("\nScinode status:")
    os.system("scinode status")


@scinode.command(help="Stop the services.")
@click.pass_context
def stop(ctx):
    """Stop scinode services.

    Examples
    --------

    scinode stop
    """

    print("Sotp Scheduler...")
    os.system("scinode scheduler stop")
    print("Stop Workers...")
    os.system("scinode worker stop-all")
    print("Stop Web...")
    os.system("scinode web stop")


@scinode.command(help="Start the services.")
@click.pass_context
def restart(ctx):
    """Restart scinode services.

    Examples
    --------

    scinode restart
    """
    import os

    os.system("scinode stop")
    os.system("scinode start")


@scinode.command(help="Show the status of scinode.")
@click.pass_context
def status(ctx):
    """Show the status of scinode.
    - database
    - rabbitmq if needed
    - scheduler
    - workers
    - web app

    Args:
        ctx (_type_): _description_
    """
    from scinode.database.client import get_db_status
    from scinode.utils.daemon import (
        inspect_daemon_status_celery,
        inspect_daemon_status_builtin,
    )
    from scinode.utils.formater import print_key_value, green, red, cyan
    import os

    print_key_value("Engine: ", cyan(ctx.obj.engine))
    try:
        db_active = get_db_status()
    except Exception:
        print_key_value("Database", red("Can not connect."))
        print(
            "Please set the database connection in the profile, or edit it directly in ~/.scinode/profile.json"
        )
        return
    else:
        if db_active:
            print_key_value("Database", green("Connected"))
        else:
            print_key_value("Database", red("Can not connect."))
            print(
                "Please set the database connection in the profile, or edit it directly in ~/.scinode/profile.json"
            )
            return
    if ctx.obj.engine == "CELERY":
        scheduler_activate = inspect_daemon_status_celery("scheduler@worker")
    else:
        scheduler_activate = inspect_daemon_status_builtin(
            "scheduler", sleep=2, daemon_type="scheduler"
        )
    if scheduler_activate:
        print_key_value("Scheduler", green("running"))
    else:
        print_key_value("Scheduler", red("is not active."))
    os.system("scinode web status")
    print("-" * 30)
    if db_active:
        print("Workers: ")
        os.system("scinode worker status")
    else:
        print_key_value("Workers", red("Can not connect."))
    print("-" * 30)


def load_entry_point():
    for entry_point in pkg_resources.iter_entry_points("scinode_cli"):
        scinode.add_command(entry_point.load())


load_entry_point()

if __name__ == "__main__":
    scinode()
