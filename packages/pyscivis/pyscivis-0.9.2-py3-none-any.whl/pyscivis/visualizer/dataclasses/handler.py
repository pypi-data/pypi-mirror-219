import attr


@attr.s
class Dim:
    """
    A dataclass containing the metadata of a dimension.

    Args:
        name (str): The name of the dimension, e.g., "X".
        size (int): The amount of elements in the dimension.
        length (float): The actual length of the dimension. Used with unit.
        unit (str): The unit for the dimension length, e.g., "mm".

    See Also:
        CurrentAxesMetaData
    """
    name: str = attr.ib()
    size: int = attr.ib()
    length: float = attr.ib()
    unit: str = attr.ib()


@attr.s
class CurrentAxesMetaData:
    """
    A dataclass containing the dimension-metadata of the currently displayed axes.

    Args:
        x (Dim): Dim metadata for the current x-axis.
        y (Dim): Dim metadata for the current y-axis.
    """
    x: Dim = attr.ib()
    y: Dim = attr.ib()
