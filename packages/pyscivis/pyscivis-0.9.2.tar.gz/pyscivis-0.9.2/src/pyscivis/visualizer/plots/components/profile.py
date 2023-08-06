from typing import TypedDict, Optional, Tuple

import numpy as np

from bokeh.layouts import column
from bokeh.plotting import figure, Figure
from bokeh.models import WheelZoomTool, Span
from pyscivis.visualizer.plots.dimension_handler import DimensionHandler
from pyscivis.visualizer.dataclasses.state import ProfileState


class ProfileClick(TypedDict):
    x: Optional[int]
    y: Optional[int]


class ProfileFigure:
    """
    Wraps all profile figures and allows to changed them in an organized way.
    """

    def __init__(self,
                 dimension_handler: DimensionHandler,
                 min_: float,
                 max_: float
                 ) -> None:
        """
        Dynamically create profiles for every dimension.

        Args:
            dimension_handler: DimensionHandler instance.
            min_: Current data-minimum.
            max_: Current data-maximum.
        """
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.min, self.max = self.pad_bounds(min_, max_)
        self.dimension_handler = dimension_handler
        self.profiles = dict()

        for index, dim in dimension_handler.dims.items():
            if dim.size <= 1:
                continue
            self.profiles[index] = self._create_profile_for_dims(dim.name, dim.length)

        self.layout = column(*list(self.profiles.values())[::-1], css_classes=["profile-figures"])

    def set_state(self, state: ProfileState):
        """
        Set state by updating all profiles to display the profile at the state's coordinates.

        Args:
            state: ProfileState containing click-coordinates.
        """
        self.set_coordinates(state.x, state.y)

    def get_state(self) -> ProfileState:
        """
        Get the state the current profile click-coordinate.

        Returns:
            ProfileState containing click-coordinates.
        """
        state = ProfileState(x=self.x, y=self.y)
        return state

    def set_coordinates(self,
                        x: Optional[int],
                        y: Optional[int]
                        ) -> None:
        """
        Set x- and y-click-coordinates (typically from a tap-event) and update the profiles.

        Args:
            x: X-Coordinate.
            y: Y-Coordinate.
        """
        self.x = x
        self.y = y
        self.update()

    def update_from_axis_change(self) -> None:
        """
        Null x- and y-click-coordinates and reset the profiles.
        """
        self.x = None
        self.y = None
        self.update(True)

    def update(self, reset_profiles: bool = False) -> None:
        """
        Updates all profiles using the last x- and y-click coordinates.

        Args:
            reset_profiles: Whether to only reset the profiles.
        """
        active_y_axis, active_x_axis = self.dimension_handler._order[-2:]

        for index, profile in self.profiles.items():
            self._update_profile_vals(profile, index, active_x_axis, active_y_axis, reset=reset_profiles)

    def _update_profile_vals(self,
                             profile: Figure,
                             index: int,
                             active_x_axis: int,
                             active_y_axis: int,
                             reset: bool = False
                             ) -> None:

        if reset:
            # TODO: Reorder on axes change?
            profile.title.text = profile.name
            profile.select_one({"name": "index_indicator"}).location = None
            profile.select_one({"name": "profile_indicator"}).data_source.data = dict(x=[np.nan], y=[np.nan])
            #profile.select_one({"name": "profile_points"}).data_source.data = dict(x=[np.nan], y=[np.nan])
            return

        if self.x is None or self.y is None:
            return

        click_coords = dict(x_id=active_x_axis, x_coord=self.x, y_id=active_y_axis, y_coord=self.y)
        vals: np.ndarray = self.dimension_handler.get_profile(index, click_coords)

        data_len = len(vals)
        image_len = self.dimension_handler.dims[index].length
        ratio = image_len/data_len

        if index == active_y_axis:
            own_index = self.y
        elif index == active_x_axis:
            own_index = self.x
        else:
            own_index = self.dimension_handler._values[index]
        own_index *= ratio
        profile.select_one({"name": "index_indicator"}).location = own_index
        profile.title.text = f"{profile.name} = {round(own_index, 1):g}"
        new_xs = np.arange(len(vals))*ratio
        new_ys = vals
        data = dict(x=new_xs, y=new_ys)
        profile.select_one({"name": "profile_indicator"}).data_source.data = data
        #profile.select_one({"name": "profile_points"}).data_source.data = data

    def update_y_bounds(self,
                        start: float,
                        end: float
                        ) -> None:
        """
        Update the y-bounds of all profiles. Uses a 10% padding on both sides.

        Args:
            start: Start value for the y-range.
            end: End value for the y-range.
        """
        padded_start, padded_end = self.pad_bounds(start, end)
        for profile in self.profiles.values():
            profile.y_range.update(start=padded_start, end=padded_end, bounds=(padded_start,padded_end))

    def _create_profile_for_dims(self,
                                 name: str,
                                 length: float,
                                 # unit=None
                                 ) -> Figure:
        """ Create a profile for one specific dimension (name and length) """
        profile = figure(title=name, width=300, height=200, y_axis_location="right",
                         x_range=(0, length-1), y_range=(self.min, self.max),
                         toolbar_location=None, tools=['pan'], name=name)
        profile.x_range.bounds = (0, length-1)
        profile.y_range.bounds = (self.min, self.max)
        vline = Span(location=None, dimension='height', name="index_indicator", line_color="#848484", line_width=1)
        profile.line(x=[np.nan], y=[np.nan], name="profile_indicator")
        #dots = profile.cross(x=[np.nan],y=[np.nan], name="profile_points")
        wz_tool = WheelZoomTool(maintain_focus=False, dimensions='height')
        #h_tool = HoverTool(renderers=[dots], tooltips="@y", mode='vline')
        profile.add_layout(vline)
        profile.add_tools(wz_tool)#, h_tool)
        profile.toolbar.active_scroll = wz_tool
        return profile

    @staticmethod
    def pad_bounds(start: float,
                   end: float,
                   padding_factor: float = 0.1
                   ) -> Tuple[float, float]:
        """
        Pad the supplied bounds by multiplying the bound-difference with the supplied padding factor.

        Args:
            start: Bound-start.
            end: Bound-end.
            padding_factor: Factor for padding.

        Returns:
            Tuple of padded bounds.

        Raises:
            ValueError: If start bigger than end.
        """
        if np.isnan(start) or np.isnan(end):
            return 0, 1

        if start > end:
            raise ValueError(f"Bound-start {start} cannot be bigger than Bound-end {end}")

        if start == end:
            padding = padding_factor if padding_factor != 0 else 0.1
        else:
            padding = (end - start) * padding_factor

        return start - padding, end + padding
