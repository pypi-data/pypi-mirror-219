from .profile import ProfileConfig, profile_datas
import os


def init_scinode_configuration():
    """Initialize configuration.
    Create folder.
    """

    # create configuration path if not exist
    if os.environ.get("SCINODE_PATH"):
        scinode_path = os.environ.get("SCINODE_PATH")
    else:
        scinode_path = os.path.expanduser("~/.scinode")
    if not os.path.exists(scinode_path):
        os.makedirs(scinode_path)
    # create custom node folder
    custom_node_path = os.path.join(scinode_path, "custom_node")
    if not os.path.exists(custom_node_path):
        os.makedirs(custom_node_path)
