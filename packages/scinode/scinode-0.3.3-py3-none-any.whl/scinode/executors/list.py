"""
https://docs.python.org/3/tutorial/datastructures.html

"""
from scinode.core.executor import Executor


class List(Executor):
    """ """

    def run(self):
        """Return the empty list."""
        if self.kwargs["Input"] is not None:
            results = (list(self.kwargs["Input"]),)
        else:
            results = ([],)
        return results


class Append(Executor):
    """ """

    def run(self):
        """ """
        """To append an new element to
        a given Python List."""
        print("    Run For node")
        from scinode.orm.db_node import DBNode

        node = DBNode(self.uuid)
        from scinode.database.db import scinodedb

        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": self.nodetree_uuid}, {f"nodes.{self.name}.counter": 1}
        )
        if ntdata["nodes"][self.name]["counter"] == 0:
            source = self.kwargs["List"]
        else:
            # get the result from the append node
            source = node.results[0]["value"]
        source.append(self.kwargs["Value"])
        results = (source,)
        self.update_counter()
        return results


class Extend(Executor):
    """ """

    def run(self):
        """ """
        """To extend an new element to
        a given Python List."""
        print("    Run For node")
        from scinode.orm.db_node import DBNode

        node = DBNode(self.uuid)
        from scinode.database.db import scinodedb

        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": self.nodetree_uuid}, {f"nodes.{self.name}.counter": 1}
        )
        if ntdata["nodes"][self.name]["counter"] == 0:
            source = self.kwargs["List"]
        else:
            # get the result from the extend node
            source = node.results[0]["value"]
        source.extend(self.kwargs["Value"])
        results = (source,)
        self.update_counter()
        return results


class Remove(Executor):
    """ """

    def run(self):
        """To remove of the first occurrence of an element in a list."""
        source = self.kwargs["List"]
        source.remove(self.kwargs["Value"])
        results = (source,)
        return results


class Index(Executor):
    """ """

    def run(self):
        """To find index of the all occurrence of an element in a list."""

        results = (self.kwargs["List"].index(self.kwargs["Value"]),)
        return results


class Count(Executor):
    """ """

    def run(self):
        """Return the number of times x appears in the list."""

        results = (self.kwargs["List"].count(self.kwargs["Value"]),)
        return results


class Pop(Executor):
    """ """

    def run(self):
        """Return the number of times x appears in the list."""

        results = (self.kwargs["List"].pop(self.kwargs["Index"]),)
        return results


class Reverse(Executor):
    """ """

    def run(self):
        """To reverse a list."""
        source = self.kwargs["List"]
        source.reverse()
        results = (source,)
        return results


class Insert(Executor):
    """ """

    def run(self):
        """To find index of the all occurrence of an element in a list."""
        source = self.kwargs["List"]
        source.insert(self.kwargs["Index"], self.kwargs["Value"])
        results = (source,)
        return results
