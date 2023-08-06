import click


@click.group(help="CLI tool to manage data.")
def data():
    pass


@data.command(help="Show data.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--identifier", help="Identifier of the item.", type=str)
@click.option("-c", "--column", help="columns of the item.", default="", type=str)
@click.option("--uuid", help="uuid of the item.")
@click.option("--limit", help="Limit of the item.", type=int, default=100)
def list(name, identifier, column, uuid, limit):
    from scinode.database.data import DataClient

    client = DataClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if identifier:
        query["identifier"] = identifier
    if uuid:
        query["uuid"] = uuid
    client.list(query, column, limit)


@data.command(help="Show the item.")
@click.argument("index", type=str)
@click.option("--all", is_flag=True, help="All the data.")
def show(index, all):
    from scinode.database.data import DataClient

    client = DataClient()
    query = {}
    if "-" in index:
        query["uuid"] = index
    else:
        query["index"] = int(index)
    client.show(query, all=all)


@data.command(help="Delete datas.")
@click.option("-n", "--name", help="Name of the item.")
@click.option("-i", "--index", help="Index of the item.", type=int)
@click.option("--uuid", help="uuid of the item.")
@click.confirmation_option(prompt="Are you sure you want to delete the items?")
def delete(name, index, uuid):
    from scinode.database.data import DataClient

    client = DataClient()
    query = {}
    if name:
        query["name"] = {"$regex": name}
    if index:
        query["index"] = index
    if uuid:
        query["uuid"] = uuid
    client.delete("data", query)
