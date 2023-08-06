from typing import List, Any

import attr
import desert
import toml


@attr.s
class ImageConfig:
    """
    A dataclass containing various configuration options that mainly concern the displayed plots and image.

    This class should not be edited, instead use "config.toml" to edit config-values.
    Use ">pyscivis -c" to get the path to your "config.toml".
    Consider checking "config.py" to get an overview over possible arguments.

    See Also:
        Config
    """
    initial_color_mapper: str = attr.ib(default="Linear",
                                        validator=attr.validators.in_(["Linear", "Log"]))
    initial_value_kind: str = attr.ib(default="Real",
                                      validator=attr.validators.in_(["Real", "Imaginary", "Abs", "Phase"]))
    initial_palette: str = attr.ib(default="Greyscale")
    initial_palette_size: int = attr.ib(default=100,
                                        validator=attr.validators.in_(range(1, 257)))

    palette_names: List[str] = attr.ib(default=["Greyscale", "Turbo", "Inferno"])
    palette_funcs: List[str] = attr.ib(default=["grey", "turbo", "inferno"])
    palette_size: int = attr.ib(default=100,
                                validator=attr.validators.in_(range(1, 257)))

    preload_bounds: bool = attr.ib(default=False)

    log_span: List[int] = attr.ib(default=[1, 10])

    histogram_bins: int = attr.ib(default=20)
    max_calc_size: int = attr.ib(default=4000*4000)

    ds_downsample_images_threshold: int = attr.ib(default=1024)
    ds_threshold: int = attr.ib(default=512)
    ds_throttle: int = attr.ib(default=50)

    pref_height: int = attr.ib(default=450)
    min_height: int = attr.ib(default=300)
    max_height: int = attr.ib(default=500)
    min_width: int = attr.ib(default=200)
    max_width: int = attr.ib(default=600)
    border: int = attr.ib(default=50)

    format_state: bool = attr.ib(default=False)

    @histogram_bins.validator
    @ds_downsample_images_threshold.validator
    @ds_threshold.validator
    @ds_throttle.validator
    @pref_height.validator
    @max_height.validator
    @min_height.validator
    @max_width.validator
    @min_width.validator
    @border.validator
    def positive_int(self, attribute: attr.Attribute, value: int):
        """ Validator to assert that int-attributes are non-negative."""
        if value < 0:
            raise ValueError(f"'{attribute.name}'({value}) must be positive. Re-check the config-file.")

    def __attrs_post_init__(self):
        if self.max_height < self.min_height:
            raise ValueError(f"'max_height'({self.max_height}) cannot be smaller "
                             f"than 'min_height'({self.min_height}). Re-check the config-file.")
        if self.max_width < self.min_width:
            raise ValueError(f"'max_width'({self.max_width}) cannot be smaller "
                             f"than 'min_width'({self.min_width}). Re-check the config-file.")

        if self.initial_palette not in self.palette_names:
            raise ValueError("'initial_palette' must be in 'palette_names': "
                             f"{self.initial_palette} not in {self.palette_names}."
                             "Re-check the config-file")

        if self.initial_palette_size > self.palette_size:
            raise ValueError(f"'initial_palette_size'({self.initial_palette_size}) cannot be smaller "
                             f"than 'palette_size'({self.palette_size}). Re-check the config-file.")

        if len(self.palette_names) != len(self.palette_funcs):
            raise ValueError(f"Length of 'palette_names'({len(self.palette_names)}) must be equal to "
                             f"length of 'palette_funcs'({len(self.palette_funcs)}). Re-check the config-file.")

        bp = get_bokeh_palettes()
        for func in self.palette_funcs:
            try:
                getattr(bp, func)
            except AttributeError:
                raise ValueError(f"'{func}' from 'palette_funcs' does not exist in 'bokeh.palettes'. "
                                 f"Re-check the config-file.")


@attr.s
class NotebookConfig:
    """
    A dataclass containing various configuration options that concern Jupyter notebook-specific settings.

    Args:
        ports (List[int]): Port-range to be used for use in docker-image.

    See Also:
        Config
    """
    ports: List[int] = attr.ib(default=[50001, 50020])

    @ports.validator
    def valid_port_range(self, attribute: attr.Attribute, value: List[int]):
        """ Validator to make sure ports are not nonsensical, i.e, negative or port0 > port1. """
        if min(value) <= 0:
            raise ValueError(f"'{attribute.name}'({value}) must only contain positive integers."
                             f" Re-check the config-file.")
        if value[0] > value[1]:
            raise ValueError(
                f"'{attribute.name}'({value}) first value in port range cannot be bigger than second value."
                f" Re-check the config-file.")


@attr.s
class ParserConfig:
    """
    A dataclass containing various configuration options that concern parser-specific settings.

    Args:
        chunk_size (int): The size (in Bytes) of chunks to be read from Acquisitions.
            Bigger chunks might be somewhat faster while smaller chunks make it possible
            to offer more feedback on how much progress was made loading data.
        always_save_mmap (bool): [NOT IMPLEMENTED] Whether to always save parsed data in a custom mmap.
        collapse_parallel (bool): Whether to delete no-information data that has its origins in the
            parallel-imaging acceleration-factor.

    Warning: Always keep chunk_size over at least 50MByte to avoid severe performance drops.

    See Also:
        Config
    """
    chunk_size: int = attr.ib(default=500 * 1000 * 1000)  # 500 MB
    always_save_mmap: bool = attr.ib(default=False)
    collapse_parallel: bool = attr.ib(default=False)

    @chunk_size.validator
    def valid_chunk_size(self, attribute: attr.Attribute, value: int):
        """ Validator to assert that the chunk size is non-negative."""
        if value <= 0:
            raise ValueError(f"'{attribute.name}'({value}) must be positive. Re-check the config-file.")


@attr.s
class Config:
    """
    A dataclass containing the compiled configuration from multiple subconfigs.

    Args:
        image (ImageConfig): ImageConfig data for the image and its plots.
        notebook (NotebookConfig): NotebookConfig data for the notebook-app.
        parser (ParserConfig): ParserConfig data for the parser.
    """
    image: ImageConfig = attr.ib()
    notebook: NotebookConfig = attr.ib()
    parser: ParserConfig = attr.ib()


ConfigSchema = desert.schema(Config)


def load_config(file_path) -> Config:  # pragma: nocover
    """
    Load configuration file into a dataclass object.

    Args:
        file_path: File path of the configuration file.

    Returns:
        A Config object filled with data from the configuration file.
    """
    return ConfigSchema.load(toml.load(file_path))


def get_bokeh_palettes() -> Any:
    # This is necessary to avoid having a hard dependency when testing configs
    import bokeh.palettes as bp
    return bp
