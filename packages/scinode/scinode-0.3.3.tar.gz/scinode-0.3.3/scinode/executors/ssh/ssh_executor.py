from scinode.core.executor import Executor
from scinode.executors.ssh.ssh_client import SSHClient
from scinode.executors.folder_manager import FolderManager
import os

_submission_file = "submission.sh"


class SSHExecutor(Executor):
    """Python class for executing commands on remote hosts via SSH."""

    def __init__(self, dbdata={}, **kwargs):
        super().__init__(dbdata=dbdata, **kwargs)
        # workdir either set by user or use the uuid of the node
        self.scheduler = dbdata.get("scheduler", {"type": "direct"})
        self.scheduler["job_name"] = dbdata["name"]
        self.computer = self.scheduler.pop("computer", "localhost")
        workdir = kwargs["workdir"] if kwargs.get("workdir", None) else dbdata["uuid"]
        self.ssh_client = SSHClient(self.computer, workdir)
        local_workdir = os.path.join(self.worker_workdir, workdir)
        self.folder = FolderManager(local_workdir)

    def run(self):
        self.create_input_file()
        self.create_submit_script()
        self.upload_folder()
        job_id = self.execute_command()
        self.check_job_state_periodically(job_id)
        self.retrieve_output_file()
        return self.read_output_file()

    def create_input_file(self):
        """Create input file for the command to be executed"""
        pass

    def create_submit_script(self):
        from scinode.executors.hpc_scheduler import SubmissionScriptGenerator

        command = (
            self.scheduler.get("command")
            if self.scheduler.get("command")
            else self._command
        )
        generator = SubmissionScriptGenerator(**self.scheduler)
        generator.add_line(self.scheduler.get("pre_command", ""))
        generator.add_line(command)
        generator.add_line(self.scheduler.get("post_command", ""))
        script_content = generator.generate_script()
        with self.folder.open(f"{_submission_file}", "w") as file:
            file.write(script_content)

    def upload_folder(self):
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        print(f"Uploading folder to remote host: {self.computer}")
        msgs = f"{self.dbdata['metadata']['nodetree_uuid']},node,{self.name}:state:UPLOADING"
        send_message_to_queue(broker_queue_name, msgs)
        self.ssh_client.connect()
        self.ssh_client.copy(self.folder.workdir, self.ssh_client.workdir)
        self.ssh_client.disconnect()

    def execute_command(self):
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name
        from scinode.utils.node import write_log

        print(f"Executing command on remote host: {self.computer}")
        self.ssh_client.connect()
        if self.scheduler.get("type", "direct") == "slurm":
            command = f"cd {self.ssh_client.workdir} && sbatch {_submission_file}"
            output = self.ssh_client.execute_command(command)
            print("sbatch output: ", output)
            job_id = output.split()[-1]
        elif self.scheduler.get("type", "direct") == "pbs":
            command = f"cd {self.ssh_client.workdir} && qsub {_submission_file}"
            output = self.ssh_client.execute_command(command)
            job_id = output.split()[-1]
        elif self.scheduler.get("type", "direct") == "sge":
            command = f"cd {self.ssh_client.workdir} && qsub {_submission_file}"
            output = self.ssh_client.execute_command(command)
            job_id = output.split()[-1]
        else:
            command = f"cd {self.ssh_client.workdir} && nohup bash {_submission_file} 2>&1 & echo $!"
            output = self.ssh_client.execute_command(command)
            print("nohup output: ", output)
            job_id = output[0]
        self.ssh_client.disconnect()
        msgs = f"{self.dbdata['metadata']['nodetree_uuid']},node,{self.name}:state:SUBMITTED"
        send_message_to_queue(broker_queue_name, msgs)
        write_log(self.dbdata["uuid"], f"Jobid: {job_id}")
        return job_id

    def check_job_state_periodically(self, job_id):
        import time
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        msgs = f"{self.dbdata['metadata']['nodetree_uuid']},node,{self.name}:state:REMOTE_RUNNING"
        send_message_to_queue(broker_queue_name, msgs)
        self.ssh_client.connect()
        while True:
            scheduler = self.scheduler.get("type", "direct")
            job_state = self.ssh_client.check_job_state(job_id, scheduler=scheduler)
            print(f"Job {job_id} state: {job_state}")
            if scheduler == "slurm" and job_state in ["COMPLETED", "FAILED", "TIMEOUT"]:
                break
            elif scheduler == "direct" and job_state != "S":
                break
            time.sleep(5)  # Wait for 5 seconds before checking again
        self.ssh_client.disconnect()

    def retrieve_output_file(self):
        self.ssh_client.connect()
        for filepath in self._retrieve_files:
            self.ssh_client.get(filepath, os.path.join(self.folder.workdir, filepath))
        self.ssh_client.disconnect()

    def read_output_file(self):
        pass
