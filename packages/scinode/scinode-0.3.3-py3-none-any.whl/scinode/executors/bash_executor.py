from scinode.core.executor import Executor


class BashExecutor(Executor):
    def __init__(self, dbdata=..., **kwargs) -> None:
        super().__init__(dbdata, **kwargs)

    def run(self):
        import subprocess

        command = self.kwargs["command"]
        if self.kwargs["cwd"]:
            self.cwd = self.kwargs["cwd"]
        else:
            self.cwd = self.worker_workdir
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
            shell=True,
        )
        output, error = process.communicate()
        exit_code = process.returncode

        if exit_code != 0:
            raise Exception(
                f"Command '{command}' failed with exit code {exit_code}:\n{error.decode()}"
            )

        return output.decode()


if __name__ == "__main__":
    dbdata = {
        "name": "abc",
        "uuid": "abc",
        "metadata": {"worker_name": "local", "nodetree_uuid": "xyz"},
    }
    ex = BashExecutor(dbdata=dbdata, command=["echo hello world"], cwd="")
    output = ex.run()
    print(output)
