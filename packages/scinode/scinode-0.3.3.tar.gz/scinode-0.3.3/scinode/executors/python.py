from scinode.core.executor import Executor
import builtins


def run_list(*args, **kwargs):
    """list and its methods.
    https://docs.python.org/3/tutorial/datastructures.html
    """
    print("    Run List node")
    function = kwargs.pop("function")
    input = kwargs.pop("input")
    if function == "list":
        if input is not None:
            return builtins.list(input)
        else:
            return []
    elif function in ["pop"]:
        r = getattr(input, function)(*args, **kwargs)
        return input, r
    else:
        r = getattr(input, function)(*args, **kwargs)
        if r is not None:
            return input, r
        else:
            return input


def run_dict(*args, **kwargs):
    """dict and its methods.
    https://docs.python.org/3/tutorial/datastructures.html
    """
    print("    Run Dict node")
    function = kwargs.pop("function")
    input = kwargs.pop("input")
    if function == "dict":
        if input is not None:
            return builtins.dict(input)
        else:
            return {}
    elif function in ["keys", "values", "items"]:
        r = getattr(input, function)(*args, **kwargs)
        return input, list(r)
    elif function in ["get", "pop"]:
        r = getattr(input, function)(*args, **kwargs)
        return input, r
    else:
        r = getattr(input, function)(*args, **kwargs)
        if r is not None:
            return input, r
        else:
            return input


class Assign(Executor):
    """ """

    def run(self):
        """ """
        """To assgin a value to a data node."""
        print("    Run Assgin node")
        from scinode.orm.db_nodetree import DBNodeTree
        from scinode.orm.db_socket import DBSocket

        nodetree_uuid = self.dbdata["metadata"]["nodetree_uuid"]
        nt = DBNodeTree(uuid=nodetree_uuid)
        ctrl_links = nt.record["ctrl_links"]
        for link in ctrl_links:
            if link["from_node"] == self.name and link["from_socket"] == "ctrl":
                # update the value of the output socket
                node_uuid = nt.record["nodes"][link["to_node"]]["uuid"]
                socket = DBSocket(
                    type="output",
                    node_uuid=node_uuid,
                    index=0,
                )
                socket.set_value(self.kwargs["value"])


def run_operator(x, y, operator="+"):
    """Check all python operators, and apply to x and y. Return a tuple of results."""
    if operator == "+":
        results = x + y
    elif operator == "-":
        results = x - y
    elif operator == "*":
        results = x * y
    elif operator == "/":
        results = x / y
    elif operator == "//":
        results = x // y
    elif operator == "%":
        results = x % y
    elif operator == "**":
        results = x**y
    elif operator == "==":
        results = x == y
    elif operator == "!=":
        results = x != y
    elif operator == ">":
        results = x > y
    elif operator == "<":
        results = x < y
    elif operator == ">=":
        results = x >= y
    elif operator == "<=":
        results = x <= y
    elif operator == "and":
        results = x and y
    elif operator == "or":
        results = x or y
    else:
        raise ValueError("Operator not supported: %s" % operator)
    return results


def setattr(source, name, value):
    """set attribute."""
    import builtins

    builtins.setattr(source, name, value)
    return source


def getitem(source, index):
    """Get items from a array."""

    if isinstance(source, dict):
        result = source[index]
    else:
        # list or array
        if type(index) in (int, float):
            index = [index]
        result = [source[i] for i in index]
        if len(result) == 1:
            result = result[0]
    return result


def setitem(source, index, value):
    """Set items value for a array."""
    if type(index) in (int, float):
        index = [index]
    index = [int(i) for i in index]
    if isinstance(source, list):
        for i in index:
            source[i] = value[i]
    else:
        source[index] = value
    return source
