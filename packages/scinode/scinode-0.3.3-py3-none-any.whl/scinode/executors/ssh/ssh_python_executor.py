from scinode.executors.ssh.ssh_executor import SSHExecutor


# create a remote python executor class that inherits from SSHExecutor
# and overrides the create_input_file and read_output_file methods

_python_script_function_pickle = """
import pickle
dbdata = pickle.load(open('{0}', 'rb'))
executor = pickle.loads(dbdata['executor']['executor'])
args = pickle.load(open('{1}', 'rb'))
kwargs = pickle.load(open('{2}', 'rb'))
result = executor(*args, **kwargs)
pickle.dump(result, open('{3}', 'wb'))

"""

_python_script_class_pickle = """
import pickle
dbdata = pickle.load(open('{0}', 'rb'))
Executor = pickle.loads(dbdata['executor']['executor'])
args = pickle.load(open('{1}', 'rb'))
kwargs = pickle.load(open('{2}', 'rb'))
executor = Executor(*args, dbdata=dbdata, **kwargs)
result = executor.run()
pickle.dump(result, open('{3}', 'wb'))

"""


_python_script_function = """
import pickle
from {0} import {1} as executor
args = pickle.load(open('{2}', 'rb'))
kwargs = pickle.load(open('{3}', 'rb'))
result = executor(*args, **kwargs)
pickle.dump(result, open('{4}', 'wb'))

"""

_python_script_class = """
import pickle
from {0} import {1} as Executor
dbdata = pickle.load(open('{2}', 'rb'))
args = pickle.load(open('{3}', 'rb'))
kwargs = pickle.load(open('{4}', 'rb'))
executor = Executor(*args, dbdata=dbdata, **kwargs)
result = executor.run()
pickle.dump(result, open('{5}', 'wb'))
"""


class SSHPythonExecutor(SSHExecutor):
    """Python class for executing python function on remote hosts via SSH."""

    _python_script_name = "python_script.py"
    _input_args = "args.pkl"
    _input_kwargs = "kwargs.pkl"
    _input_dbdata = "dbdata.pkl"
    _outputs = "outputs.pkl"

    _command = f'python3 "{_python_script_name}"'

    _retrieve_files = [_outputs]

    def create_input_file(self):
        """Create input file for the command to be executed"""
        from scinode.utils.node import (
            get_input_parameters_from_db,
            inspect_executor_arguments,
        )
        import pickle

        dbdata = self.dbdata
        parameters = get_input_parameters_from_db(dbdata)
        # "sn_ctx" is a special key for scinode
        kwargs = [k for k in dbdata["metadata"]["kwargs"] if k != "sn_ctx"]
        args, kwargs, _hash_parameters = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], kwargs
        )
        print("args: ", args)
        print("kwargs: ", kwargs)
        # Serialize the input data to a file
        with self.folder.open(self._input_args, "wb") as file:
            pickle.dump(args, file)
        with self.folder.open(self._input_kwargs, "wb") as file:
            pickle.dump(kwargs, file)
        with self.folder.open(self._input_dbdata, "wb") as file:
            pickle.dump(dbdata, file)
        # executor
        is_pickle = self.dbdata["executor"].get("is_pickle", False)
        executor_type = self.dbdata["executor"].get("type", "function")
        if is_pickle:
            if executor_type == "function":
                python_script = _python_script_function_pickle.format(
                    self._input_dbdata,
                    self._input_args,
                    self._input_kwargs,
                    self._outputs,
                )
            else:
                python_script = _python_script_class_pickle.format(
                    self._input_dbdata,
                    self._input_args,
                    self._input_kwargs,
                    self._outputs,
                )
        else:
            if executor_type == "function":
                python_script = _python_script_function.format(
                    self.dbdata["executor"]["path"],
                    self.dbdata["executor"]["name"],
                    self._input_args,
                    self._input_kwargs,
                    self._outputs,
                )
            else:
                python_script = _python_script_class.format(
                    self.dbdata["executor"]["path"],
                    self.dbdata["executor"]["name"],
                    self._input_dbdata,
                    self._input_args,
                    self._input_kwargs,
                    self._outputs,
                )
        with self.folder.open(self._python_script_name, "w") as file:
            file.write(python_script)
        self.scheduler.setdefault("type", "direct")
        print("scheduler: ", self.scheduler)

    def read_output_file(self):
        """Read output file and return the results"""
        import pickle

        with self.folder.open(self._outputs, "rb") as file:
            results = pickle.load(file)
            print("results: ", results)
        return results


if __name__ == "__main__":
    from scinode.executors.ssh.ssh_python_executor import SSHPythonExecutor
    from scinode.orm.db_node import DBNode

    node = DBNode(uuid="a51d906c-209e-11ee-9c71-598e01a81bbd")
    scheduler = {
        "computer": "localhost",
        "type": "direct",
    }
    executor = SSHPythonExecutor(dbdata=node.dbdata, scheduler=scheduler)
    executor.run()
