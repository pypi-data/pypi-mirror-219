from scinode.core.node import Node


class ScinodeNode(Node):
    identifier: str = "ScinodeNode"
    node_type: str = "Normal"

    def get_executor(self):
        return None


class DataNode(Node):
    identifier = "DataNode"
    node_type = "NORMAL"
    catalog = "Input"

    def create_properties(self):
        self.properties.new(
            "String",
            "datatype",
            default="General",
            update=self.create_sockets,
        )
        self.properties.new("String", "uuid", default="")

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "input")
        self.outputs.new(self.properties["datatype"].value, "result")
        self.kwargs = ["uuid", "input"]

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "data_node",
            "type": "function",
        }


node_list = [
    ScinodeNode,
    DataNode,
]
