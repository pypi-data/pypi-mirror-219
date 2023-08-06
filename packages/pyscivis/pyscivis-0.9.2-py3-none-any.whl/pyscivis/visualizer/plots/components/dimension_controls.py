from typing import Any, Dict, Sequence, Callable

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, Select

from pyscivis.visualizer.models import ThrottledSlider
from pyscivis.visualizer.dataclasses.state import DimensionState, AxesState

from pyscivis.visualizer.dataclasses.handler import Dim


class DimensionControls:
    """
    Manage dimension related controls, i.e., Axes-dropdowns and Dimension-sliders.
    """

    def __init__(self,
                 dim_metadata: Dict[int, Dim],
                 dim_change_cb: Callable[[int, int], Any],
                 axes_change_cb: Callable[[int, int], Any],
                 ) -> None:
        """
        Set up objects and callbacks.

        Args:
            dim_metadata: Metadata for dimensions.
            dim_change_cb: Callback to be used if dimension-values change.
            axes_change_cb: Callback to be used if axes change.
        """
        self.notify_dim_change = dim_change_cb
        self.notify_axes_change = axes_change_cb

        self.animated_dimension = None
        self.dim_sliders = list()

        self.axis_select = DimensionSelectPair(dim_metadata, self)

        # Create a bunch of DimensionSliders
        for k, v in dim_metadata.items():
            if v.size == 1:
                self.dim_sliders.append(None)
            else:
                self.dim_sliders.append(DimensionSlider(k, v.name, v.size, self))

        # Add only valid layouts to the main layout
        layout = list()
        for slider in reversed(self.dim_sliders):
            if slider is not None:
                layout.append(slider.layout)

        self.slider_layout = column(*layout, sizing_mode="stretch_width", css_classes=["slider-column"])
        self.hide_sliders([i for i in range(len(dim_metadata))][-2:])  # Hide last two axes

        self.axis_select_layout = self.axis_select.layout

    def set_state(self, state: DimensionState) -> None:
        """
        Set the state of the objects managed by this class.

        Args:
            state: DimensionState to be set.

        See Also:
            DimensionSlider, DimensionSelectPair
        """
        # TODO: (?) could use document.hold to reduce the amount of on_changes called
        axes: AxesState = state.axes
        dimensions: Dict[str, int] = state.dimensions

        self.axis_select.set_x_without_cb(axes.x_axis)
        self.axis_select.y_select.value = axes.y_axis
        for name, val in dimensions.items():
            for slider in self.dim_sliders:  # find correct slider for dim
                if slider is None or slider.name != name:
                    continue

                if val < slider.slider.start:
                    val = slider.slider.start
                elif val > slider.slider.end:
                    val = slider.slider.end

                slider.slider.value = val

    def get_state(self) -> DimensionState:
        """
        Get the state of the objects managed by this class.

        Returns:
            A State object.

        See Also:
            DimensionSlider, DimensionSelectPair
        """
        x_axis = self.axis_select.x_select.value
        y_axis = self.axis_select.y_select.value
        axes = AxesState(x_axis=x_axis, y_axis=y_axis)

        dimensions: Dict[str, int] = dict()
        for slider in self.dim_sliders:
            if slider is None:
                continue
            dimensions[slider.name] = slider.slider.value

        state = DimensionState(axes=axes, dimensions=dimensions)
        return state

    def on_axes_change(self,
                       x_axis: int,
                       y_axis: int
                       ) -> None:
        """
        Hide sliders if their dimension is displayed and notify controller of axes-change.

        Also disables the currently animated slider if called.

        Args:
            x_axis: Index of the new x-axis.
            y_axis: Index of the new y-axis.
        """
        self.disable_active_slider()
        for slider in self.dim_sliders:
            if slider is None:
                continue
            if slider.id in [x_axis, y_axis]:
                slider.hide()
            else:
                slider.show()
        self.notify_axes_change(x_axis, y_axis)

    def hide_sliders(self, axes: Sequence[int]) -> None:
        """
        Make the specified axes invisible.

        Args:
            axes (Sequence[int]): A sequence of axis-indices.
        """
        for axis in axes:
            if self.dim_sliders[axis] is not None:
                self.dim_sliders[axis].hide()

    def toggle_slider(self, index: int) -> None:
        """
        Animate a dimension slider by indefinitely increasing its value.

        A periodic callback is registered on the bokeh document that
        increases the slider-value by 1 (wraps around the maximum).
        If this method is called while another dimension slider is being
        animated, stop that animation.

        Args:
            index: Index of the axis to be animated.
        """
        if self.animated_dimension is not None and self.animated_dimension != index:
            self.disable_active_slider()
        global callback_id

        dim_slider = self.dim_sliders[index]

        if dim_slider.play_btn.label == '►':
            self.animated_dimension = index
            dim_slider.play_btn.label = '❚❚'
            callback_id = curdoc().add_periodic_callback(dim_slider.inc_slider, 200)
        else:
            self.animated_dimension = None
            dim_slider.play_btn.label = '►'
            curdoc().remove_periodic_callback(callback_id)

    def disable_active_slider(self) -> None:
        if self.animated_dimension is None:
            return
        global callback_id
        self.dim_sliders[self.animated_dimension].play_btn.label = '►'
        curdoc().remove_periodic_callback(callback_id)
        self.animated_dimension = None


