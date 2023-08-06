"""
"""
import datetime
from scinode.orm import DBItem
from scinode.database.client import scinodedb
from scinode.utils.db import insert_one, update_one
from scinode.utils.node import serialize
from scinode.common.log import logging

logger = logging.getLogger("engine")


class LaunchNodeTree(DBItem):
    """Launch nodetree to the database.

    Becareful, we have two data for nodetree.
    - full_data: includes all nodes data
    - short_data: only includes basic nodes data

    - if it does not exist in the database, save it to the database
    - if it exist in the database, find the difference. Update the difference in the database.

    uuid: str
        uuid of the nodetree.

    Example:

    >>> from scinode.engine.nodetree_launch import LaunchNodeTree
    >>> ntdata = nodetree.to_dict()
    >>> lnt = LaunchNodeTree(ntdata)
    >>> lnt.launch()
    """

    db_name: str = "nodetree"

    def __init__(self, ntdata) -> None:
        """_summary_

        Args:
            ntdata (dict): data of nodetree to be launched.
        """
        self.ntdata = ntdata
        self.uuid = ntdata["uuid"]
        self.name = ntdata["name"]

    def assign_UUID(self):
        """Assign uuid to nodetree and nodes"""
        import uuid

        # assign uuid to nodetree
        if not self.ntdata["uuid"]:
            self.ntdata["uuid"] = str(uuid.uuid1())
            self.ntdata["state"] = "CREATED"
            self.uuid = self.ntdata["uuid"]
        # assign uuid to nodes
        for name, node in self.ntdata["nodes"].items():
            # assign ndoetree uuid and worker to node
            node["metadata"]["nodetree_uuid"] = self.ntdata["uuid"]
            node["metadata"]["nodetree_worker"] = self.ntdata["metadata"]["worker_name"]
            if not node["uuid"]:
                node["uuid"] = str(uuid.uuid1())
                node["state"] = "CREATED"
            if not node["metadata"]["worker_name"]:
                node["metadata"]["worker_name"] = self.ntdata["metadata"]["worker_name"]

    def build_node_link(self):
        """Create links for nodes.

        Create the links for node inputs using:
        1) nodetree links
        2) if it is a node group tree, expose the group inputs and outputs
        sockets.

        """
        # reset node input links
        for name, node in self.ntdata["nodes"].items():
            for input in node["inputs"]:
                input["links"] = []
            for output in node["outputs"]:
                output["links"] = []
        for link in self.ntdata["links"]:
            to_socket = [
                socket
                for socket in self.ntdata["nodes"][link["to_node"]]["inputs"]
                if socket["name"] == link["to_socket"]
            ][0]
            from_socket = [
                socket
                for socket in self.ntdata["nodes"][link["from_node"]]["outputs"]
                if socket["name"] == link["from_socket"]
            ][0]
            to_socket["links"].append(link)
            from_socket["links"].append(link)
        # update the nodetree input and output
        if self.ntdata["metadata"]["type"] == "NODE_GROUP":
            pass

    def insert_nodetree_to_db(self):
        """Save a new nodetree in the database.

        - nodetree
        - all nodes
        """
        from scinode.utils.db import insert_one
        from scinode.utils.nodetree import get_nt_short_data

        # pprint(self.ntdata)
        self.ntdata["created"] = datetime.datetime.utcnow()
        self.ntdata["lastUpdate"] = datetime.datetime.utcnow()
        ntdata = get_nt_short_data(self.ntdata)
        # init message
        insert_one(ntdata, scinodedb["nodetree"])
        self.insert_nodes_to_database(self.ntdata["nodes"])

    def save(self):
        """Save Nodetree.

        - Assign uuid if needed.
        - Update uuid for links. Build compressed nodes for nodetree.
        - Analysis connectivity
        - Check exist in database or not. If not in database, save directly.
        - If in database, analyze the difference, save accordingly.
        """
        self.assign_UUID()
        self.build_node_link()
        self.build_connectivity()
        in_db = self.exist_in_db()
        if in_db:
            self.update_nodetree_db()
            self.reset_nodes(self.modified_nodes)
        else:
            self.insert_nodetree_to_db()
        logger.info(
            "Save nodetree: name={}, uuid={}".format(
                self.ntdata["name"], self.ntdata["uuid"]
            )
        )

    def update_nodetree_db(self):
        """Update nodetree in database.

        - analyze the difference.
        - save new nodes to database
        - update modified nodes to database.
        """
        new_nodes, modified_nodes, update_metadata = self.check_diff()
        self.modified_nodes = modified_nodes
        self.insert_nodes_to_database(new_nodes)
        logger.debug("Nodes to be updated: {}".format(modified_nodes))
        self.update_nodes_to_database(modified_nodes)
        # update position
        self.update_nodes_metadata(update_metadata)
        # final
        self.update_nodetree_to_database(new_nodes)

    def insert_nodes_to_database(self, nodes):
        """Insert nodes to database

        Args:
            nodes (list): a list of node names.
        """
        for name in nodes:
            # print("insert node: ", self.ntdata["nodes"][name])
            if self.ntdata["nodes"][name]["metadata"]["node_type"] in ["REF"]:
                self.ntdata["nodes"][name]["action"] = "NONE"
            logger.debug("Insert node: {}".format(name))
            self.ntdata["nodes"][name]["properties"] = serialize(
                self.ntdata["nodes"][name]["properties"]
            )
            self.ntdata["nodes"][name]["created"] = datetime.datetime.utcnow()
            self.ntdata["nodes"][name]["lastUpdate"] = datetime.datetime.utcnow()
            insert_one(self.ntdata["nodes"][name], scinodedb["node"])

    def update_nodes_to_database(self, nodes):
        """update nodes to database.

        Args:
            nodes (list): a list of node names.
        """

        for name in nodes:
            if self.ntdata["nodes"][name]["metadata"]["node_type"] in ["REF"]:
                continue
            logger.debug("update node: {}".format(name))
            self.ntdata["nodes"][name]["properties"] = serialize(
                self.ntdata["nodes"][name]["properties"]
            )
            self.ntdata["nodes"][name]["lastUpdate"] = datetime.datetime.utcnow()
            update_one(self.ntdata["nodes"][name], scinodedb["node"])

    def update_nodes_output_to_database(self, nodes):
        """Update nodes to database

        Args:
            nodes (list): a list of node names.
        """

        for name in nodes:
            logger.debug("update node: {}".format(name))
            self.ntdata["nodes"][name]["properties"] = self.ntdata["nodes"][name][
                "properties"
            ]
            outputs = {
                "uuid": self.ntdata["nodes"][name]["uuid"],
                "outputs": self.ntdata["nodes"][name]["outputs"],
            }
            update_one(outputs, scinodedb["node"])

    def update_nodes_metadata(self, nodes):
        """Check the node metadata.
        This data will not affect the calculation of the node.
        e.g. position, description
        """

        for name in nodes:
            logger.debug("update node: {}".format(name))
            position = {
                "uuid": self.ntdata["nodes"][name]["uuid"],
                "position": self.ntdata["nodes"][name]["position"],
                "description": self.ntdata["nodes"][name]["description"],
            }
            update_one(position, scinodedb["node"])

    def update_nodetree_to_database(self, new_nodes):
        """update nodetree to database"""
        import datetime
        from scinode.utils.nodetree import get_nt_short_data

        logger.debug("update nodetree: {}".format(self.ntdata["name"]))
        self.ntdata["lastUpdate"] = datetime.datetime.utcnow()
        ntdata = get_nt_short_data(self.ntdata)
        # print("update_nodetree_to_database: ", ntdata["nodes"])
        # insert new node to "nodes" field
        items = {f"nodes.{name}": ntdata["nodes"][name] for name in new_nodes}
        # skip field
        ntdata.pop("nodes")
        ntdata.update(items)
        update_one(ntdata, scinodedb["nodetree"])

    def reset_nodes(self, nodes):
        """Reset nodes

        Args:
            nodes (list): a list of node names.
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        for name in nodes:
            logger.debug(f"Reset node: {name}")
            # skip REF node
            if self.ntdata["nodes"][name]["metadata"]["node_type"] in ["REF"]:
                continue
            send_message_to_queue(
                broker_queue_name,
                f"{self.uuid},node,{name}:action:RESET",
            )

    def launch(self):
        """Launch Nodetree
        - set action to launch.
        - save to db
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        self.ntdata["state"] = "CREATED"
        self.ntdata["action"] = "LAUNCH"
        # reset modified noes
        self.set_nodes_action("LAUNCH")
        self.save()
        send_message_to_queue(
            broker_queue_name,
            f"{self.uuid},nodetree,action:LAUNCH",
        )
        logger.debug(
            "Launch nodetree: name={}, uuid={}".format(
                self.ntdata["name"], self.ntdata["uuid"]
            )
        )

    def set_nodes_action(self, action):
        """Set node action."""
        for name, node in self.ntdata["nodes"].items():
            # print("Reset node: {}".format(node))
            node["action"] = action

    def check_diff(self):
        """Find difference between nodetree and its database.

        Returns:
            new_nodes: new nodes
            modified_nodes: modified nodes
        """
        from scinode.utils.nt_analysis import DifferenceAnalysis
        from scinode.utils.nodetree import get_nt_full_data

        nt1 = get_nt_full_data({"uuid": self.uuid})
        dc = DifferenceAnalysis(nt1=nt1, nt2=self.ntdata)
        (
            new_nodes,
            modified_nodes,
            update_metadata,
        ) = dc.build_difference()
        logger.debug("New nodes: {}".format(new_nodes))
        logger.debug("Modified nodes: {}".format(modified_nodes))
        return new_nodes, modified_nodes, update_metadata

    def exist_in_db(self):
        """Check nodetree exist in database or not.

        Returns:
            bool: _description_
        """
        # query the db first, if exist, skip this step
        if self.uuid != "" and self.dbdata is not None:
            logger.debug(
                "Nodetree: name={}, uuid={} exist in database".format(
                    self.ntdata["name"], self.ntdata["uuid"]
                )
            )
            return True
        return False

    def build_connectivity(self, ntdata=None):
        """Analyze the connectivity of nodetree and save it into dict."""
        from scinode.utils.nt_analysis import ConnectivityAnalysis

        if ntdata is None:
            ntdata = self.ntdata
        logger.debug("Calculate child nodes...")
        nc = ConnectivityAnalysis(ntdata)
        self.ntdata["connectivity"] = nc.build_connectivity()


if __name__ == "__main__":
    from scinode import NodeTree

    nt = NodeTree(name="test_debug_math")
    float1 = nt.nodes.new("TestFloat", "float1")
    float1.properties["Float"].value = 3.0
    math1 = nt.nodes.new("TestAdd", "add1")
    math1.properties["x"].value = 2
    nt.links.new(float1.outputs[0], math1.inputs[1])
    nt.launch()
