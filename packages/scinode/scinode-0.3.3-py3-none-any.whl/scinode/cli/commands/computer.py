import click


@click.group(help="CLI tool to manage computers.")
def computer():
    pass


@computer.command(help="Delete computer.")
@click.argument("name")
@click.confirmation_option(
    prompt="This will delete all data for the computer. Are you delete?"
)
def delete(name):
    from scinode.config.computer import ComputerConfig

    p = ComputerConfig()
    p.delete_item(name)


@computer.command(help="Add computer")
@click.option("--file", help="Add computer from file.", type=str)
def add(file):
    import socket
    from scinode.config.computer import ComputerConfig

    p = ComputerConfig()
    if file:
        import json

        with open(file, "r") as f:
            datas = json.load(f)
            datas["activate"] = False
            p.insert_one(datas)
    else:
        name = click.prompt("Label of the computer:", default="localhost")
        hostname = click.prompt("Hostname:", default=socket.gethostname())
        username = click.prompt("Username:")
        password = click.prompt("password:", hide_input=True)
        workdir = click.prompt("Default working directory:")
        datas = {
            "name": name,
            "hostname": hostname,
            "username": username,
            "password": password,
            "workdir": workdir,
        }
        p.add_item(datas)


@computer.command(help="Show computer")
@click.argument("name", default="", type=str)
def show(name):
    from scinode.config.computer import ComputerConfig

    p = ComputerConfig()
    p.show_item(name)


@computer.command(help="list computer")
def list():
    from scinode.config.computer import ComputerConfig

    p = ComputerConfig()
    p.list_items()


@computer.command(help="Test computer")
@click.argument("name", default="", type=str)
def test(name):
    from scinode.config.computer import ComputerConfig

    p = ComputerConfig()
    if p.test(name):
        print(f"Connect to computer {name} successfully!")
    else:
        print(f"Can not connect to computer {name}.")
