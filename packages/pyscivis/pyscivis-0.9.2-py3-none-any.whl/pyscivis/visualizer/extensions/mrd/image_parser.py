from warnings import warn

import numpy as np
from ismrmrd import ImageHeader
from ismrmrd.file import Images

from pyscivis.visualizer.dataclasses.config import ParserConfig
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv

from .base_parser import BaseParser
from pyscivis.visualizer.dataclasses.parser import ParsedData

default_image_dimensions = ("Instances", "Channels", "Slices", "Y", "X")  # Slices ^= Z


class ImageParser(BaseParser):
    """
    A parser to extract images and their metadata from either ismrmrd-Images or numpy-arrays.
    """

    @staticmethod
    def parse_with_header(images: Images,
                          header: ImageHeader,
                          config: ParserConfig,
                          printer: LoadingDiv
                          ) -> ParsedData:
        """
        Take Images-data from ismrmrd-files and compile images.

        First, the image-data is retrieved from the Images-object and converted to a np.ndarray.
        Then, optional FoV-data is extracted from the header. This includes dimension lengths and units
        which usually only are set for kX, kY and kZ.

        Args:
            images: An ismrmrd-Images object.
            header: An ismrmrd-ImageHeader containing relevant metadata.
            config: An object containing the parser configuration.
            printer: A callable that accepts a string and displays it.

        Returns:
            A ParsedData object.
        """
        images_data = np.array(images.data)
        if images_data.ndim != 5:
            warn(f"ISMRMRD-images_data has unsupported number of dimensions: {images_data.ndim}; \
                please create a Github-Issue.", UserWarning)

        # the existence of a header implies a standard ismrmrd image -> use default_dimensions
        names = default_image_dimensions
        try:
            _fov = tuple(header.field_of_view)[::-1]
        except AttributeError:
            _fov = [0]

        if _fov.count(0):  # if FoV contains any 0s/was nulled/does not exist
            lengths = images_data.shape
            units = tuple(["pixel"]*images_data.ndim)
        else:
            lengths = images_data.shape[:-len(_fov)] + _fov
            _amount_fillers = images_data.ndim - len(_fov)
            units = tuple(["pixel"]*_amount_fillers) + tuple(["mm"]*len(_fov))
        return ParsedData(images_data, names, lengths, units)

