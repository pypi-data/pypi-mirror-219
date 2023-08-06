import os
import itertools
import time
import socket
from dataclasses import dataclass
from typing import Optional, Sequence, Union, Iterator, Tuple

import numpy as np
from bokeh.io import output_notebook, show as bkshow
from bokeh.document.document import Document as BokehDocument
from bokeh.resources import INLINE
from pptree import print_tree as prettyprint_tree

from pyscivis.visualizer.notebook.resources.resources import load_resources
from pyscivis.visualizer.util.themes import theme_map
from pyscivis.visualizer.extensions import extension_manager as ext_manager, FlatExtension, NestedExtension
from pyscivis.visualizer.plots import ImagePlot, ComplexPlot
from pyscivis.visualizer.dataclasses.config import load_config
from pyscivis.visualizer.util import notebook_utils as util
from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.notebook.plot_wrapper import PlotWrapper

"""
This module allows the usage of pyscivis in Jupyter Notebooks or JupyterLab.
"""

ext_manager.check_extension_validity()

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "config.toml")
config = load_config(config_path)


@dataclass
class NBState:
    """
    Just a wrapper for some state variables to avoid overusing `global`.
    """

    docker_flag = False
    custom_ports: Optional[Iterator[int]] = None
    custom_ports_length = -1
    config_ports: Optional[Iterator[int]] = None
    config_ports_length = -1
    autodiscover_ports = False
    autodiscover_delay = 2000
    theme = "default"
    notebook_url = "localhost:8888"


if config.notebook.ports:
    start: int = config.notebook.ports[0]
    end: int = config.notebook.ports[1] + 1
    NBState.config_ports = itertools.cycle(range(start, end))  # infinite iterator to stay within our port range
    NBState.config_ports_length = len(range(start, end))


def notebook_url(url: str) -> None:
    """
    Set the notebook-url so that bokeh knows where to display the plots.

    Args:
        url: URL of current notebook.
    """
    NBState.notebook_url = url


def set_theme(name: str) -> None:
    """
    Set a theme to be used for all future plots. Print valid theme names if an invalid name was supplied.

    Args:
        name: Name of theme to be set.

    """
    if name not in theme_map:
        valid_themes = ", ".join(list(theme_map.keys()))
        print(f"Invalid theme name '{name}', valid options are: {valid_themes}")
        return
    NBState.theme = name


def enable(offline: bool = False,
           docker: bool = False,
           autodiscover_ports: bool = False,
           ports: Optional[Sequence[int]] = None,
           ) -> None:
    """
    Load BokehJS into the current notebook and set up necessary configuration, e.g., in docker-env, whether to knock at ports before displaying plots.

    Args:
        offline: Setting this to True permits offline usage by loading local js-files, False will use a CDN.
        docker: Flag to enable use in dockerized Jupyter Notebook by falling back to custom/config ports.
        autodiscover_ports: If enabled ports will be knocked at to enable usage of port auto-detection tools
            before the actual plots are displayed.
        ports: Custom port range, e.g. `(10, 100)` (override config ports if not None)

    Notes:
        `docker` has to be set to `True` to activate the autodiscovery-functionality
            and the custom ports.
        The custom_ports variable of this module can be nulled if `ports`
            was specified and usage of config ports is later wanted.
            Set NBState.custom_ports manually for this.
        """
    load_resources()  # load local files into notebook, the dark-theme css for now

    options = dict()
    if offline:
        options['resources'] = INLINE

    if docker:
        NBState.docker_flag = True
        if ports:
            NBState.custom_ports = itertools.cycle(range(ports[0], ports[1]+1))
            NBState.custom_ports_length = len(range(ports[0], ports[1]+1))

    NBState.autodiscover_ports = autodiscover_ports

    output_notebook(**options)
    print_supported_extensions()


def print_supported_extensions():
    """
    Print the currently supported file-extensions.
    """
    print("Currently, the enabled extensions support usage of the following file-types:")
    file_exts = ext_manager.get_supported_files()
    file_exts = set([f[2] for f in file_exts])
    print(" ".join(file_exts))


