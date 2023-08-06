from typing import Any, Sequence, Tuple, Dict, Optional

import numpy as np

from bokeh.layouts import column
from bokeh.models import Select, Slider, RangeSlider, ColorMapper
from bokeh.models.formatters import BasicTickFormatter
from pyscivis.visualizer.dataclasses.state import PaletteState

Palette = Tuple[str]


class PaletteControls:
    """
    Wraps all palette-related controls and their callbacks.
    """

    def __init__(self,
                 color_mappers: Sequence[ColorMapper],
                 palette_map: Dict[str, Sequence[Palette]],
                 palette_size: int,
                 initial_palette: str,
                 min_: float,
                 max_: float,
                 **kwargs: Any
                 ) -> None:
        """
        Set up all controls and their callbacks.

        Args:
            color_mappers: Sequence of ColorMapper to be manipulated.
            palette_map: Dictionary mapping palette names to Sequence of palettes.
            palette_size: Maximal palette size.
            initial_palette: Name of the initial palette.
            min_: Minimum of data.
            max_: Maximum of data.
            **kwargs: Keywords passed onto the LayoutDOM containing the controls.
        """
        same_min_max_flag = False
        if min_ == max_ or np.isnan(min_) or np.isnan(max_):
            same_min_max_flag = True
            min_ = 0
            max_ = 1

        sorted_keys = sorted(palette_map.keys())

        self.palette = Select(title='Palette', value=initial_palette,
                              options=sorted_keys, sizing_mode="stretch_width",
                              css_classes=["palette-select"])

        self.palette_length = Slider(title="Palette-size", start=1,
                                     end=palette_size, value=palette_size, step=1, sizing_mode="stretch_width",
                                     css_classes=["palette-size"])

        self.palette_window = RangeSlider(title="Palette-window", start=min_, end=max_, format=BasicTickFormatter(),
                                          value=(min_, max_), step=0, sizing_mode="stretch_width",
                                          css_classes=["palette-window"], disabled=True)

        self.palette_cutoff = RangeSlider(title="Window", start=min_, end=max_, format=BasicTickFormatter(),
                                          value=(min_, max_), step=0, sizing_mode="stretch_width",
                                          css_classes=["palette-slider"], disabled=True)

        self.layout = column(self.palette, self.palette_length, self.palette_window, self.palette_cutoff,
                             **kwargs, css_classes=["palette"])

        def _palette_cb(attr: Any,
                        old: Any,
                        new: Any
                        ) -> None:
            """Change palette on name, size and cutoff change."""
            # select palette kind
            full_palette = list(palette_map[self.palette.value][self.palette_length.value-1])
            # calculate the cutoff-window
            dist = self.palette_cutoff.end - self.palette_cutoff.start
            dist_front = self.palette_cutoff.value[0] - self.palette_cutoff.start
            dist_back = self.palette_cutoff.end - self.palette_cutoff.value[1]
            ratio_front_total = dist_front/dist  # ratio of how much is to be cut off in the front
            ratio_back_total = dist_back/dist  # ratio of how much is to be cut off in the back
            front_color = full_palette[0]  # used to pad everything in front of the first slider-button
            back_color = full_palette[-1]  # used to pad everything behind the second slider button
            front_colorize_length = round(ratio_front_total * len(full_palette))
            back_colorize_length = round(ratio_back_total * len(full_palette))
            # now overwrite the palette's front and back cutoff
            full_palette[:front_colorize_length] = [front_color for _ in full_palette[:front_colorize_length]]
            if back_colorize_length > 0:  # [-0:] would return entire array
                full_palette[-back_colorize_length:] = [back_color for _ in full_palette[-back_colorize_length:]]

            for cm in color_mappers:
                cm.palette = full_palette

        def _window_cb(attr: Any,
                       old: Any,
                       new: Tuple[float]
                       ) -> None:
            """Change palette on window change."""
            for cm in color_mappers:
                cm.update(low=new[0], high=new[1])

        self._palette_cb = _palette_cb
        self._window_cb = _window_cb

        self.palette.on_change('value', _palette_cb)
        self.palette_length.on_change('value', _palette_cb)

        if not same_min_max_flag:
            self.enable_and_attach_callbacks()

    def set_state(self, state: PaletteState):
        """
        Set state by updating the slider-positions of all controls.

        Args:
            state: PaletteState containing slider-values.
        """
        self.palette.value = state.name
        self.palette_length.value = state.length
        self.palette_window.value = state.window
        self.palette_cutoff.value = state.cutoff

    def get_state(self) -> PaletteState:
        """
        Get the state of the current PaletteControls.

        Returns:
            PaletteState containing slider-values.
        """
        plt: str = self.palette.value
        length: int = int(self.palette_length.value)
        plt_window: Tuple[float, float] = self.palette_window.value
        cutoff: Tuple[float, float] = self.palette_cutoff.value

        state = PaletteState(name=plt, length=length, window=plt_window, cutoff=cutoff)
        return state

    def reset_window_sliders(self,
                             min_: Optional[float] = None,
                             max_: Optional[float] = None
                             ) -> None:
        """
        Reset window and cutoff sliders.

        If min_ and max_ are specified the start and end values of window and cutoff are changed.
        This is typically necessary when the frame's minimum and maximum have changed.

        Always resets the current slider position.

        Args:
            min_: Minimum of data.
            max_: Maximum of data.
        """
        if min_ is not None and max_ is not None:
            if min_ == max_ or np.isnan(min_) or np.isnan(max_):
                self.disable_and_detach_callbacks()
                return
            self.enable_and_attach_callbacks()
            self.palette_window.update(start=min_, end=max_)
            self.palette_cutoff.update(start=min_, end=max_)

        self.palette_window.value = (self.palette_window.start, self.palette_window.end)
        self.palette_cutoff.value = (self.palette_cutoff.start, self.palette_cutoff.end)

    def enable_and_attach_callbacks(self):
        self.palette_cutoff.on_change('value', self._palette_cb)
        self.palette_window.on_change('value', self._window_cb)
        self.palette_window.disabled = False
        self.palette_cutoff.disabled = False

    def disable_and_detach_callbacks(self):
        self.palette_cutoff._callbacks.clear()
        self.palette_window._callbacks.clear()
        self.palette_window.disabled = True
        self.palette_cutoff.disabled = True
