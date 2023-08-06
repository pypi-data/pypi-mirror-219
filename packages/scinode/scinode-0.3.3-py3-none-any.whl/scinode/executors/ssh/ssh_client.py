import paramiko
import os


class SSHClient:
    def __init__(self, computer, workdir):
        self.computer = computer
        self.load_config()
        self.workdir = os.path.join(self.computer_workdir, workdir)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def load_config(self):
        """load computer config, read the config file and set the host, username, password"""
        from scinode.config.computer import ComputerConfig

        c = ComputerConfig()
        config = c.get_item(self.computer)
        self.computer_workdir = config.get("workdir", None)
        self.hostname = config.get("hostname", "localhost")
        self.port = config.get("port", 22)
        self.username = config.get("username", None)
        self.password = config.get("password", None)
        self.key_filename = config.get("key_filename", None)

    def connect(self):
        try:
            if self.key_filename:
                self.client.connect(
                    self.hostname,
                    self.port,
                    self.username,
                    key_filename=self.key_filename,
                )
            else:
                self.client.connect(
                    self.hostname,
                    self.port,
                    self.username,
                    password=self.password,
                )
        except paramiko.AuthenticationException as e:
            raise Exception(f"Authentication failed: {str(e)}")
        except paramiko.SSHException as e:
            raise Exception(f"Unable to establish SSH connection: {str(e)}")
        except Exception as e:
            raise Exception(f"Error occurred while connecting: {str(e)}")

    def disconnect(self):
        self.client.close()

    def get(self, remote_path, local_path):
        try:
            remote_path = os.path.join(self.workdir, remote_path)
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
        except FileNotFoundError:
            print(f"Remote file '{remote_path}' does not exist.")
        except Exception as e:
            print(f"Error occurred while downloading file: {e}")

    def put(self, local_path, remote_path):
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file '{local_path}' does not exist.")
        try:
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
        except IOError as e:
            raise Exception(f"Error occurred while uploading file: {str(e)}")

    def copy(self, local_path, remote_path):
        sftp = self.client.open_sftp()
        if os.path.isfile(local_path):
            sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            self._copy_folder(sftp, local_path, remote_path)
        else:
            raise ValueError(f"Local path '{local_path}' does not exist.")
        sftp.close()

    def _copy_folder(self, sftp, local_folder_path, remote_folder_path):
        def create_remote_directory(path):
            try:
                sftp.stat(path)
            except IOError as e:
                if e.errno == 2:  # Directory does not exist
                    sftp.mkdir(path)
                else:
                    raise

        create_remote_directory(remote_folder_path)
        for root, dirs, files in os.walk(local_folder_path):
            for dir in dirs:
                remote_dir_path = os.path.join(
                    remote_folder_path,
                    os.path.relpath(os.path.join(root, dir), local_folder_path),
                )
                create_remote_directory(remote_dir_path)
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(
                    remote_folder_path,
                    os.path.relpath(local_file_path, local_folder_path),
                )
                sftp.put(local_file_path, remote_file_path)

    def remove_file(self, path):
        try:
            sftp = self.client.open_sftp()
            sftp.remove(path)
            sftp.close()
        except IOError as e:
            raise Exception(f"Error occurred while removing file: {str(e)}")

    def remove_folder(self, path):
        try:
            command = f"rm -rf {path}"
            self.execute_command(command)
        except Exception as e:
            raise Exception(f"Error occurred while removing folder: {str(e)}")

    def make_directory(self, path):
        sftp = self.client.open_sftp()
        try:
            sftp.mkdir(path)
        except IOError as e:
            if e.errno != 17:  # Ignore "Directory already exists" error
                raise
        sftp.close()

    def set_working_directory(self, directory=None):
        if directory is None:
            directory = self.workdir
        else:
            directory = os.path.join(self.workdir, directory)
        stdin, stdout, stderr = self.client.exec_command(f"cd {directory}; ls")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            raise Exception(
                f"Failed to set working directory: {stderr.read().decode()}"
            )

    def execute_command(self, command):
        try:
            # print(f"Executing command: {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            print("stderr: ", stderr.read().decode().strip())
            return stdout.read().decode().strip()
        except paramiko.SSHException as e:
            raise Exception(f"Error occurred while executing command: {str(e)}")

    def submit_slurm_job(self, script_path):
        try:
            command = f"sbatch {script_path}"
            output = self.execute_command(command)
            job_id = output.split()[-1]  # Extracting the job ID from the output
            return job_id
        except Exception as e:
            raise Exception(f"Error occurred while submitting SLURM job: {str(e)}")

    def check_job_state(self, job_id, scheduler="slurm"):
        if scheduler == "slurm":
            output = self.execute_command(f"scontrol show job {job_id} | grep JobState")
            try:
                job_state = output.split("=")[1].strip().split(" ")[0]
                return job_state
            except IndexError:
                return "FAILED"
        elif scheduler == "direct":
            result = self.execute_command(f"ps -p {job_id} -o state=")
        return result
