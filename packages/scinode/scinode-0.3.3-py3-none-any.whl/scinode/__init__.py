"""
SciNode is a platform to create node-based workflows with each node
performing a dedicated task.
"""
from scinode.core.nodetree import NodeTree
from scinode.utils import load_nodetree, load_node
from scinode.utils.decorator import node
