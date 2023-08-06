from scinode.core.node import Node


class TestFloat(Node):
    identifier = "TestFloat"
    name = "TestFloat"
    catalog = "Test"

    kwargs = ["t", "value"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)
        self.properties.new("Float", "value", default=0.0)

    def create_sockets(self):
        self.outputs.new("Float", "float")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_float",
        }


class TestString(Node):
    identifier = "TestString"
    name = "String"
    catalog = "Test"

    kwargs = ["t", "value"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)
        self.properties.new("String", "value", default="")

    def create_sockets(self):
        self.outputs.new("String", "string")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_string",
        }


class TestAdd(Node):
    """TestAdd

    Inputs:
        t (int): delay time (s).
        x (float):
        y (float):

    Outputs:
        Result (float).

    """

    identifier: str = "TestAdd"
    name = "TestAdd"
    catalog = "Test"
    kwargs = ["t", "x", "y"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        self.inputs.new("Float", "y")
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_add",
        }


class TestMinus(Node):

    identifier: str = "TestMinus"
    name = "TestMinus"
    catalog = "Test"
    kwargs = ["t", "x", "y"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        self.inputs.new("Float", "y")
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_minus",
        }


class TestPower(Node):

    identifier: str = "TestPower"
    name = "TestPower"
    catalog = "Test"
    kwargs = ["t", "x", "y"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        input = self.inputs.new("Float", "y")
        input.property.value = 2
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_power",
        }


class TestGreater(Node):

    identifier: str = "TestGreater"
    name = "TestGreater"
    catalog = "Test"
    kwargs = ["t", "x", "y"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        self.inputs.new("Float", "y")
        self.outputs.new("Bool", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_greater",
        }


class TestLess(Node):

    identifier: str = "TestLess"
    name = "TestLess"
    catalog = "Test"
    kwargs = ["t", "x", "y"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        self.inputs.new("Float", "y")
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_less",
        }


class TestSqrt(Node):

    identifier: str = "TestSqrt"
    name = "TestSqrt"
    catalog = "Test"
    kwargs = ["t", "x"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "x")
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_sqrt",
        }


class TestRange(Node):

    identifier: str = "TestRange"
    name = "Range"
    catalog = "Test"
    kwargs = ["start", "stop", "step"]

    def create_properties(self):
        self.properties.new("Float", "start", default=1)
        self.properties.new("Float", "stop", default=5)
        self.properties.new("Float", "step", default=1)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.outputs.new("Float", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_range",
        }


class TestWriteFile(Node):
    identifier = "TestWriteFile"
    name = "WriteFile"
    catalog = "Test"

    kwargs = ["directory", "filename", "content"]

    def create_properties(self):
        self.properties.new("String", "directory", default="test")
        self.properties.new("String", "filename", default="abc")
        self.properties.new("String", "content", default="abc")

    def create_sockets(self):
        self.outputs.new("String", "Filepath")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "TestWriteFile",
            "type": "class",
        }


class TestPerson(Node):

    identifier: str = "TestPerson"
    name = "Person"
    catalog = "Test"
    args = ["name", "age"]

    def create_properties(self):
        self.properties.new("Float", "name", default="Bob")
        self.properties.new("Float", "age", default=5)

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.outputs.new("General", "Person")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "person",
            "type": "function",
        }


class TestEnum(Node):

    identifier: str = "TestEnum"
    name = "Enum"
    catalog = "Test"
    kwargs = ["t", "function"]

    def create_properties(self):
        self.properties.new("Int", "t", default=1)
        self.properties.new(
            "Enum",
            "function",
            options=[
                ["add", "test_add", "add function"],
                ["sqrt", "test_sqrt", "sqrt function"],
            ],
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.outputs.new("General", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_enum",
        }


class TestEnumUpdate(Node):

    identifier: str = "TestEnumUpdate"
    name = "Enum"
    catalog = "Test"

    def create_properties(self):
        self.properties.new("Int", "t", default=1)
        self.properties.new(
            "Enum",
            "function",
            default="add",
            options=[
                ["add", "test_add", "add function"],
                ["sqrt", "test_sqrt", "sqrt function"],
            ],
            update=self.create_sockets,
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        if self.properties["function"].value in ["add"]:
            self.inputs.new("Float", "x")
            self.inputs.new("Float", "y")
            self.kwargs = ["t", "x", "y"]
        elif self.properties["function"].value in ["sqrt"]:
            self.inputs.new("Float", "x")
            self.kwargs = ["t", "x"]
        self.outputs.new("General", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": self.properties["function"].content,
            "type": "function",
        }


class TestRemoteDiff(Node):
    """TestRemoteDiff

    Inputs:
        file1 (str): path to file1.
        file2 (str): path to file2.

    Outputs:
        Result (str): difference between file1 and file2.

    """

    identifier: str = "TestRemoteDiff"
    name = "TestRemoteDiff"
    catalog = "Test"
    kwargs = ["file1", "file2"]

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("String", "file1")
        self.inputs.new("String", "file2")
        self.outputs.new("String", "result")

    def get_executor(self):
        return {
            "path": "scinode.executors.ssh.test_ssh_executor",
            "name": "RemoteDiff",
            "type": "class",
        }


node_list = [
    TestFloat,
    TestString,
    TestPower,
    TestAdd,
    TestMinus,
    TestGreater,
    TestLess,
    TestSqrt,
    TestRange,
    TestEnum,
    TestEnumUpdate,
    TestWriteFile,
    TestPerson,
    TestRemoteDiff,
]
