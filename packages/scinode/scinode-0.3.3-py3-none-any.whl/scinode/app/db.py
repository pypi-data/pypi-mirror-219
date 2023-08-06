from pymongo import MongoClient
from scinode.config import profile_datas

scinode_client = MongoClient(profile_datas["db_address"])
db = scinode_client[profile_datas["db_name"]]


def query_node_data(coll, query, request):
    """Qeury data from database

    Args:
        coll (Mongodb collection): _description_
        query (dict): _description_
        request (request): _description_

    Returns:
        _type_: _description_
    """
    # total record
    recordsTotal = coll.count_documents(query)
    # search filter
    search = request.args.get("search[value]")
    if search:
        query.update({"name": {"$regex": search, "$options": "i"}})
    total_filtered = coll.count_documents(query)
    query = coll.find(
        query,
        {
            "_id": 0,
            "name": 1,
            "index": 1,
            "uuid": 1,
            "state": 1,
            "action": 1,
            "identifier": 1,
            "metadata": 1,
            "inner_id": 1,
        },
    )
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["index", "name", "state", "action"]:
            col_name = "name"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        if descending:
            order.append([col_name, -1])
        else:
            order.append([col_name, 1])
        i += 1
    if order:
        query = query.sort(order)
    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.skip(start).limit(length)
    return query, total_filtered, recordsTotal


def query_nodetree_data(coll, query, request):
    """Qeury data from database

    Args:
        coll (Mongodb collection): _description_
        query (dict): _description_
        request (request): _description_

    Returns:
        _type_: _description_
    """
    # total record
    recordsTotal = coll.count_documents({})
    # search filter
    search = request.args.get("search[value]")
    print("query: ", query, "search: ", search)
    if search:
        query.update({"name": {"$regex": search, "$options": "i"}})
    print("query: ", query)
    total_filtered = coll.count_documents(query)
    query = coll.find(
        query,
        {
            "_id": 0,
            "name": 1,
            "index": 1,
            "uuid": 1,
            "state": 1,
            "action": 1,
            "metadata": 1,
        },
    )
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["index", "name", "state", "action"]:
            col_name = "index"
        if col_name in ["worker_name"]:
            col_name = "metadata.{}".format(col_name)
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        if descending:
            order.append([col_name, -1])
        else:
            order.append([col_name, 1])
        i += 1
    if order:
        query = query.sort(order)
    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.skip(start).limit(length)
    return query, total_filtered, recordsTotal


def query_component_data(coll, query, request):
    """Qeury data from database

    Args:
        coll (Mongodb collection): _description_
        query (dict): _description_
        request (request): _description_

    Returns:
        _type_: _description_
    """
    # total record
    recordsTotal = coll.count_documents({})
    # search filter
    search = request.args.get("search[value]")
    if search:
        query.update({"metadata.identifier": {"$regex": search, "$options": "i"}})
    total_filtered = coll.count_documents(query)
    query = coll.find(
        query,
        {
            "name": 1,
            "index": 1,
            "uuid": 1,
            "metadata.catalog": 1,
        },
    )
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["index", "name"]:
            col_name = "name"
        if col_name in ["catalog"]:
            col_name = "metadata.{}".format(col_name)
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        if descending:
            order.append([col_name, -1])
        else:
            order.append([col_name, 1])
        i += 1
    # print("order: ", order)
    if order:
        query = query.sort(order)
    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.skip(start).limit(length)
    return query, total_filtered, recordsTotal


def query_template_data(coll, query, request):
    """Qeury data from database

    Args:
        coll (Mongodb collection): _description_
        query (dict): _description_
        request (request): _description_

    Returns:
        _type_: _description_
    """
    # total record
    recordsTotal = coll.count_documents({})
    # search filter
    search = request.args.get("search[value]")
    if search:
        query = {
            "metadata.platform": "rete",
            "name": {"$regex": search, "$options": "i"},
        }
    else:
        query = {"metadata.platform": "rete"}
    total_filtered = coll.count_documents(query)
    query = coll.find(
        query,
        {
            "_id": 0,
            "name": 1,
            "index": 1,
            "uuid": 1,
            "state": 1,
            "action": 1,
            "metadata": 1,
        },
    )
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["index", "name", "state", "action", "worker_name"]:
            col_name = "name"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        if descending:
            order.append([col_name, -1])
        else:
            order.append([col_name, 1])
        i += 1
    if order:
        query = query.sort(order)
    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.skip(start).limit(length)
    return query, total_filtered, recordsTotal


def query_socket_data(coll, query, request):
    """Qeury data from database

    Args:
        coll (Mongodb collection): _description_
        query (dict): _description_
        request (request): _description_

    Returns:
        _type_: _description_
    """
    # total record
    recordsTotal = coll.count_documents(query)
    # search filter
    search = request.args.get("search[value]")
    if search:
        query.update({"name": {"$regex": search, "$options": "i"}})
    total_filtered = coll.count_documents(query)
    query = coll.find(
        query,
        {
            "_id": 0,
            "name": 1,
            "index": 1,
            "uuid": 1,
            "identifier": 1,
            "value": 1,
        },
    )
    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        if col_index is None:
            break
        col_name = request.args.get(f"columns[{col_index}][data]")
        if col_name not in ["index", "name", "state", "action"]:
            col_name = "name"
        descending = request.args.get(f"order[{i}][dir]") == "desc"
        if descending:
            order.append([col_name, -1])
        else:
            order.append([col_name, 1])
        i += 1
    if order:
        query = query.sort(order)
    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query.skip(start).limit(length)
    return query, total_filtered, recordsTotal
