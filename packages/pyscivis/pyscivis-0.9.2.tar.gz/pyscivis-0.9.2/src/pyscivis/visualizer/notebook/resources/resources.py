import json
import os
from typing import List


CSS_FILES = ["dark.css"]


def load_resources():
    from IPython.core.display import Javascript, display_javascript
    resources = get_wrapped_css()
    resources = [Javascript(f"$('head').append({json.dumps(res)})") for res in resources]
    display_javascript(*resources)


def get_wrapped_css() -> List[str]:
    """
    Read static CSS files and turn wrap them in HTML-script tags.

    Returns:
        List of wrapped JavaScript code.
    """
    wrapped_css = list()
    for css_file in CSS_FILES:
        path = os.path.join(os.path.dirname(__file__), css_file)

        with open(path, "r") as res:
            wrapped = "<style class='pyscivis' type='text/css'>%s</style>" % res.read()
            wrapped_css.append(wrapped)

    return wrapped_css
