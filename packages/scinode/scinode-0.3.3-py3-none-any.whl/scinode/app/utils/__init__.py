def register(pool, entry):
    name, static = entry()
    pool[name] = static


def get_entries(entry_point_name):
    from importlib.metadata import entry_points

    pool = {}
    eps = entry_points().get(entry_point_name, [])
    for entry_point in eps:
        entry = entry_point.load()
        register(pool, entry)
    return pool


# seperate the entry points into different groups
# groups are component, socket, control
def get_entry_point_filename():
    entries = get_entries("scinode_static")
    components = []
    sockets = []
    controls = []
    for plugin_name, value in entries.items():
        components.append(f"{plugin_name}_components.js")
        sockets.append(f"{plugin_name}_sockets.js")
        controls.append(f"{plugin_name}_controls.js")
    return {"components": components, "sockets": sockets, "controls": controls}


if __name__ == "__main__":
    entries = get_entries("scinode_static")
    print(entries)
    entries = get_entry_point_filename("scinode_static")
    print(entries)
