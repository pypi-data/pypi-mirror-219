import os
import shutil


class FolderManager:
    def __init__(self, workdir):
        self.workdir = workdir
        if not os.path.exists(self.workdir):
            self.create_folder(self.workdir)

    def get_sub_folder(self, relative_path, create=True):
        absolute_path = os.path.join(self.workdir, relative_path)
        if create and not os.path.exists(absolute_path):
            self.create_folder(absolute_path)
        return FolderManager(absolute_path)

    def list_files(self, path):
        return os.listdir(path)

    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def delete_folder(self, path):
        os.rmdir(path)

    def get_file(self, remote_path, local_path):
        shutil.copyfile(remote_path, local_path)

    def put_file(self, local_path, filename):
        shutil.copyfile(local_path, os.path.join(self.workdir, filename))

    def copy_file(self, source_path, destination_path):
        shutil.copyfile(source_path, destination_path)

    def remove_file(self, path):
        os.remove(path)

    def execute_command(self, command):
        return os.system(command)

    def submit_slurm_job(self, job_script):
        return self.execute_command(f"sbatch {job_script}")

    def open(self, file_path, mode="r", **kwargs):
        return open(os.path.join(self.workdir, file_path), mode, **kwargs)
