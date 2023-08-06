class Executor:
    """Base-class for all executors.

    Prepare and run the code.
    """

    def __init__(self, dbdata={}, **kwargs) -> None:
        """init a instance of executor.

        Args:
            dbdata (dict, optional): data of the node. Defaults to {}.
            worker_name (str, optional): name of the worker. Defaults to "local".
        """
        self.kwargs = kwargs
        self.dbdata = dbdata
        self.worker_name = dbdata["metadata"]["worker_name"]
        self.uuid = dbdata["uuid"]
        self.nodetree_uuid = dbdata["metadata"]["nodetree_uuid"]
        self.name = dbdata["name"]
        self.load_data()

    def get_worker_config(self):
        """Get worker data by the worker name

        Returns:
            dict: worker configuration
        """
        from scinode.daemon.worker_config import WorkerConfig

        dc = WorkerConfig(name=self.worker_name)
        return dc.data

    @property
    def worker_workdir(self):
        data = self.get_worker_config()
        return data["workdir"]

    def before_run(self):
        """Prepare data before run."""
        pass

    def after_run(self):
        """Handler data after run."""
        pass

    def load_data(self):
        pass

    def run(self):
        """Run the job."""
        pass

    def cancel(self):
        """callback for cancellation."""
        pass

    def update_counter(self):
        """Update the counter of the node.

        Args:
            counter (int): counter of the node.
        """
        from scinode.database.client import scinodedb

        scinodedb["nodetree"].update_many(
            {"uuid": self.nodetree_uuid},
            {"$inc": {f"nodes.{self.name}.counter": 1}},
        )
