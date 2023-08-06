"""
"""
from scinode.engine.node_engine import EngineNode
from scinode.database.client import scinodedb
from scinode.engine.mq import Consumer
import traceback
import time
from scinode.common.log import logging

logger = logging.getLogger("engine")


class EngineWorker(Consumer):
    """EngineWorker Class.

    Example:

    >>> en = EngineWorker()
    >>> en.process()
    """

    coll_name = "worker"

    def __init__(self, name=None, queue=None, pool=None, futures=None) -> None:
        """_summary_

        Args:
            name (_type_, optional): _description_. Defaults to None.
            pool (_type_, optional): _description_. Defaults to None.
        """
        self.name = name
        self.pool = pool
        self.futures = futures
        super().__init__(name, queue)

    def process(self, msg):
        """Ppply message node and worker."""
        print(f"process: {msg}")
        try:
            uuid, catalog, body = msg.split(",")
        except Exception as e:
            print(e)
            return 1
        if catalog == "node":
            try:
                self.apply_node_message(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                data = msg.split(":")
                name = data[0]
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "FAILED"}}
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.error": str(error)}}
                )
        elif catalog == "worker":
            try:
                self.apply_consumer_action(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(
                        str(error)
                    )
                )
        else:
            raise Exception(f"Unknown type {catalog}")

        return 0

    def apply_node_message(self, uuid, msg):
        """apply action to all nodes"""
        from scinode.database.client import scinodedb
        from scinode.utils.db import write_log

        # print(f"apply_node_message: {msg}")
        data = msg.split(":")
        if len(data) == 3:
            name, key, value = data
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.{key}": value}}
            )
            if key == "action":
                self.apply_node_action(uuid, name, value)
        write_log({"metadata.nodetree_uuid": uuid, "name": name}, f"\n{msg}\n", "node")
        # logger.debug("apply_node_message, time: {}".format(time.time() - tstart))

    def apply_node_action(self, uuid, name, action):
        tstart = time.time()
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"apply_node_action: {name}, {action}")
        if action == "NONE":
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.action": "NONE"}}
            )
        elif action == "LAUNCH":
            self.launch_node(uuid, name)
        elif action == "EXPOSE_OUTPUTS":
            self.expose_outputs(uuid, name)
        else:
            print("Unknown action: ", action)
        # print("apply_node_action: ", self.record["nodes"])
        # logger.debug("apply_node_action, time: {}".format(time.time() - tstart))

    def launch_node(self, uuid, name):
        """Launch node"""
        print(f"\nLaunch node: {name}, {uuid}")
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        node = EngineNode(uuid=ntdata["nodes"][name]["uuid"], worker_name=self.name)
        future = node.process(self.pool, self.futures.get(uuid), action="LAUNCH")
        self.futures[uuid] = future

    def expose_outputs(self, uuid, name):
        """Expose node group outputs."""
        print(f"\n Expose node group: {name}")
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        node = EngineNode(uuid=ntdata["nodes"][name]["uuid"], worker_name=self.name)
        future = node.process(
            self.pool, self.futures.get(uuid), action="EXPOSE_OUTPUTS"
        )
        self.futures[uuid] = future

    def cancel_node(self, uuid, name):
        """Cancel node"""
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        uuid = ntdata["nodes"][name]["uuid"]
        future = self.futures.get(uuid)
        if future is not None:
            log = "Node is running: {}.\n".format(future.running())
            was_calcelled = future.cancel()
            if was_calcelled:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
                )
                log += "Node is cancelled: {}".format(was_calcelled)
                # self.update_db_keys({"outputs": {}})
            else:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                log += "Can not cancel node.".format()
        else:
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            log = "Future is None. Node {} is not running. Can not cancel.".format(
                self.dbdata["name"]
            )

    def stop_consumer(self, name):
        from scinode.daemon.worker import DaemonWorker

        print(f"Sotp worker {name}...")
        self.queue.update_index(self.queue.index + 1)
        worker = DaemonWorker(name)
        worker.stop()

    def restart_consumer(self, name):
        import os

        print(f"Restart worker {name}...")
        scinodedb["mq"].update_one(
            {"name": name}, {"$set": {"msg": [], "indices": [0]}}
        )
        os.system("scinode worker hard-restart")
