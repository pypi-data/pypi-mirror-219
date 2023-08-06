def load_nodetree(index):
    from scinode.database.client import scinodedb
    from scinode import NodeTree

    if isinstance(index, int):
        ntdata = scinodedb["nodetree"].find_one({"index": index}, {"_id": 0, "uuid": 1})
        nt = NodeTree.load(uuid=ntdata["uuid"])
        return nt
    elif isinstance(index, str):
        nt = NodeTree.load(uuid=index)
        return nt


def get_nt_full_data(query):
    from scinode.database.client import scinodedb
    from scinode.utils.node import get_node_data

    ntdata = scinodedb["nodetree"].find_one(query)
    nodes = {}
    for name, node in ntdata["nodes"].items():
        nodes[name] = get_node_data({"uuid": node["uuid"]}, {})
    ntdata["nodes"] = nodes
    return ntdata


def get_nt_short_data(ntdata):
    from copy import deepcopy

    ntdata_short = deepcopy(ntdata)
    for name, node in ntdata["nodes"].items():
        if node["metadata"]["node_type"] in ["REF"]:
            node["state"] = "FINISHED"
            node["action"] = "NONE"
        ntdata_short["nodes"][name] = {
            "name": node["name"],
            "identifier": node["metadata"]["identifier"],
            "node_type": node["metadata"]["node_type"],
            "register_path": node["metadata"]["register_path"],
            "uuid": node["uuid"],
            "state": node["state"],
            "action": node["action"],
            "worker": node["metadata"]["worker_name"],
            "counter": node["metadata"]["counter"],
        }
    return ntdata_short


def nt_export_py(ntdata):
    from scinode.utils.node import deserialize

    # print("ntdata: ", ntdata)
    s = """
from scinode import NodeTree
nt = NodeTree(name="{}", uuid="{}")
""".format(
        ntdata["name"], ntdata["uuid"]
    )
    # nodes
    for name, node in ntdata["nodes"].items():
        # print("node: ", node)
        s += """
node = nt.nodes.new("{}", "{}")
""".format(
            node["metadata"]["identifier"], node["name"]
        )
        # set node properties
        properties = deserialize(node["properties"])
        for name, p in properties.items():
            # print("\np: ", p)
            if p["value"] == "":
                continue
            if p["type"] in ["String", "Enum"]:
                s += """node.properties["{}"].value = "{}"
""".format(
                    p["name"], p["value"]
                )
            else:
                s += """node.properties["{}"].value = {}
""".format(
                    p["name"], p["value"]
                )

    # links
    for link in ntdata["links"]:
        s += """
nt.links.new(nt.nodes["{}"].outputs["{}"], nt.nodes["{}"].inputs["{}"])""".format(
            link["from_node"],
            link["from_socket"],
            link["to_node"],
            link["to_socket"],
        )

    # launch
    s += """
nt.launch()
"""
    return s


def to_edit_dict(ntdata):
    """Export to edit dict

    Args:
        ntdata (_type_): _description_

    Returns:
        _type_: _description_
    """
    from scinode.utils.node import to_edit_dict

    # print("ntdata: ", ntdata)
    data = {
        "name": ntdata["name"],
        "uuid": ntdata["uuid"],
        "state": ntdata["state"],
        "action": ntdata["action"],
        "description": ntdata["description"],
        "metadata": {
            "version": ntdata["version"],
            "platform": ntdata["metadata"]["platform"],
            "worker_name": ntdata["metadata"]["worker_name"],
        },
    }
    # nodes
    data["nodes"] = []
    for name, node in ntdata["nodes"].items():
        nd = to_edit_dict(node)
        data["nodes"].append(nd)
    return data


def to_show_dict(ntdata):
    """Export to show dict.

    Args:
        ntdata (_type_): _description_

    Returns:
        _type_: _description_
    """
    from scinode.utils.node import to_show_dict

    # print("ntdata: ", ntdata)
    data = {
        "name": ntdata["name"],
        "uuid": ntdata["uuid"],
        "state": ntdata["state"],
        "action": ntdata["action"],
        "description": ntdata["description"],
        "metadata": {
            "version": ntdata["version"],
            "platform": ntdata["metadata"]["platform"],
            "worker_name": ntdata["metadata"]["worker_name"],
        },
    }
    # nodes
    data["nodes"] = []
    for name, node in ntdata["nodes"].items():
        nd = to_show_dict(node)
        data["nodes"].append(nd)
    return data


