from typing import Optional

from PIL import Image
import numpy as np

from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.extensions import FlatExtension
from pyscivis.visualizer.plots import ImagePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv

"""
This module exemplifies the creation of flat extensions, i.e., un-nested ones.
"""


def _read_img_as_greyscale(path: str,
                           width: Optional[int] = None,
                           height: Optional[int] = None
                           ) -> np.ndarray:
    """
    Read a greyscale image into a numpy array.

    Args:
        width: Width to resize the image to.
        height: Height to resize the image to.
        path: Path of image.

    Returns:
        2-dimensional numpy-array containing [y, x] of the image (in this order).
    """
    img: Image.Image
    with Image.open(path) as img:
        if width is not None and height is not None:
            img = img.resize((width, height))
        img = img.convert('L')
        np_arr = np.asarray(img)

    return np_arr


class PILExtensionFlat(FlatExtension):
    """
    This extension allows loading of some PIL-supported images.
    """

    alias = "pil_flat"
    supported_files = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    file_description = "PIL-supported Images"
    multiple = True

    def create_plot(self,
                    loading_div: Optional[LoadingDiv] = None) -> ImagePlot:
        """
        Read a PIL-supported image from the specified path and return a plot with that image.

        Returns:
            An ImagePlot object.
        """
        if loading_div is not None:
            loading_div.set_text("Loading image..")

        all_images = []
        if len(self.path) > 1:
            width = height = 500
        else:
            width = height = None
        for path in self.path:  # we set multiple=True so we get a tuple of paths instead of just one string
            image = _read_img_as_greyscale(path, width, height)
            all_images.append(image)

        image_data = np.array(all_images)
        parsed = ParsedData(
            data=image_data,
            dim_names=["images", "y", "x"],
            dim_lengths=image_data.shape,
            dim_units=["px", "px", "px"]
        )

        return ImagePlot(parsed, self.config.image)

