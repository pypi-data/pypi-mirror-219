import concurrent.futures as cf
from typing import Callable, Optional
import os

import numpy as np


def real(arr: np.ndarray) -> np.ndarray:
    """
    Calculate the real part of the specified numpy-array using multiple threads.

    Args:
        arr: Numpy-array with a complex dtype.

    Returns:
        Numpy-array containing the real part of the input array.

    Examples:
        >>> real(np.array([1+2j, 3+4j]))
        array([1., 3.])

    """
    return _tpe_func(arr, np.real)


def imag(arr: np.ndarray) -> np.ndarray:
    """
    Calculate the imaginary part of the specified numpy-array using multiple threads.

    Args:
        arr: Numpy-array with a complex dtype.

    Returns:
        Numpy-array containing the imaginary part of the input array.

    Examples:
        >>> imag(np.array([1+2j, 3+4j]))
        array([2., 4.])
    """
    return _tpe_func(arr, np.imag)


def abso(arr: np.ndarray) -> np.ndarray:
    """
    Calculate the absolute value of each element in the specified numpy-array using multiple threads.

    Args:
        arr: Numpy-array.

    Returns:
        Numpy-array containing the corresponding absolute values.

    Examples:
        >>> abso(np.array([1+2j, 3+4j]))
        array([2.23606798, 5.        ])

        >>> abso(np.array([-1, 3]))
        array([1, 3])

    Notes:
        For complex inputs the modulus (distance between origin and (real, imag) in the complex plane) is calculated.
    """
    return _tpe_func(arr, np.abs)


def angle(arr: np.ndarray) -> np.ndarray:
    """
    Calculate the angle of each complex number in the specified numpy-array using multiple threads.

    Args:
        arr: Numpy-array.

    Returns:
        Numpy-array containing the corresponding angles.

    Examples:
        >>> angle(np.ndarray([1, 1j, 1+1j]))
        array([0.        , 1.57079633, 0.78539816])

    Notes:

    """
    return _tpe_func(arr, np.angle)


def _tpe_func(arr: np.ndarray,
              func: Callable[[np.ndarray], np.ndarray],
              n_chunks: Optional[int] = None,
              fallback_threshold: int = 1000000  # experimenting indicates that 500k is where MT-overhead is amortised
              ) -> np.ndarray:
    """
    Apply the specified function to the specified sequence in a multithreaded fashion.

    This function was conceived to multithread `np.real`, `np.imag`, `np.angle`, and `np.phase`.
    Similar functions might work, but are not supported.

    Args:
        arr: Sequence that the function should be applied on.
        func: Callable to be applied on the sequence.
        n_chunks: Number of chunks the input-array will be cut into. These chunks are then fed to the multithreading-logic.
            By default the number of chunks if derived from the CPU-count. It is capped at the size of the input-array.
        fallback_threshold: Input-arrays with a size less than `fallback_threshold` are handled without multithreading.

    Returns:
        The resulting numpy-ndarray.

    Examples:
        >>> _tpe_func(np.array([1, -2, -3]), np.abs)
        array([1, 2, 3])
    """
    # use np inbuilt if array is too small
    if arr.size < fallback_threshold:  # experimenting indicates that this might be roughly where the MT overhead is amortised
        return func(arr)

    # if n_chunks was not specified: try to determine a good number from the cpu-count (or use 64 as a fallback)
    if n_chunks is None:
        n_cpus = os.cpu_count()
        n_chunks = n_cpus*16 if n_cpus is not None else 64

    n_chunks = min(n_chunks, arr.size)  # cannot have more chunks than array elements
    # chunk array into 'n_chunk' pieces
    arr_flat = arr.ravel()
    arr_chunked = np.array_split(arr_flat, n_chunks)

    # pre-allocate our array that will be filled with the partial results
    thread_results = np.empty(arr.size, dtype="float32")

    # multithreading work
    with cf.ThreadPoolExecutor() as executor:
        index = 0
        for result in executor.map(func, arr_chunked):
            thread_results[index:index+result.size] = result
            index += result.size

    # reshape back to original shape
    return thread_results.reshape(arr.shape)
