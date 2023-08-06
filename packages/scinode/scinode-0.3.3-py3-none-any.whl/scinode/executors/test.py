import time
from scinode.core.executor import Executor
from scinode.utils.decorator import node


def test_float(t=0, value=0.0):
    """Float node."""
    time.sleep(t)
    return value


def test_string(t=0, value=""):
    """String node."""
    time.sleep(t)
    return value


def test_enum(t=0, value=""):
    """Enum node."""
    time.sleep(t)
    return value


def test_add(t=0, x=0, y=0):
    """Add node."""
    time.sleep(t)
    return x + y


def test_minus(t=0, x=0, y=0):
    """Minus node."""
    time.sleep(t)
    return x - y


def test_power(t=0, x=0, y=0):
    """Power node."""
    from math import pow

    time.sleep(t)
    return pow(x, y)


def test_greater(t=0, x=0, y=0):
    """Greater than node"""
    time.sleep(t)
    return x > y


def test_less(t=0, x=0, y=0):
    """Less than node"""
    time.sleep(t)
    return x < y


def test_sqrt(t=0, x=1):
    """sqrt node"""
    from math import sqrt

    time.sleep(t)
    return sqrt(x)


def test_range(start=0, stop=5, step=1):
    """Range node"""
    return list(range(start, stop, step))


class TestWriteFile(Executor):
    """Test write a file to a path.

    Args:
        Executor (_type_): _description_
    """

    def run(self):
        """"""
        import os

        print("    TestWriteFile job")
        workdir = os.path.join(
            self.worker_workdir,
            self.kwargs["directory"],
        )
        if not os.path.exists(workdir):
            os.mkdir(workdir)
        filepath = os.path.join(
            workdir,
            self.kwargs["filename"],
        )
        with open(filepath, "w") as f:
            f.write(self.kwargs["content"])
        return filepath


class Person:
    name = "Bob"
    age = 5

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def run(self):
        return self

    def __repr__(self) -> str:
        s = "Person(name={}, age={})".format(self.name, self.age)
        return s


def person(name, age):
    return Person(name, age)


@node(
    identifier="NodeTreeIfInExecutor",
    args=["x"],
    inputs=[["General", "x"]],
    outputs=[["General", "result"]],
)
def test_nodetree_if_in_executor(x):
    """Test run nodetree in an executor."""
    from scinode import NodeTree

    nt = NodeTree(name="nodetree_in_executor")
    if x < 0:
        op1 = nt.nodes.new("Operator", operator="+", x=x, y=-1)
    else:
        op1 = nt.nodes.new("Operator", operator="-", x=x, y=1)
    nt.launch()
    nt.wait()
    return op1.results[0]["value"]


@node(
    identifier="NodeTreeForInExecutor",
    args=["x"],
    inputs=[["General", "x"]],
    outputs=[["General", "result"]],
)
def test_nodetree_for_in_executor(x):
    """Test run nodetree in an executor."""
    from scinode import NodeTree

    nt = NodeTree(name="nodetree_in_executor")
    ops = [nt.nodes.new("Operator", operator="+", x=i, y=1) for i in range(x)]
    nt.launch()
    nt.wait()
    y = [op.results[0]["value"] for op in ops]
    return y


@node(
    identifier="NodeTreeForInExecutor2",
    args=["x"],
    inputs=[["General", "x"]],
    outputs=[["General", "result"]],
)
def test_nodetree_for_in_executor_2(x):
    """Test run nodetree in an executor."""
    from scinode import NodeTree

    nt = NodeTree(name="nodetree_in_executor")
    op1 = nt.nodes.new("Operator", operator="+")
    total = 0
    for i in range(x):
        nt.reset_node(op1.name)
        op1.inputs[0].value = total
        op1.inputs[1].value = i
        nt.launch()
        nt.wait()
        total = op1.results[0]["value"]
    return total
