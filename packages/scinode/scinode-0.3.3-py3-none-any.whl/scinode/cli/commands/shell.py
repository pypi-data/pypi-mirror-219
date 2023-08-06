import click


DEFAULT_MODULES_LIST = [
    ("scinode.core.nodetree", "NodeTree"),
    ("scinode.core.node", "Node"),
    ("scinode.utils.db", "load"),
    ("scinode.utils.nodetree", "load_nodetree"),
    ("scinode.utils.node", "load_node"),
    ("scinode.orm.db_nodetree", "DBNodeTree"),
    ("scinode.orm.db_node", "DBNode"),
    ("scinode.utils.decorator", "node"),
]


def get_start_namespace():
    """Load all default modules"""
    namespace = {}

    for app_mod, model_name in DEFAULT_MODULES_LIST:
        namespace[model_name] = getattr(
            __import__(app_mod, {}, {}, model_name), model_name
        )
    return namespace


@click.command(help="Start a python shell with preloaded SciNode modules.")
def shell():
    """Start a python shell with preloaded SciNode modules."""
    from IPython import start_ipython

    namespace = get_start_namespace()
    banner = "Welcome to the SciNode shell."
    try:
        import IPython
    except ImportError:
        # IPython not available; use regular Python REPL.
        from code import InteractiveConsole

        InteractiveConsole(locals=namespace).interact(banner, "")
    else:
        print(banner)
        start_ipython(argv=[], display_banner=False, user_ns=namespace)
