from scinode.config.base_config import BaseConfig
from pathlib import Path
from termcolor import colored

default_profile = {
    "name": "default",
    "computer": "localhost",
    "db_address": "mongodb://localhost:27017/",
    "db_name": "scinode_db",
    "fild_db": "gridfs",
    "config_path": str(Path.home() / ".scinode"),
    "engine": "Concurrent",
    "broker_url": "amqp://localhost//",
}


class ProfileConfig(BaseConfig):

    name = "profile"

    def __init__(self):
        super().__init__()
        if len(self.config) == 0:
            default_profile["current"] = True
            self.add_item(default_profile)

    def get_current_profile(self):
        for _profile_name, profile in self.config.items():
            if profile.get("current", False):
                profile["name"] = _profile_name
                return profile
        return None  # Return None or handle the case where no current profile is found

    def set_current_profile(self, name):
        if name not in self.config:
            raise ValueError(f"Profile '{name}' does not exist.")

        # Update the current field for each profile
        for profile_name in self.config:
            self.config[profile_name]["current"] = False

        # Set the specified profile as the current profile
        self.config[name]["current"] = True
        self.save_config()

        print(f"Current profile set to: {name}")

    def list_items(self):
        # print(f"Items in {self.__class__.__name__}:")
        for name, value in self.config.items():
            if value.get("current", False):
                print(colored(name, "green"))
            else:
                print(name)


def get_current_profile():
    p = ProfileConfig()
    return p.get_current_profile()


profile_datas = get_current_profile()

if __name__ == "__main__":
    p = ProfileConfig()
    p.list_items()