class DimensionSlider:
    """
    Wrap a slider, callback and data for identifying objects of this class.
    """

    def __init__(self,
                 index: int,
                 name: str,
                 length: int,
                 controller: DimensionControls
                 ) -> None:
        """
        Set up attributes, the slider, button and necessary callbacks.

        Args:
            index: Index for this slider.
            name: Name of this slider.
            length: Size of this slider.
            controller: Parent controlling this object.
        """

        # TODO: (?) onDragStart = disable_active_slider
        self.id = index
        self.name = name
        self.length = length
        self.slider = ThrottledSlider(base_delay=200, title=name, start=0, end=length-1,
                                      value=0, step=1, sizing_mode="stretch_width")
        self.slider.on_change('value', lambda attr, old, new: controller.notify_dim_change(index, new))

        dec_btn = Button(label='<', aspect_ratio=1, align="center")
        self.play_btn = Button(label='►', aspect_ratio=1, align="center")
        inc_btn = Button(label='>', aspect_ratio=1, align="center")

        dec_btn.on_click(self.dec_slider)
        self.play_btn.on_click(lambda: controller.toggle_slider(index))
        inc_btn.on_click(self.inc_slider)

        btn_row = row(dec_btn, self.play_btn, inc_btn)
        self.layout = row(self.slider, btn_row)

    def inc_slider(self):
        if self.slider.value == self.slider.end:
            self.slider.value = self.slider.start
        else:
            self.slider.value += 1

    def dec_slider(self):
        if self.slider.value == self.slider.start:
            self.slider.value = self.slider.end
        else:
            self.slider.value -= 1

    def show(self) -> None:
        """
        Make self visible.
        """
        self.layout.visible = True

    def hide(self) -> None:
        """
         Make self invisible.
        """
        self.layout.visible = False


class DimensionSelectPair:
    """
    Wrap two axes-selection widgets and their interaction.
    """

    def __init__(self,
                 options: Dict[int, Dim],
                 controller: DimensionControls
                 ) -> None:
        """
        Set up both selects and their callbacks.

        Args:
            options: Dictionary mapping dimension-indices to Dim metadata.
            controller: Parent controlling this object.
        """
        self.options = {v.name: k for k, v in options.items() if v.size > 1}
        self.controller = controller
        self.x_select = Select(title="X-Axis", options=sorted(self.options.keys()))
        self.y_select = Select(title="Y-Axis", options=sorted(self.options.keys()))

        self.x_select.value = list(self.options.keys())[-1]
        self.y_select.value = list(self.options.keys())[-2]

        self.x_select.on_change('value', self.on_x_change)
        self.y_select.on_change('value', self.on_y_change)

        self.layout = column(self.x_select, self.y_select, css_classes=["axes-selector"])

    def on_x_change(self,
                    attr: Any,
                    old: str,
                    new: str
                    ) -> None:
        """
        Checks if the y-select currently has the new value and swaps them if yes, then calls a callback.

        Args:
            attr: Attribute name.
            old: Former name of the x-axis.
            new: New name for the y-axis.

        Note:
            Converts the name into the according index for the callback.
        """
        if new == self.y_select.value:  # workaround to avoid unnecessary cbs
            self.set_y_without_cb(old)
        x_new = self.options[new]
        y_new = self.options[self.y_select.value]
        self.controller.on_axes_change(x_new, y_new)

    def on_y_change(self,
                    attr: Any,
                    old: str,
                    new: str
                    ) -> None:
        """
        Checks if the x-select currently has the new value and swaps them if yes, then calls a callback.

        Args:
            attr: Attribute name.
            old: Former name of the y-axis.
            new: New name for the y-axis.

        Note:
            Converts the name into the according index for the callback.
        """
        if new == self.x_select.value:  # workaround to avoid unnecessary cbs
            self.set_x_without_cb(old)
        x_new = self.options[self.x_select.value]
        y_new = self.options[new]
        self.controller.on_axes_change(x_new, y_new)

    def set_x_without_cb(self, val: str) -> None:
        """
        Set a value to the x-axis without calling the callback.

        Args:
            val: New name for the x-axis.
        """
        self._remove_x_select_cb()
        self.x_select.value = val
        self._attach_x_select_cb()

    def set_y_without_cb(self, val: str) -> None:
        """
        Set a value to the y-axis without calling the callback.

        Args:
            val: New name for the y-axis.
        """
        self._remove_y_select_cb()
        self.y_select.value = val
        self._attach_y_select_cb()

    def _remove_x_select_cb(self) -> None:
        self.x_select.remove_on_change('value', self.on_x_change)

    def _attach_x_select_cb(self) -> None:
        self.x_select.on_change('value', self.on_x_change)

    def _remove_y_select_cb(self) -> None:
        self.y_select.remove_on_change('value', self.on_y_change)

    def _attach_y_select_cb(self) -> None:
        self.y_select.on_change('value', self.on_y_change)
