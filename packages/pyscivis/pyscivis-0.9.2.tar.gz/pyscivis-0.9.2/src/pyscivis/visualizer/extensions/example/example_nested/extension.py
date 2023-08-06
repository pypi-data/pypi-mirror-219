from typing import Optional

import numpy as np

from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.extensions import NestedExtension
from pyscivis.visualizer.plots import ImagePlot, TablePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv


class ExampleNestedExtension(NestedExtension):  # pragma: nocover

    alias = "example_nested"
    multiple = True
    supported_files = "*"
    file_description = "Create Image for each filepath w/ TreeWidget"

    def create_plot(self,
                    leaf_name: str,
                    container_name: str,
                    container_type: str,
                    loading_div: Optional[LoadingDiv] = None):

        path = self.data_leaves[leaf_name]

        if container_type == "header":
            path: tuple   # path is a tuple for the header
            column_dict = dict(keys=list(), values=list())
            for index, p in enumerate(path):
                column_dict["keys"].append(f"Image{index}'s path")
                column_dict["values"].append(p)
            column_dict["keys"].append("Length of all paths combined")
            comb_length = len("".join(path))
            column_dict["values"].append(comb_length)
            return TablePlot(column_dict)
        else:  # image
            path: str
            np.random.seed(seed=len(path))  # let's make the image the same for paths with the same length
            data = np.random.rand(2, 4, 3, 34, 35)
            parsed = ParsedData(
                data=data,
                dim_names=["dim4", "dim3", "dim2", "dim1", "dim0"],
                dim_lengths=np.array(data.shape)*2,
                dim_units=["mm", "mm", "mm", "mm", "mm"],
            )
            return ImagePlot(parsed, self.config.image)

    def get_valid_leaf_type_combinations(self):
        return list(self.data_leaves.keys())

    @staticmethod
    def get_tree_structure(file_path):

        tree_structure = list()
        root_name = f"{len(file_path)} random images"
        root = {"id": "root", "parent": "#", "text": root_name, "type": "file"}
        tree_structure.append(root)
        header = {"id": "header", "parent": "root", "text": "Header", "type": "header"}
        tree_structure.append(header)
        for index, path in enumerate(file_path):
            node = {"id": path, "parent": "root", "text": str(index), "type": "images"}
            tree_structure.append(node)
        return tree_structure

    @staticmethod
    def get_data_leaves(file_path):
        data_leaves = dict()
        for path in file_path:
            data_leaves[path] = path
        data_leaves["header"] = file_path  # tuple of all paths
        return data_leaves

