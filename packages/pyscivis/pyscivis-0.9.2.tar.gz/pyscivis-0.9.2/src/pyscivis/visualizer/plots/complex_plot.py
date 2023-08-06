import math
from typing import Optional

from bokeh.models import LayoutDOM
from pyscivis.visualizer.dataclasses.config import ImageConfig
from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.dataclasses.state import State
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv

from . import ImagePlot
from .components import ValueRadios


class ComplexPlot(ImagePlot):
    """
    Creates the visualization plots for acquisitions, organizes callbacks of components and keeps everything updated.
    """

    def __init__(self,
                 data: ParsedData,
                 config: ImageConfig,
                 loading_indicator: Optional[LoadingDiv] = None,
                 title: str = ""
                 ) -> None:
        """
        Call constructor of Superclass and initialize value-handler controls.

        Args:
            data: Parsed acquisition data.
            config: Configuration settings for plots displayed by this class.
            loading_indicator: None in notebook, LoadingDiv in standalone, used to print messages in the Loading-screen.
        """
        super().__init__(data, config, loading_indicator=loading_indicator, title=title)
        if loading_indicator is not None:
            loading_indicator.set_text("Setting up complex-value toggles...")
        vk = config.initial_value_kind
        self.value_controls = ValueRadios(self.on_value_change, vk)
        if self.handler.value_handler != self.value_controls.active_handler:
            self.on_value_change()

    def get_layout(self) -> LayoutDOM:
        """
        Compile all plots and controls into one LayoutDOM.

        Returns:
            LayoutDOM containing multiple layouts.
        """
        layout = super().get_layout()
        layout.select_one({"name": "col_left"}).children.insert(-1, self.value_controls.layout)

        return layout

    def set_state(self, state: State) -> None:
        """
        Set the state of the currently displayed app from a specified State object.

        Most state information is set by calling the superclass' `set_state`.
        Here, only the state of the value-controls is set.

        Args:
            state: State to be set.
        """
        self.value_controls.set_state(state.value_kind)
        super().set_state(state)

    def get_state(self) -> State:
        """
        Get the state of the currently displayed app.

        Most state information is retrieved by calling the superclass' `get_state`.
        Here, only the state of the value-controls are retrieved.

        Returns:
            A State object.
        """
        state: State = super().get_state()
        state.value_kind = self.value_controls.get_state()
        return state

    def on_value_change(self) -> None:
        """
        This method updates most figures when the value-handler controls were changed.
        """
        self.handler.value_handler = self.value_controls.active_handler
        new_image = self._get_data()
        min_, max_ = self._get_min_max()
        self.img.update_image(new_image)
        self.palette_sliders.reset_window_sliders(min_, max_)
        sel_vals = self.img.get_selected_values()
        self.histogram.update_min_max(min_, max_)
        self.histogram.update(new_image, sel_vals)
        self.statistics.update(sel_vals)
        self.profile_figure.update_y_bounds(min_, max_)
        self.profile_figure.update()

        if math.isnan(min_) or math.isnan(max_):
            min_ = max_ = 0
        for cm in self.color_mappers:
            cm.update(low=min_, high=max_)
