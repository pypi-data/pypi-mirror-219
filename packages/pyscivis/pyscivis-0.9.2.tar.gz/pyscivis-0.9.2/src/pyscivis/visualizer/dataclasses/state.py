from typing import Dict, Tuple, Optional, List

import attr
import desert
from json.decoder import JSONDecodeError


@attr.s
class AxesState:
    """
    A dataclass containing the name of the x- and y-axis.

    Args:
        x_axis (str): Name of the current x_axis.
        y_axis (str): Name of the current y_axis.

    See Also:
        DimensionState
    """
    x_axis: str = attr.ib()
    y_axis: str = attr.ib()


@attr.s
class DimensionState:
    """
    A dataclass containing the state of all dimensions, including the active axes.

    Args:
        axes (AxesState): AxesState of the current axes.
        dimensions (Dict[str, int]): Maps dimension names to their values.

    See Also:
        State
    """
    axes: AxesState = attr.ib()
    dimensions: Dict[str, int] = attr.ib()


@attr.s
class RangeState:
    """
    A dataclass containing the state of a BokehRange.

    Args:
        start (float): Start value of the range.
        end (float): End value of the range.
        bounds (Tuple[float, float]): (Start, End)-tuple defining hard zooming-/scrolling-bounds.

    See Also:
        ImageState
    """
    start: float = attr.ib()
    end: float = attr.ib()
    bounds: Tuple[float, float] = attr.ib(converter=tuple)


@attr.s
class ROIState:
    """
    A dataclass containing the state of the region-of-interest (drawn rectangle).

    Args:
        x (List[float]): A list containing one x-axis-coordinate.
        y (List[float]): A list containing one y-axis-coordinate.
        width (List[float]): A list containing one width-value.
        height (List[float]): A list containing one height-value.

    See Also:
        ImageState
    """
    x: List[float] = attr.ib()
    y: List[float] = attr.ib()
    width: List[float] = attr.ib()
    height: List[float] = attr.ib()

    @x.validator
    @y.validator
    @width.validator
    @height.validator
    def valid_length(self, attribute: attr.Attribute, value: List):
        """
        Check if the attribute contains exactly one or no element.

        Args:
            attribute: The attribute to check.
            value: The value to be checked.
        """
        if len(value) > 1:
            raise ValueError(f"'{attribute.name}'({value}) must be of length <= 1.")


@attr.s
class ImageState:
    """
    A dataclass containing the state of an Image.

    Args:
        x_range (RangeState): RangeState of the x-range.
        y_range (RangeState): RangeState of the y-range.
        roi (ROIState): ROIState of the region-of-interest.

    See Also:
        State
    """
    x_range: RangeState = attr.ib()
    y_range: RangeState = attr.ib()
    roi: ROIState = attr.ib()


@attr.s
class ProfileState:
    """
    A dataclass containing the state of all Profile-figures.

    Args:
        x (Optional[int]): x-Click-coordinate for profile calculation.
        y (Optional[int]): y-Click-coordinate for profile calculation.

    See Also:
        State
    """
    x: Optional[int] = attr.ib()
    y: Optional[int] = attr.ib()


@attr.s
class PaletteState:
    """
    A dataclass containing the state palette settings.

    Args:
        name (str): Name of the selected palette.
        length (int): Palette-size of all palettes.
        window (Tuple[float, float]): Windowing (start, end)-tuple-
        cutoff (Tuple[float, float]): Cutoff (start, end)-tuple.

    See Also:
        State
    """
    name: str = attr.ib()
    length: int = attr.ib()
    window: Tuple[float, float] = attr.ib(converter=tuple)
    cutoff: Tuple[float, float] = attr.ib(converter=tuple)


@attr.s
class State:
    """
    A dataclass containing the compiled state of all substates.

    Args:
        dimension (DimensionState): DimensionState of the dimensions.
        image (ImageState): ImageState of image.
        profile (ProfileState): ProfileState of profiles.
        palette (PaletteState): PaletteState of palette.
        fit_to_frame (bool): If fit-to-frame is enabled.
        active_color_mapper (int): Index of the active ColorMapper.
        value_kind (Optional[int]): Currently selected value_kind index.
    """
    dimension: DimensionState = attr.ib()
    image: ImageState = attr.ib()
    profile: ProfileState = attr.ib()
    palette: PaletteState = attr.ib()
    fit_to_frame: bool = attr.ib()
    active_color_mapper: int = attr.ib()
    value_kind: Optional[int] = attr.ib(default=None)


StateSchema = desert.schema(State)


def state_from_json(json_state) -> State:  # pragma: nocover
    """
    Convert a JSON-like string to a State object.

    Args:
        json_state: JSON-representation of State object.

    Returns:
        The parsed State object.
    """
    return StateSchema.loads(json_state)


def state_to_json(state: State, **kwargs) -> str:  # pragma: nocover
    """
    Convert a State object to JSON.

    Args:
        state: State object to be converted.
        **kwargs: Additional JSON-dumps keyword-arguments, like 'indent'.

    Returns:
        A JSON-like string.

    """
    return StateSchema.dumps(state, **kwargs)


def is_json_state(string) -> bool:
    """
    Check if a string is a valid JSON-representation of a State object.

    Args:
        string: String to be checked.

    Returns:
        True if the string is a valid JSON-representation of a State object, else False.
    """
    try:
        state_from_json(string)
        return True
    except JSONDecodeError:
        return False
