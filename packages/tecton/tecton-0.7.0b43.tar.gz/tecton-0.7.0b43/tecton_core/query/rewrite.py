from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Type

from tecton_core import conf
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode


class Rewrite(ABC):
    @abstractmethod
    def rewrite(self, node: NodeRef) -> NodeRef:
        raise NotImplementedError


# Mutates the input
def rewrite_tree(tree: NodeRef):
    if not conf.get_bool("QUERY_REWRITE_ENABLED"):
        return
    rewrites: List[Rewrite] = []
    for rewrite in rewrites:
        rewrite.rewrite(tree)


def tree_contains(tree: NodeRef, node_type: Type[QueryNode]) -> bool:
    """Returns True if the tree contains a NodeRef of the given type, False otherwise."""
    if isinstance(tree.node, node_type):
        return True

    return any(tree_contains(subtree, node_type) for subtree in tree.inputs)
