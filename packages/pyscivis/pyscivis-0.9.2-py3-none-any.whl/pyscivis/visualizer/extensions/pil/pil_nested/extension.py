import os
from typing import Optional, Tuple, List, Dict

from PIL import Image
import numpy as np

from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.extensions import NestedExtension
from pyscivis.visualizer.plots import ImagePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv

"""
This module exemplifies the creation of nested extensions, using "flat" files.
"""


class PILExtensionNested(NestedExtension):
    """
    This extension allows loading of some PIL-supported images.
    """

    alias = "pil_nested"
    supported_files = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    file_description = "PIL-supported Images (Nested)"
    multiple = True

    def create_plot(self,
                    leaf_name: str,
                    container_name: str,
                    container_type: str,
                    loading_div: Optional[LoadingDiv] = None
                    ) -> ImagePlot:
        """
        Read a PIL-supported image from the specified path and return a plot with that image.

        Args:
            leaf_name: Full ID of clicked leaf, in this case the path of the image.
            container_name: Name of container with plot-data, not used here since we address images by the path.
            container_type: Type of the container, not used since all plots are images.
            loading_div: Used to notify user of progress, if None -> stdout.

        Returns:
            An ImagePlot object.
        """
        if loading_div is not None:
            loading_div.set_text("Loading image..")

        pil_image: Image.Image = self.data_leaves[leaf_name]
        pil_image = pil_image.convert('L')
        np_arr = np.asarray(pil_image)

        parsed = ParsedData(
            data=np_arr,
            dim_names=["y", "x"],
            dim_lengths=np_arr.shape,
            dim_units=["px", "px"]
        )

        return ImagePlot(parsed, self.config.image)

    def get_valid_leaf_type_combinations(self) -> List[str]:
        return [name for name in self.data_leaves.keys()]

    @staticmethod
    def get_tree_structure(file_path: Tuple[str]) -> List[Dict[str, str]]:
        """
        Create a tree structure for the specified files.

        In this case we create a tree with depth 2, the Root and its (image-)children.

        Args:
            file_path: File paths for images.

        Returns:
            List of Dicts containing data to fill a FileTree.

        """
        tree_structure = list()
        root_name = f"A whole {len(file_path)} images"
        root = {"id": "root", "parent": "#", "text": root_name, "type": "file"}
        tree_structure.append(root)
        for path in file_path:
            node_name = os.path.basename(path)
            node = {"id": path, "parent": "root", "text": node_name, "type": "images"}
            tree_structure.append(node)
        return tree_structure

    @staticmethod
    def get_data_leaves(file_path: Tuple[str]) -> Dict[str, Image.Image]:
        """
        Collect all leaves from the file paths into a dict, here: (filepath, Image)-dict.

        Args:
            file_path: Sequence of file paths.
        """
        data_leaves = dict()
        for path in file_path:
            data_leaves[path] = Image.open(path)
        return data_leaves
