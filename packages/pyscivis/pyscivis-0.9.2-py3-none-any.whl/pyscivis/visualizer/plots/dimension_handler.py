from typing import Dict, Tuple, Callable, Optional

import numpy as np
import numpy.typing as npt
from functools import lru_cache

from pyscivis.visualizer.plots.components.loading_div import LoadingDiv
from pyscivis.visualizer.plots.components.value_controls import LABEL_FUNC_MAP
from pyscivis.visualizer.dataclasses.parser import ParsedData
from pyscivis.visualizer.dataclasses.handler import Dim, CurrentAxesMetaData
from pyscivis.visualizer.util.jit_nanminmax import fast_nanminmax


class DimensionHandler:
    """
    Handle dimension-related operations.

    Operations performed by this class include:
    - getting the current image
    - changing dimensions
    - calculating minima and maxima
    - getting the profile at a certain point in direction of a specified dimension

    Public attributes are:

    value_handler (Callable[[npt.ArrayLike], npt.ArrayLike]):
    A callable that accepts a numpy-arraylike and returns a numpy-arraylike, e.g., np.real.

    dims (Dict[int, Dim])::
    A dictionary containing dimension-related data and mapping it to the dimension-index.
    """

    def __init__(self,
                 parsed: ParsedData,
                 preload_bounds: bool = False,
                 loading_indicator: Optional[LoadingDiv] = None,
                 ) -> None:
        """
        Do initial validation of the parsed-data and set up class attributes.

        Args:
            parsed (:obj:`ParsedData`): A ParsedData object containing dimension-related data.

        Raises:
            ValueError: If `parsed` has an illegal shape, e.g., less than 2 dimensions or more dim_units than dimensions.
        """
        p = parsed
        if p.data.size == 0:
            raise ValueError("'data' must not be empty.")
        if p.data.ndim < 2:
            raise ValueError("'data' must at least be 2-dimensional")
        if len(p.dim_names) != len(set(p.dim_names)):
            raise ValueError("'names' must contain unique axis-names.")
        if p.data.ndim != len(p.dim_names):
            raise ValueError("'data.ndim' and 'names' must be of same size.")
        if p.data.ndim != len(p.dim_lengths):
            raise ValueError("'data.ndim' and 'lengths' must be of same size.")
        if p.data.ndim != len(p.dim_units):
            raise ValueError("'data.ndim' and 'units' must be of same size.")

        zipped = zip(p.dim_names, p.dim_lengths, p.dim_units)

        self._orig_data = p.data  # used only for having a baseline to manipulate
        self._cur_data = p.data  # used for displaying (set by manipulating _orig_data)
        self.value_handler: Callable[[npt.ArrayLike], npt.ArrayLike] = LABEL_FUNC_MAP["Real"]
        self.dims: Dict[int, Dim] = {index: Dim(name, p.data.shape[index], length, unit) for index, (name, length, unit) in enumerate(zipped)}
        self._order = np.array([i for i in range(p.data.ndim)])
        self._values = np.array([0 for _ in p.dim_names])

        self.preload_bounds = preload_bounds
        self.loading_indicator = loading_indicator

        if preload_bounds:
            for key, func in LABEL_FUNC_MAP.items():
                if loading_indicator is not None:
                    loading_indicator.set_text(f"Pre-loading bounds for {key}...")
                self._get_data_min_max(func)  # save in cache

    def change_axes(self,
                    x_axis: int,
                    y_axis: int
                    ) -> None:
        """
        Take the ids of the new axes and change our data to have these axes last.

        First a transpose-order is determined by removing the specified ids from the original order
        and appending them to the back. This transpose-order is then used to re-order the original data.

        Args:
            x_axis: An integer resembling the index of the new x-axis in `dims`.
            y_axis: An integer resembling the index of the new y-axis in `dims`.
        """
        if x_axis == y_axis:
            raise ValueError(f"x_axis and y_axis cannot be the same. x_axis: {x_axis}, y_axis: {y_axis}")
        new_axes = [y_axis, x_axis]

        transpose_order = list(range(self._orig_data.ndim))
        transpose_order = [dim for dim in transpose_order if dim not in new_axes] + new_axes

        self._order = np.array(transpose_order)
        self._cur_data = np.transpose(self._orig_data, transpose_order)

    def set_dim_value(self,
                      dim_index: int,
                      value: int
                      ) -> None:
        """
        Set the specified dimension-index to the specified value.

        Args:
            dim_index: An integer resembling the index of the dimension to manipulate.
            value: An integer resembling the new value.
        """
        self._values[dim_index] = value

    def get_data(self) -> np.ndarray:
        """
        Return the current image.

        More precisely, the last two (transposed) dimensions are retrieved and the current value_handler
        is applied (i.e., np.real, np.angle, ..) to obtain the relevant portion of the data.

        Returns:
            An image as a 2-dimensional np.ndarray.
        """
        values = self.get_ordered_values()[:-2]
        data = self._cur_data[tuple(values)]
        return self.value_handler(data)

    def get_metadata(self) -> CurrentAxesMetaData:
        """
        Return the metadata of the currently active axes.

        Returns:
            A CurrentAxesMetaData object.
        """
        y, x = self._order[-2:]
        return CurrentAxesMetaData(x=self.dims[x], y=self.dims[y])

    def get_profile(self,
                    dim_id: int,
                    point: Dict[str, int],
                    ) -> np.ndarray:
        """
        Calculate the profile of a dimension at a given point.

        If the specified dimension index happens to be either the active x- or y-axis the profile can be interpreted
        as going along the axis.
        If the specified dimension is not active the profile means going `into` the image in direction of the dimension.

        Args:
            dim_id: The index of the dimension.
            point: A dictionary containing x- and y-coordinates used for the starting point of the profile.

        Returns:
            A 1-dimensional numpy-array containing the profile values of the specified dimension.
        """
        values = self._values.copy()
        # Set the point-coordinates for the active x- and y-dimension
        values[point['x_id']] = point['x_coord']  # no effect if x_id=dim_id
        values[point['y_id']] = point['y_coord']  # no effect if y_id=dim_id

        # Transpose the dimension to be profiled to the back of
        # our data and the dimension values, then retrieve the
        # profile by accessing the data with the dim-values
        transpose_order = list(range(self._orig_data.ndim))
        transpose_order = [dim for dim in transpose_order if dim != dim_id] + [dim_id]
        data = np.transpose(self._orig_data, transpose_order)
        values = values[transpose_order]
        return self.value_handler(data[tuple(values)[:-1]])  # [:-1] means we only get data for dim_id

    def get_ordered_values(self) -> np.ndarray:
        """
        Retrieve the current values in the current order.

        Current order means the order of the dimensions when this method is called, e.g., (1, 2, 0) ^= (y, x, z)
        To access the values for the base dimension-order, e.g., (0, 1, 2), use `_values` directly.

        Returns:
            A 1-dimensional numpy-array containing the ordered values.
        """
        return self._values[self._order]

    def get_local_min_max(self) -> Tuple[float, float]:
        """
        Calculate the minimum and the maximum of the current image (last 2 dimensions).

        Returns:
            A (min, max)-tuple.
        """
        min_ = np.nanmin(self.get_data())
        max_ = np.nanmax(self.get_data())
        return min_.item(), max_.item()

    def get_data_min_max(self) -> Tuple[float, float]:
        """
        Calculate and caches the minimum and maximum of the entire dataset.

        The return value is always the same for non-complex data.
        For complex data there is 4 different (min, max)-tuples possible:
        one for each value_handler, i.e., real, phase, angle, abs.

        Returns:
            A (min, max)-tuple.

        Notes:
            The min-max calculation is done by a custom, parallelized+chunked Numba-JIT script to perform min-max-calculation
                simultaneously. Check "pyscivis/visualizer/util/jit_nanminmax.py" for more information.
        """
        return self._get_data_min_max(self.value_handler)

    @lru_cache()
    def _get_data_min_max(self, value_handler: Callable[[npt.ArrayLike], npt.ArrayLike]) -> Tuple[float, float]:
        """ Helper method to allow caching (by explicitly specifying parameters for the decorator to use) """
        # only want to print the state if there is a loading-div and we are not currently in the process
        # of caching the min and max
        print_state_flag = self.loading_indicator is not None and not self.preload_bounds

        if print_state_flag:
            self.loading_indicator.set_text("Calculating MinMax-Bounds...")

        min_, max_ = fast_nanminmax(value_handler(self._orig_data).ravel(), 16)

        if print_state_flag:
            self.loading_indicator.hide()
        return min_, max_

