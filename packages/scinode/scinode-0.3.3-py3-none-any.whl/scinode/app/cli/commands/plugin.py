import click
from pathlib import Path


@click.group(help="CLI tool to manage plugin.")
def plugin():
    pass


@plugin.command(help="Install plugin.")
@click.option("-n", "--name", help="port.", type=str)
def list(name):
    from scinode.app.utils import get_entries
    from pathlib import Path

    path = Path(__file__).parent.parent
    eps = get_entries("scinode_static")
    for plugin_name, static in eps.items():
        print(plugin_name)


@plugin.command(help="Install plugin.")
@click.option("-n", "--name", help="port.", type=str)
def install(name):
    import shutil
    from scinode.app.utils import get_entries
    from pathlib import Path

    path = Path(__file__).parent.parent.parent
    eps = get_entries("scinode_static")
    dst_folder = path / "static"
    for plugin_name, static in eps.items():
        print("Install {} plugin.".format(plugin_name))
        for key, value in static.items():
            src = value
            dst = dst_folder / f"{key}s" / f"{plugin_name}_{key}s.js"
            # print(src, dst)
            try:
                shutil.copyfile(src, dst)
                print(f"  Copy {key}...")
            except shutil.SameFileError:
                print("  Skip same file.")
            except PermissionError:
                print("Permission denied.")
            except:
                print("Error occurred while copying file.")
        print(f"Install plugin {plugin_name} successfully.")
