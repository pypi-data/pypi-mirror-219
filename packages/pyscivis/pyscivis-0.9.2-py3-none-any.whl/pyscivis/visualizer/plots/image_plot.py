from typing import List, Tuple, Optional

import numpy as np
from bokeh.document import Document
from bokeh.layouts import column, row
from bokeh.models import LinearColorMapper, ColorBar, Panel, Tabs, LayoutDOM, Spacer
from bokeh.models.widgets import Toggle, RadioButtonGroup

from pyscivis.visualizer.dataclasses.config import ImageConfig
from pyscivis.visualizer.dataclasses.state import State
from pyscivis.visualizer.plots.base_plot import BasePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv
from pyscivis.visualizer.plots.components.state import StateFigure
from pyscivis.visualizer.util import create_palettes
from pyscivis.visualizer.plots.dimension_handler import DimensionHandler
from pyscivis.visualizer.plots.components import ImageFigure, HistogramFigure, DimensionControls, PaletteControls, \
    StatisticsFigure, ProfileFigure
from pyscivis.visualizer.models import OffsetLogColorMapper, OffsetLogTickFormatter
from pyscivis.visualizer.dataclasses.parser import ParsedData


class ImagePlot(BasePlot):
    """
    Creates the visualization plots for images, organizes callbacks of components and keeps everything updated.
    """

    def __init__(self,
                 data: ParsedData,
                 config: ImageConfig,
                 use_rgba: bool = False,
                 loading_indicator: Optional[LoadingDiv] = None,
                 title: str = ""
                 ) -> None:
        """
        Set up all figures and plots using the specified configuration object.

        Args:
            data: Parsed images data.
            config: Configuration settings for plots displayed by this class.
            use_rgba: If True an 'image_rgba'-glyph will be used instead of an 'image'-glyph, also disabled palettes.
            loading_indicator: None in notebook, LoadingDiv in standalone, used to print messages in the Loading-screen.
        """
        self.document: Optional[Document] = None  # Only used by the notebook for "add_next_tick_callback"
        # Flipping the np-data array along the y-axis
        data.data = data.data[..., ::-1, ::]
        self.handler = DimensionHandler(data, config.preload_bounds, loading_indicator=loading_indicator)

        if loading_indicator is not None:
            loading_indicator.set_text("Setting up widgets...")

        img_data = self._get_data()  # Initial 2D image data

        # "Fit to frame" toggle #
        self.fit_to_frame_toggle = Toggle(label="Fit bounds to frame", css_classes=["fit-to-frame-toggle"])
        self.fit_to_frame_toggle.on_click(lambda x: self.on_fit_to_frame_click())

        # Axis sliders and changers #
        self.dim_controls = DimensionControls(self.handler.dims, self.on_dim_change, self.on_axes_change)

        _min, _max = self._get_min_max()

        # Create palettes #
        palette_size = config.palette_size
        name_func_map = dict(zip(config.palette_names, config.palette_funcs))
        palette_map = create_palettes(palette_size, name_func_map)

        # ColorBars #
        color_bars = dict()
        initial_palette = palette_map[config.initial_palette][config.initial_palette_size-1]

        # Linear ColorBar #
        if np.isnan(_min) or np.isnan(_max):
            low = high = 0
        else:
            low = _min
            high = _max
        lin_cm = LinearColorMapper(palette=initial_palette, low=low, high=high)
        lin_cb = ColorBar(color_mapper=lin_cm)
        color_bars["Linear"] = lin_cb

        # Logarithmic ColorBar #
        ls = config.log_span
        log_cm = OffsetLogColorMapper(palette=initial_palette, log_span=ls, low=low, high=high)
        log_tf = OffsetLogTickFormatter(log_span=ls, low=low, high=high)

        def link_to_tf(attr, old, new):
            setattr(log_tf, attr, new)

        log_cm.on_change("low", link_to_tf)  # making sure that the custom Log models are synchronized
        log_cm.on_change("high", link_to_tf)
        log_cb = ColorBar(color_mapper=log_cm, formatter=log_tf)
        color_bars["Log"] = log_cb

        # Creating a ColorBar chooser #
        color_bar_keys: List[str] = list(color_bars.keys())
        initial_cm_index: int = color_bar_keys.index(config.initial_color_mapper)
        if not use_rgba:
            self.cbar_radios = RadioButtonGroup(labels=color_bar_keys, active=initial_cm_index, css_classes=["cbar-radios"])
            self.cbar_radios.on_click(lambda x: self.img.change_cbar(x))
        else:
            self.cbar_radios = Spacer()

        # Grabbing ordered list of cm-references for later use #
        self.color_mappers = [cb.color_mapper for cb in color_bars.values()]

        # Getting metadata of starting image #
        metadata = self.handler.get_metadata()
        dw = metadata.x.length
        dh = metadata.y.length
        x_unit = metadata.x.unit
        y_unit = metadata.y.unit

        # Create Image&State tabs #
        self.img = ImageFigure(self.on_selection_change, self.on_tap, img_data,
                               dw, dh, color_bars, initial_cm_index, use_rgba, config, title)

        self.img.plot.xaxis.axis_label = f"{metadata.x.name} ({x_unit})"
        self.img.plot.yaxis.axis_label = f"{metadata.y.name} ({y_unit})"

        image_tab = Panel(child=self.img.layout, title="Image")
        state_tab = Panel(child=StateFigure(config.format_state,
                                            self.set_state,
                                            self.get_state),
                          title="State")
        self.main_tabs = Tabs(tabs=[image_tab, state_tab])

        # Initialising remaining components #
        self.palette_sliders = PaletteControls(self.color_mappers, palette_map, palette_size, config.initial_palette,
                                               _min, _max, width=200, height=200, sizing_mode="stretch_width")
        self.histogram = HistogramFigure(img_data, _min, _max,
                                         bins=config.histogram_bins, max_calc_size=config.max_calc_size)
        self.statistics = StatisticsFigure(img_data, metadata, max_calc_size=config.max_calc_size,
                                           sizing_mode="stretch_width", margin=(25, 0, 0, 0))
        self.profile_figure = ProfileFigure(self.handler, _min, _max)

    def get_layout(self) -> LayoutDOM:
        """
        Compile all plots and controls into one LayoutDOM.

        Returns:
            LayoutDOM containing multiple layouts.
        """
        c_b = column(self.dim_controls.slider_layout, self.histogram.layout, sizing_mode="stretch_width", name="col_bottom")
        c = column(self.main_tabs, c_b)
        c_l = column(self.palette_sliders.layout, self.fit_to_frame_toggle, self.cbar_radios,
                     self.dim_controls.axis_select_layout, self.statistics.layout, name="col_left")
        c_r = column(self.profile_figure.layout, name="col_right")
        ro = row(c_l, c, c_r)
        return ro

    def set_state(self, state: State) -> None:
        """
        Set the state of the currently displayed app.

        Args:
            state: A State object.
        """
        self.dim_controls.set_state(state.dimension)
        self.img.set_state(state.image)
        self.profile_figure.set_state(state.profile)
        self.fit_to_frame_toggle.active = state.fit_to_frame
        self.palette_sliders.set_state(state.palette)
        self.cbar_radios.active = state.active_color_mapper

    def get_state(self) -> State:
        """
        Get the state of the currently displayed app.

        Returns:
            A State object.
        """
        dims = self.dim_controls.get_state()
        img = self.img.get_state()
        palette = self.palette_sliders.get_state()
        profile = self.profile_figure.get_state()
        fit_to_frame = self.fit_to_frame_toggle.active
        color_mapper = self.cbar_radios.active

        state = State(dimension=dims, image=img, profile=profile, palette=palette,
                      fit_to_frame=fit_to_frame, active_color_mapper=color_mapper)
        return state

    def on_tap(self,
               x: int,
               y: int
               ) -> None:
        """
        Update profiles-figures on tap.

        Note:
            This is a callback function called only from an Image object.

        Args:
            x: X-coordinate of the click in data-space.
            y: Y-coordinate of the click in data-space.
        """
        self.profile_figure.set_coordinates(x, y)
        self.img.set_crosshair(x, y)

    def on_fit_to_frame_click(self) -> None:
        """
        Fit or unfit current frame depending on if the button was toggled on or off.

        Note:
            This is a callback function called if fit_to_frame_toggle was clicked.
        """
        self.fit()

    def on_dim_change(self,
                      dim_index: int,
                      new: int
                      ) -> None:
        """
        Update figures if dimension values were changed.

        Note:
            This is a callback function called only from a DimensionControls object.

        Args:
            dim_index: Index of Dimension that was changed.
            new: New value for dimension.
        """
        self.handler.set_dim_value(dim_index, new)
        new_image = self._get_data()
        self.img.update_image(new_image)

        sel_vals = self.img.get_selected_values()

        if self.fit_to_frame_toggle.active:
            self.fit()

        self.histogram.update(new_image, sel_vals)
        self.statistics.update(sel_vals)
        self.profile_figure.update()

    def on_axes_change(self,
                       x_axis: int,
                       y_axis: int
                       ) -> None:
        """
        Update figures if axes were changed.

        Note:
            This is a callback function called only from a DimensionControls object.

        Args:
            x_axis: Index of the new x-axis.
            y_axis: Index of the new y-axis.
        """
        self.handler.change_axes(x_axis, y_axis)

        # get metadata of new axes
        metadata = self.handler.get_metadata()
        new_image = self._get_data()
        dw = metadata.x.length
        dh = metadata.y.length
        x_unit = metadata.x.unit
        y_unit = metadata.y.unit

        self.img.change_image(new_image, dw, dh)

        self.img.plot.xaxis.axis_label = f"{metadata.x.name} ({x_unit})"
        self.img.plot.yaxis.axis_label = f"{metadata.y.name} ({y_unit})"

        self.img.reset_selection()

        sel_vals = self.img.get_selected_values()

        if self.fit_to_frame_toggle.active:
            self.fit()

        self.histogram.update(new_image, sel_vals)
        self.statistics.update(sel_vals, metadata)

        self.profile_figure.update_from_axis_change()

    def on_selection_change(self) -> None:
        """
        Updates the histogram and statistics if the ROI changed.

        Note:
            This is a callback function called only from an Images object.
        """
        if self.dim_controls.animated_dimension is None:
            sel_vals = self.img.get_selected_values()
            self.histogram.update_selection(sel_vals)
            self.statistics.update(sel_vals)

    def fit(self) -> None:
        """
        Fit the various ranges to global or local min-max, depending on fit-to-frame-toggle.

        If fit-to-frame is active/pushed down use the local, else if it is inactive/pushed out use the global min-max.
        This method is called when the image changes, or the toggle is pressed.
        """
        # TODO: Maybe keep sliders at "fitted" interval on unfitting from frame? Possible QoL-Improvement
        min_, max_ = self._get_min_max()
        self.histogram.update_min_max(min_, max_)
        data = self.handler.get_data()
        selected = self.img.get_selected_values()
        self.histogram.update(data, selected)
        self.profile_figure.update_y_bounds(min_, max_)
        self.palette_sliders.reset_window_sliders(min_, max_)

        if np.isnan(min_) or np.isnan(max_):
            min_ = max_ = 0
        for cm in self.color_mappers:
            cm.update(low=min_, high=max_)

    def _get_data(self) -> np.ndarray:
        """ Just a shorthand. """
        return self.handler.get_data()

    def _get_min_max(self) -> Tuple[float, float]:
        """ Get global or local (min, max)-tuple depending on the fit-to-frame-toggle. """
        if self.fit_to_frame_toggle.active:
            return self.handler.get_local_min_max()
        else:
            return self.handler.get_data_min_max()

