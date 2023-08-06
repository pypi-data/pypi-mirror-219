import click
from pathlib import Path
from colorama import Fore, Style


def worker_not_exist(name, computer):
    return (
        Fore.RED
        + "Error!!! Worker {}@{} is not setup.\n".format(name, computer)
        + Style.RESET_ALL
    )


def start_worker(
    ctx, name, data, pool=None, concurrency=None, sleep=None, foreground=None
):
    print(f"Start worker: {name}")
    if ctx.obj.engine == "CELERY":
        from scinode.engine.celery.worker import CeleryWorker

        kwargs = {}
        kwargs["queue"] = name
        if concurrency:
            kwargs["concurrency"] = concurrency
        if pool:
            kwargs["pool"] = pool
        worker = CeleryWorker(name=name, **kwargs)
        worker.start()
    else:
        from scinode.daemon.worker import DaemonWorker

        worker = DaemonWorker(name, pool=pool, concurrency=concurrency, sleep=sleep)
        print("Start worker {}, idle time: {}".format(worker.name, sleep))
        if foreground:
            worker.run()
        else:
            worker.start()


@click.group(help="CLI tool to manage Worker.")
def worker():
    pass


@worker.command(help="Start the worker.")
@click.argument("name", default="broker", type=str)
@click.option(
    "-p",
    "--pool",
    type=click.Choice(
        ["prefork", "thread", "process", "gevent", "eventlet"], case_sensitive=False
    ),
    default="thread",
)
@click.option("-c", "--concurrency", help="concurrency", type=int)
@click.option("--foreground", is_flag=True, default=False, help="Use foreground mode")
@click.option("-s", "--sleep", default=1, help="Idle sleep time")
@click.pass_context
def start(ctx, name, pool, concurrency, foreground, sleep):
    """Start worker instance.

    Examples
    --------

    scinode worker start local --concurrency=100 --pool eventlet
    """
    from scinode.database.client import scinodedb
    from scinode.database.worker import WorkerClient

    computer = ctx.obj.current_profile["computer"]
    data = scinodedb["worker"].find_one({"name": name, "computer": computer})
    if data is None:
        print(worker_not_exist(name, computer))
        print("Please setup a new one or choose worker from:")
        client = WorkerClient()
        client.show({"computer": computer})
        return
    start_worker(
        ctx,
        name,
        data,
        pool=pool,
        concurrency=concurrency,
        foreground=foreground,
        sleep=sleep,
    )


@worker.command(help="Stop the worker.")
@click.argument("name", default="broker", type=str)
@click.option("--computer", help="Computer", type=str)
@click.pass_context
def stop(ctx, name, computer=None):
    from scinode.database.worker import WorkerClient

    worker_client = WorkerClient()
    if not computer:
        computer = ctx.obj.current_profile["computer"]
    data = worker_client.get_worker(name, computer)
    if data is None:
        print(worker_not_exist(name, computer))
    if ctx.obj.engine == "CELERY":
        ctx.obj.app.control.broadcast("shutdown", destination=[f"{name}@worker"])
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},worker,STOP")


@worker.command(help="Stop all worker.")
@click.pass_context
def stop_all(ctx):
    if ctx.obj.engine == "CELERY":
        ctx.obj.app.control.broadcast("shutdown")
    else:
        from scinode.utils.db import push_message
        from scinode.database.worker import WorkerClient

        worker = WorkerClient()
        data = worker.get_data()
        for d in data:
            push_message(d["name"], f"{d['name']},worker,STOP")


@worker.command(help="Restart the worker.")
@click.argument("name", default="broker", type=str)
@click.option("--computer", help="Computer", type=str)
@click.pass_context
def restart(ctx, name, computer=None):
    from scinode.database.worker import WorkerClient

    worker_client = WorkerClient()
    if not computer:
        computer = ctx.obj.current_profile["computer"]
    data = worker_client.get_worker(name, computer)
    if data is None:
        print(worker_not_exist(name, computer))
    if ctx.obj.engine == "CELERY":
        ctx.obj.app.control.broadcast("pool_restart", destination=[f"{name}@worker"])
    else:
        from scinode.utils.db import push_message

        push_message(name, f"{name},worker,RESTART")


