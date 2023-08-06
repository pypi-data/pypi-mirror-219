import math
from typing import Any, Callable, TypedDict, Sequence

import numpy as np
from bokeh.models import BoxEditTool, ColumnDataSource, TapTool, CustomJS
from attr import asdict
from pyscivis.visualizer.dataclasses.state import ImageState, RangeState, ROIState
from pyscivis.visualizer.plots.components.crosshair import Crosshair

from .griddable_image import GriddableImage


class Point(TypedDict):
    x: Sequence[float]  # always length 1
    y: Sequence[float]


class ROI(TypedDict):
    x: Sequence[float]
    y: Sequence[float]
    width: Sequence[float]
    height: Sequence[float]


class ImageFigure(GriddableImage):
    """
    Takes care of mostly non-image related stuff on the images-plot, like managing the ROI and taps.
    """

    def __init__(self,
                 selection_callback: Callable[[], None],
                 tap_callback: Callable[[int, int], None],
                 *args: Any
                 ) -> None:
        """
        Set up the ROI, including its shadow-overlay and tool and the tap-tool.

        Args:
            selection_callback: Callable to be fired when the selection changes.
            tap_callback: Callable to be fired when a tap-event happens.
            *args: Image-related arguments passed onto the GriddableImage parent class.
        """
        super().__init__(*args)  # Create the actual image

        self.selected_src = ColumnDataSource(data=dict(selected=[]))
        self.img_shadow = self.plot.multi_polygons(color=['grey'], alpha=0.4)
        self.roi_renderer = self.plot.rect('x', 'y', 'width', 'height',
                                           source=ColumnDataSource(data=dict(x=[], y=[], width=[], height=[])),
                                           fill_alpha=0.0)

        self.roi_renderer.data_source.on_change("data", lambda attr, old, new:
                                                self.notify_selection_change(new, selection_callback))

        self._crosshair = Crosshair()
        self.plot.add_layout(self._crosshair.x_line)
        self.plot.add_layout(self._crosshair.y_line)

        self.be_tool = BoxEditTool(num_objects=1, renderers=[self.roi_renderer])
        # taptool = p.select(type=TapTool) for refactoring

        self.plot.add_tools(self.be_tool, TapTool())

        self._init_tap_tool_hack(tap_callback)
        self.layout = self.plot

    def set_state(self, state: ImageState) -> None:
        """
        Set the state of the plot and ROI.

        Args:
            state: A ImageState object.
        """
        self.plot.x_range.update(**asdict(state.x_range))
        self.plot.y_range.update(**asdict(state.y_range))
        self.roi_renderer.data_source.data = asdict(state.roi)

    def get_state(self) -> ImageState:
        """
        Get the ImageState including the current plot ranges and ROI-bounds.

        Returns:
            A ImageState object.
        """
        x_r = self.plot.x_range
        y_r = self.plot.y_range

        x_range = RangeState(start=x_r.start, end=x_r.end, bounds=x_r.bounds)
        y_range = RangeState(start=y_r.start, end=y_r.end, bounds=y_r.bounds)
        roi = ROIState(**self.roi_renderer.data_source.data)
        state = ImageState(x_range=x_range, y_range=y_range, roi=roi)
        return state

    def change_cbar(self, index: int) -> None:
        """
        Make the specified ColorBar visible, hide all others.

        Args:
            index: Index of ColorBar to be made visible.
        """
        for idx, cbar in enumerate(self.color_bars.values()):
            if idx == index:
                self.img_glyphs[idx].visible = True
                cbar.visible = True
            else:
                self.img_glyphs[idx].visible = False
                cbar.visible = False

    def set_crosshair(self,
                      ds_x: int,
                      ds_y: int
                      ) -> None:
        """
        Set crosshair coordinates.

        This function calculates screen-space coordinates for the supplied data-space coordinates and centers them
        on the specified pixel.

        Args:
            ds_x: Data-space X-coordinate.
            ds_y: Data-space Y-coordinate.
        """
        ss_x = (ds_x+0.5) * self.x_ratio
        ss_y = (ds_y+0.5) * self.y_ratio
        self._crosshair.toggle_visible(True)
        self._crosshair.set_coordinates(ss_x, ss_y)

    def notify_tap(self,
                   point: Point,
                   tap_callback: Callable[[int, int], None]
                   ) -> None:
        """
        Calculate screen-space to data-space coordinates and notify of tap.

        Args:
            point: Point containing x- and y-coordinates.
            tap_callback: Callable accepts x- and y-coordinates.
        """
        x = int(point['x'][0] / self.x_ratio)
        y = int(point['y'][0] / self.y_ratio)
        tap_callback(x, y)

    def notify_selection_change(self,
                                bounds: ROI,
                                selection_callback: Callable[[], None]
                                ) -> None:
        """
        Adjust the shadow-overlay of the ROI and notify the parent.

        Args:
            bounds: New ROI bounds.
            selection_callback: Callable fired on selection change.
        """
        self._adjust_roi_shadow_overlay(bounds)
        selection_callback()

    def reset_selection(self) -> None:
        """
        Delete the ROI.
        """
        self.roi_renderer.data_source.data = dict(x=[], y=[], width=[], height=[])
        # roi_renderer DS change will automatically trigger notify_selection_change/shadow adjustments

    def get_selected_values(self) -> np.ndarray:
        """
        Calculates the values that are inside the ROI.

        Returns:
            A 2-dimensional numpy-array containing the sliced image.
        """
        src_img = self.image_data
        if not self.roi_renderer.data_source.data['x']:
            return src_img
        else:
            # roi_renderer contains possibly stretched coordinates
            # (due to a pixel resembling more/less than 1 length-unit)
            bounds_stretched = self.roi_renderer.data_source.data

            # need to convert image-space to pixel-space
            x_0 = bounds_stretched['x'][0] / self.x_ratio
            width = bounds_stretched['width'][0] / self.x_ratio
            y_0 = bounds_stretched['y'][0]
            height = bounds_stretched['height'][0]

            x_start = math.floor(x_0 - 0.5*width)
            x_end = math.ceil(x_0 + 0.5*width)
            y_start = math.floor(y_0 - 0.5*height)
            y_end = math.ceil(y_0 + 0.5*height)

            if x_start < 0:
                x_start = 0
            if y_start < 0:
                y_start = 0
            # *_end does not matter as slicing already handles "index-out-range"-upper limits gracefully

            return src_img[y_start:y_end, x_start:x_end]

    def _adjust_roi_shadow_overlay(self, roi_bounds: ROI):
        """ Adjust the shadow-overlay of the ROI (everything outside the rectangle). """
        data = dict(self.img_shadow.data_source.data)
        # reset polygon bounds
        data['xs'] = [[[]]]
        data['ys'] = [[[]]]

        # if roi was not deleted (has a height)
        if roi_bounds['height']:
            img_poly_xs = [0, self.x_span, self.x_span, 0]
            img_poly_ys = [0, 0, self.y_span, self.y_span]

            x_start = roi_bounds['x'][0] - 0.5 * roi_bounds['width'][0]
            x_end = roi_bounds['x'][0] + 0.5 * roi_bounds['width'][0]
            y_start = roi_bounds['y'][0] - 0.5 * roi_bounds['height'][0]
            y_end = roi_bounds['y'][0] + 0.5 * roi_bounds['height'][0]
            hole_xs = [x_start, x_end, x_end, x_start]
            hole_ys = [y_start, y_start, y_end, y_end]
            data['xs'][0][0].extend((img_poly_xs, hole_xs))
            data['ys'][0][0].extend((img_poly_ys, hole_ys))
            self.img_shadow.visible = True

        else:  # roi deleted
            # necessary hack to not reset fill_color
            data['xs'][0][0].append([0])
            data['ys'][0][0].append([0])
            self.img_shadow.visible = False

        self.img_shadow.data_source.data = dict(data)

    def _init_tap_tool_hack(self, tap_callback: Callable[[int, int], None]) -> None:
        """ Make taps only be propagated if the tap-tool is active (and the taps are in bounds). """
        tap_tool_toggle = ColumnDataSource(data=dict())
        callback = CustomJS(args=dict(tt=self.plot.select(type=TapTool)[0], source=tap_tool_toggle,
                                      x_range=self.plot.x_range, y_range=self.plot.y_range),
                            code="""
            // check if taptool is active            
            if (!tt.active)
                return
            var x = cb_obj.x
            var y = cb_obj.y
            // check if click was inside image
            if (x < x_range.start || x >= x_range.end)
                return
            if (y < y_range.start || y >= y_range.end)
                return
            var data = {'x': [x], 'y': [y]}
            source.data = data
        """)
        self.plot.js_on_event("tap", callback)
        # deactivated because it interferes with the box-edit-tool double-taps
        # self.plot.on_event("doubletap", lambda x: self._crosshair.toggle_visible())
        tap_tool_toggle.on_change('data', lambda attr, old, new: self.notify_tap(new, tap_callback))
