from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict, Any, Sequence

from pyscivis.visualizer.dataclasses.config import Config
from pyscivis.visualizer.plots import ImagePlot, ComplexPlot, TablePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv


class FlatExtension(ABC):
    """
    Base class for all extensions that do not wish to use a file browser to navigate through data.

    Strongly recommended for single non-hierarchical files, e.g., .jpg, .png, .txt, etc.

    Also recommended, if you want to 'merge' multiple selected files into
    one piece of data and display them as one plot.
    If you want to navigate multiple files independently (using a file browser)
    use NestedExtension instead.
    """
    @property
    @abstractmethod
    def alias(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def multiple(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def supported_files(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def file_description(self):
        raise NotImplementedError()

    def __init__(self,
                 path: Union[str, Sequence[str]],
                 config: Config
                 ) -> None:
        """
        Set up class attributes.

        Args:
            path: Path of file to be loaded.
            config: Config object.
        """

        if self.multiple is True:  # want to make sure we check a boolean not a property
            if isinstance(path, str):
                path = (path, )  # compatibility for notebook path entry

        self.path = path
        self.config = config

    @abstractmethod
    def create_plot(self,
                    loading_div: Optional[LoadingDiv] = None
                    ) -> Union[ImagePlot, ComplexPlot, TablePlot]:
        """
        Create a plot by reading data directly from a non-nested file.

        Raises:
            NotImplementedError: This method is meant to be overridden.
        """
        raise NotImplementedError()


class NestedExtension(FlatExtension):
    """
    Base class for all extensions that want to create a file browser for the user to choose data from.

    Recommended for hierarchical files like 'h5'-files or if selecting
    a large amount of unrelated data-files.
    If you wish to merge all data of an h5 into one plot and
    do not need a file browser, use FlatExtension instead.
    """

    def __init__(self,
                 path: Union[str, Sequence[str]],
                 config: Config
                 ) -> None:
        """
        Set up file handler and required data structures for a ContainerExtension.

        Args:
            path: Path of the file to be loaded.
            config: Config object.
        """
        super().__init__(path, config)
        self.tree_struct = self.get_tree_structure(self.path)
        self.data_leaves = self.get_data_leaves(self.path)

    @abstractmethod
    def create_plot(self,
                    leaf_name: str,
                    container_name: str,
                    container_type: str,
                    loading_div: Optional[LoadingDiv] = None
                    ) -> Union[ImagePlot, ComplexPlot, TablePlot]:
        """
        Create a plot and return its layout.

        Args:
            leaf_name: Full ID of clicked leaf.
            container_name: Name of container with plot-data.
            container_type: Type of the container.
            loading_div: Used to notify user of progress, if None -> stdout.

        Returns:
            An ImagePlot or ComplexPlot .

        Raises:
            NotImplementedError: This method is meant to be overridden.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_valid_leaf_type_combinations(self) -> List[str]:
        """
        Infer valid name-type combinations from leaf-list.

        Raises:
            NotImplementedError: This function is meant to be overridden.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_tree_structure(file_path: str) -> List[Dict[str, str]]:
        """
        Construct a flat tree-structure to be used by the filetree-widget.

        Args:
            file_path: Path of file to be parsed into a tree structure.

        Raises:
            NotImplementedError: This method is meant to be overridden.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_data_leaves(file_path: str) -> Dict[str, Any]:
        """
        Get (container-name, container-data)-Dictionary.

        Args:
            file_path: Path of file to be parsed.

        Raises:
            NotImplementedError: This method is meant to be overridden.
        """
        raise NotImplementedError()
