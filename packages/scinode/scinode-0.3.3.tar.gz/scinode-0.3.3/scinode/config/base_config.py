import json
import os
from termcolor import colored


class BaseConfig:

    name = "scinode"

    def __init__(self, config_file=None):
        if os.environ.get("SCINODE_PATH"):
            scinode_path = os.environ.get("SCINODE_PATH")
        else:
            scinode_path = os.path.expanduser("~/.scinode")
        self.create_directory(scinode_path)
        config_file = config_file or os.path.join(scinode_path, f"{self.name}.json")
        self.config_file = config_file
        self.config = {}

        # Load existing configuration data if the file exists
        if os.path.isfile(self.config_file):
            self.load_config()

    def load_config(self):
        with open(self.config_file, "r") as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def add_item(self, item):
        name = item.pop("name")
        if name in self.config:
            raise ValueError(f"An item with the name '{name}' already exists.")
        self.config[name] = item
        self.save_config()

    def get_item(self, name):
        if name in self.config:
            config = self.config[name]
            config["name"] = name
            return config
        else:
            return None

    def delete_item(self, name):
        if name in self.config:
            del self.config[name]
            self.save_config()

    def show_item(self, name=None):
        if name in self.config:
            item = self.config[name]
            print(f"{self.name}: {name}\n")
            for key, value in item.items():
                print("{:20s}: {}".format(key, colored(value, "yellow")))
        else:
            print(f"Item '{name}' does not exist.")

    def list_items(self):
        # print(f"Items in {self.__class__.__name__}:")
        for name in self.config:
            print(name)

    def show_config(self):
        print(f"Configuration: {self.__class__.__name__}")
        for name, item in self.config.items():
            print(f"{name}: {item}")

    def add_from_json(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
        for item in data:
            name = item.pop("name")
            if name in self.config:
                raise ValueError(f"An item with the name '{name}' already exists.")
            self.config[name] = item
        self.save_config()

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
