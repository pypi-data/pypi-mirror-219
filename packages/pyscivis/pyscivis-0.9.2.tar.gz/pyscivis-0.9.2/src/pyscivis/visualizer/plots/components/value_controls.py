from typing import Callable, Union

from bokeh.models import RadioButtonGroup

import pyscivis.visualizer.util.multithreaded_npops as mt

LABEL_FUNC_MAP = {"Real": mt.real,
                  "Imaginary": mt.imag,
                  "Abs": mt.abso,
                  "Phase": mt.angle}


class ValueRadios:
    """
    Contains Radio-Buttons for every value-kind (Real, Imaginary, Abs, Phase).
    """

    def __init__(self,
                 on_value_change: Callable[[], None],
                 active_key: str
                 ) -> None:
        """
        Create radios and set up callbacks.

        Args:
            on_value_change: Callable to fire on radio-change.
            active_key: The initially active radio-button.
        """
        active_index = list(LABEL_FUNC_MAP.keys()).index(active_key)
        self.rg = RadioButtonGroup(labels=list(LABEL_FUNC_MAP.keys()), active=active_index)
        self.active_handler = list(LABEL_FUNC_MAP.values())[self.rg.active]
        self.rg.on_change("active", lambda attr, old, new: self.notify_parent())
        self.on_value_change = on_value_change

        self.layout = self.rg

    def set_state(self, number_kind: int) -> None:
        """
        Set state by activating the specified radio.

        Args:
            number_kind: Index of radio-button to be activated.
        """
        self.rg.active = number_kind

    def get_state(self) -> int:
        """
        Get the state of the current RadioGroup.

        Returns:
            Index of the active radio-button.
        """
        return self.rg.active

    def notify_parent(self) -> None:
        """
        Retrieve value handler for radio button and notify parent.
        """
        _handler = list(LABEL_FUNC_MAP.values())[self.rg.active]
        self.active_handler = _handler
        self.on_value_change()

    def set_active_handler(self, index: Union[int, str]) -> None:
        """
        Change the active radio-button and notify the parent.

        Args:
            index: Index or name of radio-button to be activated.
        """
        if isinstance(index, str):
            index = list(LABEL_FUNC_MAP.keys()).index(index)
        self.rg.active = index
