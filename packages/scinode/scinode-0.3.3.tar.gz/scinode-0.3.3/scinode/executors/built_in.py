from scinode.core.executor import Executor


class PropertyToSocket(Executor):
    """Out the properties as sockets."""

    def run(self):
        results = ()
        outputs = self.dbdata["outputs"]
        # all kwargs as one socket
        if len(outputs) == 1 and len(self.kwargs) != 1:
            return self.kwargs
        # one kwarg as one socket
        # here we need to check
        for socket in outputs:
            results += (self.kwargs[socket["name"]],)
        return results


class ResultToSocket(Executor):
    """Out the result as sockets."""

    def run(self):
        from scinode.utils.node import get_results

        db_results = get_results(self.uuid)
        results = ()
        for result in db_results:
            results += (result["value"],)
        return results


def InputToSocket(*args):
    """Out the input as sockets."""
    results = ()
    for x in args:
        results += (x,)
    return results


def data_node(uuid="", input=None):
    """Out the data node result as sockets."""
    from scinode.utils.node import get_socket_data

    results = ()
    if uuid == "" or uuid is None:
        results = input
    else:
        results = get_socket_data({"uuid": uuid})
    return results


class NodeGroup(Executor):
    """Out the properties as sockets."""

    def run(self):
        """For node group.
        Run the nodetree.
        Connections to the Group Input will become attached
        to the input sockets of the coresponding nodes.
        """
        from scinode import NodeTree
        from scinode.core.node import Node
        from scinode.database.client import scinodedb
        from scinode.utils.node import get_node_data

        # nodetree of this node group
        nt = NodeTree.load(self.uuid)
        print("Load NodeTree successfully.")
        ng_data = get_node_data({"uuid": self.uuid})
        # assgin properties
        # print(f"Expose properties to the node group {nt.name}")
        for prop in nt.group_properties:
            node, prop_name, new_prop_name = prop
            nt.nodes[node].properties[prop_name].value = ng_data["properties"][
                new_prop_name
            ]["value"]
        # inputs
        # print(f"Expose inputs to the node group {nt.name}")
        ng_node_inputs = ng_data["inputs"]
        for input in nt.group_inputs:
            node_name, socket_name, new_socket_name = input
            # property
            if nt.nodes[node_name].inputs[socket_name].property is not None:
                nt.nodes[node_name].inputs[socket_name].property.value = ng_data[
                    "properties"
                ][new_socket_name]["value"]
            # input node
            # find input of this node
            for node_group_input in ng_node_inputs:
                if node_group_input["name"] == new_socket_name:
                    links = node_group_input["links"]
            for link in links:
                # the name of the input node should be unique
                name = f"{node_name}_{socket_name}_ref"
                # delete old input node
                nt.delete_nodes([name])
                # add the new input node
                print(f"Add input node: {name} to node group {nt.name}")
                ndata = scinodedb["node"].find_one(
                    {
                        "metadata.nodetree_uuid": ng_data["metadata"]["nodetree_uuid"],
                        "name": link["from_node"],
                    },
                    {"uuid": 1},
                )
                node0 = Node.load(ndata["uuid"])
                node = node0.copy(name=name, nodetree=nt, is_ref=True)
                # all the input node should be finished
                node.state = "FINISHED"
                nt.nodes.append(node)
                nt.links.new(
                    node.outputs[link["from_socket"]],
                    nt.nodes[node_name].inputs[socket_name],
                )
        print(f"Launch node group nodetree: {nt.name}")
        nt.launch()
        return None
