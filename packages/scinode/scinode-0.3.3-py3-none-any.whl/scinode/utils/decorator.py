from typing import Any


def create_node(ndata):
    """Create a node class from node data.

    Args:
        ndata (dict): node data

    Returns:
        _type_: _description_
    """
    from scinode.core.node import Node

    # print("ndata: ", ndata)
    class MyNode(Node):
        identifier: str = ndata["identifier"]
        node_type: str = ndata["node_type"]
        args = ndata.get("args", [])
        kwargs = ndata.get("kwargs", [])
        catalog = ndata.get("catalog", "Others")
        register_path = ndata.get("register_path", "")

        def create_properties(self):
            for prop in ndata.get("properties", []):
                kwargs = prop[2] if len(prop) > 2 else {}
                self.properties.new(prop[0], prop[1], **kwargs)

        def create_sockets(self):
            for input in ndata.get("inputs", []):
                inp = self.inputs.new(input[0], input[1])
                if len(input) > 2:
                    prop = [input[2][0], input[1], input[2][1]]
                    # print("prop: ", prop)
                    kwargs = prop[2] if len(prop) > 2 else {}
                    inp.add_property(prop[0], prop[1], **kwargs)
            for output in ndata.get("outputs", []):
                self.outputs.new(output[0], output[1])

        def get_executor(self):
            executor = ndata.get("executor", {})
            return executor

    return MyNode


def create_node_group(ngdata):
    """Create a node group class from node group data.

    Args:
        ngdata (dict): node data

    Returns:
        _type_: _description_
    """
    from scinode.core.node import Node

    class MyNodeGroup(Node):
        identifier: str = ngdata["identifier"]
        node_type: str = "GROUP"
        catalog = ngdata.get("catalog", "Others")
        register_path = ngdata.get("register_path", "")

        def get_default_node_group(self):
            nt = ngdata["nt"]
            nt.name = self.name
            nt.uuid = self.uuid
            nt.parent_node = self.uuid
            nt.worker_name = self.worker_name
            return ngdata["nt"]

    return MyNodeGroup


def register_node(
    identifier,
    node_type="Normal",
    args={},
    kwargs={},
    properties=[],
    inputs=[],
    outputs=[],
    executor={},
    register_path="",
    catalog="Others",
):
    from scinode.utils import register
    from scinode.nodes import node_pool

    ndata = {
        "identifier": identifier,
        "node_type": node_type,
        "catalog": catalog,
        "args": args,
        "kwargs": kwargs,
        "properties": properties,
        "inputs": inputs,
        "outputs": outputs,
        "executor": executor,
        "register_path": register_path,
    }
    node = create_node(ndata)
    try:
        register(node_pool, [node])
    except Exception as e:
        print(f"Warnning: Register node {ndata['identifier']} failed.", e)
        return None
    return node


def register_node_group(identifier, nt, register_path="", catalog="Others"):
    from scinode.utils import register
    from scinode.nodes import node_pool

    ngata = {
        "identifier": identifier,
        "catalog": catalog,
        "nt": nt,
        "register_path": register_path,
    }
    node = create_node_group(ngata)
    try:
        register(node_pool, [node])
    except Exception as e:
        print(f"Warnning: Register node group {ngata['identifier']} failed.", e)
        return None
    return node


# decorator with arguments indentifier, args, kwargs, properties, inputs, outputs, executor
def decorator_node(
    identifier,
    node_type="Normal",
    args={},
    kwargs={},
    properties=[],
    inputs=[],
    outputs=[],
    catalog="Others",
):
    """Generate a decorator that register a function as a SciNode node.

    Attributes:
        indentifier (str): node identifier
        catalog (str): node catalog
        args (list): node args
        kwargs (dict): node kwargs
        properties (list): node properties
        inputs (list): node inputs
        outputs (list): node outputs
    """

    def decorator(func):
        import cloudpickle as pickle

        # use cloudpickle to serialize function
        executor = {
            "executor": pickle.dumps(func),
            "type": "function",
            "is_pickle": True,
        }
        node = register_node(
            identifier,
            node_type,
            args,
            kwargs,
            properties,
            inputs,
            outputs,
            executor,
            catalog=catalog,
        )
        func.identifier = identifier
        func.node = node
        return func

    return decorator


# decorator with arguments indentifier, args, kwargs, properties, inputs, outputs, executor
def decorator_node_group(identifier, catalog="Others", executor_path=None):
    """Generate a decorator that register a function as a SciNode node.

    Attributes:
        indentifier (str): node identifier
    """

    def decorator(func):
        import cloudpickle as pickle

        # use cloudpickle to serialize function
        executor = {
            "executor": pickle.dumps(func),
            "type": "pickle",
        }
        nt = func()
        node = register_node_group(identifier, nt, catalog=catalog)
        return node

    return decorator


class NodeDecoratorCollection:
    """Collection of node decorators."""

    node = staticmethod(decorator_node)
    group = staticmethod(decorator_node_group)

    __call__: Any = node  # Alias '@node' to '@node.node'.


node = NodeDecoratorCollection()

if __name__ == "__main__":

    @node.group("TestAdd")
    def my_add_group():
        from scinode import NodeTree

        nt = NodeTree()
        add1 = nt.nodes.new("TestAdd", "add1")
        add2 = nt.nodes.new("TestAdd", "add2")
        add3 = nt.nodes.new("TestAdd", "add3")
        nt.links.new(add1.outputs[0], add3.inputs[0])
        nt.links.new(add2.outputs[0], add3.inputs[1])
        nt.group_properties = [
            ("add1", "t", "t1"),
            ("add2", "t", "t2"),
        ]
        nt.group_inputs = [("add1", "x", "x"), ("add2", "x", "y")]
        nt.group_outputs = [("add3", "Result", "Result")]
        return nt
