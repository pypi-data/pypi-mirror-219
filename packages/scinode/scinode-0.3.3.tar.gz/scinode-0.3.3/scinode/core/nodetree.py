from scinode.core.collection import NodeCollection, LinkCollection, NodeTreeCollection
from uuid import uuid1
from scinode.common.log import logging

logger = logging.getLogger("nodetree")


def skip_ref_node(func):
    def wrapper(self, name, **kwargs):
        if self.nodes[name].node_type == "REF":
            raise Exception("Can not change state of a reference node")
        return func(self, name, **kwargs)

    return wrapper


class NodeTree:
    """Nodetree is a collection of nodes and links.

    Attributes:

    worker_name: str
        name of the worker which will run this nodetree.
        Default value: local
    uuid: str
        uuid of this nodetree.
    state: str
        state of this nodetree.
    action: str
        action of this nodetree.
    platform: str
        platform that used to creat this nodetree.

    Examples:

    >>> from scinode import NodeTree
    >>> nt = NodeTree(name="my_first_nodetree")

    add nodes:

    >>> float1 = nt.nodes.new("TestFloat", name = "float1")
    >>> add1 = nt.nodes.new("TestAdd", name = "add1")

    add links:

    >>> nt.links.new(float1.outputs[0], add1.inputs[0])

    Launch the nodetree:

    >>> nt.launch()

    """

    worker_name: str = "local"
    platform: str = "scinode"
    uuid: str = ""
    type: str = "NORMAL"
    group_properties = []
    group_inputs = []
    group_outputs = []

    def __init__(
        self,
        name="NodeTree",
        uuid=None,
        worker_name="local",
        type="NORMAL",
        parent="",
        parent_node="",
        scatter_node="",
        scattered_label="",
    ) -> None:
        """_summary_

        Args:
            name (str, optional): name of the nodetree.
                Defaults to "NodeTree".
            uuid (str, optional): uuid of the nodetree.
                Defaults to None.
            worker_name (str, optional): name of the worker.
                Defaults to "local".
            parent (str, optional): uuid of the parent nodetree.
                Defaults to ''.
        """
        self.name = name
        self.uuid = uuid or str(uuid1())
        self.worker_name = worker_name
        self.type = type
        self.parent = parent
        self.parent_node = parent_node
        self.scatter_node = scatter_node
        self.scattered_label = scattered_label
        self.nodetrees = NodeTreeCollection(self)
        self.nodes = NodeCollection(self)
        self.links = LinkCollection(self)
        self.ctrl_links = LinkCollection(self)
        self.state = "CREATED"
        self.action = "NONE"
        self.description = ""
        self.log = ""
        logger.info("Create NodeTree: {}".format(self.name))

    def launch(self, worker_name=None, wait=False, timeout=60):
        """Launch the nodetree."""
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        logger.info("Launch NodeTree: {}".format(self.name))
        if worker_name is not None:
            self.worker_name = worker_name
        self.save()
        msg = f"{self.uuid},nodetree,action:LAUNCH"
        send_message_to_queue(broker_queue_name, msg)
        if wait:
            self.wait(timeout=timeout)

    def save(self):
        """Save nodetree to database."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.debug("Save nodetree to database: {}".format(self.name))
        self.state = "CREATED"
        ntdata = self.to_dict()
        lnt = LaunchNodeTree(ntdata)
        lnt.save()

    def to_dict(self, short=False):
        """To dict

        Returns:
            dict: nodetree data
        """
        from scinode.version import __version__

        metadata = self.get_metadata()
        nodes = self.nodes_to_dict(short=short)
        links = self.links_to_dict()
        ctrl_links = self.ctrl_links_to_dict()
        data = {
            "version": "scinode@{}".format(__version__),
            "uuid": self.uuid,
            "name": self.name,
            "state": self.state,
            "action": self.action,
            "error": "",
            "metadata": metadata,
            "nodes": nodes,
            "links": links,
            "ctrl_links": ctrl_links,
            "description": self.description,
            "log": self.log,
        }
        return data

    def get_metadata(self):
        """metadata to dict"""
        metadata = {
            "type": self.type,
            "worker_name": self.worker_name,
            "parent": self.parent,
            "platform": self.platform,
            "parent_node": self.parent_node,
            "scatter_node": self.scatter_node,
            "scattered_label": self.scattered_label,
            "group_properties": self.group_properties,
            "group_inputs": self.group_inputs,
            "group_outputs": self.group_outputs,
        }
        return metadata

    def nodes_to_dict(self, short=False):
        """nodes to dict"""
        # save all relations using links
        nodes = {}
        for node in self.nodes:
            if short:
                nodes[node.name] = node.to_dict(short=short)
            else:
                nodes[node.name] = node.to_dict()
        return nodes

    def links_to_dict(self):
        """links to dict"""
        # save all relations using links
        links = []
        for link in self.links:
            links.append(link.to_dict())
        # logger.debug("Done")
        return links

    def ctrl_links_to_dict(self):
        """ctrl_links to dict"""
        # save all relations using ctrl_links
        ctrl_links = []
        for link in self.ctrl_links:
            ctrl_links.append(link.to_dict())
        # logger.debug("Done")
        return ctrl_links

    def to_yaml(self):
        """Export to a yaml format data.
        Results of the nodes are not exported."""
        import yaml

        data = self.to_dict()
        for name, node in data["nodes"].items():
            node.pop("results", None)
        s = yaml.dump(data, sort_keys=False)
        return s

    def reset(self):
        """Reset nodetree."""
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        msg = f"{self.uuid},nodetree,action:RESET"
        send_message_to_queue(broker_queue_name, msg)

    def update(self):
        from scinode.database.client import scinodedb

        query = {"uuid": self.uuid}
        data = scinodedb["nodetree"].find_one(
            query, {"index": 1, "state": 1, "action": 1, "nodes": 1}
        )
        self.index = data["index"]
        self.state = data["state"]
        self.action = data["action"]
        self.update_nodes(data["nodes"])

    def update_nodes(self, data):
        for node in self.nodes:
            node.state = data[node.name]["state"]
            node.counter = data[node.name]["counter"]
            node.action = data[node.name]["action"]
            node.update()

    @skip_ref_node
    def reset_node(self, name):
        """Reset node.

        Args:
            name (str): name of the node to be reseted
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        msg = f"{self.uuid},node,{name}:action:RESET"
        send_message_to_queue(broker_queue_name, msg)

    @skip_ref_node
    def pause_node(self, name):
        """pause node.

        Args:
            name (str): name of the node to be paused
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        msg = f"{self.uuid},node,{name}:state:PAUSED"
        send_message_to_queue(broker_queue_name, msg)

    @skip_ref_node
    def play_node(self, name):
        """play node.

        Args:
            name (str): name of the node to be played
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        msg = f"{self.uuid},node,{name}:state:CREATED"
        send_message_to_queue(broker_queue_name, msg)
        msg = f"{self.uuid},node,{name}:action:CHECK"
        send_message_to_queue(broker_queue_name, msg)

    @classmethod
    def from_dict(cls, ntdata):
        """Rebuild nodetree from dict ntdata.

        Args:
            ntdata (dict): data of the nodetree.

        Returns:
            Nodedtree: a nodetree
        """
        import cloudpickle as pickle

        # subnodetree
        nt = cls(
            name=ntdata["name"],
            uuid=ntdata.get("uuid"),
            worker_name=ntdata["metadata"]["worker_name"],
        )
        # print("from_dict: ", nt.uuid)
        for key in ["state", "action", "description"]:
            if ntdata.get(key):
                setattr(nt, key, ntdata.get(key))
        # read all the metadata
        for key in [
            "parent",
            "parent_node",
            "scatter_node",
            "scattered_label",
            "group_properties",
            "group_inputs",
            "group_outputs",
        ]:
            if ntdata["metadata"].get(key):
                setattr(nt, key, ntdata["metadata"].get(key))
        for name, ndata in ntdata["nodes"].items():
            # register the node created by decorator
            if ndata.get("executor", {}).get("is_pickle", False):
                from scinode.nodes import node_pool

                node_class = pickle.loads(ndata["node_class"])
                node_pool[node_class.identifier] = node_class
            node = nt.nodes.new(
                ndata["metadata"]["identifier"],
                name=name,
                uuid=ndata.pop("uuid", None),
            )
            node.update_from_dict(ndata)
        # re-build links
        for link in ntdata.get("links", []):
            nt.links.new(
                nt.nodes[link["from_node"]].outputs[link["from_socket"]],
                nt.nodes[link["to_node"]].inputs[link["to_socket"]],
            )
        # re-build control links
        for link in ntdata.get("ctrl_links", []):
            nt.ctrl_links.new(
                nt.nodes[link["from_node"]].ctrl_outputs[link["from_socket"]],
                nt.nodes[link["to_node"]].ctrl_inputs[link["to_socket"]],
            )
        return nt

    @classmethod
    def from_yaml(cls, filename=None, string=None):
        """Build nodetree from yaml file.

        Args:
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            Nodetree: _description_
        """
        import yaml
        from scinode.utils.nodetree import yaml_to_dict
        from pprint import pprint

        # load data
        if filename:
            with open(filename, "r") as f:
                ntdata = yaml.safe_load(f)
        elif string:
            ntdata = yaml.safe_load(string)
        else:
            raise Exception("Please specific a filename or yaml string.")
        ntdata = yaml_to_dict(ntdata)
        nt = cls.from_dict(ntdata)
        return nt

    def copy(self, name=None):
        """Copy nodetree.

        The nodes and links are copied.

        """
        name = f"{self.name}_copy" if name is None else name
        nt = self.__class__(name=name, uuid=None)
        # should pass the nodetree to the nodes as parent
        nt.nodes = self.nodes.copy(parent=nt)
        # create links
        for link in self.links:
            nt.links.new(
                nt.nodes[link.from_node.name].outputs[link.from_socket.name],
                nt.nodes[link.to_node.name].inputs[link.to_socket.name],
            )
        return nt

    def copy_using_dict(self):
        """Copy nodetree using dict data.

        Fist export the nodetree to dict data.
        Then reset uuid of nodetree and nodes.
        Finally, rebuild the nodetree from dict data.
        """
        ntdata = self.to_dict()
        # copy nodes
        # reset uuid for nodetree
        ntdata["uuid"] = str(uuid1())
        # reset uuid for nodes
        for name, node in ntdata["nodes"].items():
            node["uuid"] = str(uuid1())
        nodetree = self.from_dict(ntdata)
        # copy links
        # TODO the uuid of the socket inside the links should be udpated.
        # print("copy nodetree: ", nodetree)
        return nodetree

    @classmethod
    def load(cls, uuid):
        """Load data from database.
        1) attributes
        2) nodes
        3) links
        """
        from scinode.utils.node import deserialize
        from scinode.database.client import scinodedb

        if "-" in str(uuid):
            ntdata = scinodedb["nodetree"].find_one({"uuid": uuid})
        else:
            ntdata = scinodedb["nodetree"].find_one({"index": uuid})
        # populate the nodes data
        nodes = ntdata.pop("nodes")
        ntdata["nodes"] = {}
        for name, node in nodes.items():
            ndata = scinodedb["node"].find_one({"uuid": node["uuid"]})
            ndata["properties"] = deserialize(ndata["properties"])
            ntdata["nodes"][name] = ndata
        nodetree = cls.from_dict(ntdata)
        return nodetree

    def copy_subset(self, node_list, name=None, add_ref=True):
        """Copy a subset of a nodetree.

        Args:
            node_list (list of string): names of the nodes to be copied.
            name (str, optional): name of the new nodetree. Defaults to None.

        Returns:
            NodeTree: A new NodeTree
        """

        logging.debug(f"Copy {len(node_list)} nodes to a new NodeTree")
        name = f"{self.name}_copy" if name is None else name
        nt = self.__class__(name=name, uuid=None)
        for node in node_list:
            nt.nodes.append(self.nodes[node].copy(nodetree=nt))
        # copy links
        for link in self.links:
            # create ref node for input node that is not in the new nodetree
            if (
                add_ref
                and link.from_node.name not in nt.nodes.keys()
                and link.to_node.name in nt.nodes.keys()
            ):
                nt.nodes.append(
                    self.nodes[link.from_node.name].copy(nodetree=nt, is_ref=True)
                )
            # add link if both nodes are in the new nodetree
            if (
                link.from_node.name in nt.nodes.keys()
                and link.to_node.name in nt.nodes.keys()
            ):
                nt.links.new(
                    nt.nodes[link.from_node.name].outputs[link.from_socket.name],
                    nt.nodes[link.to_node.name].inputs[link.to_socket.name],
                )
        return nt

    def __getitem__(self, keys):
        """Get a sub-nodetree by the names of nodes."""
        nt = self.copy_subset(keys)
        return nt

    def __iadd__(self, other):
        self.nodes.extend(other.nodes.copy(parent=self))
        # create links
        for link in other.links:
            nt.links.new(
                nt.nodes[link.from_node.name].outputs[link.from_socket.name],
                nt.nodes[link.to_node.name].inputs[link.to_socket.name],
            )
        return self

    def __add__(self, other):
        """Sum of two nodetree."""
        self += other
        return self

    def delete_nodes(self, node_list):
        """_summary_

        Args:
            node_list (_type_): _description_
        """
        for name in node_list:
            # remove links connected to the node
            link_index = []
            for index, link in enumerate(self.links):
                if link.from_node.name == name or link.to_node.name == name:
                    link_index.append(index)
            del self.links[link_index]
            # remove the node
            self.nodes.delete(name)

    def wait(self, timeout=50):
        """Wait for nodetree to finish."""
        import time

        start = time.time()
        self.update()
        while self.state not in ("PAUSED", "FINISHED", "FAILED", "CANCELLED"):
            time.sleep(0.5)
            self.update()
            if time.time() - start > timeout:
                logger.info(f"Waiting time longer than {timeout}.")
                return
        logger.info("NodeTree finished, state: {}".format(self.state))

    def __repr__(self) -> str:
        s = ""
        s += 'NodeTree(name="{}, uuid="{}")\n'.format(self.name, self.uuid)
        return s


if __name__ == "__main__":
    nt = NodeTree("test")
    nt.nodes.new("TestFloat")
    nt1 = nt.copy()
    assert nt1.uuid != nt.uuid
