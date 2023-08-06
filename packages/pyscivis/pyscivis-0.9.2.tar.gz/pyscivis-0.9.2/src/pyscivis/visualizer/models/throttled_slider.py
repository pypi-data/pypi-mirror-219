from time import perf_counter
from functools import partial

from bokeh.models.widgets import Slider

# Most of the credit goes to Matt_Agee (https://discourse.bokeh.org/t/server-side-throttled-slider/3212)

class ThrottledSlider(Slider):
    """
    Extends the bokeh Slider to provide throttling of callbacks provided to on_update
    """

    #__implementation__ = "throttled_slider.ts"

    def __init__(self, base_delay, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cb_set = False
        self._base_delay = base_delay
        self._delay = base_delay

    def on_change(self, attr, callback):
        """
        Register a server side callback to be executed when slider attributes change

        Args:
            attr: Attribute that changed.
            callback: Callback to fire.
        """
        update_function = self._callback_wrapper(callback)
        super().on_change(attr, partial(self._callback_setter, update_function))

    def _callback_setter(self, update_function, attr, old, new):
        if not self._cb_set:
            self._document.add_timeout_callback(partial(update_function, attr, old), self._delay)
            self._cb_set = True

    def _callback_wrapper(self, callback):
        """
        Wraps callback to use self.value instead of new.

        This ensures the callback has the most recent slider value at execution.
        Also modifies the delay between callback execution to account for time taken
        performing the callback's work.
        """

        def throttled_cb(*args):
            start_time = perf_counter()
            attr, old = args
            callback(attr, old, self.value)

            # Modify delay to account for time taken executing callback
            self._delay = max(self._base_delay - 1000 * (perf_counter() - start_time), 50)
            self._cb_set = False

        return throttled_cb
