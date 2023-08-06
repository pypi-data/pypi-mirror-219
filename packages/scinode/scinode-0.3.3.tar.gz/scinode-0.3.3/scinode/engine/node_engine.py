from scinode.orm import DBItem
import traceback
from scinode.common.log import logging

logger = logging.getLogger("engine")


class EngineNode(DBItem):
    """EngineNode Class.
    Process the node with the data from the database.
    It can be called by the worker or called manually.

    uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:
    >>> # load node data from database
    >>> query = {"uuid": "your-node-uuid"}
    >>> dbdata = scinodedb["node"].find_one(query)
    >>> node = EngineNode(uuid=dbdata["uuid"])  # , self.worker_name)
    >>> future = node.process(pool, future)

    """

    db_name: str = "node"

    def __init__(self, uuid=None, dbdata=None, worker_name="local") -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the node.
                Defaults to None.
            dbdata (dict, optional): data of the node from database.
                Defaults to None.
        """
        # print("Init Node Engine...")
        if dbdata:
            uuid = dbdata["uuid"]
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]
        self.worker_name = worker_name
        self.inner_id = self.record["inner_id"]
        self.nodetree_uuid = self.record["metadata"]["nodetree_uuid"]
        self.scattered_from = self.record["metadata"]["scattered_from"]
        self.scattered_label = self.record["metadata"]["scattered_label"]

    def process(self, pool, future=None, action=None):
        """process data based on the action flag.

        Args:
            pool (ThreadPoolExecutor): Pool used to submit job
            future (concurrent.futures.Future, optional): Defaults to None.

        Returns:
            oncurrent.futures.Future: _description_
        """
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        print(f"Node Engine, process: {self.name}")
        try:
            future = self.apply_action(pool, future, action=action)
        except Exception:
            import traceback

            error = traceback.format_exc()
            log = "xxxxxxxxxx Failed xxxxxxxxxx\nNode {} failed due to: {}".format(
                self.name, error
            )
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)

        return future

    def apply_action(self, pool, future=None, action=None):
        """Apply node action

        Args:
            pool (dict): _description_
            future (future, optional): _description_. Defaults to None.
            action (_type_, optional): _description_. Defaults to None.

        Returns:
            future: _description_
        """
        if not action:
            action = self.record["action"]
        log = "\nWorker: {}\n".format(self.worker_name)
        log += "\nAction: {}\n".format(action)
        self.write_log(log)
        if action is None or action.upper() == "NONE":
            return
        elif action.upper() == "LAUNCH":
            future = self.launch(pool)
        elif action.upper() == "EXPOSE_OUTPUTS":
            self.expose_outputs()
            return None
        elif action.upper() == "CANCEL":
            self.cancel(future)
            return None
        else:
            log = "\nAction {} is not supported.".format(self.action)
            self.write_log(log)
        return future

    def launch(self, pool=None):
        """Launch node"""
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name
        from scinode.database.client import scinodedb
        from scinode.utils import get_ctx
        from scinode.utils.node import (
            get_input_parameters_from_db,
            inspect_executor_arguments,
            get_executor,
            calc_node_hash,
            reuse_results_by_caching,
            has_keyword_arg,
        )
        from scinode.executors.ssh.ssh_python_executor import SSHPythonExecutor
        from scinode.executors.ssh.ssh_executor import SSHExecutor
        import inspect

        # code here
        dbdata = self.record
        parameters = get_input_parameters_from_db(dbdata)
        # print("parameters: ", parameters)
        # "sn_ctx" is a special key for scinode
        kwargs = [k for k in dbdata["metadata"]["kwargs"] if k != "sn_ctx"]
        args, kwargs, hash_parameters = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], kwargs
        )
        node_hash = calc_node_hash(dbdata, hash_parameters)
        if dbdata["metadata"].get("use_cache", False):
            # match hash
            cache_node = scinodedb["node"].find_one(
                {"hash": node_hash}, {"_id": 0, "name": 1, "uuid": 1, "outputs": 1}
            )
            if cache_node is not None:
                # msgs = f"{nodetree_uuid},node,{node_name}:action:CACHING"
                # send_message_to_queue(broker_queue_name, msgs)
                exit_code = reuse_results_by_caching(dbdata, cache_node)
                if exit_code == 0:
                    return
        newvalues = {"$set": {"hash": node_hash}}
        scinodedb["node"].update_one({"uuid": self.uuid}, newvalues)
        # print("  Parameters: ", parameters)
        log = "args: {}\n".format(args)
        log += "kwargs: {}\n".format(kwargs)
        #
        Executor, executor_type = get_executor(self.dbdata["executor"])
        log += "Executor: {}\n".format(Executor)
        self.write_log(log)
        # print("  Executor: ", Executor)
        if (
            dbdata["scheduler"].get("computer", "") == ""
            or inspect.isclass(Executor)
            and issubclass(Executor, SSHExecutor)
        ):
            if inspect.isclass(Executor) and hasattr(Executor, "run"):
                # For user defined node, we can add worker name to kwargs
                if has_keyword_arg(Executor, "dbdata") and "dbdata" not in kwargs:
                    kwargs["dbdata"] = dbdata
                executor = Executor(*args, **kwargs)
                future = pool.submit(executor.run)
            else:
                if "sn_ctx" in dbdata["metadata"]["kwargs"]:
                    # get context from db
                    sn_ctx = get_ctx(self.dbdata)
                    kwargs["sn_ctx"] = sn_ctx
                future = pool.submit(Executor, *args, **kwargs)
        else:
            self.write_log(
                "Node to be submitted to remote computer {}.\n".format(
                    dbdata["scheduler"].get("computer")
                )
            )

            executor = SSHPythonExecutor(
                dbdata=self.dbdata,
            )
            future = pool.submit(executor.run)
        msgs = f"{self.nodetree_uuid},node,{self.name}:state:RUNNING"
        send_message_to_queue(broker_queue_name, msgs)
        log = "\nNode is launched.\n"
        print("\nNode {} is launched.\n".format(dbdata["name"]))
        self.write_log(log)
        future.add_done_callback(self.check_future_done)

        return future

    def expose_outputs(self):
        """expose node group result from child nodes"""
        from scinode.utils.node import expose_outputs

        expose_outputs(self.dbdata)

    @property
    def input_node_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        from scinode.utils.node import get_input_node_data
        from scinode.database.client import db_node

        nodes = get_input_node_data(self.record, db_node)
        # print("Total: {} parent nodes.".format(len(nodes)))
        return nodes

    def check_future_done(self, future):
        """Check if node finished

        Args:
            future (_type_): _description_

        Raises:
            Exception: _description_
        """
        from scinode.utils.node import save_node_results
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        log = "\n  Check result for Node: {}, {}.".format(self.inner_id, self.name)
        if future.exception() is not None:
            error = future.exception()
            log += "\nxxxxxxxxxx Failed xxxxxxxxxx\nFuture with exception: {}".format(
                error
            )
            # self.state = "FAILED"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)
            return
        elif future.cancelled():
            log == "\n  Job was cancelled"
            # self.state = "CANCELLED"
            # self.action = "NONE"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            self.update_db_keys({"error": "Job was cancelled"})
            self.write_log(log)
            return
        else:
            # result of node group need to be exposed
            if self.record["metadata"]["node_type"] == "GROUP":
                msgs = f"{self.nodetree_uuid},node,{self.name}:state:RUNNING"
                send_message_to_queue(broker_queue_name, msgs)
                return
            # job is done, try to get result
            try:
                future_results = future.result()
                save_node_results(self.dbdata, future_results)
                msgs = f"{self.nodetree_uuid},node,{self.name}:state:FINISHED"
                send_message_to_queue(broker_queue_name, msgs)
            except Exception:
                error = traceback.format_exc()
                log += "\nxxxxxxxxxx Failed xxxxxxxxxx\nFetch results from future failed, due to: {}".format(
                    error
                )
                # self.state = "FAILED"
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                self.update_db_keys({"error": str(error)})
                self.write_log(log)
                return

    @property
    def dbdata(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.utils.node import get_node_data

        query = {"uuid": self.uuid}
        dbdata = get_node_data(query)
        return dbdata

    def __repr__(self) -> str:
        s = ""
        s += 'EngineNode(name="{}", uuid="{}", nodetree_uuid = {},\
state={}, action={})'.format(
            self.name,
            self.uuid,
            self.nodetree_uuid,
            self.state,
            self.action,
        )
        return s

    def write_log(self, log, worker=False, database=True):
        from scinode.utils.db import write_log

        if worker:
            print(log)
        if database:
            write_log({"uuid": self.uuid}, log, "node")
