import ctypes
import collections
from typing import Any, Dict, List, Tuple, Callable, Iterator, Union

"""
This module includes miscellaneous helper functions. 
"""

def to_string(obj: Any) -> str:
    if isinstance(obj, (ctypes.Array, collections.Sequence)):  # might as well check sequence
        return ", ".join(obj)
    else:
        return str(obj)


def format_(val: Union[float, str],
            lower_bound: int = 3,
            upper_bound: int = 5
            ) -> str:
    if isinstance(val, str):
        return val

    if val < 10**-lower_bound or val > 10**upper_bound:
        return "{:.2e}".format(val)
    else:
        return "{:.2f}".format(val)


Palette = Tuple[str]


def create_palettes(length: int,
                    name_func_map: Dict[str, str]
                    ) -> Dict[str, List[Palette]]:
    """
    Take length of palettes and a name-funcname-map, call func from bokeh.palettes and create multiple palette-lists.

    Args:
        length: Size of the biggest palette
        name_func_map: Pairs of palette names and bokeh.palette-function names, e.g. {"TurboPalette": "turbo"}

    Returns:
        A dict mapping palette names to a list of palettes
    """
    import bokeh.palettes as bp

    def palette(plt_func: Callable[[int], Palette],
                size: int
                ) -> Iterator[Palette]:
        i = 0
        while i < size:
            yield plt_func(i + 1)
            i += 1

    palette_map = dict()
    for name, func_name in name_func_map.items():
        func: Callable[[int], Palette] = getattr(bp, func_name)
        palette_map[name] = list(palette(func, length))

    return palette_map