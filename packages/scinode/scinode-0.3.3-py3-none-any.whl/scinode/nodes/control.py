from scinode.core.node import Node


class ScinodeIf(Node):
    """If Node

    inputs:
        Input (General): default: None

    outputs:
        Result: the same value of the input

    ctrl_inputs:
        Entry : entry of the node
        Back : back to the entry

    ctrl_outputs:
        Exit : exit the node
        True : go to the true branch
        False : go to the false branch

    executor:
        path: scinode.executors.control.if_node
        name: ScinodeIf
        type: class
    """

    identifier: str = "If"
    node_type: str = "Normal"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "input")
        self.outputs.new("General", "result")
        self.kwargs = ["input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "back")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "exit")
        self.ctrl_outputs.new("General", "true")
        self.ctrl_outputs.new("General", "false")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.if_node",
            "name": "ScinodeIf",
            "type": "class",
        }


class ScinodeFor(Node):
    """For Node

    inputs:
        Input (General): default: None

    outputs:
        Result: the i-th value of the input, i is the iteration number

    ctrl_inputs:
        Entry : entry of the loop
        Iter : start the next iteration

    ctrl_outputs:
        Exit : exit the node
        Loop : go to the loop body
        Jump : exit the loop

    executor:
        path: scinode.executors.control.for_node
        name: ScinodeFor
        type: class
    """

    identifier: str = "For"
    node_type: str = "Normal"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "input")
        self.outputs.new("General", "result")
        self.kwargs = ["input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "iter")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "exit")
        self.ctrl_outputs.new("General", "loop")
        self.ctrl_outputs.new("General", "jump")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.for_node",
            "name": "ScinodeFor",
            "type": "class",
        }


class ScinodeSwitch(Node):
    identifier: str = "Switch"
    node_type: str = "Switch"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "input")
        self.inputs.new("General", "switch")
        self.outputs.new("General", "result")
        self.kwargs = ["input", "switch"]

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.switch_node",
            "name": "ScinodeSwitch",
            "type": "class",
        }


class ScinodeUpdate(Node):
    identifier: str = "Update"
    node_type: str = "Update"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "input")
        self.inputs.new("General", "update")
        self.outputs.new("General", "result")
        self.kwargs = ["input", "update"]

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.update_node",
            "name": "ScinodeUpdate",
            "type": "class",
        }


class ScinodeScatter(Node):
    identifier = "Scatter"
    node_type = "Control"
    catalog = "Control"

    def create_properties(self):
        self.properties.new("String", "datatype", default="General")

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        socket = self.inputs.new("General", "input")
        socket.link_limit = 100
        self.outputs.new("General", "result")
        self.kwargs = ["input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "back")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "exit")
        self.ctrl_outputs.new("General", "scatter")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.scatter_node",
            "name": "ScinodeScatter",
            "type": "class",
        }


node_list = [
    ScinodeIf,
    ScinodeFor,
    ScinodeSwitch,
    ScinodeUpdate,
    ScinodeScatter,
]
