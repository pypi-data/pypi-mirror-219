from scinode.core.node import Node


class BashNode(Node):
    """Node to run bash command.

    properties:
        command: bash command
        cwd: working directory

    inputs:
        dep: upstreaming dependencies

    outputs:
        Result: result of the bash command

    """

    identifier = "BashNode"
    node_type = "NORMAL"
    catalog = "Utils"

    def create_properties(self):
        self.properties.new("String", "command")

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "dep")
        self.inputs.new("String", "cwd")
        self.outputs.new("General", "result")
        self.kwargs = ["command", "cwd"]

    def get_executor(self):
        return {
            "path": "scinode.executors.bash_executor",
            "name": "BashExecutor",
            "type": "class",
        }


node_list = [
    BashNode,
]
