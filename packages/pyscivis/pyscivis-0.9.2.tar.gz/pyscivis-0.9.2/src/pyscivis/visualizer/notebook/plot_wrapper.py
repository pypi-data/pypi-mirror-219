from functools import wraps, partial
from typing import Union, Dict, Optional

from pyscivis.visualizer.dataclasses.state import State
from pyscivis.visualizer.plots import ImagePlot, ComplexPlot
from pyscivis.visualizer.plots.components.value_controls import LABEL_FUNC_MAP as VALID_VALUE_KINDS


def on_next_tick(func):
    """ Decorator to allow doc-modification outside the main thread. """

    @wraps(func)
    def _impl(self, *args, **kwargs):
        return self.plot.document.add_next_tick_callback(partial(func, self, *args, **kwargs))

    return _impl


class PlotWrapper:
    """ This class is used to keep a reference to displayed plots and modify them programmatically. """

    def __init__(self, plot: Union[ImagePlot, ComplexPlot]) -> None:
        """
        Save plot and the plot's bokeh-document for future use.

        Args:
            plot: Plot object to be wrapped.
        """
        self.plot = plot

    @on_next_tick
    def set_state(self, state: State) -> None:    # pragma: nocover
        """
        Set the state of the plot manually.

        Args:
            state: A State object.
        """
        self._set_state(state)

    def _set_state(self, state: State) -> None:
        self.plot.set_state(state)

    def get_state(self) -> State:
        """
        Get the state of the plot manually.

        Returns:
            A State object.
        """
        return self.plot.get_state()

    @on_next_tick
    def set_dimension(self,
                      name: str,
                      value: int
                      ) -> None:    # pragma: nocover
        """
        Change a dimension if the dimension-name is valid.

        Automatically caps the values into range of (start, end) of slider.

        Args:
            name: Name of the dimension.
            value: New dimension value.
        """
        self._set_dimension(name, value)

    def _set_dimension(self,
                       name: str,
                       value: int
                       ) -> None:
        if self._is_valid_dimension_name(name):
            for dim in self.plot.dim_controls.dim_sliders:
                if dim.name == name:
                    min_, max_ = dim.slider.start, dim.slider.end
                    if value < min_:
                        value = min_
                    elif value > max_:
                        value = max_
                    dim.slider.value = value

    @on_next_tick
    def set_x_axis(self, name: str) -> None:    # pragma: nocover
        """
        Change the dimension displayed by the x-axis if the dimension-name is valid.

        Args:
            name: Name of the dimension.
        """
        self._set_x_axis(name)

    def _set_x_axis(self, name: str) -> None:
        """Set the x-axis value to name"""
        if self._is_valid_dimension_name(name):
            self.plot.dim_controls.axis_select.x_select.value = name

    @on_next_tick
    def set_y_axis(self, name: str) -> None:    # pragma: nocover
        """
        Change the dimension displayed by the y-axis if the dimension-name is valid.

        Args:
            name: Name of the dimension.
        """
        self._set_y_axis(name)

    def _set_y_axis(self, name: str) -> None:
        """Set the x-axis value to name"""
        if self._is_valid_dimension_name(name):
            self.plot.dim_controls.axis_select.y_select.value = name

    def _is_valid_dimension_name(self, name: str) -> bool:
        """
        Check if name is a valid dimension identifier and prints valid names if False.

        Args:
            name: Name of the dimension.

        Returns:
            True if name is valid, else False.
        """
        axis_select = self.plot.dim_controls.axis_select
        if name in axis_select.options:
            return True

        print("Specified dimension does not exist, possible dimensions are: " +
              ", ".join(list(axis_select.options.keys())))
        return False

    @on_next_tick
    def set_value_kind(self, name: str) -> None:    # pragma: nocover
        """
        Set the value kind of a ComplexPlot.

        Args:
            name: Name of the new value kind ("Real", "Imaginary", "Abs", "Phase")
        """
        self._set_value_kind(name)

    def _set_value_kind(self, name: str) -> None:
        if not isinstance(self.plot, ComplexPlot):
            print("Plot does not have complex values.")
            return
        valid = list(VALID_VALUE_KINDS)
        if name not in valid:
            print(f"Value kind {name} has to be one of {valid}.")
            return

        self.plot.value_controls.set_active_handler(name)

    def get_stats(self) -> Dict:
        """
        Get a copy of the current image-statistics.

        Returns:
            A dictionary containing statistics.
        """
        return self.plot.statistics.stats.copy()

    @on_next_tick
    def toggle_controls(self,
                        left: Optional[bool] = None,
                        bottom: Optional[bool] = None,
                        right: Optional[bool] = None
                        ) -> None:  # pragma: nocover
        """
        Toggle the visibility of the left, bottom or right control-columns.

        Args:
            left: Whether to hide the left column.
            bottom: Whether to hide the bottom column.
            right: Whether to hide the right column.

        Notes:
            Broken because of bokeh as of bokeh-2.3.2: https://github.com/bokeh/bokeh/issues/11339
            TODO: Updating bokeh once 2.4 releases might fix this
        """
        self._toggle_controls(left, bottom, right)

    def _toggle_controls(self,
                         left: Optional[bool] = None,
                         bottom: Optional[bool] = None,
                         right: Optional[bool] = None
                         ) -> None:
        doc = self.plot.document
        if left is not None:
            doc.select_one({"name": "col_left"}).visible = left
        if bottom is not None:
            doc.select_one({"name": "col_bottom"}).visible = bottom
        if right is not None:
            doc.select_one({"name": "col_right"}).visible = right

    @on_next_tick
    def toggle_fit_to_frame(self, active: Optional[bool] = None) -> None:    # pragma: nocover
        """
        Toggle the fit-to-frame-toggle.

        If 'active' is unspecified, the toggle's state will be flipped, else 'active' is applied.

        Args:
            active: Boolean for activating/disabling the fit_to_frame_toggle.
        """
        self._toggle_fit_to_frame(active)

    def _toggle_fit_to_frame(self, active: Optional[bool] = None) -> None:
        if active is not None:
            self.plot.fit_to_frame_toggle.active = active
        else:
            self.plot.fit_to_frame_toggle.active = not self.plot.fit_to_frame_toggle.active
