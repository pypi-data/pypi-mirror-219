from flask import Blueprint, render_template, request
from scinode.app.db import db

template_bp = Blueprint("template_bp", __name__, template_folder="templates")


# =================================
# template
# =================================
@template_bp.route("/")
def templates():
    return render_template("template_table.html", title="template Table")


# post: creat a new template
@template_bp.route("/", methods=["POST"])
def template_post():
    import uuid, pickle
    from scinode.utils.node import insert_one

    data = request.json
    nodetree_record = db["nodetree"].find_one({"uuid": data["uuid"]}, {"_id": 0})
    nodetree_record["uuid"] = str(uuid.uuid4())
    # remove data
    nodetree_record["state"] = "CREATED"
    # save nodes
    for name, node in nodetree_record["nodes"].items():
        node_record = db["node"].find_one({"uuid": node["uuid"]}, {"_id": 0})
        node_record["uuid"] = str(uuid.uuid4())
        node_record["results"] = pickle.dumps({})
        insert_one(node_record, db["template_node"])
        node["uuid"] = node_record["uuid"]
    insert_one(nodetree_record, db["template_nodetree"])
    return {"uuid": nodetree_record["uuid"]}


# get:
@template_bp.route("/<uuid>")
def template_get(uuid):
    from scinode.app.utils.rete_adapter import ReteAdaptor

    query = {"uuid": uuid}
    nodetree_data = ReteAdaptor.getEditor(query, db, is_template=True)
    # print(template_data)
    return render_template(
        "nodetree_editor.html", title="Nodetree", nodetree_data=nodetree_data
    )


# delete: delete a template
@template_bp.route("/<uuid>", methods=["DELETE"])
def template_delete(uuid):
    query = {}
    query["uuid"] = uuid
    db["template_nodetree"].delete_one(query)
    return {"message": True}


@template_bp.route("/api/template_data")
def template_data():
    from scinode.app.db import query_template_data

    query = {}
    query, total_filtered, recordsTotal = query_template_data(
        db["template_nodetree"], query, request
    )
    # template_data
    template_data = list(query)
    for data in template_data:
        data["worker_name"] = data["metadata"]["worker_name"]
    # response
    return {
        "data": template_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }
