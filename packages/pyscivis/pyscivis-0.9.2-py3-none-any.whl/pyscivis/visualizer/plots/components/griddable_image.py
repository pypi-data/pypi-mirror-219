import math
from typing import Dict, Union, List, Tuple

import numpy as np
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, WheelZoomTool, ColorBar, Image as ImageGlyph, \
    PolyAnnotation, Title
from bokeh.plotting import figure

from pyscivis.visualizer.util.downsample import downsample_2d_mean
from pyscivis.visualizer.dataclasses.config import ImageConfig

dims_jscode = """
    var update_dims = function () {
        var new_data = {
            height: [plot.height],
            width: [plot.width],
            x_start: [plot.x_range.start],
            y_start: [plot.y_range.start],
            x_end: [plot.x_range.end],
            y_end: [plot.y_range.end]
        };
        dims.data = new_data;
    };
    var throttle = window.throttle
    if (typeof throttle != 'undefined' && throttle != null) {
        clearTimeout(throttle);
    }
    
    window.throttle = setTimeout(update_dims, %i, "replace");
    """


class GriddableImage:
    """
    Takes care of keeping the displayed image up to date, regridding/downsampling and sizing it.
    """

    def __init__(self,
                 image_data: np.ndarray,
                 dw: float,
                 dh: float,
                 color_bars: Dict[str, ColorBar],
                 initial_cbar: Union[int, str],
                 use_rgba: bool,
                 config: ImageConfig,
                 title: str = ""
                 ) -> None:
        """
        Set up config attributed, callbacks, and the image including tools.

        Args:
            image_data: 2-dimensional numpy-array containing image data.
            dw: Length of the x-axis.
            dh: Length of the y-axis.
            color_bars: Dictionary mapping ColorBar names to ColorBar objects.
            initial_cbar: Either the index (in color_bars) or the name of the inital ColorBar.
            use_rgba: Whether to use an 'image_rgba'-glyph; disabled color-bar/-mapper logic.
            config: A ImageConfig object.
            title: Optional title displayed above the main plot.
        """
        self.PREF_HEIGHT = config.pref_height
        self.MIN_HEIGHT = config.min_height
        self.MAX_HEIGHT = config.max_height
        self.MIN_WIDTH = config.min_width
        self.MAX_WIDTH = config.max_width
        self.MIN_BORDER = config.border

        self.ds_downsample_images_threshold = config.ds_downsample_images_threshold
        self.ds_threshold = config.ds_threshold
        self.downsample_flag = False

        self.image_data: np.ndarray = np.array([])
        self.x_span: float = 0
        self.y_span: float = 0
        self.x_ratio: float = 0
        self.y_ratio: float = 0

        self.image_source = ColumnDataSource(data=dict(image=[], x=[], y=[], dw=[], dh=[]))
        self.client_dims = ColumnDataSource(data=dict(width=[], height=[],
                                                      x_start=[], x_end=[],
                                                      y_start=[], y_end=[]))

        self.client_dims.on_change('data', lambda attr, old, new: self.regrid_image(self.ds_threshold))

        self.plot = figure(tools=["pan", "reset"], toolbar_location="above",
                           x_range=(0, 1), y_range=(0, 1),
                           min_border_left=self.MIN_BORDER, min_border_bottom=self.MIN_BORDER,
                           min_border_top=self.MIN_BORDER, min_border_right=self.MIN_BORDER * 2,
                           css_classes=["image-figure"])
        self.plot.add_layout(Title(text=""), "above")
        self.plot.add_layout(Title(text=title, align="center"), "above")
        self.plot.toolbar.logo = None

        ds_indicator = PolyAnnotation(
            fill_color="red",
            fill_alpha=0.4,
            xs=[10, 5, 5, 10, 15, 20, 20, 15],
            ys=[5, 10, 15, 20, 20, 15, 10, 5],
            xs_units='screen',
            ys_units='screen',
            visible=False,
            name="ds_indicator"
        )
        self.plot.add_layout(ds_indicator)

        # TODO: update this in bokeh 2.4 with range_change event
        range_js_cb = dims_jscode % config.ds_throttle
        self.plot.x_range.js_on_change('start', CustomJS(code=range_js_cb,
                                                         args=dict(plot=self.plot, dims=self.client_dims)))
        self.plot.y_range.js_on_change('start', CustomJS(code=range_js_cb,
                                                         args=dict(plot=self.plot, dims=self.client_dims)))
        self.plot.x_range.js_on_change('end', CustomJS(code=range_js_cb,
                                                       args=dict(plot=self.plot, dims=self.client_dims)))
        self.plot.y_range.js_on_change('end', CustomJS(code=range_js_cb,
                                                       args=dict(plot=self.plot, dims=self.client_dims)))

        self.img_glyphs: List[ImageGlyph] = list()
        if not use_rgba:
            if isinstance(initial_cbar, int):
                initial_cbar: str = list(color_bars.keys())[initial_cbar]  # Grab key name if initial_cbar is an int

            for name, c_bar in color_bars.items():
                img = self.plot.image(source=self.image_source, name='image',
                                      image='image', x='x', y='y', dw='dw', dh='dh',
                                      color_mapper=c_bar.color_mapper)
                self.img_glyphs.append(img)
                if name != initial_cbar:
                    img.visible = False
                    c_bar.visible = False
                self.plot.add_layout(c_bar, "right")
            self.color_bars = color_bars
        else:
            img = self.plot.image_rgba(source=self.image_source, name='image',
                                       image='image', x='x', y='y', dw='dw', dh='dh')
            self.img_glyphs.append(img)

        wz_tool = WheelZoomTool(zoom_on_axis=False, maintain_focus=False)
        h_tool = HoverTool(tooltips="@image ($x{%i}, $y{%i})",
                           formatters={"$x": "printf", "$y": "printf"},
                           renderers=[glyph for glyph in self.img_glyphs])
        self.plot.add_tools(wz_tool, h_tool)

        # this will not start the js_logic because it has not been loaded into the browser by now
        self.change_image(image_data, dw, dh)

        data = dict(width=[self.plot.width], height=[self.plot.height],
                    x_start=[0], x_end=[self.x_span],
                    y_start=[0], y_end=[self.y_span])
        self.client_dims.data = data  # so we take matters in our own hands and cheat a bit here

    def change_image(self,
                     image_data: np.ndarray,
                     dw: float,
                     dh: float
                     ) -> None:
        """
        Completely change image, including its axes and resetting the bounds.

        Args:
            image_data: 2-dimensional numpy-array containing image data.
            dw: Length of the x-axis.
            dh: Length of the y-axis.
        """
        self._set_reset_ranges(dw, dh)
        self.image_data = image_data

        if image_data.size > self.ds_downsample_images_threshold**2:
            self.downsample_flag = True
        else:
            self.downsample_flag = False
            data = dict(image=[image_data], x=[0], y=[0], dw=[dw], dh=[dh])
            self.image_source.stream(data, rollover=True)

        self.x_span = dw
        self.y_span = dh
        self.x_ratio = self.x_span / self.image_data.shape[1]
        self.y_ratio = self.y_span / self.image_data.shape[0]
        width, height = self._calc_width_height(self.x_span, self.y_span)

        # This is necessary to only update the plot and ranges if they would
        # actually change, since updating the plot and ranges with old values
        # would not cause a re-grid to happen (because no change was detected)
        if self.plot.width != width or self.plot.height != height or \
                self.plot.x_range.end != dw or self.plot.y_range.end != dh or \
                self.plot.x_range.start != 0 or self.plot.y_range.start != 0:
            self.plot.update(width=width, height=height)
            self.plot.x_range.update(start=0, end=self.x_span,
                                     bounds=(0, self.x_span))  # this will trigger update image
            self.plot.y_range.update(start=0, end=self.y_span, bounds=(0, self.y_span))

        # if old values are actually the same (for fully zoomed out images with same {x, y}-size)
        else:
            self.regrid_image(self.ds_threshold)

    def update_image(self, image_data: np.ndarray) -> None:
        """
        Only update the current frame, keep axes and bounds (think next image in image-series).

        Args:
            image_data: 2-dimensional numpy-array containing image data.
        """
        self.image_data = image_data
        if not self.downsample_flag:
            self.image_source.data.update(image=[image_data])
        self.regrid_image(self.ds_threshold)

    def regrid_image(self, threshold: int) -> None:
        """
        Regrid the image depending on the current zoom.

        This function checks if the current zoom-level of an image has more values than we want to display,
        as specified by the threshold².
        If there is too many values, we grid the data and aggregate(mean) just as much as we need to make it fit
        into the threshold bounds.
        If the amount of values is fine, e.g., zoomed in or small image, it will be displayed as is.

        Args:
            threshold: Threshold-value signifying up to what point to downsample and when to use the original image.

        Notes:
            As of bokeh-2.3.2 `threshold` should not be larger than 512 (512*512 allowed datapoints)
                because the browser will struggle with drawing that amount of glyphs onto a canvas.
        """

        if not self.downsample_flag:
            # downsampling for this image was disabled because the size
            # is smaller than ds_downsample_images_threshold**2
            return

        dims_data = self.client_dims.data
        if not dims_data['width'] or not dims_data['height']:
            return
        # Note: In the following code ss_{...} variables refer to screen-space
        #                             ds_{...} variables refer to data-space

        # using max&min to make sure the ranges are in bounds
        # (bokeh tends to allow -1.2e^12 even though the bounds are at 0)
        ss_x_start = max(dims_data['x_start'][0], 0)
        ss_y_start = max(dims_data['y_start'][0], 0)
        ss_x_end = min(dims_data['x_end'][0], self.x_span)
        ss_y_end = min(dims_data['y_end'][0], self.y_span)

        # clean up bokeh-noise,
        # e.g., fully zoomed out the x-range-start can be at 1.2e^12 (should be 0)
        ss_x_start = round(ss_x_start, 6)
        ss_y_start = round(ss_y_start, 6)
        ss_x_end = round(ss_x_end, 6)
        ss_y_end = round(ss_y_end, 6)

        # calculated padded (by max 1 element on each side)
        # data-space bounds for new image
        # padding is necessary to avoid gaps at the borders
        ds_x_start = int(ss_x_start / self.x_ratio)  # int interchangeable with math.floor
        ds_x_end = math.ceil(ss_x_end / self.x_ratio)
        ds_y_start = int(ss_y_start / self.y_ratio)
        ds_y_end = math.ceil(ss_y_end / self.y_ratio)

        # calculate offset for x- and y-start of the new image
        # necessary to avoid "jumpy" behaviour when panning
        # (without the offset the entirety of a pixel would always
        #  be in the screen, this allows partial pixels)
        ss_x_offset = ss_x_start % self.x_ratio
        ss_y_offset = ss_y_start % self.y_ratio
        ss_x_start -= ss_x_offset
        ss_y_start -= ss_y_offset

        # crop image_data to only contain (padded) data for the
        # current zoom state
        new_img = self.image_data[ds_y_start:ds_y_end,
                                  ds_x_start:ds_x_end]

        # data space spans
        ds_span_x_r = (ds_x_end - ds_x_start)
        ds_span_y_r = (ds_y_end - ds_y_start)
        # screen space spans
        ss_span_x_r = ds_span_x_r * self.x_ratio
        ss_span_y_r = ds_span_y_r * self.y_ratio

        data_points_on_x_axis = ds_span_x_r
        data_points_on_y_axis = ds_span_y_r
        # check if the cropped image has more data than we are allowed to display
        if data_points_on_x_axis * data_points_on_y_axis <= threshold ** 2:
            self.plot.select_one({'name': 'ds_indicator'}).visible = False
        else:
            self.plot.select_one({'name': 'ds_indicator'}).visible = True

            # frontend plot-size
            width = dims_data['width'][0]
            height = dims_data['height'][0]

            # calculate dimensions of down-sampled image

            # safeguard to ensure width+height are always >=1
            width = max(width, 1)
            height = max(height, 1)
            # capping size at threshold because that's the point of the threshold
            # capping size at data-points-amount because the down-sampled image cannot
            #   be bigger than the original (that would be up-sampling)
            width = min(width, threshold, data_points_on_x_axis)
            height = min(height, threshold, data_points_on_y_axis)

            new_img = downsample_2d_mean(new_img, (height, width), np.nan)

        new_data = dict(image=[new_img], x=[ss_x_start], y=[ss_y_start], dw=[ss_span_x_r], dh=[ss_span_y_r])
        self.image_source.stream(new_data, rollover=True)

    def _calc_width_height(self,
                           sx: float,
                           sy: float
                           ) -> Tuple[float, float]:
        """
        Calculate the width and height of the image-plot.

        It is tried to keep the original x/y-ratio. However, if any
        of the {MIN, MAX}x{WIDTH, HEIGHT} constraints would be violated,
        the ratio is changed to fit into these constraints.

        Finally, a margin to accommodate other image-plot elements,
        like the ColorBar are added (without the margin they would
        change the ratio),

        Args:
            sx: Length of the x-axis.
            sy: Length of the y-axis.

        Returns:
            A (width, height)-tuple.
        """
        ratio = sx / sy

        min_allowed_ratio = self.MIN_WIDTH / self.MAX_HEIGHT
        max_allowed_ratio = self.MAX_WIDTH / self.MIN_HEIGHT

        if ratio <= min_allowed_ratio:  # rect is more "portrait" than bounds allow
            height = self.MAX_HEIGHT
            width = self.MIN_WIDTH

        elif ratio >= max_allowed_ratio:  # rect is more "landscape" than bounds allow
            height = self.MIN_HEIGHT
            width = self.MAX_WIDTH

        else:  # goal ratio is displayable without violating min/max bounds
            height = self.PREF_HEIGHT
            width = int(height * ratio)
            # if height was guessed too wrong we correct the bounds
            if width > self.MAX_WIDTH:
                width = self.MAX_WIDTH
                height = int(self.MAX_WIDTH / ratio)
            elif width < self.MIN_WIDTH:
                width = self.MIN_WIDTH
                height = int(self.MIN_WIDTH / ratio)

        #  Add borders to accommodate outer layout parts
        return width + 3 * self.MIN_BORDER, height + 2 * self.MIN_BORDER

    def _set_reset_ranges(self, x_end, y_end):
        """
        Reset the reset range of the plot's {x, y}-range. Necessary to make sure the reset-tool works properly.
        """
        self.plot.x_range.update(reset_start=0, reset_end=x_end)
        self.plot.y_range.update(reset_start=0, reset_end=y_end)
