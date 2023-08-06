def build_nodetree_python_script(ntdata, nodes):
    import pickle

    print("ntdata: ", ntdata)
    s = """
from scinode import NodeTree
nt = NodeTree(name="{}")
""".format(
        ntdata["name"]
    )
    # nodes
    for node in nodes:
        print("node: ", node)
        s += """
node = nt.nodes.new("{}", "{}")
""".format(
            node["metadata"]["identifier"], node["label"]
        )
        # set node properties
        properties = pickle.loads(node["properties"])
        for name, p in properties.items():
            print("\np: ", p)
            if p["value"] == "":
                continue
            if p["type"] in ["String", "Enum"]:
                s += """
node.properties["{}"].value = "{}"
    """.format(
                    p["name"], p["value"]
                )
            else:
                s += """
node.properties["{}"].value = {}
    """.format(
                    p["name"], p["value"]
                )

    # links
    for link in ntdata["links"]:
        s += """
nt.links.new(nt.nodes["{}"].outputs["{}"], nt.nodes["{}"].inputs["{}"])
""".format(
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


def print_editor(editor):
    from copy import deepcopy

    editor = deepcopy(editor)
    print("\n" + "-" * 60)
    print("Nodetree: ")
    nodes = editor.pop("nodes", {})
    for k, v in editor.items():
        print("{:10s} : {}".format(k, v))
    print("-" * 30)
    print("\nNodes: ")
    for id, node in nodes.items():
        print("\n" + "-" * 20)
        for k, v in node.items():
            if k in ["log"]:
                continue
            print("{:10s} : {}".format(k, v))
    print("-" * 60 + "\n")
