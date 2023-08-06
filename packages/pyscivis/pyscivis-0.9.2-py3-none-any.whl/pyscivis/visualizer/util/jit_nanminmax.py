from typing import Union, Tuple, List

import numba as nb
import numpy as np
from math import isinf, inf, nan


@nb.njit(fastmath=True)
def _minmax_nan(array: Union[list, np.ndarray]) -> Tuple[float, float]:
    """ Dynamically calculate the nanmin and nanmax values of an array. """
    maximum = -inf
    minimum = inf
    for i in array:
        if i > maximum:
            maximum = i
        if i < minimum:
            minimum = i
    if isinf(minimum):
        minimum = nan
        maximum = nan
    return minimum, maximum


@nb.njit(parallel=True)
def _minmax_chunks_nan(array: Union[list, np.ndarray],
                       chunk_ranges: np.ndarray
                       ) -> Tuple[float, float]:
    """ Parallelize calling of "_minmax_nan"using chunks and return the final result. """
    n_chunks = len(chunk_ranges)
    max_results = [-inf] * n_chunks
    min_results = [inf] * n_chunks
    for i in nb.prange(n_chunks):
        start = chunk_ranges[i][0]
        end = chunk_ranges[i][1]
        chunk_minimum, chunk_maximum = _minmax_nan(array[start:end])
        min_results[i] = chunk_minimum
        max_results[i] = chunk_maximum
    return min(min_results), max(max_results)  # stdlib min/max ignore nans


def even_chunk_sizes(dividend: int,
                     divisor: int
                     ) -> List[int]:
    """ Calculate even chunk sizes. """
    quotient, remainder = divmod(dividend, divisor)
    cells = [quotient for _ in range(divisor)]
    for i in range(remainder):
        cells[i] += 1
    return cells


def even_chunk_ranges(dividend: int,
                      divisor: int
                      ) -> List[Tuple[int, int]]:
    """ Calculate chunk ranges in form of '[(start_0, end_0), ..., (start_n-1, end_n-1)]'. """
    sizes = even_chunk_sizes(dividend, divisor)
    ranges = []
    start = 0
    for s in sizes:
        end = start + s
        ranges.append((start, end))
        start = end
    return ranges


def fast_nanminmax(array: Union[list, np.ndarray],
                   n_chunks: int
                   ) -> Tuple[float, float]:
    """
    Custom function returning the equivalent of (np.nanmin, np.nanmax).
    To improve performance and parallelize both operations Numba's JIT and it's parallel-option is leveraged.

    The array is split into multiple chunks whose min-max calculation is then distributed over multiple threads.

    Args:
        array: 1D array to calculate min & max on.
        n_chunks: Amount of chunks that should be used to split the array.

    Returns:
        A (min, max)-tuple.
    """
    if array.size < 10000000:
        return np.nanmin(array), np.nanmax(array)
    chunk_ranges = np.array([
        [start, end]
        for start, end
        in even_chunk_ranges(len(array), n_chunks)
    ], dtype=np.int64)
    return _minmax_chunks_nan(array, chunk_ranges)
