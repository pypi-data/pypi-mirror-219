from typing import Optional

from bokeh.models import Span


class Crosshair:
    """ Wrapper around two bokeh-spans, allowing easy creation and manipulation of a crosshair. """

    def __init__(self):
        """
        Set up two bokeh-spans.
        """
        settings = dict(line_alpha=0.8, line_color="#d3d3d3")
        self.x_line = Span(dimension="width", location=None, **settings)
        self.y_line = Span(dimension="height", location=None, **settings)

    def set_coordinates(self,
                        x: float,
                        y: float
                        ) -> None:
        """
        Changes the X- and Y-coordinates of the Y- and X-span respectively.

        Args:
            x: New X-coordinate of the Y-span.
            y: New Y-coordinate of the X-span
        """
        self.x_line.location = y
        self.y_line.location = x

    def toggle_visible(self, visible: Optional[bool] = None) -> None:
        """
        Set the crosshair's visibility to the specified value. Toggle visibility if value not specified or None.

        Args:
            visible: Show Crosshair if True, hide if False, if None switch state.
        """
        if visible is None:
            visible = not self.x_line.visible

        self.x_line.visible = visible
        self.y_line.visible = visible