def nt_export_yaml(ntdata):
    import yaml

    ntdata = to_show_dict(ntdata)
    s = yaml.dump(ntdata, sort_keys=False)
    return s


def nt_export_yaml_string(ntdata):

    # print("ntdata: ", ntdata)
    s = f"""
name: {ntdata["name"]}
uuid: {ntdata["uuid"]}
state: {ntdata["state"]}
action: {ntdata["action"]}
description: {ntdata["description"]}
metadata:
  version: {ntdata["version"]}
  platform: {ntdata["metadata"]["platform"]}
  worker_name: {ntdata["metadata"]["worker_name"]}
"""
    # nodes
    s += """nodes:"""
    for name, node in ntdata["nodes"].items():
        # print("node: ", node)
        s += f"""
  - identifier: {node["metadata"]["identifier"]}
    uuid: {node["uuid"]}
    name: {node["name"]}
    state: {node["state"]}
    action: {node["action"]}
"""
        # set node properties
        properties = node.get("properties")
        if properties:
            s += """    properties:"""
        for name, p in properties.items():
            s += f"""
      {p["name"]}: {p["value"]}"""
    # links
    s += """links:"""
    for link in ntdata["links"]:
        s += f"""
  - from_node: {link["from_node"]}
    from_socket: {link["from_socket"]}
    to_node: {link["to_node"]}
    to_socket: {link["to_socket"]}"""
    return s


def nt_export(query, format="yaml", filename=None):
    """Export nodetree to yaml or python

    Args:
        query (_type_): _description_
        filename (_type_, optional): _description_. Defaults to None.
    """
    ntdata = get_nt_full_data(query)
    if format.upper() == "PYTHON":
        s = nt_export_py(ntdata)
    else:
        s = nt_export_yaml(ntdata)
    if filename:
        with open(filename, "w") as f:
            f.write(s)
    return s


def yaml_to_dict(data):
    """Convert yaml data into dict."""
    ntdata = data
    nodes = ntdata.pop("nodes")
    ntdata["nodes"] = {}
    links = []
    for node in nodes:
        # metadata
        metadata = node.get("metadata", {})
        metadata["identifier"] = node.pop("identifier")
        node["metadata"] = metadata
        # properties
        properties = {}
        if node.get("properties"):
            for name, p in node["properties"].items():
                properties[name] = {"value": p}
        node["properties"] = properties
        # links
        if node.get("inputs"):
            for input in node["inputs"]:
                input["to_node"] = node["name"]
                links.append(input)
        ntdata["nodes"][node["name"]] = node
    ntdata["links"] = links
    ntdata.setdefault("ctrl_links", {})
    return ntdata


def print_nodetree(ntdata):
    from copy import deepcopy

    ntdata = deepcopy(ntdata)
    print("-" * 60)
    nodes = ntdata.pop("nodes", {})
    links = ntdata.pop("links", {})
    metadata = ntdata.pop("metadata", {})
    for k, v in ntdata.items():
        print(f"{k}: {v}")
    for k, v in metadata.items():
        print(f"metadata.{k}: {v}")
    for name, node in nodes.items():
        print(f"node: {name}")
        metadata = node.pop("metadata", {})
        for k, v in node.items():
            print(f"  {k}: {v}")
        for k, v in metadata.items():
            print(f"  metadata.{k}: {v}")
    for link in links:
        print(f"link: {link}")
    print("-" * 60)


def wait_nt(nt, timeout=50):
    """Wait for nodetree to finish"""
    import time

    start = time.time()
    nt.update()
    while nt.state not in ("PAUSED", "FINISHED", "FAILED", "CANCELLED"):
        time.sleep(0.5)
        if time.time() - start > timeout:
            break
        nt.update()
