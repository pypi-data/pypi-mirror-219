"""
This module was adapted from https://github.com/esa-esdl/gridtools

                        The MIT License (MIT)

Copyright (c) 2016, Brockmann Consult GmbH and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Tuple, Any

from numba import prange, njit
import numpy as np

_EPS = 1e-10

def downsample_2d_mean_nojit(src: np.ndarray,
                       shape: Tuple[int, int],
                       fill_value: Any = np.nan
                       ) -> np.ndarray:
    """
    Downsample a 2D-numpy-array to the specified shape.

    Args:
        src: 2D-array to be downsampled.
        shape: (height, width)-shape of the downsampled array.
        fill_value: Value to be used instead infinitesimal values (< 1e-10).

    Returns:
        A downsampled numpy-array with the specified shape.

    Raises:
        ValueError: If specified shape is larger than source shape at any point.

    Notes:
        Adapted from https://github.com/esa-esdl/gridtools/blob/master/gridtools/resampling.py#L309
    """
    src_h, src_w = src.shape
    out_h, out_w = shape
    out = np.empty(shape, dtype=src.dtype)
    if src_w == out_w and src_h == out_h:
        return src

    if out_w > src_w or out_h > src_h:
        raise ValueError("invalid target size")

    scale_x = src_w / out_w
    scale_y = src_h / out_h

    for out_y in prange(out_h):
        src_yf0 = (scale_y * out_y)
        src_yf1 = (src_yf0 + scale_y)
        src_y0 = int(src_yf0)
        src_y1 = int(src_yf1)

        wy0 = 1.0 - (src_yf0 - src_y0)
        wy1 = src_yf1 - src_y1
        if wy1 < _EPS:
            wy1 = 1.0
            if src_y1 > src_y0:
                src_y1 -= 1
        for out_x in range(out_w):
            src_xf0 = (scale_x * out_x)
            src_xf1 = src_xf0 + scale_x
            src_x0 = int(src_xf0)
            src_x1 = int(src_xf1)
            wx0 = 1.0 - (src_xf0 - src_x0)
            wx1 = src_xf1 - src_x1
            if wx1 < _EPS:
                wx1 = 1.0
                if src_x1 > src_x0:
                    src_x1 -= 1
            v_sum = 0.0
            w_sum = 0.0
            for src_y in range(src_y0, src_y1 + 1):
                wy = wy0 if (src_y == src_y0) else wy1 if (src_y == src_y1) else 1.0
                for src_x in range(src_x0, src_x1 + 1):
                    wx = wx0 if (src_x == src_x0) else wx1 if (src_x == src_x1) else 1.0
                    v = src[src_y, src_x]
                    if np.isfinite(v):
                        w = wx * wy
                        v_sum += w * v
                        w_sum += w
            if w_sum < _EPS:
                out[out_y, out_x] = fill_value
            else:
                out[out_y, out_x] = v_sum / w_sum
    return out


downsample_2d_mean = njit(downsample_2d_mean_nojit, nogil=True, parallel=True)