def show(plot: Union[ImagePlot, ComplexPlot], n_retries=0, max_retries=0) -> None:
    """
    Wrap bokeh's show, allowing easier display of custom Plot-objects with automatic port assignment.

    If a port-range was specified it will try to iterate over the entire range to find an open port.

    Args:
        plot: The custom plot object to display.
        n_retries: Current amount of retries used.
        max_retries: Max amount of allowed retries.
    """
    def sp(doc: BokehDocument) -> None:  # adds the actual app into the specified bokeh-document
        """ Function handler creating a new document as required per bokeh.io.show. """
        layout = plot.get_layout()
        layout.css_classes = [NBState.theme]
        doc.theme = theme_map[NBState.theme]
        doc.add_root(layout)
        plot.document = doc
    if not NBState.docker_flag:  # no dockerized environment -> use standard bokeh port assignment
        bkshow(sp, notebook_url=NBState.notebook_url)
        return

    ports = None
    if NBState.custom_ports is not None:  # custom_ports have priority over config-defined ports
        ports = NBState.custom_ports
        max_retries = NBState.custom_ports_length
    elif NBState.config_ports is not None:
        ports = NBState.config_ports
        max_retries = NBState.config_ports_length

    if ports is None:  # use bokeh's default port
        bkshow(sp, notebook_url=NBState.notebook_url)
    else:
        port = next(ports)
        try:
            if NBState.autodiscover_ports:
                _knock_at_port(port, NBState.autodiscover_delay)
            bkshow(sp, notebook_url=NBState.notebook_url, port=port)
        except OSError:
            if n_retries == max_retries:
                raise OSError(f"Could not find open port in specified port range. Tried {n_retries} ports.")
            else:
                show(plot, n_retries+1, max_retries)


def load_file(f_path: str,
              extension_name: Optional[str] = None
              ) -> Optional[Union[PlotWrapper, "NotebookHandler"]]:
    """
    Load the specified file and return a PlotWrapper if it is a flat file or a more complex handler if it is nested.

    The specified extension name is used to get the corresponding extension which is then used to parse the specified
    file-path (which can consist of multiple

    Args:
        extension_name: Extension name to be used for handling the file path.
        f_path: Path to file.

    Returns:
        NotebookHandler or PlotWrapper.
    """
    try:
        ext_handler = ext_manager.get_extension_handler(f_path, extension_name, config)
    except ValueError:
        print("It looks like the specified path does not have a file-extension. "
              "Please specify the extension yourself by calling this function"
              " with the argument 'extension_name'.\n")
        _print_extension_options(ext_manager.get_extension_names_and_descriptions())
        return
    except IndexError:
        print("There are multiple valid extensions for the specified file(s). "
              "Please specify the extension yourself by calling this function"
              " with the argument 'extension_name'.\n")
        _print_extension_options(ext_manager.get_extension_names_and_descriptions())
        return

    if isinstance(ext_handler, NestedExtension):
        tree_struct = ext_handler.tree_struct
        root = util.nodeify_tree_structure(tree_struct)
        prettyprint_tree(root, nameattr="text")  # prints a nice layout of the file
        print("\n")
        return NotebookHandler(ext_handler)
    elif isinstance(ext_handler, FlatExtension):
        plot = ext_handler.create_plot()
        show(plot)
        return PlotWrapper(plot)
    else:
        raise TypeError("This should never happen")


load = load_file


def _print_extension_options(name_desc_list: Sequence[Tuple[str, str]]) -> None:
    print("Possible extension_name values are:\n")

    options = [f"'{alias}' to load {desc}" for alias, desc in name_desc_list]
    print("\n".join(options))


def _knock_at_port(port: int,
                   delay: int,
                   ) -> None:
    """
    Uses a (possibly non-open) port for a web-socket connection and wait the specified delay afterwards.

    Args:
        port: Port to knock at.
        delay: Time in milliseconds to wait after knocking, to give time for autodetection tools to forward ports.

    Raises:
        OSError: If port is currently in use.
    """

    nb_url = NBState.notebook_url
    if nb_url.startswith("http"):
        server_url = nb_url.rsplit(':', 1)[0]
    else:
        server_url = f"http://{nb_url.split(':')[0]}"
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((server_url, port))
        except OSError as ose:
            raise ose    # if port is already in use we want to bubble the exception up to skip this port
        finally:
            s.close()

    time.sleep(delay/1000)


