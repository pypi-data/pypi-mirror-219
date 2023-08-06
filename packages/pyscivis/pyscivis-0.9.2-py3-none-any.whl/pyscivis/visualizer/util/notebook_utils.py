from typing import Dict, List


class MRDNode:
    """
    A node class as required by the pptree package.
    """

    def __init__(self,
                 text: str,
                 type_: str,
                 parent: "MRDNode" = None
                 ) -> None:
        """
        Create a MRDNode object with the supplied test, type and parent.

        Args:
            text: Text to display.
            type_: Type of this node.
            parent: MRDNode parent.
        """
        self.text = text
        self.type_ = type_
        self.children = []
        if parent:
            parent.children.append(self)


def nodeify_tree_structure(tree_structure: List[Dict[str, str]]) -> MRDNode:
    """
    Convert a tree-like structured list to a node-tree.

    Args:
        tree_structure: A List of Dictionaries containing name and type.

    Returns:
        The root MRDNode.

    """
    root = MRDNode("root", "root")
    _nodeify_tree_structure(root, tree_structure)
    return root


def _nodeify_tree_structure(parent_node: MRDNode,
                            tree_structure: List[Dict[str, str]]
                            ) -> None:
    """ Recursive helper function for nodeify_tree_structure. """
    for node_dict in tree_structure:
        if node_dict['parent'] == parent_node.text:
            node = MRDNode(node_dict['text'], node_dict['type'], parent_node)
            _nodeify_tree_structure(node, tree_structure)
