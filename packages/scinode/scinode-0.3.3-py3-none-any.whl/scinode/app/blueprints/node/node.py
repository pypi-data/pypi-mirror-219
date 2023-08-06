from flask import Blueprint, render_template, request
from scinode.app.db import db

node_bp = Blueprint("node_bp", __name__, template_folder="templates")


@node_bp.route("/")
def nodes():
    return render_template("node_table.html", title="Node Table")


@node_bp.route("/api/node_data")
def node_data():
    from scinode.app.db import query_node_data

    query = {}
    query, total_filtered, recordsTotal = query_node_data(db["node"], query, request)
    # node_data
    node_data = []
    for record in query:
        data = {}
        data["index"] = record["index"]
        data["uuid"] = record["uuid"]
        data["name"] = record["metadata"]["identifier"]
        data["state"] = record["state"]
        data["action"] = record["action"]
        node_data.append(data)
    # print("node_data:", node_data)
    # response
    return {
        "data": node_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@node_bp.route("/<uuid>")
def node_get(uuid):
    """Get node data

    Args:
        uuid (str): uuid of the node

    Returns:
        _type_: _description_
    """
    from scinode.utils.node import get_results

    query = {"uuid": uuid}
    query = db["node"].find(query, {"_id": 0})
    # node_data
    node_data = list(query)[0]
    # print(node_data)
    node_data["properties"] = node_data["properties"]
    #
    results = get_results(uuid)
    node_data["results"] = results
    # change to string for display
    node_data["properties"] = node_data["properties"]
    for key, p in node_data["properties"].items():
        p["value"] = str(p["value"])
    node_data["results"] = []
    for data in results:
        data = {"name": data["name"], "value": data["value"]}
        node_data["results"].append(str(data))
    # remove node_class and executor
    node_data.pop("node_class")
    node_data.pop("executor")
    # print(node_data["results"])
    return render_template("node_viewer.html", title="Node", node_data=node_data)


@node_bp.route("/edit/<uuid>")
def node_edit(uuid):
    """Edit node data

    Args:
        uuid (str): uuid of the node

    Returns:
        _type_: _description_
    """
    from scinode.database.node import NodeClient

    client = NodeClient()
    query = {"uuid": uuid}
    current_node, data = client.get_yaml_data(query)
    # print("current_node:", current_node)
    return current_node


@node_bp.route("/edit/<uuid>", methods=["POST"])
def node_edit_post(uuid):
    """Save edited node data

    Args:
        uuid (str): uuid of the node

    Returns:
        _type_: _description_
    """
    from scinode.orm.db_nodetree import DBNodeTree
    from scinode.app.utils.rete_adapter import properties_to_show_str

    data = request.json
    nt = DBNodeTree(uuid=data["nodetree_uuid"])
    ndata = nt.edit_node_from_yaml(uuid=data["uuid"], string=data["node_edit"])
    ndata = properties_to_show_str(ndata["properties"])
    # print("ndata:", ndata)
    msg = f'Edit node {data["name"]} successfully!'
    return {"message": msg, "node_data": ndata}


# put: put a nodetree
@node_bp.route("/<uuid>", methods=["PUT"])
def node_put(uuid):
    items = request.json
    query = {"uuid": uuid}
    newvalues = {"$set": items}
    db["node"].update_one(query, newvalues)
    return {"message": True}


# delete: delete a node
@node_bp.route("/<uuid>", methods=["DELETE"])
def node_delete(uuid):
    query = {"uuid": uuid}
    print(query)
    db["node"].delete_one(query)
    return {"message": "Delete nodet: {} successfully!".format(uuid)}
