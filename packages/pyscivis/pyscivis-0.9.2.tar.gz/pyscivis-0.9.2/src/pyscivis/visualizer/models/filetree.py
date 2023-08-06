
from bokeh.core.properties import (String, List, Dict, Tuple, Readonly)
from bokeh.models import Widget


class Tree(Widget):
    """
    A widget to represent a tree-like structure with retractable nodes.

    This is a custom extension wrapping a 3rd party javascript library.
    Supply a flat list of dicts, like in the example below to initialize the tree.

    Examples:
        tree = [{"id": "ajson1", "parent": "#", "text": "Filename", "type": "file"},
            {"id": "ajson2", "parent": "ajson1", "text": "Container1", "type": "container"},
            {"id": "ajson3", "parent": "ajson2", "text": "images", "type": "images"},
            {"id": "ajson4", "parent": "ajson2", "text": "header", "type": "header"},
            {"id": "ajson5", "parent": "ajson1", "text": "Container2", "type": "container"},
            {"id": "ajson6", "parent": "ajson5", "text": "Container3", "type": "container"},
            {"id": "ajson7", "parent": "ajson6", "text": "acquisition", "type": "acquisitions"},
            {"id": "ajson8", "parent": "ajson6", "text": "header", "type": "header"}]
        filetree = Tree(tree=tree)

    """

    # __implementation__ = "filetree.ts"

    # selected leaf node's parent name and own name and header type
    selected = Readonly(Tuple(String, String, String, default=("", "", "")))
    theme = String(default="light")
    # flat list used to create tree structure
    tree = List(Dict(String, String), default=[])

"""tree = [{"id": "ajson1", "parent": "#", "text": "Filename", "type": "file"},
        {"id": "ajson2", "parent": "ajson1", "text": "Container1", "type": "container"},
        {"id": "ajson3", "parent": "ajson2", "text": "images", "type": "images"},
        {"id": "ajson4", "parent": "ajson2", "text": "header", "type": "header"},
        {"id": "ajson5", "parent": "ajson1", "text": "Container2", "type": "container"},
        {"id": "ajson6", "parent": "ajson5", "text": "Container3", "type": "container"},
        {"id": "ajson7", "parent": "ajson6", "text": "acquisition", "type": "acquisitions"},
        {"id": "ajson8", "parent": "ajson6", "text": "header", "type": "header"}]

tree_widget = Tree(tree=tree, width=600, height=600)
js_cb = CustomJS(code="console.log(cb_obj.selected)")
tree_widget.js_on_change("selected", js_cb)
tree_widget.on_change("selected", lambda attr, old, new: print(new))
curdoc().add_root(tree_widget)"""
