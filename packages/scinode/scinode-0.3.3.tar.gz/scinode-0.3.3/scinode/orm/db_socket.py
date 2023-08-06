from scinode.common.log import logging

logger = logging.getLogger("orm")


class DBSocket:
    """DBSocket Class.
    Object Relational Mapping for Socket.

    node_uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:

    >>> # load socket from data
    >>> socket = DBSocket(uuid=uuid)
    """

    db_name: str = "node"

    def __init__(
        self, type="input", node_uuid=None, name=None, index=None, dbdata=None
    ) -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the socket.
                Defaults to None.
            dbdata (dict, optional): data of the socket from database.
                Defaults to None.
        """
        self.type = f"{type}s"
        if dbdata:
            node_uuid = dbdata["node_uuid"]
            name = dbdata["name"]
        self.node_uuid = node_uuid
        self.name = name if name is not None else None
        self.index = index if index is not None else None
        if self.name is None and self.index is None:
            raise ValueError("Either name or index should be provided.")
        self.record = self.dbdata

    @property
    def dbdata(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.database.client import scinodedb

        query = {"uuid": self.node_uuid}
        proj = {self.type: 1, "_id": 0}
        dbdatas = scinodedb["node"].find_one(query, proj)[self.type]
        print(self.name, self.index)
        if self.name is not None:
            sdata = [data for data in dbdatas if data["name"] == self.name][0]
        elif self.index is not None:
            sdata = dbdatas[self.index]
        return sdata

    @property
    def uuid(self):
        return self.dbdata["uuid"]

    @property
    def links(self):
        return self.get_links()

    def get_links(self):
        record = self.dbdata
        return record["links"]

    @property
    def value(self):
        return self.get_value()

    def get_value(self):
        """Get value of the socket.
        Input: input value.
        Output: result."""
        if self.type == "inputs":
            from scinode.utils.node import get_input_socket_value

            value = get_input_socket_value(self.dbdata)
        else:
            from scinode.utils.node import get_socket_data

            value = get_socket_data({"uuid": self.uuid})
        return value["value"]

    @value.setter
    def value(self, value):
        self.set_value(value)

    def set_value(self, value):
        from scinode.utils.node import save_socket_data

        dbdata = self.dbdata
        dbdata["value"] = value
        save_socket_data(dbdata)

    def __repr__(self) -> str:
        s = ""
        s += 'NodeSocekt(name="{}")'.format(self.name)
        return s