def display(data: np.ndarray,
            dim_names: Optional[Sequence[str]] = None,
            dim_units: Optional[Sequence[str]] = None,
            dim_lengths: Optional[Sequence[float]] = None,
            transpose: bool = True,
            title: str = ""
            ) -> PlotWrapper:
    """
    Display a user supplied image if data is real or acquisition if data is complex.

    Args:
        data: N-dimensional numpy-array.
        dim_names: Sequence of dimension-names.
        dim_units: Sequence of units for dimensions.
        dim_lengths: Sequence of length of dimensions (corresponds to their unit).
        transpose: Interpret data in [x, y, z] format if True, else treat input as [z, y, x].
        title: Optional title displayed above the main plot.

    Returns:
        A PlotWrapper object.

    Note:
        Fails if only one of `dim_units` and `dim_lengths` was specified.
        Also fails if amount of data dimensions is unequal to the length of the specified dim_* parameters.
    """

    input_errors = list()
    if dim_names is not None and data.ndim != len(dim_names):
        input_errors.append(f"`dim_names` has to have exactly one value for every dimension,\n\
                             length: {len(dim_names)}, dim-count: {data.ndim}")
    if (dim_units is None) ^ (dim_lengths is None):
        input_errors.append("Have to set both `dim_units` and `dim_names` or neither.")

    if dim_units is not None and data.ndim != len(dim_units):
        input_errors.append(f"`dim_units` has to have exactly one value for every dimension,\n\
              length: {len(dim_units)}, dim-count: {data.ndim}")
    if dim_lengths is not None and data.ndim != len(dim_lengths):
        input_errors.append(f"`dim_lengths` has to have exactly one value for every dimension,\n\
              length: {len(dim_lengths)}, dim-count: {data.ndim}")

    if input_errors:
        err_str = '\n'.join(input_errors)
        print(f"One more multiple invalid arguments were passed:\n {err_str}")
        return

    if transpose:
        data = np.transpose(data)
        if dim_names is not None:
            dim_names = dim_names[::-1]
        if dim_units is not None:
            dim_lengths = dim_lengths[::-1]  # dim_lengths can't be None at this point
            dim_units = dim_units[::-1]

    if np.iscomplexobj(data):  # complex ndarray -> acquisition
        data = np.array(data, dtype="complex64")
        parsed = parse_raw(data, dim_names, dim_lengths, dim_units)
        plot = ComplexPlot(parsed, config.image, title=title)
    else:
        parsed = parse_raw(data, dim_names, dim_lengths, dim_units)
        plot = ImagePlot(parsed, config.image, title=title)

    show(plot)
    return PlotWrapper(plot)


def parse_raw(data: np.ndarray,
              dim_names: Optional[Sequence[str]] = None,
              dim_lengths: Optional[Sequence[str]] = None,
              dim_units: Optional[Sequence[str]] = None,
              ) -> ParsedData:
    """
    Take a user-supplied np.ndarray and header and compile them into either images or a kspace.

    Args:
        data: An np.ndarray containing either complex or real values.
        dim_names: A sequence of strings resembling the dimension names of the data.
        dim_lengths: A sequence of strings resembling the dimension names of the data.
        dim_units: A sequence of strings resembling the dimension names of the data.

    Returns:
        A ParsedData object.

    """
    if dim_names is None:
        dim_names = list()
        for i in reversed(range(data.ndim)):
            dim_names.append(f"dim{i}")
    dim_names = tuple(dim_names)

    if dim_units is None:
        dim_units = ["pixel"] * data.ndim
    dim_units = tuple(dim_units)

    if dim_lengths is None:
        dim_lengths = data.shape
    dim_lengths = tuple(dim_lengths)

    return ParsedData(data, dim_names, dim_lengths, dim_units)


class NotebookHandler:
    """
    Manages ISMRMRD-files, creates&displays plots inside the notebook.
    """

    def __init__(self, handler: NestedExtension) -> None:
        """
        Set up the handler, create some shortcuts, and print valid combinations for container.

        Args:
            handler: ExtensionHandler used to parse the file and create plots.
        """
        self.handler = handler
        self.valid_combinations: Sequence[str] = handler.get_valid_leaf_type_combinations()
        self.print_valid()

    def display(self, combination: str) -> PlotWrapper:
        """
        Display a plot in a notebook cell.

        Args:
            combination: A "name:type" combination.

        Returns:
            A PlotWrapper object.
        """
        if combination not in self.valid_combinations:
            raise ValueError(f"{combination} is not a valid key. "
                             "Use NotebookHandler.print_valid to see valid combinations.")
        l_name = c_name = type_ = ""
        if combination.count(";") == 1:
            c_name, type_ = combination.split(";")
        elif combination.count(";") == 0:
            l_name = combination

        plot = self.handler.create_plot(leaf_name=l_name, container_name=c_name, container_type=type_)
        show(plot)

        return PlotWrapper(plot)

    def print_valid(self):
        print("Valid arguments for NotebookHandler.display are:\n")
        print("\n".join(self.valid_combinations))
