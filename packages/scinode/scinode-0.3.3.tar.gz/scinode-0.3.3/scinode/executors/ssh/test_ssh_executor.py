from scinode.executors.ssh.ssh_executor import SSHExecutor


class RemoteDiff(SSHExecutor):

    _input_file1_name = "file1"
    _input_file2_name = "file2"
    _ouput_file_name = "output"

    _command = f"diff {_input_file1_name} {_input_file2_name} > {_ouput_file_name}"

    _retrieve_files = [_ouput_file_name]

    def create_input_file(self):
        """Create input file for the remote command."""
        self.folder.put_file(self.kwargs["file1"], self._input_file1_name)
        self.folder.put_file(self.kwargs["file2"], self._input_file2_name)

    def read_output_file(self):
        """Read output file from the remote command."""
        with self.folder.open(self._ouput_file_name, "r") as file:
            results = file.read()
        return results


if __name__ == "__main__":
    from scinode.executors.test_ssh_executor import RemoteDiff

    dbdata = {
        "uuid": "diff",
        "name": "test",
        "metadata": {"worker_name": "local", "nodetree_uuid": "abc"},
    }
    scheduler = {
        "type": "direct",
    }
    computer = "localhost"
    pw = RemoteDiff(
        dbdata=dbdata,
        file1="/home/xing/test/scinode/remote_command/file1",
        file2="/home/xing/test/scinode/remote_command/file2",
        scheduler=scheduler,
        computer=computer,
    )
    results = pw.run()
    print("results: ", results)
