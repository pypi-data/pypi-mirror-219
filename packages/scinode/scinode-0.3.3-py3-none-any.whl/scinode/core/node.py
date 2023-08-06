# Copyright (c) 2022 SciNode
#
# This file is part of SciNode.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from scinode.core.collection import (
    PropertyCollection,
    InputSocketCollection,
    OutputSocketCollection,
)
from uuid import uuid1
from scinode.common.log import logging

logger = logging.getLogger("node")


class Node:
    """Base class for Node.

    Attributes:

    identifier: str
        The identifier is used for loading the Node.
    node_type: str
        type of this node. "Normal", "REF", "GROUP".
    inner_id: int
        node id inside the nodetree.
    nodetree_uuid: str
        uuid of the nodetree this node belongs to.
    worker_name: str
        name of the worker which will run this node.
    counter: int
        number of time this node has been executed.
    args: list
        postional arguments of the exector.
    kwargs: list
        keyword arguments of the exector.
    platform: str
        platform that used to creat this node.
    copied_from: str
        copied_from node which is copied.
    scattered_from: str
        scattered_from node which is scattered, usually same as the copied_from.

    Examples:

    add nodes:

    >>> float1 = nt.nodes.new("TestFloat", name = "float1")
    >>> add1 = nt.nodes.new("TestDelayAdd", name = "add1")

    load node:

    >>> from scinode.core.node import Node
    >>> node = Node.load(uuid=uuid)

    copy node:

    >>> n = node.copy(name="new_name")

    append node to nodetree:

    >>> nt.nodes.append(node)
    """

    identifier: str = "Node"
    node_type: str = "Normal"
    inner_id: int = 0
    nodetree_uuid: str = ""
    worker_name: str = ""
    counter: int = 0
    platform: str = "scinode"
    catalog: str = "Node"
    register_path: bool = False
    args = []
    kwargs = []
    group_inputs = []
    group_outputs = []

    def __init__(
        self,
        inner_id=0,
        name=None,
        uuid=None,
        nodetree=None,
        copied_from: str = "",
        scattered_from: str = "",
        scattered_label: str = "",
        scatter_node: str = "",
        scheduler: dict = {},
        computer: str = "",
    ) -> None:
        self.inner_id = inner_id
        self.name = name or "{}{}".format(self.identifier, inner_id)
        self.uuid = uuid or str(uuid1())
        self.nodetree = nodetree
        self.copied_from = copied_from
        self.scattered_from = scattered_from
        self.scattered_label = scattered_label
        self.scatter_node = scatter_node
        self.scheduler = scheduler
        self.computer = computer
        self.ref_uuid = ""
        self.copy_uuid = ""
        self.properties = PropertyCollection(self)
        self.inputs = InputSocketCollection(self)
        self.outputs = OutputSocketCollection(self)
        self.ctrl_inputs = InputSocketCollection(self)
        self.ctrl_outputs = OutputSocketCollection(self)
        self.executor = None
        self.state = "CREATED"
        self.action = "NONE"
        self.position = [30 * self.inner_id, 30 * self.inner_id]
        self.description = ""
        self.log = ""
        self.ng = self.get_node_group() if self.node_type.upper() == "GROUP" else None
        self.create_properties()
        self.create_sockets()
        self.create_ctrl_sockets()
        # logger.debug("Create {}: {}".format(self.node_type, self.name))

    def create_properties(self):
        """Create properties for this node.
        If this node is a group node, create properties based on the exposed properties.
        """
        self.properties.clear()
        if self.node_type.upper() == "GROUP":
            self.create_group_properties()

    def create_group_properties(self):
        """Create properties based on the exposed properties."""
        for prop in self.group_properties:
            node, prop_name, new_prop_name = prop
            if prop_name not in self.ng.nodes[node].properties.keys():
                raise ValueError(
                    "Property {} does not exist in the properties of node {}".format(
                        prop_name, node
                    )
                )
            p = self.ng.nodes[node].properties[prop_name].copy()
            p.name = new_prop_name
            # TODO add the default value to group property
            self.properties.append(p)

    def create_sockets(self):
        """Create input and output sockets for this node.
        If this node is a group node, create sockets based on group inputs and outputs.
        """
        self.inputs.clear()
        self.outputs.clear()
        if self.node_type.upper() == "GROUP":
            self.create_group_sockets()

    def create_ctrl_sockets(self):
        """Create control input and output sockets for this node."""
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "entry")
        socket = self.ctrl_inputs.new("General", "ctrl")
        socket.link_limit = 1000
        socket = self.ctrl_outputs.new("General", "exit")
        socket = self.ctrl_outputs.new("General", "ctrl")
        socket.link_limit = 1000

    def create_group_sockets(self):
        """Create input and output sockets based on group inputs
        and outputs.

        group_inputs = [
            ["add1", "x", "x"],
            ["add1", "y", "y"]]
        """
        for input in self.group_inputs:
            node, socket, name = input
            if socket not in self.ng.nodes[node].inputs.keys():
                raise ValueError(
                    "Socket {} does not exist in the intputs of node {}".format(
                        socket, node
                    )
                )
            identifier = self.ng.nodes[node].inputs[socket].identifier
            self.inputs.new(identifier, name)
        for output in self.group_outputs:
            node, socket, name = output
            if socket not in self.ng.nodes[node].outputs.keys():
                raise ValueError(
                    "Socket {} does not exist in the outputs of node {}".format(
                        socket, node
                    )
                )
            identifier = self.ng.nodes[node].outputs[socket].identifier
            self.outputs.new(identifier, name)

    def reset(self):
        """Reset this node and all its child nodes to "CREATED".

        Note, even through the core principle require that each node
        run independently. This action will set the state of this node and
        all its child nodes to "CREATED". Because this is execute by human.
        In order to do that, we need use the nodetree to reset its child nodes.
        """
        from scinode.orm.db_nodetree import DBNodeTree

        if self.node_type not in ["REF"]:
            ent = DBNodeTree(uuid=self.uuid)
            ent.reset_node(self.name)
        self.update()

    def pre_save(self):
        """Pre action before save data to database.
        If this node is a group node, save the nodetree group.
        """
        if self.node_type.upper() == "GROUP":
            self.ng.worker_name = self.worker_name
            # print("node group nodes: ", self.ng.nodes.keys())
            self.ng.save()

    def pre_load(self):
        """Pre action before load data from database."""
        pass

    @property
    def group_properties(self):
        return self.ng.group_properties if self.ng else []

    @property
    def group_inputs(self):
        return self.ng.group_inputs if self.ng else []

    @property
    def group_outputs(self):
        return self.ng.group_outputs if self.ng else []

    @property
    def node_group(self):
        return self.get_node_group()

    def get_node_group(self):
        """Get the node group of this node.

        Returns:
            NodeTree: The node group of this node.
        """
        from scinode.database.client import scinodedb

        ntdata = scinodedb["nodetree"].find_one({"uuid": self.uuid}, {"name": 1})
        if ntdata is not None:
            from scinode import NodeTree

            nt = NodeTree.load(self.uuid)
            return nt
        else:
            return self.get_default_node_group()

    def get_default_node_group(self):
        from scinode import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
        )
        return nt

    def to_dict(self, short=False):
        """Save all datas, include properties, input and output sockets.

        This will be called when execute nodetree
        """
        from scinode.version import __version__
        import json
        import hashlib
        import cloudpickle as pickle

        logger.debug("save_to_db: {}".format(self.name))

        if not self.worker_name:
            self.worker_name = self.nodetree.worker_name if self.nodetree else ""
        self.pre_save()

        if short:
            data = {
                "name": self.name,
                "identifier": self.identifier,
                "node_type": self.node_type,
                "uuid": self.uuid,
                "register_path": self.register_path,
            }
        else:
            metadata = self.get_metadata()
            properties = self.properties_to_dict()
            input_sockets = self.input_sockets_to_dict()
            output_sockets = self.output_sockets_to_dict()
            ctrl_input_sockets = self.ctrl_input_sockets_to_dict()
            ctrl_output_sockets = self.ctrl_output_sockets_to_dict()
            executor = self.executor_to_dict()
            data = {
                "version": "scinode@{}".format(__version__),
                "uuid": self.uuid,
                "name": self.name,
                "inner_id": self.inner_id,
                "state": self.state,
                "action": self.action,
                "error": "",
                "metadata": metadata,
                "properties": properties,
                "inputs": input_sockets,
                "outputs": output_sockets,
                "ctrl_inputs": ctrl_input_sockets,
                "ctrl_outputs": ctrl_output_sockets,
                "executor": executor,
                "scheduler": self.scheduler,
                "position": self.position,
                "description": self.description,
                "log": self.log,
                "hash": "",
                "node_class": pickle.dumps(""),
            }
            # calculate the hash of metadata
            hash_metadata = {
                "executor": executor,
                "args": self.args,
                "kwargs": self.kwargs,
            }
            # we can not hash binary data for the moment
            if not executor["is_pickle"]:
                data["metadata"]["hash"] = hashlib.md5(
                    json.dumps(hash_metadata).encode("utf-8")
                ).hexdigest()
            else:
                data["metadata"]["hash"] = str(uuid1())
                # we pickle the class and save it to database
                # so that we can register when load it in the nodetree
                data["node_class"] = pickle.dumps(self.__class__)
        return data

    def get_metadata(self):
        """Export metadata to a dictionary."""
        metadata = {
            "node_type": self.node_type,
            "catalog": self.catalog,
            "identifier": self.identifier,
            "nodetree_uuid": self.nodetree.uuid
            if self.nodetree
            else self.nodetree_uuid,
            "ref_uuid": self.ref_uuid,
            "copy_uuid": self.copy_uuid,
            "platform": self.platform,
            "copied_from": self.copied_from,
            "scattered_from": self.scattered_from,
            "scattered_label": self.scattered_label,
            "scatter_node": self.scatter_node,
            "counter": self.counter,
            "args": self.args,
            "kwargs": self.kwargs,
            "group_properties": self.group_properties,
            "group_inputs": self.group_inputs,
            "group_outputs": self.group_outputs,
            "worker_name": self.worker_name,
            "computer": self.computer,
            "register_path": self.register_path,
        }
        if not self.worker_name:
            metadata.update({"worker_name": self.nodetree.worker_name})
        else:
            metadata.update({"worker_name": self.worker_name})
        return metadata

    def properties_to_dict(self):
        """Export properties to a dictionary.
        This data will be used for calculation.
        """
        properties = {}
        for p in self.properties:
            properties[p.name] = p.to_dict()
        # properties from inputs
        # data from property
        for input in self.inputs:
            if input.property is not None:
                properties[input.name] = input.property.to_dict()
            else:
                properties[input.name] = None
        return properties

    def input_sockets_to_dict(self):
        """Export input sockets to a dictionary."""
        # save all relations using links
        inputs = []
        for socket in self.inputs:
            inputs.append(socket.to_dict())
        return inputs

    def output_sockets_to_dict(self):
        """Export output sockets to a dictionary."""
        # save all relations using links
        outputs = []
        for socket in self.outputs:
            outputs.append(socket.to_dict())
        return outputs

    def ctrl_input_sockets_to_dict(self):
        """Export ctrl_input sockets to a dictionary."""
        # save all relations using links
        ctrl_inputs = []
        for socket in self.ctrl_inputs:
            ctrl_inputs.append(socket.to_dict())
        return ctrl_inputs

    def ctrl_output_sockets_to_dict(self):
        """Export ctrl_output sockets to a dictionary."""
        # save all relations using links
        ctrl_outputs = []
        for socket in self.ctrl_outputs:
            ctrl_outputs.append(socket.to_dict())
        return ctrl_outputs

    def executor_to_dict(self):
        """Export executor dictionary to a dictionary.
        Three kinds of executor:
        - Python built-in function. e.g. getattr
        - User defined function
        - User defined class.
        """
        executor = self.get_executor() or self.executor
        if executor is None:
            return executor
        executor.setdefault("type", "function")
        executor.setdefault("is_pickle", False)
        if not executor["is_pickle"] and "name" not in executor:
            executor["name"] = executor["path"].split(".")[-1]
            executor["path"] = executor["path"][0 : -(len(executor["name"]) + 1)]
        return executor

    @classmethod
    def from_dict(cls, data):
        """Rebuild Node from dict data."""
        from scinode.nodes import node_pool
        import cloudpickle as pickle

        # register the node created by decorator
        if data.get("executor", {}).get("is_pickle", False):
            from scinode.nodes import node_pool

            node_class = pickle.loads(data["node_class"])
            node_pool[node_class.identifier] = node_class
        node = node_pool[data["metadata"]["identifier"]](
            name=data["name"], uuid=data["uuid"]
        )
        # load properties
        node.update_from_dict(data)
        return node

    def update_from_dict(self, data):
        """udpate node from dict data.
        Set metadata and properties.
        """
        for key in ["uuid", "state", "action", "description", "hash", "position"]:
            if data.get(key):
                setattr(self, key, data.get(key))
        # read all the metadata
        for key in [
            "worker_name",
            "parent",
            "scatter_node",
            "scattered_from",
            "scattered_label",
            "nodetree_uuid",
        ]:
            if data["metadata"].get(key):
                setattr(self, key, data["metadata"].get(key))
        # properties first, because the socket may be dynamic
        for name in self.properties.keys():
            if name in data["properties"]:
                # logging.debug(f"Set property {name}, value: {data['properties'][name]}")
                self.properties[name].value = data["properties"][name]["value"]
        # inputs
        # print("inputs: ", data.get("inputs", None))
        if data.get("inputs", None):
            for i in range(len(data["inputs"])):
                if data["inputs"][i].get("uuid", None):
                    self.inputs[i].uuid = data["inputs"][i]["uuid"]
                if self.inputs[i].name in data["properties"]:
                    p = data["properties"][self.inputs[i].name]
                    self.inputs[i].property.value = p["value"]
        # outputs
        # print("outputs: ", data.get("outputs", None))
        if data.get("outputs", None):
            for i in range(len(data["outputs"])):
                if data["outputs"][i].get("uuid", None):
                    self.outputs[i].uuid = data["outputs"][i]["uuid"]

    @classmethod
    def update_from_yaml(cls, filename=None, string=None):
        """update db node from yaml file.

        Args:
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            node: _description_
        """
        import yaml
        from scinode.utils.node import yaml_to_dict
        from pprint import pprint

        # load data
        if filename:
            with open(filename, "r") as f:
                ndata = yaml.safe_load(f)
        elif string:
            ndata = yaml.safe_load(string)
        else:
            raise Exception("Please specific a filename or yaml string.")
        ndata = yaml_to_dict(ndata)
        nt = cls.load(ndata["uuid"])
        return nt

    @classmethod
    def load(cls, uuid):
        """Load Node data from database."""
        from scinode.utils.node import get_node_data

        if "-" in str(uuid):
            ndata = get_node_data({"uuid": uuid})
        else:
            ndata = get_node_data({"index": uuid})
        # cls.pre_load(ndata)
        node = cls.from_dict(ndata)
        return node

    @classmethod
    def new(cls, identifier, name=None):
        """Create a node from a identifier."""
        from scinode.nodes import node_pool
        import difflib

        if identifier not in node_pool:
            items = difflib.get_close_matches(identifier, node_pool)
            if len(items) == 0:
                msg = "Identifier: {} is not defined.".format(identifier)
            else:
                msg = "Identifier: {} is not defined. Do you mean {}".format(
                    identifier, ", ".join(items)
                )
            raise Exception(msg)
        NodeClass = node_pool[identifier]
        node = NodeClass(name=name)
        return node

    def copy(self, name=None, nodetree=None, is_ref=False):
        """Copy a node.

        Copy a node to a new node. If nodetree is None, the node will be copied inside the same nodetree, otherwise the node will be copied to a new nodetree.
        The properties, inputs and outputs will be copied.

        Args:
            name (str, optional): _description_. Defaults to None.
            nodetree (NodeTree, optional): _description_. Defaults to None.

        Returns:
            Node: _description_
        """
        print(f"Copy node {self.name}, as a ref: {is_ref}")
        if nodetree is not None:
            # copy node to a new nodetree, keep the name
            name = self.name if name is None else name
        else:
            # copy node inside the same nodetree, change the name
            nodetree = self.nodetree
            name = f"{self.name}_copy" if name is None else name
        node = self.__class__(
            name=name, uuid=None, nodetree=nodetree, copied_from=self.uuid
        )
        # becareful when copy the properties, the value should be copied
        # it will update the sockets, so we copy the properties first
        # then overwrite the sockets
        for i in range(len(self.properties)):
            node.properties[i].value = self.properties[i].value
        # should pass the node to the socket as parent
        if is_ref:
            node.node_type = "REF"
            node.ref_uuid = self.uuid
        node.inputs = self.inputs.copy(parent=node, is_ref=is_ref)
        node.outputs = self.outputs.copy(parent=node, is_ref=is_ref)
        return node

    def get_executor(self):
        """Get the default executor."""
        executor = None
        if self.node_type.upper() == "GROUP":
            executor = {
                "path": "scinode.executors.built_in",
                "name": "NodeGroup",
                "type": "class",
            }
        return executor

    def get_results(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.utils.node import get_results

        results = get_results(self.uuid)
        return results

    def update(self):
        """Update node."""
        pass

    @property
    def results(self):
        return self.get_results()

    def ref_to(self, uuid):
        """Set reference node."""
        from scinode.database.client import scinodedb

        self.node_type = "REF"
        self.ref_uuid = uuid
        ndata = scinodedb["node"].find_one(
            {"uuid": uuid}, {"_id": 0, "metadata.identifier": 1, "outputs": 1}
        )
        assert ndata != None
        assert self.identifier == ndata["metadata"]["identifier"]
        for i in range(len(ndata["outputs"])):
            self.outputs[i].uuid = ndata["outputs"][i]["uuid"]

    def __repr__(self) -> str:
        s = ""
        s += '{}(name="{}", properties = ['.format(self.__class__.__name__, self.name)
        s += ", ".join([f'"{x}"' for x in self.properties.keys()])
        s += "], inputs = ["
        s += ", ".join([f'"{x}"' for x in self.inputs.keys()])
        s += "], outputs = ["
        s += ", ".join([f'"{x}"' for x in self.outputs.keys()])
        s += "])\n"
        return s

    def set(self, data):
        """Set properties by a dict.

        Args:
            data (dict): _description_
        """
        from scinode.core.socket import NodeSocket

        for key, value in data.items():
            if key in self.properties.keys():
                self.properties[key].value = value
            elif key in self.inputs.keys():
                if isinstance(value, NodeSocket):
                    self.nodetree.links.new(value, self.inputs[key])
                else:
                    self.inputs[key].property.value = value
            else:
                raise Exception(
                    "No property named {}. Accept name are {}".format(
                        key, list(self.properties.keys() + list(self.inputs.keys()))
                    )
                )

    def get(self, key):
        """Get the value of property by key.

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.properties[key].value

    def save(self):
        """Modify and save a node to database.

        If node does not exist in database, it will raise an exception.
        One can only modify the following properties of a node:
        - metadata, including the description, tags, worker_name
        - properties, including the value of properties, and the value of the inputs.
        One can not modify the following properties of a node:
        - node name
        - nodetree
        - links

        #TODO is there a race condition here?
        """
        from scinode.database.client import scinodedb
        from scinode.utils.node import serialize
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        query = {"uuid": self.uuid}
        ndata = scinodedb["node"].find_one(query, {"name": 1})
        if ndata is None:
            raise Exception("Node {} does not exist in database.".format(self.uuid))
        metadata = self.get_metadata()
        properties = self.properties_to_dict()
        new_data = {
            "metadata": metadata,
            "properties": serialize(properties),
        }
        # reset the node
        msg = f"{self.nodetree_uuid},node,{self.name}:action:RESET"
        send_message_to_queue(broker_queue_name, msg)
        # update
        scinodedb["node"].update_one(query, {"$set": new_data})


def build_node_from_json(dbdata):
    import importlib

    module = importlib.import_module("{}".format(dbdata["node_path"]))
    node_type = getattr(module, dbdata["node_type"])
    node = node_type.from_json(dbdata)
    return node
