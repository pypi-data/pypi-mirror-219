from flask import Blueprint, render_template, request
from scinode.app.db import db
from flask import make_response


data_bp = Blueprint("data_bp", __name__, template_folder="templates")


@data_bp.route("/")
def datas():
    return render_template("data_table.html", title="Node Table")


@data_bp.route("/api/socket_data")
def socket_data():
    from scinode.app.db import query_socket_data

    query = {}
    query, total_filtered, recordsTotal = query_socket_data(db["data"], query, request)
    # socket_data
    socket_data = []
    for record in query:
        data = {}
        data["index"] = record["index"]
        data["uuid"] = record["uuid"]
        data["name"] = record["name"]
        data["identifier"] = record.get("identifier", "")
        socket_data.append(data)
    # print("socket_data:", socket_data)
    # response
    return {
        "data": socket_data,
        "recordsFiltered": total_filtered,
        "recordsTotal": recordsTotal,
        "draw": request.args.get("draw", type=int),
    }


@data_bp.route("/<uuid>")
def node_get(uuid):
    """Get node data

    Args:
        uuid (str): uuid of the node

    Returns:
        _type_: _description_
    """
    from scinode.utils.node import get_socket_data

    result = get_socket_data({"uuid": uuid})
    # change to string for display
    if result["identifier"] in ["General"]:
        result["value"] = str(result["value"])
    print("result: ", result)
    return render_template("data_viewer.html", title="Data", socket_data=result)


@data_bp.route("/<uuid>.cif")
def download_file(uuid):
    # Generate your text file (replace with your own logic)
    from scinode.utils.node import get_socket_data
    from ase.io.cif import write_cif_image
    from io import StringIO

    s = StringIO()
    results = get_socket_data({"uuid": uuid})
    atoms = results["value"]
    atoms.pbc = True
    print("atoms: ", atoms)
    write_cif_image("", atoms, s, wrap=True, labels=None, loop_keys={})
    # Create a response object with the file data
    text = s.getvalue()
    # print("cif text: ", text)
    response = make_response(text)
    # Set the headers to force download and set filename
    response.headers.set("Content-Disposition", "attachment", filename="file.cif")
    response.headers.set("Content-Type", "text/plain")
    # Return the response object
    return response
