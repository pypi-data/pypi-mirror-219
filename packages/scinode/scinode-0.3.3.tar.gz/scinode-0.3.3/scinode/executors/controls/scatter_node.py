from scinode.core.executor import Executor
from scinode.database.client import scinodedb


class ScinodeScatter(Executor):
    """Scatter nodes executor"""

    def run(self):
        """
        0) Find all subtrees created by this node, and delete them
        1) Find all nodes controled by the scatter node
        2) Create a new nodetree nt1
        3) build all children node inside new nodetree nt1
        4) use REF node
        5) launch the nodetree
        """
        print("Run for scatter {}".format(self.name))
        self.prepare()
        self.new_nodetree()
        self.set_scattered_state()

    def prepare(self):
        from scinode import NodeTree

        self.delete_sub_nodetree()
        if isinstance(self.kwargs["input"], dict):
            labels = self.kwargs["input"].keys()
        else:
            labels = range(len(self.kwargs["input"]))
        self.labels = labels
        print("  Scatter labels: {}".format(self.labels))
        # nodetree data
        self.nt = NodeTree.load(self.dbdata["metadata"]["nodetree_uuid"])
        connectivity = scinodedb["nodetree"].find_one(
            {"uuid": self.dbdata["metadata"]["nodetree_uuid"]}, {"connectivity": 1}
        )["connectivity"]
        self.copy_nodes = connectivity["control_node"][self.name].get("scatter", [])
        print("copy_nodes: ", self.copy_nodes)

    def delete_sub_nodetree(self):
        """Delete nodetrees which are scattered from this node."""
        from scinode.database.nodetree import NodetreeClient

        # Find all subtrees created by this node, and delete them
        client = NodetreeClient()
        query = {"metadata.scatter_node": self.uuid}
        client.delete(query)

    def new_nodetree(self):
        """Copy child nodes to new nodetrees."""
        n = len(self.copy_nodes)
        for label in self.labels:
            # add new nodetree
            name = "{}_{}".format(self.nt.name, label)
            print(f"Copy {n} nodes to new nodetree: {name}")
            nt = self.nt.copy_subset(self.copy_nodes, name=name)
            print(f"Nodetree uuid: {nt.uuid}")
            self.update_nodetree(nt, label)
            nt.save()
            nt.launch()

    def update_nodetree(self, nt, label):
        """Update nodetree metadata and node metadata.

        1) Add scattered_label to the metadata
        2) remove the scatter node from the new nodetree
        3) add a data node to the new nodetree, set the input socket value.
        4) link it to the child node of the scatter node

        """
        # update nodetree metadata
        nt.parent = self.dbdata["metadata"]["nodetree_uuid"]
        nt.scatter_node = self.uuid
        nt.scattered_label = label
        # update node metadata
        for name in self.copy_nodes:
            nt.nodes[name].scattered_from = nt.nodes[name].copied_from
            nt.nodes[name].scattered_label = label
        # delete the scatter node
        nt.delete_nodes([self.name])
        # add a data node, and link it to the child node of the scatter node
        data_node = nt.nodes.new("DataNode", f"{self.name}_data_{label}")
        data_node.set({"datatype": self.dbdata["properties"]["datatype"]["value"]})
        # set the output socket the copied scatter node
        data_node.inputs["input"].property.value = self.kwargs["input"][label]
        # Add the links
        for link in self.dbdata["outputs"][0]["links"]:
            nt.links.new(
                data_node.outputs["result"],
                nt.nodes[link["to_node"]].inputs[link["to_socket"]],
            )
        # data_node.state = "FINISHED"
        # data_node.scattered_from = self.uuid
        # data_node.scattered_label = str(label)

    def set_scattered_state(self):
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        scatter = {}
        for label in self.labels:
            scatter[str(label)] = "CREATED"
        # all the children nodes should not run, instead the state should be scattered.
        for name in self.copy_nodes:
            print(f"    Set Node {name} state to SCATTERED.")
            msg = f"{self.nodetree_uuid},node,{name}:state:SCATTERED"
            send_message_to_queue(broker_queue_name, msg)
            #
            print(f"    Add new key: scatter for Node {name}.")
            newvalues = {"$set": {f"nodes.{name}.scatter": scatter}}
            query = {"uuid": self.nt.uuid}
            scinodedb["nodetree"].update_one(query, newvalues)
        return None
