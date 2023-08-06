from functools import partial
import threading
from typing import Optional

import numpy as np
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, glyphs, Label, WheelZoomTool
from bokeh.plotting import figure

delayed_cb: Optional[threading.Timer] = None


class HistogramFigure:
    """
    Manages the creation of a histogram-figure and its bounds.
    """
    def __init__(self,
                 data: np.ndarray,
                 min_: float,
                 max_: float,
                 bins: int = 20,
                 max_calc_size: int = 4000*4000,  # 16kk ~= 0.5s calculation @ i7-3770,
                 enable_dynamic_rebinning: bool = True
                 ) -> None:
        """
        Set up the figure and its initial two histogram-glyphs with placeholder data.

        Args:
            data: N-dimensional numpy-array containing data to be binned into a histogram.
            min_: Minimum of the data, used to calculate x-range start.
            max_: Maximum of the data, used to calculate x-range end.
            bins: Amount of histogram bins.
            max_calc_size: Threshold of when not to calculate a histogram anymore.
            enable_dynamic_rebinning: Whether to automatically rebin the histogram if zoomed in/out or panned.
        """

        # we need min_max as parameters because the Histogram only has access to 1 frame which
        # is not enough for min_max because we want min_max to be constant for an entire image-series

        self.min_max = (0., 1.)
        self.max_calc_size = max_calc_size
        self.bins = bins

        tooltip = [
            ("amount", "@top")
        ]

        fig = figure(tools=["hover,reset,pan,box_zoom"], toolbar_location="left", tooltips=tooltip,
                     plot_height=200, sizing_mode="stretch_width", x_range=(0, 1),
                     y_range=(1e-1, 2*data.size), y_axis_type="log", y_axis_location="right",
                     min_border=10, css_classes=["histogram-figure"])
        wztool = WheelZoomTool(maintain_focus=False, dimensions="width")
        fig.add_tools(wztool)

        fig.toolbar.active_scroll = wztool
        fig.toolbar.active_drag = "auto"
        fig.toolbar.logo = None

        fig.y_range.bounds = (1e-1, 2*data.size)
        self.h_main: glyphs.Quad = fig.quad(bottom=1, left=[1], right=[1], top=[1],
                                            color="white", line_color="#3A5785", visible=False)
        self.h_selected: glyphs.Quad = fig.quad(bottom=1, left=[1], right=[1], top=[1],
                                                alpha=0.5, color="#3A5785", line_color=None, visible=False)

        self.no_display = Label(x=fig.width/2, y=fig.height/2, x_units="screen", y_units="screen",
                                text=f"Selection size is bigger than threshold of {max_calc_size}",
                                render_mode="css", border_line_color="darkgrey", border_line_alpha=1.0,
                                background_fill_color="white", background_fill_alpha=1.0,
                                text_align="center")

        fig.add_layout(self.no_display, place="center")

        fig.hover.renderers = [self.h_selected]
        fig.hover.mode = "vline"

        fig.xgrid.grid_line_color = None
        fig.yaxis.major_label_orientation = np.pi / 6
        fig.background_fill_color = "#fafafa"

        self.cur_data = [data, data]  # all, selection
        self.cur_bins = bins

        self.fig = fig
        self.layout = fig

        self.update_min_max(min_, max_)
        self.update(data, data)
        if enable_dynamic_rebinning:
            self._attach_range_events()

    def update(self,
               entire_img: np.ndarray,
               selection: np.ndarray
               ) -> None:
        """
        Update both histogram-glyphs with supplied data.

        Args:
            entire_img: N-dimensional numpy-array for the main-histogram-glyph.
            selection: N-dimensional numpy-array for the selected-histogram-glyph.
        """
        self.cur_data = [entire_img, selection]

        if entire_img.size*2 != self.fig.y_range.end:
            self.fig.y_range.end = entire_img.size*2
            self.fig.y_range.bounds = (1e-1, entire_img.size*2)

        if selection.size > self.max_calc_size:
            self.h_main.visible = False
            self.h_selected.visible = False
            self.no_display.visible = True
            return

        self.h_selected.visible = True
        self.no_display.visible = False

        sel_ds: ColumnDataSource = self.h_selected.data_source.data
        main_ds: ColumnDataSource = self.h_main.data_source.data

        x_start, x_end = self.fig.x_range.start, self.fig.x_range.end

        if entire_img.size > self.max_calc_size:
            self.h_main.visible = False
            selected_vals = selection.ravel()

            hist_selected, hedges = self.filtered_histogram(x_start, x_end, selected_vals, range=self.min_max, bins=self.cur_bins)

            # Need this here to avoid a delay in updates between all & selected
            sel_ds.update(left=hedges[:-1], right=hedges[1:], top=hist_selected)

        else:
            self.h_main.visible = True

            all_vals = entire_img.ravel()
            hist_all, hedges = self.filtered_histogram(x_start, x_end, all_vals, range=self.min_max, bins=self.cur_bins)

            if entire_img.shape == selection.shape:
                sel_ds.update(left=hedges[:-1], right=hedges[1:], top=hist_all)
                main_ds.update(left=hedges[:-1], right=hedges[1:], top=hist_all)
            else:
                selected_vals = np.array(selection).ravel()

                hist_selected, _ = self.filtered_histogram(x_start, x_end, selected_vals, range=self.min_max, bins=self.cur_bins)
                sel_ds.update(left=hedges[:-1], right=hedges[1:], top=hist_selected)
                main_ds.update(left=hedges[:-1], right=hedges[1:], top=hist_all)
                # Need this here to avoid a delay in updates between all & selected

    def update_selection(self, selection: np.ndarray) -> None:
        """
        Update only the selected-histogram-glyph.

        Args:
            selection:  N-dimensional numpy-array for the selected-histogram-glyph.
        """
        self.cur_data[1] = selection

        if selection.size > self.max_calc_size:
            self.h_selected.visible = False
            self.no_display.visible = True
            return

        vals = selection.ravel()
        hhist, hedges = np.histogram(vals, range=self.min_max, bins=self.cur_bins)
        sel_cds: ColumnDataSource = self.h_selected.data_source.data
        sel_cds.update(left=hedges[:-1], right=hedges[1:], top=hhist)
        self.h_selected.visible = True
        self.no_display.visible = False

    def update_min_max(self,
                       min_: float,
                       max_: float
                       ) -> None:
        """
        Update the bounds of the histogram plot and the range for future histogram calculations.

        Args:
            min_: Start value.
            max_: End value.
        """

        if np.isnan(min_) or np.isnan(max_) or min_ == 0 and max_ == 0:
            min_ = 0
            max_ = 1

        self.min_max = (min_, max_)
        pad = 0.1 * (max_ - min_)
        self.layout.x_range.update(start=min_-pad,
                                   end=max_+pad,
                                   bounds=(min_-pad, max_+pad),
                                   reset_start=min_-pad,
                                   reset_end=max_+pad)

    @staticmethod
    def filtered_histogram(start, end, *args, **kwargs):
        """
        Filters the edges and histogram-values to be within the specified start-end range.

        Useful for limiting the amount of drawn glyphs to the visible area.

        Args:
            start: Value before which the histogram is cut off.
            end: Value after which the histogram is cut off.
            *args: Arguments passed on to `np.histogram`.
            **kwargs: Keyword-arguments passed on to `np.histogram`.

        Returns:
            Tuple containing histogram heights and the edges (exactly like `np.histogram`).
        """
        hist, edges = np.histogram(*args, **kwargs)

        left_edges = edges[:-1]
        right_edges = edges[1:]
        # this does include the leftmost partial rect but not
        # the rightmost one
        mask = (start <= right_edges) & (left_edges < end)
        # so we find the rightmost edge here and set it to visible
        idx_shown = np.argmax(mask)  # find idx of first shown edge
        true_onwards = mask[idx_shown:]
        if all(true_onwards):
            mask = np.insert(mask, -1, True)  # make it visible
        else:
            idx_first_false = np.argmin(true_onwards)  # find idx of first non-visible edge
            mask = np.insert(mask, idx_first_false, True)  # make it visible

        #print(idx_first_false)

        valid_edges = edges[mask]
        valid_hist = hist[mask[:-1]]

        # if the last element gets filtered we need to remove the last histogram value
        if not mask[-1]:
            valid_hist = valid_hist[:-1]

        return valid_hist, valid_edges

    def _attach_range_events(self):
        """
        Attach a throttled callback listening to changes in the figure's x-range and rebinning if necessary.
        """
        # cur_zoom_level = self.min_max[1] - self.min_max[0]

        self.fig.x_range.on_change("start", lambda attr, old, new: self._range_change_throttled())
        self.fig.x_range.on_change("end", lambda attr, old, new: self._range_change_throttled())

    def _range_change_throttled(self):
        timeout = 0.01  # 10ms
        global delayed_cb
        if delayed_cb is not None:
            delayed_cb.cancel()
        threaded_rebin = partial(curdoc().add_next_tick_callback, self.rebin_histogram)
        delayed_cb = threading.Timer(timeout, threaded_rebin)
        delayed_cb.start()

    def rebin_histogram(self):
        # TODO: Possible improvement: Differentiate between zoom and pan, for pan don't recalc the histogram
        # nonlocal cur_zoom_level
        # self.min_max = start, end
        start, end = self.fig.x_range.start, self.fig.x_range.end
        new_x_width = end - start
        # if new_x_width == cur_zoom_level: #math.isclose(cur_range, cur_zoom_level, abs_tol=0):
        #     print("%s and %s are close" % (new_x_width, cur_zoom_level))
        #     return
        # print("%s and %s are not close" % (new_x_width, cur_zoom_level))
        orig_x_width = self.min_max[1] - self.min_max[0]
        self.cur_bins = round(orig_x_width / new_x_width * self.bins)
        self.update(*self.cur_data)
