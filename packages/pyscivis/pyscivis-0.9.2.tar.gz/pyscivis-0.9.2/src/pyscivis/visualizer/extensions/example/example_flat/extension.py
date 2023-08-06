import time

import numpy

from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.extensions import FlatExtension
from pyscivis.visualizer.plots import ImagePlot


class ExampleFlatExtension(FlatExtension):  # pragma: nocover

    alias = "example_flat"
    multiple = False
    supported_files = "*"
    file_description = "Read filepath into ASCII"

    def create_plot(self, loading_div=None):

        # This allows us to print messages to a notebook
        # or a (standalone's) loading screen with the same function
        if loading_div is None:  # invoked from a notebook
            print_msg = print
        else:  # invoked from the standalone app
            print_msg = loading_div.set_text

        # Display text while we are "calculating" the plot
        print_msg("I am currently very busy.")
        time.sleep(3)

        # Here we act as if `multiple=False` was set as a class variable
        # so self.path is a string (as opposed to a tuple of strings).
        # Now: Convert the selected file-path to a list containing its ASCII-equivalent
        x_axis_values = [ord(c) for c in self.path]

        height = 50
        amount_images = 5

        multidim_image = list()

        # Create a 3D Image
        for _ in range(amount_images):
            two_dim_image = list()
            for y in range(height):
                x_vals = numpy.roll(x_axis_values, y)  # shift array by y
                two_dim_image.append(x_vals)
            multidim_image.append(two_dim_image)

        multidim_image = numpy.array(multidim_image)

        # The Plot expects to be supplied with a ParsedData object:
        parsed = ParsedData(
            data=multidim_image,
            dim_names=["images", "y", "x"],
            dim_lengths=multidim_image.shape,
            dim_units=["image", "char", "char"]  # units for the axes
        )

        # We return an ImagePlot because our data is not complex
        return ImagePlot(parsed, self.config.image)

        # Check Section 3 for information on what kind of Plots we can display
