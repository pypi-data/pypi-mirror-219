from typing import Optional, Union

import numpy as np
from PIL import Image
from pyscivis.visualizer.dataclasses.parser import ParsedData

from pyscivis.visualizer.extensions import FlatExtension
from pyscivis.visualizer.plots import ImagePlot, ComplexPlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv


class PILExtensionRGBA(FlatExtension):

    alias = "pil_rgba"
    supported_files = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    file_description = "PIL-supported RGBA-Image"
    multiple = False

    def create_plot(self, loading_div: Optional[LoadingDiv] = None) -> Union[ImagePlot, ComplexPlot]:
        img: Image.Image
        with Image.open(self.path) as img:
            img = img.convert('RGBA')
            np_arr = np.asarray(img).view(dtype=np.uint32).squeeze()
        data = ParsedData(
            data=np_arr,
            dim_names=["y", "x"],
            dim_lengths=np_arr.shape,
            dim_units=["px", "px"]
        )
        self.config.image.ds_min_elements = 1000
        return ImagePlot(data, self.config.image, use_rgba=True)