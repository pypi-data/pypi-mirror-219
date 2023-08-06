from abc import ABC, abstractmethod
from functools import partial
from typing import Union, Sequence, Optional, Callable

from ismrmrd.xsd.ismrmrdschema.ismrmrd import ismrmrdHeader as AcquisitionsHeader
from ismrmrd import ImageHeader
from ismrmrd.file import Acquisitions, Images

from pyscivis.visualizer.dataclasses.config import ParserConfig
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv

from pyscivis.visualizer.dataclasses.parser import ParsedData

import numpy as np


class BaseParser(ABC):
    """
    The base class for Parsers that enforces "parse_with_header" to be implemented.
    """

    @classmethod
    def parse(cls,
              data: Union[np.ndarray, Images, Acquisitions],
              header: Optional[Union[Sequence[str], ImageHeader, AcquisitionsHeader]],
              config: ParserConfig,
              loading_indicator: Optional[LoadingDiv] = None
              ) -> ParsedData:
        """
        The main method to be called when there is data to be parsed.

        Depending on the supplied data-type either a series of images or a kspace is compiled into a ParsedData object.
        This method chooses the right parsing-method depending on the type of data and takes care of giving the correct
        printing-callable.

        Args:
            data: An ismrmrd-File-Container or a numpy-array.
            header: An ismrmrd-header belonging to the ismrmrd-File-Container or a Sequence of
             strings with names for the dimensions of a numpy array.
            config: An object containing the parser configuration.
            loading_indicator: A bokeh-layout-object that can display the current state graphically.

        Returns:
            A ParsedData object.
        """
        if loading_indicator is not None:
            printer = loading_indicator.set_text
        else:
            printer = partial(print, end="\r")

        return cls.parse_with_header(data, header, config, printer)

    @staticmethod
    @abstractmethod
    def parse_with_header(data: Union[Images, Acquisitions],
                          header: Union[ImageHeader, AcquisitionsHeader],
                          config: ParserConfig,
                          printer: Callable[[str], None]
                          ) -> ParsedData:
        """
        Abstract method meant to be overridden by subclasses.

        Args:
            data: An ismrmrd-File-Container.
            header: An ismrmrd-header belonging to the ismrmrd-File-Container.
            config: An object containing the parser configuration.
            printer: A callable that accepts a string and displays it.

        Raises:
            NotImplementedError: This method is meant to be overridden.
        """
        raise NotImplementedError()

