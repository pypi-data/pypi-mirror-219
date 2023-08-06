import pathlib
from setuptools import setup, find_packages


def test_suite():
    import unittest

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="scinode",
    version="0.3.3",
    description="Design computational workflow using nodes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/scinode/scinode",
    author="Xing Wang",
    author_email="xingwang1991@gmail.com",
    license="MIT License",
    classifiers=[],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["scinode=scinode.cli.main:scinode"],
        "scinode_cli": [
            "profile = scinode.cli.commands.profile:profile",
            "worker = scinode.cli.commands.worker:worker",
            "scheduler = scinode.cli.commands.scheduler:scheduler",
            "node = scinode.cli.commands.node:node",
            "nodetree = scinode.cli.commands.nodetree:nodetree",
            "data = scinode.cli.commands.data:data",
            "mq = scinode.cli.commands.mq:mq",
            "computer = scinode.cli.commands.computer:computer",
            "shell = scinode.cli.commands.shell:shell",
            "web = scinode.app.cli.commands.web:web",
            "plugin = scinode.app.cli.commands.plugin:plugin",
        ],
        "scinode_node": [
            "built_in = scinode.nodes.built_in:node_list",
            "bash_node = scinode.nodes.bash_node:node_list",
            "control = scinode.nodes.control:node_list",
            "python_builtin = scinode.nodes.python_builtin:node_list",
            "numpy_node = scinode.nodes.numpy_node:node_list",
            "test = scinode.nodes.test:node_list",
            "utils = scinode.nodes.utils:node_list",
            "test_node_group = scinode.nodes.test_node_group:node_list",
        ],
        "scinode_socket": [
            "built_in = scinode.sockets.built_in:socket_list",
        ],
        "scinode_property": [
            "built_in = scinode.properties.built_in:property_list",
        ],
    },
    install_requires=[
        "psutil",
        "numpy",
        "scipy",
        "click",
        "dnspython",
        "pymongo",
        "mongoengine",
        "pandas",
        "pyyaml",
        "colorama",
        "termcolor",
        "ipython",
        "blinker",
        "flask",
        "gunicorn",
        "cloudpickle",
        "disk-objectstore",
        "paramiko",
        "celery",
    ],
    extras_require={
        "celery": ["celery", "gevent"],
    },
    package_data={},
    include_package_data=True,
    python_requires=">=3.6",
    test_suite="setup.test_suite",
)
