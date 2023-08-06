from scinode.core.node import Node


class IfSelect(Node):
    """The IfSelect node suppors the ScinodeIf node."""

    identifier: str = "IfSelect"
    node_type: str = "Normal"
    catalog = "Utils"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Bool", "condition")
        self.inputs.new("General", "input1")
        self.inputs.new("General", "input2")
        self.outputs.new("General", "result")
        self.kwargs = ["condition", "input1", "input2"]

    def get_executor(self):
        return {
            "path": "scinode.executors.utils",
            "name": "if_select",
            "type": "function",
        }


node_list = [
    IfSelect,
]
