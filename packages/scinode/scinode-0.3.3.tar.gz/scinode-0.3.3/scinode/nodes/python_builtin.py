from scinode.core.node import Node


class IntNode(Node):
    """Output a int value."""

    identifier = "Int"
    name = "Int"
    catalog = "input"

    args = ["value"]
    kwargs = []

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Int", "value")
        self.outputs.new("Int", "int")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "int",
            "type": "function",
        }


class FloatNode(Node):
    """Output a float value."""

    identifier = "Float"
    name = "Float"
    catalog = "input"

    args = ["value"]
    kwargs = []

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Float", "value")
        self.outputs.new("Float", "float")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "float",
            "type": "function",
        }


class BoolNode(Node):
    """Output a bool value."""

    identifier = "Bool"
    name = "Bool"
    catalog = "input"

    args = ["value"]
    kwargs = []

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("Bool", "value")
        self.outputs.new("Bool", "bool")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "bool",
            "type": "function",
        }


class StrNode(Node):
    """Output a string."""

    identifier = "String"
    name = "String"
    catalog = "input"

    args = ["value"]
    kwargs = []

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("String", "value")
        self.outputs.new("String", "string")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "str",
            "type": "function",
        }


class Dict(Node):
    """Dict data type and its methods.

    Executor:
        Python builtin function: dict and its methods.


    Example:
        # Create a dict
        dict1 = nt.nodes.new("Dict", function="dict", input={"a": 1, "b": 2})
        # get a item by key
        get = nt.nodes.new("Dict", function="get", Key="b")
        nt.links.new(dict1.outputs[0], get.inputs[0])
        # add an item to the dict
        setitem = nt.nodes.new("Dict", function="__setitem__", Key="c", Value=3)
        nt.links.new(dict1.outputs[0], setitem.inputs[0])
    """

    identifier = "Dict"
    name = "Dict"
    catalog = "Builtin"

    list_func_items = [
        ["dict", "dict", "dict"],
        ["clear", "clear", "clear"],
        ["copy", "copy", "copy"],
        ["fromkeys", "fromkeys", "fromkeys"],
        ["get", "get", "get"],
        ["items", "items", "items"],
        ["keys", "keys", "keys"],
        ["pop", "pop", "pop"],
        ["popitem", "popitem", "popitem"],
        ["setdefault", "setdefault", "setdefault"],
        ["update", "update", "update"],
        ["values", "values", "values"],
        ["__setitem__", "__setitem__", "__setitem__"],
    ]

    def create_properties(self):
        self.properties.new(
            "Enum",
            "function",
            default="dict",
            options=self.list_func_items,
            update=self.create_sockets,
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.kwargs = ["function", "input"]
        self.inputs.new("General", "input")
        self.outputs.new("General", "dict")
        if self.properties["function"].value in ["dict"]:
            pass
        elif self.properties["function"].value in ["get"]:
            self.inputs.new("General", "key")
            self.args = ["key"]
            self.outputs.new("General", "result")
        elif self.properties["function"].value in ["fromkeys"]:
            self.inputs.new("General", "keys")
            self.args = ["keys"]
        elif self.properties["function"].value in ["pop"]:
            self.inputs.new("General", "key")
            self.args = ["key"]
            self.outputs.new("General", "result")
        elif self.properties["function"].value in ["clear"]:
            pass
        elif self.properties["function"].value in ["keys", "values", "items"]:
            self.outputs.new("General", "result")
        elif self.properties["function"].value in ["__setitem__"]:
            self.inputs.new("General", "key")
            self.inputs.new("General", "value")
            self.args = ["key", "value"]
        elif self.properties["function"].value in ["update"]:
            self.inputs.new("General", "value")
            self.args = ["value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "run_dict",
            "type": "function",
        }


class Getattr(Node):
    """The Getattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: getattr()

    Results:
        A pyhont object.

    Example:

    >>> att = nt.nodes.new("Getattr")
    >>> att.properties["name"].value = "real"

    """

    identifier: str = "Getattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "source")
        inp = self.inputs.new("String", "name")
        inp.property.value = "__class__"
        self.outputs.new("General", "result")
        self.args = ["source", "name"]

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "getattr",
            "type": "function",
        }


class Setattr(Node):
    """The Setattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: setattr()

    Results:
        A pyhont object.

    Example:

    >>> nt = NodeTree(name="test_setattr")
    >>> person1 = nt.nodes.new("TestPerson", "person1")
    >>> str1 = nt.nodes.new("TestString", "str1")
    >>> str1.properties["String"].value = "Peter"
    >>> att = nt.nodes.new("Setattr")
    >>> att.properties["name"].value = "name"
    >>> nt.links.new(person1.outputs[0], att.inputs["source"])
    >>> nt.links.new(str1.outputs[0], att.inputs["value"])

    """

    identifier: str = "Setattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "source")
        inp = self.inputs.new("General", "name")
        inp.property.value = "__class__"
        self.inputs.new("General", "value")
        self.outputs.new("General", "result")
        self.args = ["source", "name", "value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setattr",
            "type": "function",
        }


