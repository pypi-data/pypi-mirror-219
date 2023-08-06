import os
import tkinter
from tkinter.filedialog import askopenfilename
from typing import List, Tuple


def select_file_tkinter(extension_name: str, valid_extensions: Tuple[Tuple[str, str, str], ...], multiple: bool):
    filetype_extensions: List[Tuple[str, str]] = list()
    for alias, desc, filetype in valid_extensions:
        if alias == extension_name:
            filetype_extensions = [(desc, filetype)]
    if not filetype_extensions:
        raise ValueError(f"No such extension {extension_name}")
    filetype_extensions.append(("All files", "*"))

    root = tkinter.Tk()
    root.attributes('-topmost', True)
    root.withdraw()

    return askopenfilename(filetypes=filetype_extensions,
                           multiple=multiple)


def select_file_from_list(file_root: str, valid_ext_names):
    tree_list = []
    for (dirpath, _, filenames) in os.walk(file_root):
        if dirpath == file_root:
            parent = "#"
        else:
            parent = os.path.dirname(dirpath)

        nodes = []

        dir_name = os.path.basename(dirpath)
        directory = dict(text=dir_name, id=dirpath, type="container", parent=parent)
        nodes.append(directory)
        for filename in filenames:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in valid_ext_names:
                continue
            file_path = os.path.join(dirpath, filename)
            file_node = dict(text=filename, id=file_path, type="header", parent=dirpath)
            nodes.append(file_node)

        tree_list.extend(nodes)

    return tree_list
