from typing import List, Union, Optional, Dict, Tuple

import ismrmrd
from bokeh.models import Div
from ismrmrd.file import Container
from pyscivis.visualizer.extensions import NestedExtension
from pyscivis.visualizer.plots import ImagePlot, ComplexPlot
from pyscivis.visualizer.plots.table_plot import TablePlot

from .image_parser import ImageParser
from .acquisition_parser import AcquisitionParser
from .header_parser import HeaderParser

from .tree_util import extract_data_leaves, extract_tree_structure


class MRDExtension(NestedExtension):
    """
    Extension to handle ISMRMRD-type h5-files.
    """

    alias = "mrd"
    supported_files = ".h5"
    file_description = "ISMRMRD-files"
    multiple = True

    def create_plot(self,
                    leaf_name: str,
                    container_name: str,
                    container_type: str,
                    loading_div: Optional[Div] = None
                    ) -> Union[ImagePlot, ComplexPlot, TablePlot]:
        """
        Create plot by accessing the ismrmrd.Container directly, based on name and type of container.

        Args:
            leaf_name: Full ID of clicked leaf, not used  because we address files by their parent container and type.
            container_name: Name of the ismrmrd container.
            container_type: Type of the ismrmrd container.
            loading_div: If a loading div is to be used for progress notification.

        Returns:
            An ImagePlot or ComplexPlot.
        """
        try:
            container = self.data_leaves[container_name]  # retrieve h5-container
        except KeyError:
            raise ValueError(f"File-Leaf '{container_name}' does not occur in dict of File-Leaves ")

        parser_conf = self.config.parser
        plot_config = self.config.image
        # parse container depending on its header and create a plot
        if container_type == "images":
            data = container.images
            header = container.images[0].getHead()
            parsed_img = ImageParser.parse(data, header, parser_conf, loading_indicator=loading_div)
            return ImagePlot(parsed_img, plot_config, loading_indicator=loading_div)
        elif container_type == "acquisitions":
            data = container.acquisitions
            header = container.header
            parsed_acq = AcquisitionParser.parse(data, header, parser_conf, loading_indicator=loading_div)
            return ComplexPlot(parsed_acq, plot_config, loading_indicator=loading_div)
        elif container_type == "header":
            header_tree = HeaderParser.parse(container.header, loading_indicator=loading_div)
            return TablePlot(header_tree, loading_indicator=loading_div)
        elif container_type == "waveforms":
            # examples of ismrmrd waveforms are hard to come by
            # will be implemented once actually needed by anyone
            raise NotImplementedError
        else:  # unknown, don't do anything
            pass

    def get_valid_leaf_type_combinations(self) -> List[str]:
        """
        Check what kind of data a container contains and combine this type with the name of the parent container.

        Returns:
            A list of valid combinations that can be used to identify a specific data-container.

        """
        #  create valid leaf-name + type combinations
        valid_combinations = list()
        for name, container in self.data_leaves.items():
            valid_types: List[str] = list()

            if container.has_images():
                valid_types.append("images")
            if container.has_acquisitions():
                valid_types.append("acquisitions")
            if container.has_header():
                valid_types.append("header")
            if container.has_waveforms():
                valid_types.append("waveforms")
            valid_combinations.extend([name + ";" + _type for _type in valid_types])
        return valid_combinations

    @staticmethod
    def file_handler(path: str) -> ismrmrd.File:
        return ismrmrd.File(path, mode="r")

    @staticmethod
    def get_tree_structure(path: Tuple[str]) -> List[Dict[str, str]]:
        return extract_tree_structure(path, MRDExtension.file_handler)

    @staticmethod
    def get_data_leaves(path: Tuple[str]) -> Dict[str, Container]:
        return extract_data_leaves(path, MRDExtension.file_handler)
