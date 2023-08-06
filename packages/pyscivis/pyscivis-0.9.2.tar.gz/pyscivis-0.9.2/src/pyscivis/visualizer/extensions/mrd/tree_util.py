import os
from typing import Dict, List, Tuple, Callable
import ismrmrd

"""
This module includes various utility functions for parsing 
ISMRMRD-Files and converting them to python-native datastructures.
"""


def extract_data_leaves(paths: Tuple[str, ...],
                        file_handler: Callable[[str], ismrmrd.File]
                        ) -> Dict[str, ismrmrd.file.Container]:
    """
    Extracts only the leaves of an h5-file and enhances them with additional information.

    Args:
        paths: Paths of ismrmrd-files.
        file_handler: Callable accepting a path-str and returning a file-handler.

    Returns:
        A list of dictionaries mapping leaf-names to H5-Containers.

    """
    leaf_dict = dict()
    for path in paths:
        ismrmrd_file = file_handler(path)
        file_basename = os.path.basename(path)
        _extract_data_leaves(leaf_dict, ismrmrd_file, "root_"+file_basename)
    return leaf_dict


def _extract_data_leaves(leaf_dict: Dict[str, ismrmrd.file.Container],
                         container: ismrmrd.file.Container,
                         parent_name: str
                         ) -> None:
    """ Recursive helper function for extract_data_leaves. """
    for child_name in container:
        child = container[child_name]
        headers = child.available()
        own_name = parent_name+"_"+child_name
        if headers:
            leaf_dict[own_name] = child
        else:
            _extract_data_leaves(leaf_dict, container[child_name], own_name)


"""
[
    {"id": "root_ajson1", "parent": "#", "text": "Filename"},
    {"id": "root_ajson1_ajson2", "parent": "root_ajson1", "text": "Container1", "type": "container"},
    {"id": "root_ajson1_ajson2_ajson3", "parent": "root_ajson1_ajson2", "text": "Image1", "type": "image"},
    {"id": "root_ajson1_ajson2_ajson4", "parent": "root_ajson1_ajson2", "text": "Header1", "type": "header"},
    {"id": "root_ajson1_ajson5", "parent": "root_ajson1", "text": "Container2", "type": "container"},
]
"""


def extract_tree_structure(paths: Tuple[str],
                           file_handler: Callable[[str], ismrmrd.File]
                           ) -> List[Dict[str, str]]:
    """
    Extract the file structure of a h5-File into a flat list.

    Args:
        paths:  Paths of ismrmrd-files.
        file_handler: Callable accepting a path-str and returning a file-handler.

    Returns:
        A list of dictionaries containing meta-information and their hierarchical parent.

    """

    ret = list()
    root = {"id": "root", "parent": "#", "text": "Files", "type": "file"}
    ret.append(root)
    for path in paths:
        ismrmrd_file = file_handler(path)
        file_basename = os.path.basename(path)
        id_ = "root_"+file_basename
        file = {"id": id_, "parent": "root", "text": file_basename, "type": "file"}
        ret.append(file)
        for child_key in ismrmrd_file:
            _extract_tree_structure(ret, ismrmrd_file[child_key], child_key, id_)
    return ret


def _extract_tree_structure(node_list: List[Dict[str, str]],
                            container: ismrmrd.file.Container,
                            container_name: str,
                            parent_name: str
                            ) -> None:
    """ Recursive helper function for extract_tree_structure. """
    id_ = parent_name+"_"+container_name
    cur = {"id": id_, "parent": parent_name, "text": container_name, "type": "container"}
    node_list.append(cur)

    headers = container.available()
    for header in headers:
        h = {"id": id_+"_"+header, "parent": id_, "text": header, "type": header}
        node_list.append(h)

    for child_key in container:
        _extract_tree_structure(node_list, container[child_key], child_key, id_)


leaf_types = ["images", "acquisitions", "header", "waveforms"]

