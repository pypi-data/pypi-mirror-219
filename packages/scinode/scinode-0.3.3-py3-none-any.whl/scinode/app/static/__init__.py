def main():
    from pathlib import Path

    path = Path(__file__).parent
    static = {
        "component": path / "components" / "app_components.js",
        "socket": path / "sockets" / "app_sockets.js",
        "control": path / "controls" / "app_controls.js",
    }
    return "app", static


if __name__ == "__main__":
    print(main())
