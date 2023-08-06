from scinode.config.base_config import BaseConfig
from pathlib import Path

default_computer = {
    "name": "localhost",
    "hostnmae": "localhost",
    "workdir": str(Path.home() / "/scinode"),
}


class ComputerConfig(BaseConfig):

    name = "computer"

    def test(self, name):
        from scinode.executors.ssh_client import SSHClient

        client = SSHClient(name, "~/")
        try:
            client.connect()
            client.disconnect()
            return True
        except Exception as e:
            return False


if __name__ == "__main__":
    p = ComputerConfig()
    p.list_items()
