from scinode.common.log import logging

logger = logging.getLogger("app")


def properties_to_show_str(properties):
    """Convert properties to show a str.
    Replace the general property with its string value, which
    will be shown in the node GUI.

    Note, this is different from the edit section of the node, which
    is show as a yaml string.
    """
    # print("ntdata: ", ntdata)
    # set node_full properties
    new_properties = {}
    for key, value in properties.items():
        if value["identifier"] in ["General", "BaseDict", "BaseList"]:
            new_properties[key] = str(value["value"])
        else:
            new_properties[key] = value["value"]
    return new_properties


class ReteAdaptor:
    """Adaptor serves as a bridge between SciNode and Rete."""

    @staticmethod
    def getScinodeDB(editor):
        """get SciNode data from a Rete Editor data,
        save the nodetree and all nodes to db.

        Args:
            nodetree (dict): _description_
            nodes (dict): _description_
        """
        from scinode.utils.node import get_node_data

        nodes = {}
        links = []
        for key, ndata in editor["nodes"].items():
            if ndata["metadata"].pop("local", False):
                continue
            node = ndata.copy()
            print("node: ", node["name"])
            # print("name: ", ndata["name"])
            node["name"] = node["label"]
            node["inner_id"] = node["id"]
            # update properties
            # node['properties'] = node['controls']
            # update data
            # todo use serialize for property
            node["properties"] = ndata["controls"]
            # update inputs and outputs
            node["inputs"] = []
            # print("inputs: ", ndata["inputs"])
            # restore te link from input link
            for name, data in ndata["inputs"].items():
                node["inputs"].append(data)
                links.extend(data["links"])
            # For the outputs, we only need the metadata of the socket
            # e.g. name, uuid, we don't need the links, because Scinode
            # only save inputs
            node["outputs"] = []
            # logger.info(f'outputs: {ndata["outputs"]}')
            for name, data in ndata["outputs"].items():
                node["outputs"].append(data)
            node["properties"] = node["properties"]
            # replace the properties with type general
            # the general property is not saved in js,
            # so the data is wrong. Becase we can not edit a
            # general property in js, so we should replace it with the orignal one from the database.
            # this also includes the general input sockets with general property
            dbdata = get_node_data(
                {"uuid": node["uuid"]},
                {"properties": 1, "node_class": 1, "executor": 1},
            )
            if dbdata is not None:
                for name, prop in dbdata["properties"].items():
                    if prop["identifier"] in ["General", "BaseDict", "BaseList"]:
                        node["properties"][prop["name"]] = dbdata["properties"][
                            prop["name"]
                        ]
                # for decoratored node, we should update the node_class, and executor
                node["node_class"] = dbdata.get("node_class", None)
                node["executor"] = dbdata.get("executor", {})
            nodes[node["name"]] = node
            # insert_one(node, db['node'])
        #
        editor["version"] = editor.pop("id")
        editor["nodes"] = nodes
        editor["links"] = links
        return editor

    @staticmethod
    def getEditor(query, db, is_template=False):
        """Load data from database, and change to Editor format.

        Args:
            record (mongodb cursor): _description_
            db (_type_): _description_

        Returns:
            dict: _description_
        """
        from scinode.utils.node import deserialize, get_node_constructor

        # print(query)
        if is_template:
            db_nodetree_name = "template_nodetree"
            db_node_name = "template_node"
        else:
            db_nodetree_name = "nodetree"
            db_node_name = "node"
        ntdata = db[db_nodetree_name].find_one(query, {"_id": 0, "connectivity": 0})
        if ntdata is None:
            return None
        # fetch node data
        nodes = {}
        for key, data in ntdata["nodes"].items():
            ndata = db[db_node_name].find_one(
                {"uuid": data["uuid"]},
                {
                    "_id": 0,
                    "node_class": 0,
                    "executor": 0,
                    "log": 0,
                },
            )
            ndata["state"] = ntdata["nodes"][key]["state"]
            nodes[key] = ndata
        editor = ntdata.copy()
        # print("getEditor: ", ntdata)
        editor["id"] = editor.pop("version")
        editor_nodes = {}
        # print(nodes)
        for node_name, ndata in nodes.items():
            node = ndata.copy()
            constructor = get_node_constructor(ndata)
            constructor["controls"] = constructor.pop("properties", {})
            constructor["name"] = constructor.pop("identifier")
            node["constructor"] = constructor
            # print("getEditor, ndata: ", ndata)
            node.pop("version", None)
            node.pop("properties", None)
            # node_class is a binary data, can not be serialized
            node["id"] = node["inner_id"]
            node["label"] = node["name"]
            node["name"] = node["metadata"]["identifier"]
            node["state"] = ntdata["nodes"][node_name]["state"]
            # properties to data
            # print("properties: ", ndata["properties"])
            properties = deserialize(ndata["properties"])
            # replace the value use the string of the value for general property
            # print("properties: ", properties)
            node["data"] = properties_to_show_str(properties)
            # initialize outputs to a dict
            node["outputs"] = {
                output["name"]: {
                    "uuid": output["uuid"],
                    "connections": [],
                }
                for output in ndata["outputs"]
            }
            # input of scinode is a list, while in Rete edit, it is a map (dict)
            node["inputs"] = {input["name"]: input for input in ndata["inputs"]}
            # metadata
            # icon
            if node["metadata"]["node_type"] == "GROUP":
                node["metadata"]["icon"] = "fa-list"
            elif node["metadata"]["node_type"] == "REF":
                node["metadata"]["icon"] = "fa-chain"
            else:
                node["metadata"]["icon"] = "fa-gear"
            editor_nodes[node["id"]] = node
        # load links
        # For SciNode, only the inputs are used to re-create the links.
        # For Rete, the editor only read the outputs to create the links.
        # Therefore, we need to loop through the links to create the outputs
        # Because the inputs and outputs are always paired together as a link,
        # no information is lost.
        for link in ntdata["links"]:
            output_node = nodes[link["from_node"]]["inner_id"]
            input_node = nodes[link["to_node"]]["inner_id"]
            connection = {
                "node": input_node,
                "input": link["to_socket"],
                "data": {},
            }
            editor_nodes[output_node]["outputs"][link["from_socket"]][
                "connections"
            ].append(connection)
        #
        editor["nodes"] = editor_nodes
        # print("get editor: ", editor)
        return editor
