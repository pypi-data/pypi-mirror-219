import threading
from typing import Any, Optional, Tuple, Union

from tornado import gen

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Spacer, Div, Button, ColumnDataSource, CustomJS, Dropdown
from bokeh.core.property.wrappers import PropertyValueColumnData

from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.plots import ImagePlot
from pyscivis.visualizer.standalone.file_selector import select_file_tkinter, select_file_from_list
from pyscivis.visualizer.util.themes import theme_map
from pyscivis.visualizer.extensions import FlatExtension, NestedExtension
from pyscivis.visualizer.extensions import extension_manager as ext_manager
from pyscivis.visualizer.demo import demo

from pyscivis.visualizer.plots.components.loading_div import LoadingDiv
from pyscivis.visualizer.models import Tree
from pyscivis.visualizer.dataclasses.config import Config


class MainComponent:
    """
    Main component displayed in the standalone app.
    """

    def __init__(self,
                 config: Config,
                 file: Optional[str] = None,
                 noselector: bool = False,
                 server: Optional[str] = None,
                 **kwargs: Any
                 ) -> None:
        """
        Set up file-selector and its callback, show file if necessary and initialize intro-button.

        Args:
            config: Config object.
            file: If there is a file to be displayed initially.
            noselector: If the file-selector should be hidden.
            **kwargs: Keyword arguments being swallowed.
        """
        self.config = config
        self.leaf_dict = dict()
        self.loading_div = LoadingDiv()

        ext_manager.check_extension_validity()
        if not noselector:  # create File-Selection button
            valid_extensions = ext_manager.get_supported_files()

            def sel_file_wrapper(extension_name: str):
                multiple = ext_manager.extension_allows_multiple(extension_name)
                if server is None:
                    filename = select_file_tkinter(extension_name, valid_extensions, multiple)
                    if filename:
                        self.update(filename, extension_name)
                else:
                    file_root = server
                    valid_ext_names = [filetype for alias, _, filetype in valid_extensions if alias == extension_name][0]
                    tree = select_file_from_list(file_root, valid_ext_names)

                    tree_widget = Tree(tree=tree, sizing_mode="stretch_both")
                    saved_layout = self.layout.children[0]
                    for layout in self.layout.children:
                        layout.visible = False
                    self.layout.children[0] = tree_widget

                    def select_file_and_restore_layout(attr, old, new):
                        _, filename, _ = new
                        self.layout.children[0] = saved_layout
                        for layout in self.layout.children:
                            layout.visible = True
                        self.update(filename, extension_name)
                    tree_widget.on_change("selected", select_file_and_restore_layout)

            file_input_btn = Dropdown(label="Select File", menu=[(desc, alias) for alias, desc, _ in valid_extensions])
            file_input_btn.on_click(lambda x: sel_file_wrapper(x.item))
        else:
            file_input_btn = Spacer()

        self.layout = row(column(file_input_btn, Spacer()),
                          column(Div(), sizing_mode="stretch_both", margin=(50, 50, 50, 50)),
                          column(self.loading_div.layout, width=0, height=0, name="hidden_row")
                          )
        self.layout_backup = None
        self.init_intro()
        self.theme = "default"
        self.init_theme_toggle()


        if file is not None:
            self.update(file)

    def update(self,
               path: str,
               extension_name: Optional[str] = None
               ) -> None:
        """
        Load a new file and update the filetree-widget.

        Args:
            extension_name: Name of extension to be used to handle the file, deduced from file-path if None.
            path: Path of file to be loaded.
        """
        handler: Union[FlatExtension, NestedExtension] = ext_manager.get_extension_handler(
                                                                extension_name=extension_name,
                                                                path=path,
                                                                config=self.config
                                                            )
        if isinstance(handler, NestedExtension):
            tree_list = handler.tree_struct
            self.leaf_dict = handler.data_leaves
            file_tree = Tree(tree=tree_list, theme=self.theme, width=300, height=600)
            file_tree.on_change("selected", lambda attr, old, new: self.change_plot(new, handler))
            self.layout.children[0].children[1] = file_tree
            self.layout.children[1].children[0] = Spacer()  # Space for  plot
        elif isinstance(handler, FlatExtension):
            self.layout.children[0].children[1] = Spacer()  # Delete old FileTree
            self.layout.children[1].children[0] = Spacer()
            self.change_plot(None, handler)

    def change_plot(self, leaf_header: Optional[Tuple[str, str, str]], handler) -> None:
        """
        Change the displayed plot to the one selected with the file-tree.

        Args:
            handler: ExtensionHandler used for parsing and creating the plot.
            leaf_header: (leaf_name, container_name, header)-tuple used to get data from the current file.
        """
        self.loading_div.set_text("Loading plot...")
        #self.layout.children[2].children[0] = self.loading_div.layout  # add loading overlay
        doc = curdoc()

        def calc_and_replace() -> None:  # entry-point for thread
            if leaf_header is not None:
                parent_name, own_name, header_type = leaf_header
                plot = handler.create_plot(
                    container_name=parent_name,
                    leaf_name=own_name,
                    container_type=header_type,
                    loading_div=self.loading_div
                )
            else:
                plot = handler.create_plot(loading_div=self.loading_div)

            @gen.coroutine
            def replace_plot() -> None:
                self.loading_div.hide()
                self.layout.children[1].children[0] = plot.get_layout()
            doc.add_next_tick_callback(replace_plot)  # can only modify doc like this outside of main thread

        # have to start a new thread to keep the main
        # thread idle so that document callbacks can fire
        threading.Thread(target=calc_and_replace).start()

    def init_theme_toggle(self) -> None:
        """
        Initialize the dark-mode toggle with hidden bokeh-buttons.
        """
        dark_js = CustomJS(code="""
                    const dark_styles = document.querySelectorAll(".dark-style")
                    const default_styles = document.querySelectorAll(".default-style")

                    for (let i=0; i<dark_styles.length; i++) {
                        dark_styles[i].removeAttribute("media")
                    }
                    for (let i=0; i<default_styles.length; i++) {
                        default_styles[i].setAttribute("media", "max-width: 1px")
                    }
                    $("#root").jstree("set_theme","default-dark");
                """)

        light_js = CustomJS(code="""
                    const dark_styles = document.querySelectorAll(".dark-style")
                    const default_styles = document.querySelectorAll(".default-style")

                    for (let i=0; i<dark_styles.length; i++) {
                        dark_styles[i].setAttribute("media", "max-width: 1px")
                    }
                    for (let i=0; i<default_styles.length; i++) {
                        default_styles[i].removeAttribute("media")
                    }
                    $("#root").jstree("set_theme","default");
                """)

        def theme_cb(theme):
            self.theme = theme
            curdoc().theme = theme_map[theme]

        btn_light = Button(css_classes=["btn-lightmode"], visible=False)
        btn_light.js_on_click(light_js)
        btn_light.on_click(lambda x: theme_cb("default"))

        btn_dark = Button(css_classes=["btn-darkmode"], visible=False)
        btn_dark.js_on_click(dark_js)
        btn_dark.on_click(lambda x: theme_cb("dark"))

        self.layout.select_one({'name': 'hidden_row'}).children.extend((btn_light, btn_dark))

    def init_intro(self) -> None:
        """
        Initialize the intro-button.
        """
        # The intro button is hidden and invoked from
        # the frontend by calling $(.bokeh-intro).click()
        # which happens if the frontend-only intro-button
        # is clicked
        intro_button = Button(css_classes=["bokeh-intro"], visible=False)
        intro_state = ColumnDataSource(data=dict(step=[-1]))

        intro_state.on_change("data", lambda attr, old, new: self.set_intro_step(new))
        intro_button.js_on_click(CustomJS(args=dict(cds=intro_state),
                                          code="""
                                              window.intro_state = cds
                                          """))

        self.layout.select_one({'name': 'hidden_row'}).children.append(intro_button)

    def set_intro_step(self, new_data: PropertyValueColumnData):
        """
        Start the intro or revert to the initial state, depending on the step provided.

        Args:
            new_data: Dictionary-like object containing a "step" key-value pair.
        """
        if "step" not in new_data.keys():
            raise ValueError("Unexpected CDS-attribute change detected.")
        step = new_data["step"][0]

        if step == 0 and self.layout_backup is None:
            # all the slicing shenanigans are because we need to keep the hidden intro_button in the layout
            # for some reason the server-side callback will be removed if he is not in the layout
            self.layout_backup = self.layout.children[:-1]  # saving the layouts row
            file_input_btn = Button(label="Select File", css_classes=["fileinputbtn", "invisible"])
            file_input_btn.js_on_click(CustomJS(code="setStep(4)"))
            tree_list = [
                {"id": "root", "parent": "#", "text": "Your_File.h5", "type": "file"},
                {"id": "container0", "parent": "root", "text": "dataset0", "type": "container"},
                {"id": "container1", "parent": "root", "text": "dataset1", "type": "container"},
                {"id": "container2", "parent": "root", "text": "dataset1", "type": "container"},
                {"id": "Acq0", "parent": "container0", "text": "ImportantImages", "type": "images"},
                {"id": "Acq1", "parent": "container1", "text": "MoreImportantImages", "type": "images"},
                {"id": "Acq2", "parent": "container2", "text": "MostImportantImages", "type": "images"},
            ]
            file_tree = Tree(tree=tree_list, theme=self.theme, width=300, height=600, css_classes=["invisible"])
            file_tree.js_on_change("selected", CustomJS(code="setStep(5)"))

            images = demo.get_images(640, 525)
            data = ParsedData(images,
                              dim_names=["Images", "Y", "X"],
                              dim_lengths=[3, 600, 1000],
                              dim_units=["pixel", "mm", "mm"])
            plot = ImagePlot(data, self.config.image).get_layout()
            plot.css_classes = ["main-app", "invisible"]
            self.layout.children[:-1] = \
                [
                    column(file_input_btn, file_tree),
                    column(plot, margin=(50, 50, 50, 50))
                 ]

        if step == -1:
            self.layout.children[:-1] = self.layout_backup
            self.layout_backup = None
