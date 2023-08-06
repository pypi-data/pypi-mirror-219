def scinode_to_rete(data):
    """SciNode component json data to rete component json data.

    - "properties" to "controls"
    - find contorl for input socket with same name.

    Args:
        data (dict): _description_
    """
    # rename "properties" to "controls"
    print("scinode_to_rete: ", data)
    data["controls"] = data.pop("properties")
    control_keys = [d["name"] for d in data["controls"]]
    input_keys = [d["name"] for d in data["inputs"]]
    inter = set(input_keys).intersection(set(control_keys))
    for input in data["inputs"]:
        input["control"] = data["controls"][control_keys.index(input["name"])]
    data["controls"] = [x for x in data["controls"] if x["name"] not in inter]
    return data


def rete_to_scinode(data):
    """Rete component json data to  SciNode component json data.

    - "controls" to "properties"
    - find contorl for input socket with same name.

    Args:
        data (dict): _description_
    """
    # rename "properties" to "controls"
    data["properties"] = data.pop("controls")
    for input in data["inputs"]:
        if "control" in input:
            d = input.pop("control")
            d["name"] = input["name"]
            data["properties"].append(d)
    return data


if __name__ == "__main__":
    from scinode.app.build_node_from_json import template

    component_json = template[0]
    component_json = scinode_to_rete(component_json)
    import pprint

    pprint.pprint(component_json)