class Getitem(Node):
    """The Getitem node suppors index lookups.

    Executor:
        Python builtin function: __getitem__()

    Results:
        A pyhont object.

    Example:

    >>> getitem1 = nt.nodes.new("Getitem", "getitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> nt.links.new(nt.nodes["power1"].outputs[0], getitem1.inputs["source"])
    >>> nt.links.new(arange1.outputs[0], getitem1.inputs["index"])
    """

    identifier: str = "Getitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "source")
        inp = self.inputs.new("General", "index")
        inp.property.value = 0
        self.outputs.new("General", "result")
        self.args = ["source", "index"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "getitem",
            "type": "function",
        }


class Setitem(Node):
    """The Setitem node is used for assigning a value to an item.

    Executor:
        Python builtin function: __setitem__()

    Results:
        A pyhont object.

    Example:

    >>> setitem1 = nt.nodes.new("Setitem", "setitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> linspace2 = nt.nodes.new("ScinodeNumpy", "linspace2")
    >>> linspace2.set({"function": "linspace", "start": 11, "stop": 15, "num": 2})
    >>> nt.links.new(nt.nodes["linspace1"].outputs[0], setitem1.inputs["source"])
    >>> nt.links.new(arange1.outputs[0], setitem1.inputs["index"])
    >>> nt.links.new(linspace2.outputs[0], setitem1.inputs["value"])
    """

    identifier: str = "Setitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "source")
        inp = self.inputs.new("General", "index")
        inp.property.value = 0
        self.inputs.new("General", "value")
        self.outputs.new("General", "result")
        self.args = ["source", "index", "value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setitem",
            "type": "function",
        }


class Assign(Node):
    """Assign is used to perform operations on variables and values."""

    identifier: str = "Assign"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "value")
        self.kwargs = ["value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "Assign",
            "type": "class",
        }


class List(Node):
    """List data type and its methods.

    Executor:
        Python builtin function: list and its methods.


    Example:
        # Create a list
        list1 = nt.nodes.new("List", function="list", input=[1, 2, 3])
        # Append an item to the list
        append1 = nt.nodes.new("List", function="append", Value=4)
        nt.links.new(list1.outputs[0], append1.inputs[0])

    """

    identifier: str = "List"
    node_type: str = "Normal"
    catalog = "Builtin"

    list_func_items = [
        ["list", "list", "list"],
        ["append", "append", "append"],
        ["extend", "extend", "extend"],
        ["remove", "remove", "remove"],
        ["index", "index", "index"],
        ["count", "count", "count"],
        ["insert", "insert", "insert"],
        ["pop", "pop", "pop"],
        ["reverse", "reverse", "reverse"],
    ]

    def create_properties(self):
        self.properties.new(
            "Enum",
            "function",
            default="list",
            options=self.list_func_items,
            update=self.create_sockets,
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.args = []
        self.kwargs = ["function", "input"]
        self.inputs.new("General", "input", default=[])
        self.outputs.new("General", "list")
        if self.properties["function"].value in ["list"]:
            pass
        elif self.properties["function"].value in [
            "append",
            "extend",
            "remove",
        ]:
            self.inputs.new("General", "value")
            self.args = ["value"]
        elif self.properties["function"].value in [
            "index",
            "count",
        ]:
            self.inputs.new("General", "value")
            self.args = ["value"]
            self.outputs.new("Int", "result")
        elif self.properties["function"].value in ["insert"]:
            self.inputs.new("Int", "index")
            self.inputs.new("General", "value")
            self.args = ["index", "value"]
        elif self.properties["function"].value in ["pop"]:
            self.inputs.new("Int", "index")
            self.args = ["index"]
            self.outputs.new("General", "value")
        elif self.properties["function"].value in ["reverse"]:
            pass

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "run_list",
            "type": "function",
        }


class Operator(Node):
    """Standard operators in Python.

    Executor:
        Python builtin operators.


    Example:
        # Create a add node
        add1 = nt.nodes.new("Operator", operator="+")
        # Create a compare node
        lt = nt.nodes.new("Operator", operator=">")
    """

    identifier: str = "Operator"
    node_type: str = "Normal"
    catalog = "Builtin"

    # TODO: add more operators
    operator_items = [
        ["+", "add", "add"],
        ["-", "sub", "sub"],
        ["*", "mul", "mul"],
        ["/", "truediv", "truediv"],
        ["%", "mod", "mod"],
        ["**", "pow", "pow"],
        ["//", "floordiv", "floordiv"],
        ["==", "eq", "eq"],
        ["!=", "ne", "ne"],
        [">", "gt", "gt"],
        ["<", "lt", "lt"],
        [">=", "ge", "ge"],
        ["<=", "le", "le"],
    ]

    def create_properties(self):
        self.properties.new(
            "Enum",
            "operator",
            default="+",
            options=self.operator_items,
            update=self.create_sockets,
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        inp = self.inputs.new("General", "x")
        inp.add_property("Float", 0)
        inp = self.inputs.new("General", "y")
        inp.add_property("Float", 0)
        self.outputs.new("General", "result")
        self.args = ["x", "y"]
        self.kwargs = []

    def get_executor(self):
        return {
            "path": "operator",
            "name": self.properties["operator"].content,
            "type": "function",
        }


node_list = [
    IntNode,
    FloatNode,
    BoolNode,
    StrNode,
    List,
    Dict,
    Operator,
    Assign,
    Getattr,
    Setattr,
    Getitem,
    Setitem,
]
