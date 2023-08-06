from abc import ABC, abstractmethod

from bokeh.models import LayoutDOM


class BasePlot(ABC):
    """ Abstract class serving as the base for plots, enforcing implementation of required methods. """
    @abstractmethod
    def get_layout(self) -> LayoutDOM:
        """
        Return the UNIQUE layout of the plot, i.e., parts of the layout MUST NOT be reused at any point.

        Raises:
            NotImplementedError: This method is supposed to be overridden.
        """
        raise NotImplementedError
