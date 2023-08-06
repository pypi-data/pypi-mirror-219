import click
import os


def is_web_running():
    # read web pid file, print the status
    from scinode.config.profile import ProfileConfig
    from scinode.utils.process import is_process_running

    profile = ProfileConfig()
    current_profile = profile.get_current_profile()

    config_path = current_profile["config_path"]
    pidfile = os.path.join(config_path, "web.pid")
    web_active = is_process_running(pidfile)
    return web_active


def stop_web():
    from scinode.utils.process import stop_process, read_pid
    from scinode.config.profile import ProfileConfig
    from scinode.utils.process import is_process_running

    profile = ProfileConfig()
    current_profile = profile.get_current_profile()
    stop_process(read_pid(os.path.join(current_profile["config_path"], "web.pid")))


@click.group(help="CLI tool to manage web app.")
def web():
    pass


@web.command(help="Start the web.")
@click.option("--debug", is_flag=True, default=False, help="Use debug mode")
@click.option("--port", help="port.", type=int, default=5000)
def start(debug, port):
    from scinode.app.app import create_app

    app = create_app()
    kwargs = {}
    kwargs["debug"] = debug
    kwargs["port"] = port
    # webbrowser.open_new('http://127.0.0.1:{}/'.format(port))
    app.run(**kwargs)
    # os.system(
    # "nohup scinode web start > ~/.scinode/web.log & echo $! > ~/.scinode/web.pid &"
    # )
    print(f"Please visit the web app at: http://127.0.0.1:{port}/")


@web.command(help="Stop the web.")
def stop():
    web_active = is_web_running()
    if web_active:
        stop_web()
    else:
        print("Web is not active.")


@web.command(help="Show the status of the app.")
def status():
    from scinode.utils.formater import print_key_value, green, red

    web_active = is_web_running()
    if web_active:
        print_key_value("Web", green("running on http://127.0.0.1:5000/"))
    else:
        print_key_value("Web", red("is not active."))
