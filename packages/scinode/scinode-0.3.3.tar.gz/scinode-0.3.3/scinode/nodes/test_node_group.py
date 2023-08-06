from scinode.core.node import Node


class TestSqrtPowerAdd(Node):

    identifier: str = "TestSqrtPowerAdd"
    name = "TestSqrtPowerAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_default_node_group(self):
        from scinode import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
            type="NODE_GROUP",
        )
        sqrt1 = nt.nodes.new("TestSqrt", "sqrt1")
        power1 = nt.nodes.new("TestPower", "power1")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt1.outputs[0], add1.inputs[0])
        nt.links.new(power1.outputs[0], add1.inputs[1])
        nt.group_properties = [
            ("sqrt1", "t", "t1"),
            ("add1", "t", "t2"),
        ]
        nt.group_inputs = [
            ("sqrt1", "x", "x"),
            ("power1", "x", "y"),
        ]
        nt.group_outputs = [("add1", "result", "result")]
        return nt


class TestForSum(Node):

    identifier: str = "TestForSum"
    name = "TestForSum"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_default_node_group(self):
        from scinode import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
            type="NODE_GROUP",
        )
        for1 = nt.nodes.new("For", "for1")
        add1 = nt.nodes.new("Operator", "add1", operator="+")
        float1 = nt.nodes.new("Float", "float1")
        assign1 = nt.nodes.new("Assign", "assign1")
        nt.links.new(for1.outputs[0], add1.inputs[0])
        nt.links.new(float1.outputs[0], add1.inputs[1])
        nt.links.new(add1.outputs[0], assign1.inputs[0])
        nt.ctrl_links.new(for1.ctrl_outputs["loop"], add1.ctrl_inputs["entry"])
        nt.ctrl_links.new(assign1.ctrl_outputs[0], for1.ctrl_inputs["iter"])
        nt.ctrl_links.new(assign1.ctrl_outputs["ctrl"], float1.ctrl_inputs["ctrl"])
        nt.group_properties = []
        nt.group_inputs = [
            ("for1", "input", "input"),
        ]
        nt.group_outputs = [("float1", "float", "result")]
        return nt


class TestNestedSqrtAdd(Node):

    identifier: str = "TestNestedSqrtAdd"
    name = "TestNestedSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_default_node_group(self):
        from scinode import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
            type="NODE_GROUP",
        )
        sqrt_power_add1 = nt.nodes.new("TestSqrtPowerAdd", "sqrt_power_add1")
        sqrt_power_add2 = nt.nodes.new("TestSqrtPowerAdd", "sqrt_power_add2")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt_power_add1.outputs[0], add1.inputs[0])
        nt.links.new(sqrt_power_add2.outputs[0], add1.inputs[1])
        nt.group_inputs = [("sqrt_power_add1", "x", "x"), ("sqrt_power_add2", "x", "y")]
        nt.group_outputs = [["add1", "result", "result"]]
        return nt


node_list = [
    TestSqrtPowerAdd,
    TestForSum,
    TestNestedSqrtAdd,
]
