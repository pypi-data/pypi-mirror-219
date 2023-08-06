"""
"""
from scinode.engine.nodetree_engine import EngineNodeTree
from scinode.database.client import scinodedb
from scinode.engine.mq import Consumer
import traceback
from scinode.common.log import logging

logger = logging.getLogger("engine")


class EngineScheduler(Consumer):
    """Engine Scheduler Class.

    Example:

    >>> en = EngineScheduler(queue=mq)
    >>> en.consume_messages()
    """

    coll_name = "scheduler"

    def process(self, msg):
        """process message"""
        print(f"process: {msg}")
        try:
            uuid, catalog, body = msg.split(",")
        except Exception as e:
            print(e)
            return 1
        if catalog == "nodetree":
            try:
                ent = EngineNodeTree(uuid=uuid)
                ent.apply_nodetree_message(body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {"error": str(error)}}
                )
                return 1
        elif catalog == "node":
            try:
                ent = EngineNodeTree(uuid=uuid)
                ent.apply_node_message(body)
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
                return 1
        elif catalog == "ctrl_link":
            try:
                ent = EngineNodeTree(uuid=uuid)
                ent.apply_ctrl_link_message(body)
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
                return 1
        elif catalog == "scheduler":
            try:
                self.apply_consumer_action(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(
                        str(error)
                    )
                )
                return 1
        else:
            raise Exception(f"Unknown type {catalog}")
            return 1

        return 0

    def stop_consumer(self, name):
        from scinode.daemon.scheduler import DaemonScheduler

        print(f"Sotp scheduler {name}...")
        # because the we can not update the index after stopping the daemon,
        # we update the queue index before that
        self.queue.update_index(self.queue.index + 1)
        worker = DaemonScheduler(name)
        worker.stop()

    def restart_consumer(self, name):
        import os

        print(f"Restart scheduler {name}...")
        scinodedb[self.coll_name].update_one(
            {"name": name}, {"$set": {"msg": [], "indices": [0]}}
        )
        os.system("scinode scheduler hard-restart")
