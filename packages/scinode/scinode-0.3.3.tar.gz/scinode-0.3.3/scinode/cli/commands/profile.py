import click


@click.group(help="CLI tool to manage profiles.")
def profile():
    pass


@profile.command(help="Reset profile.")
@click.confirmation_option(
    prompt="This will delete all data in the database for this profile. Are you reset?"
)
def reset():
    from scinode.database.db import ScinodeDB

    db = ScinodeDB()
    for name in ["nodetree", "node", "daemon", "broker"]:
        db.reset(name)


@profile.command(help="Delete profile.")
@click.argument("name")
@click.confirmation_option(
    prompt="This will delete all data for the profile. Are you delete?"
)
def delete(name):
    from scinode.config.profile import ProfileConfig
    from termcolor import colored

    p = ProfileConfig()
    current_profile = p.get_current_profile()
    if current_profile["name"] == name:
        print(colored("\nYou can't delete the current profile.\n", "red"))
        return
    p.delete_item(name)


@profile.command(help="Add profile")
@click.option("--file", help="Add profile from file.", type=str)
def add(file):
    import socket
    from scinode.config.profile import ProfileConfig
    from pathlib import Path

    p = ProfileConfig()
    if file:
        import json

        with open(file, "r") as f:
            datas = json.load(f)
            datas["current"] = False
            p.add_item(datas)
    else:
        name = click.prompt("Name of the profile:", default="scinode")
        computer = click.prompt("Name of the computer:", default=socket.gethostname())
        db_address = click.prompt(
            "Address of mongodb service:", default="mongodb://localhost:27017/"
        )
        db_name = click.prompt("Name of the database:", default="scinode_db")
        file_db = click.prompt(
            "Backend of large data",
            type=click.Choice(["gridfs", "disk"], case_sensitive=False),
            default="gridfs",
        )
        default_config_path = str(Path.home() / ".scinode")
        config_path = click.prompt(
            "Default configuration directory:", default=default_config_path
        )
        engine = click.prompt(
            "Engine:",
            type=click.Choice(["Concurrent", "Celery"], case_sensitive=False),
            default="Concurrent",
        )
        if engine.upper() == "CELERY":
            broker_url = click.prompt(
                "Address of rabbitmq service:", default="amqp://localhost//"
            )
        else:
            broker_url = "amqp://localhost//"
        datas = {
            "name": name,
            "computer": computer,
            "db_address": db_address,
            "db_name": db_name,
            "file_db": file_db,
            "config_path": config_path,
            "engine": engine,
            "broker_url": broker_url,
            "activate": False,
        }
        p.add_item(datas)


@profile.command(help="Show profile")
@click.argument("name", default="", type=str)
@click.pass_context
def show(ctx, name):
    ctx.obj.profile.show_item(name)


@profile.command(help="list profile")
def list():
    from scinode.config.profile import ProfileConfig

    p = ProfileConfig()
    p.list_items()


@profile.command(help="use profile")
@click.argument("name")
def use(name):
    from scinode.config.profile import ProfileConfig

    p = ProfileConfig()
    p.set_current_profile(name)
