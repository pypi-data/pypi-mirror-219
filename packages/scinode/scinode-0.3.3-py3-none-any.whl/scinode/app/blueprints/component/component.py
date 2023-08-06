from flask import Blueprint, render_template, request
from scinode.app.db import db
import pprint

component_bp = Blueprint("component_bp", __name__, template_folder="templates")


# =================================
# componetns
# =================================
@component_bp.route("/")
def components():
    return render_template("component_table.html", title="Component Table")


# get:
@component_bp.route("/<uuid>")
def component_get(uuid):
    from scinode.app.blueprints.component.utils import scinode_to_rete

    query = {"uuid": uuid}
    component_json = db["component"].find_one(query, {"_id": 0})
    # print(list(component_json))
    component_json["real_name"] = component_json["name"]
    component_json["name"] = "Template"
    #
    component_json = scinode_to_rete(component_json)
    #
    nodetree_data = {
        "id": "scinode@0.1.0",
        "nodes": {
            "1": {
                "id": 1,
                "data": {},
                "position": [0, 0],
                "name": component_json["name"],
                "uuid": uuid,
            }
        },
    }
    # print(component_json)
    # print(nodetree_data)
    return render_template(
        "component_editor.html",
        title="Component Editor",
        component_json=component_json,
        nodetree_data=nodetree_data,
    )


# post: creat a new component
@component_bp.route("/", methods=["POST"])
def component_post():
    from scinode.app.build_node_from_json import build_components_from_db
    from scinode.app.blueprints.component.utils import rete_to_scinode
    from scinode.nodes.build_node_from_database import build_nodes_from_db
    import uuid

    data = request.json
    data["uuid"] = str(uuid.uuid4())
    if db["component"].count_documents({"name": data["name"]}) > 0:
        return {
            "success": False,
            "message": "Node: '{}' already registered. \
                    Please choose another name".format(
                data["name"]
            ),
        }
    data = rete_to_scinode(data)
    pprint.pprint(data)
    db["component"].insert_one(data)
    build_components_from_db()
    # build_nodes_from_db()
    return {
        "success": True,
        "message": "Add node '{}' successfully!".format(data["name"]),
        "uuid": data["uuid"],
    }


# put: update component
@component_bp.route("/<uuid>", methods=["PUT"])
def component_put(uuid):
    from scinode.app.build_node_from_json import build_components_from_db
    from scinode.nodes.build_node_from_database import build_nodes_from_db

    data = request.json
    query = {"uuid": uuid}
    newvalues = {"$set": data}
    db["component"].update_one(query, newvalues)
    build_components_from_db()
    build_nodes_from_db()
    return {
        "success": True,
        "message": "Update node '{}' successfully!".format(data["name"]),
        "uuid": data["uuid"],
    }


# delete: delete a component
@component_bp.route("/<uuid>", methods=["DELETE"])
def component_delete(uuid):
    from scinode.app.build_node_from_json import build_components_from_db
    from scinode.nodes.build_node_from_database import build_nodes_from_db
    from scinode.database.db import ScinodeDB

    db = ScinodeDB()
    query = {}
    query["uuid"] = uuid
    db.delete("component", query)
    build_components_from_db()
    build_nodes_from_db()
    return {"message": "Delete component: {} successfully!".format(uuid)}


@component_bp.route("/editor")
def component_editor():
    from scinode.app.build_node_from_json import template
    from scinode.app.blueprints.component.utils import scinode_to_rete

    component_json = template[0]
    # print("component_json: ", component_json)
    component_json = scinode_to_rete(component_json)
    nodetree_data = {
        "id": "scinode@0.1.0",
        "nodes": {"1": {"id": 1, "data": {}, "position": [0, 0], "name": "Template"}},
    }
    pprint.pprint(component_json)
    return render_template(
        "component_editor.html",
        title="Component Editor",
        component_json=component_json,
        nodetree_data=nodetree_data,
    )


@component_bp.route("/api/component_data")
def component_data():
    from scinode.app.db import query_component_data

    query = {}
    query, total_filtered, recordsTotal = query_component_data(
        db["component"], query, request
    )
    # component_data
    component_data = []
    for record in query:
        data = {}
        data["uuid"] = record["uuid"]
        data["name"] = record["name"]
        data["catalog"] = record["metadata"]["catalog"]
        component_data.append(data)
    # print("component_data:", component_data)
    # response
    return {
        "data": component_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@component_bp.route("/importer")
def component_importer():
    return render_template("component_importer.html")


@component_bp.route("importer", methods=["POST"])
def component_importer_api():
    from scinode.app.build_node_from_json import build_components_from_db
    from flask import flash, redirect
    import json
    import uuid

    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    data = json.loads(file.read())
    n = len(data)
    # check name
    # check uuid and name
    for item in data:
        if "uuid" not in item or item["uuid"] == "":
            item["uuid"] = str(uuid.uuid4())
    #
    # print("data: ", data)
    db["component"].insert_many(data)
    build_components_from_db()
    return {
        "success": True,
        "message": "Import {} components successfully!".format(n),
    }


@component_bp.route("/exporter")
def component_exporter():
    return render_template("component_exporter.html")


@component_bp.route("/download", methods=["GET"])
def component_download():
    from flask import Response
    from bson.json_util import dumps

    components = db["component"].find({}, {"_id": 0})
    components = dumps(list(components), indent=2)
    # check if the post request has the file part
    # components.headers['Content-Disposition'] = 'attachment;filename=components.json'
    return Response(
        components,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=components.json"},
    )