@worker.command(help="Restart the worker.")
@click.argument("name", default="broker", type=str)
@click.option(
    "--pool",
    type=click.Choice(["thread", "process", "celery"], case_sensitive=False),
    default="thread",
)
@click.option("--concurrency", default=0, help="Sleep time")
@click.option("--sleep", default=1, help="Idle sleep time")
def hard_restart(name, pool, concurrency, sleep):
    from scinode.daemon.worker import DaemonWorker

    worker = DaemonWorker(name, pool=pool, concurrency=concurrency, sleep=sleep)
    worker.restart()


@worker.command(help="Show the log file of the worker.")
@click.option("--limit", help="Number of lines to be shown.", default=100, type=int)
@click.argument("name", default="broker", type=str)
def log(name, limit):
    from scinode.daemon.worker import DaemonWorker

    worker = DaemonWorker(name=name)
    worker.showlog(limit)


@worker.command(help="Add new worker.")
@click.option("--file", help="Read configuration from file.", type=str)
@click.pass_context
def add(ctx, file):
    from scinode.daemon.worker_config import WorkerConfig

    if file:
        WorkerConfig.from_json(file)
    else:
        name = click.prompt("Name of this worker:", default="local")
        default_path = str(Path.home() / "scinode")
        workdir = click.prompt("Default working directory:", default=default_path)
        if ctx.obj.engine == "CELERY":
            config = WorkerConfig(name=name, workdir=workdir)
            config.insert()
        else:
            sleep = click.prompt("Idle time:", default=1, type=float)
            config = WorkerConfig(name=name, workdir=workdir, sleep=sleep)
            config.insert()


@worker.command(help="Delete workers.")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete the workers?")
def delete(name):
    from scinode.daemon.worker import DaemonWorker
    from scinode.database.client import scinodedb
    from scinode.database.worker import WorkerClient
    import datetime

    client = WorkerClient()
    query = {"name": name}
    datas = scinodedb["worker"].find_one(query, {"_id": 0})
    worker = DaemonWorker(name=datas["name"])
    d = worker.data
    t = int((datetime.datetime.utcnow() - d["lastUpdate"]).total_seconds())
    if t < 2 * d["sleep"]:
        print(
            "Worker {} is likely running now. Please stop it first.".format(
                datas["name"]
            )
        )
    else:
        client.delete("worker", {"name": datas["name"]})


@worker.command(help="List workers.")
@click.option("--name", help="Name of the item.")
@click.option("--index", help="Index of the item.", type=int)
@click.option("--uuid", help="uuid of the item.")
@click.option("--state", help="state of the item.")
def list(name, index, uuid, state):
    from scinode.database.worker import WorkerClient

    client = WorkerClient()
    query = {}
    if name:
        query["name"] = name
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    if state:
        query["state"] = state
    client.list(query)


@worker.command(help="Show the data of a worker.")
@click.argument("name", default="broker", type=str)
def show(name):
    from scinode.database.worker import WorkerClient

    client = WorkerClient()
    query = {}
    query["name"] = name
    client.show(query)


@worker.command(help="Show the status of a worker.")
@click.option("-n", "--name", help="Name of the item.")
@click.pass_context
def status(ctx, name):
    from scinode.database.worker import WorkerClient

    worker_client = WorkerClient()
    query = {}
    if name:
        query["name"] = name
    worker_client.print_status(query)


@worker.command(help="Edit the data of a worker.")
@click.argument("name", type=str)
def edit(name):
    from scinode.daemon.worker_config import WorkerConfig
    import yaml

    worker = WorkerConfig(name=name)
    data = worker.data
    data.pop("lastUpdate", None)
    old_text = yaml.dump(data, sort_keys=False)
    new_text = click.edit(old_text, extension=".toml")
    # print(new_text)
    if new_text:
        data = yaml.safe_load(new_text)
        for key, value in data.items():
            setattr(worker, key, value)
        worker.save()
        click.secho(f"Edit worker {name} successfully!", fg="green")
