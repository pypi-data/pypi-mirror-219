from typing import Callable

from bokeh.layouts import row, column
from bokeh.models import TextAreaInput, Button, CustomJS, FileInput
from pyscivis.visualizer.dataclasses.state import state_to_json, state_from_json, is_json_state, State
import base64


download_state_code = \
    """
    function doDownload(str) {
      function dataUrl(data) {
        return "data:x-text/plain;charset=utf-8," + escape(data);
      }
      var downloadLink = document.createElement("a");
      downloadLink.href = dataUrl(str);
      downloadLink.download = "state.txt";
    
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
    doDownload(textbox.value)
    """


def StateFigure(format_state: bool,
                set_state_cb: Callable[[State], None],
                get_state_cb: Callable[[], State]):
    """
    Create a StateFigure (Textbox, {upload, download, get-state, set-state}-buttons)

    Args:
        format_state: Whether the state should be formatted in a pretty way.
        set_state_cb: Callback fired if a state change was fired by the user.
        get_state_cb: Callback fired if the user requests the current state.

    Returns:
        A bokeh LayoutDOM containing the StateFigure

    """
    # TextBox

    state_text_box = TextAreaInput(rows=14, max_length=None)
    indent = 4 if format_state else None

    # Get- and Set-state buttons
    def set_state_text(state: State) -> None:
        text = state_to_json(state, indent=indent)
        state_text_box.value = text

    get_state_btn = Button(label="Get State")
    get_state_btn.on_click(lambda x: set_state_text(get_state_cb()))
    set_state_btn = Button(label="Set State", disabled=True)
    set_state_btn.on_click(lambda x:
                           set_state_cb(state_from_json(state_text_box.value)))
    text_btn_row = row(get_state_btn, set_state_btn)

    # Download button
    download_state_btn = Button(label="Download State", disabled=True)
    download_state = CustomJS(args=dict(textbox=state_text_box),
                              code=download_state_code)
    download_state_btn.js_on_click(download_state)

    # Upload Button
    hidden_file_upload_btn = FileInput(accept=".txt", multiple=False, visible=False, css_classes=["file-input"])

    def set_text_from_b64(s_b64):
        s_bytes = base64.b64decode(s_b64)
        state_text_box.value = s_bytes.decode('utf-8')

    hidden_file_upload_btn.on_change("value", lambda attr, old, new: set_text_from_b64(new))

    upload_state_btn = Button(label="Upload State")  # using this as a visually matching "fake"-file-input
    upload_state_btn.js_on_click(CustomJS(code="document.querySelector('.file-input input').click()"))

    def on_text_change(new_text):
        disabled = not is_json_state(new_text)
        set_state_btn.disabled = disabled
        download_state_btn.disabled = disabled

    state_text_box.on_change("value", lambda attr, old, new: on_text_change(new))

    file_btn_row = row(download_state_btn, upload_state_btn, hidden_file_upload_btn)
    state_layout = column(state_text_box, text_btn_row, file_btn_row)

    return state_layout
