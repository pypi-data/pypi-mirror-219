from tornado import gen

from bokeh.models import Div
from bokeh.layouts import row


class LoadingDiv:
    """
    Wraps a loading screen and a text-Div to display a status message.
    """

    def __init__(self, text: str = "Placeholder") -> None:
        """
        Set up the loading-Div and status-Div.

        Args:
            text: Initial text to be displayed in the status message.
        """
        loading_screen = Div(text="""<div class="loading style-2"><div class="loading-wheel"></div></div>""")
        self.text_div = Div(text=text, css_classes=["loading-text"])
        self.layout = row(loading_screen, self.text_div, visible=False)  # hidden by default

    def set_text(self, text: str) -> None:
        """
        Set the status text from any thread (main or other).

        Args:
            text: Text to display.

        Note:
            The text will not be set if the main-thread is not passing control to bokeh/is busy.
        """
        @gen.coroutine
        def _set_text():
            self.layout.visible = True
            self.text_div.text = text
        self.text_div.document.add_next_tick_callback(_set_text)

    def show(self) -> None:
        @gen.coroutine
        def _show():
            self.layout.visible = True
        self.text_div.document.add_next_tick_callback(_show)

    def hide(self) -> None:
        @gen.coroutine
        def _hide():
            self.layout.visible = False
        self.text_div.document.add_next_tick_callback(_hide)
