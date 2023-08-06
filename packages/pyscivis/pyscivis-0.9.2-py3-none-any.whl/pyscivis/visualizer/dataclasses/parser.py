from typing import Sequence

import attr
from numpy import ndarray


@attr.s()
class ParsedData:
    """
    A dataclass containing the data put together by a Parser.

    The data contained in objects of this class is used by plots to draw onto the canvas.
    All arguments are mandatory, e.g., "dim_lengths" cannot be set to None, even if it is equal to the shape of data.

    Args:
        data (np.ndarray): An n-dimensional numpy-array containing dimension data.
        dim_names (Sequence[str]): A sequence of strings resembling the names of the dimensions.
        dim_lengths (Sequence[float]): A sequence of floats resembling the lengths of the dimensions.
        dim_units (Sequence[str]): A sequence of strings resembling the units of the dimensions.

    Example:
        ParsedData(
            data=np.array([[0, 1], [2, 3]]),
            dim_names=["y", "x"],
            dim_lengths=[2.5, 5],
            dim_units=["mm", "mm"]
        )
    """
    data: ndarray = attr.ib()
    dim_names: Sequence[str] = attr.ib()
    dim_lengths: Sequence[float] = attr.ib()
    dim_units: Sequence[str] = attr.ib()

    def __attrs_post_init__(self):
        n_dim = self.data.ndim
        if n_dim != len(self.dim_names) or \
           n_dim != len(self.dim_lengths) or \
           n_dim != len(self.dim_units):
            raise ValueError(f"`data.ndim ({n_dim})`, `len(dim_names) ({len(self.dim_names)})`,"
                             f" `len(dim_lengths) ({len(self.dim_lengths)})`, and `len(dim_units)"
                             f" ({len(self.dim_units)})` all have to be equal.")
