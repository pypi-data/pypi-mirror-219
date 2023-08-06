"""
"""
from scinode.database.client import scinodedb
from scinode.common.log import logging

logger = logging.getLogger("engine")


class MQ:
    """MQ Class.
    Message Queue for SciNode.


    Example:

    >>> # load message
    >>> mq = MQ(name="local")
    >>> mq.read_messages()
    """

    coll_name: str = "mq"

    def __init__(self, name) -> None:
        """_summary_

        Args:
            name (str, optional): name of the message queue.
        """
        self.name = name
        self.init_database()

    def init_database(self):
        """Create a collection in the database if not exist."""
        from scinode.database.db import scinodedb

        data = scinodedb[self.coll_name].find_one({"name": self.name})
        if not data:
            mq = {
                "name": self.name,
                "log": "",
                "msg": [],
                "indices": [0],
            }
            scinodedb[self.coll_name].insert_one(mq)
            print(f"Create a new message queue {self.name} successfully!")

    @property
    def dbdata(self):
        from scinode.database.client import scinodedb

        return scinodedb[self.coll_name].find_one(
            {"name": self.name}, {"_id": 0, "msg": 1, "indices": 1}
        )

    @property
    def index(self):
        "Get the index of the new message"
        from scinode.database.client import scinodedb

        data = scinodedb[self.coll_name].find_one(
            {"name": self.name}, {"_id": 0, "indices": {"$slice": -1}}
        )
        return data["indices"][0]

    def read_messages(self, limit=1e9):
        index = self.index
        msgs = scinodedb[self.coll_name].find_one(
            {"name": self.name}, {"_id": 0, "msg": {"$slice": [index, 1e6]}}
        )["msg"]
        return msgs, index

    def update_index(self, index):
        scinodedb[self.coll_name].update_one(
            {"name": self.name}, {"$push": {"indices": index}}
        )

    def show(self, limit=1e9):
        print("\n")
        print(f"Message qeuue: {self.name}")
        print("-" * 40)
        data = self.dbdata
        n = len(data["indices"])
        index = max(1, n - limit)
        for i in range(index, n):
            print(i - 1, i, "total: ", data["indices"][i] - data["indices"][i - 1])
            for m in data["msg"][data["indices"][i - 1] : data["indices"][i]]:
                uuid, catalog, msg = m.split(",")
                print(uuid, catalog, msg)
        print(
            "\nTo be processed: {}".format(len(data["msg"][data["indices"][n - 1] :]))
        )
        print(data["msg"][data["indices"][n - 1] :])


class Consumer:
    """Message consumer.

    Examples

    >>> # load message
    >>> mq = MQ(name="local")
    >>> consumer = Consumer(queue = mq)
    >>> consumer.consume_messages()
    """

    coll_name = "consumer"

    def __init__(self, name=None, queue=None):
        self.name = name
        self.queue = queue

    def consume_messages(self):
        # Consume the messages from the queue and acknowledge it.
        msgs, index = self.queue.read_messages()
        if len(msgs) == 0:
            return
        for msg in msgs:
            exit_code = self.process(msg)
            if exit_code != 0:
                print(f"Failed to consume message {msg}.")
            index += 1
            self.queue.update_index(index)

    def process(self):
        """Process message."""
        pass

    def apply_consumer_action(self, name, action):
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"apply_consumer_action: {name}, {action}")
        if action == "STOP":
            self.stop_consumer(name)
        elif action == "UPDATE":
            self.update_consumer(name)
        elif action == "REstart":
            self.restart_consumer(name)

    def update_consumer(self, name):
        from scinode.utils.db import update_one
        import datetime

        update_one(
            {"name": name, "lastUpdate": datetime.datetime.utcnow()},
            scinodedb[self.coll_name],
            key="name",
        )

    def stop_consumer(self):
        pass

    def restart_consumer(self):
        pass
