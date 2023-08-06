import pymongo
from scinode.config.profile import profile_datas

scinode_client = pymongo.MongoClient(
    profile_datas["db_address"], serverSelectionTimeoutMS=10
)
scinodedb = scinode_client[profile_datas["db_name"]]
db_nodetree = scinodedb["nodetree"]
db_node = scinodedb["node"]


def get_db_status():
    """Get the status of the database connection."""
    try:
        scinode_client.server_info()
        active = True
    except pymongo.errors.ServerSelectionTimeoutError as err:
        active = False
    return active
