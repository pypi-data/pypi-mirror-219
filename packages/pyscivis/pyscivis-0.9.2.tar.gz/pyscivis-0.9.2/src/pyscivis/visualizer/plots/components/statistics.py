from typing import Any, Dict, Union, Optional

import numpy as np

from bokeh.models import Div
from bokeh.layouts import column
from pyscivis.visualizer.dataclasses.handler import CurrentAxesMetaData

from ...util import format_


class StatisticsFigure:
    """
    Calculate and display statistics based on the provided data and metadata.
    """

    def __init__(self,
                 arr: np.ndarray,
                 metadata: CurrentAxesMetaData,
                 max_calc_size: int,
                 **kwargs: Any
                 ) -> None:
        """
        Set up HTML-table and its stylesheet and create initial statistics.

        Args:
            arr: N-dimensional numpy-array.
            metadata: CurrentAxesMetaData.
            max_calc_size: Threshold for calculating statistics, if the data-size
                is higher than this a Placeholder will be used.
            **kwargs: Kwargs for styling the statistics-layout directly passed on to the LayoutDOM.
        """
        self.stats = dict()  # the most recent statistics are saved here for external access

        style_div = Div(text=
                        "<style type='text/css'>"
                        ".statistics-table {font-family: Arial, Helvetica, sans-serif; border-collapse: collapse}"     
                        ".statistics-table td{border: 1px solid #ddd;padding: 4px;}"        
                        ".statistics-table tr:nth-child(even){background-color: #f2f2f2;}"        
                        ".statistics-table tr:hover {background-color: #ddd;}"
                        "</style>", visible=False)
        self._text_div = Div(css_classes=["statistics-table"], sizing_mode="stretch_width")
        self._metadata = metadata
        self._max_calc_size = max_calc_size

        self.layout = column(style_div, self._text_div, **kwargs)
        self.update(arr)

    def update(self,
               arr: np.ndarray,
               metadata: Optional[CurrentAxesMetaData] = None
               ) -> None:
        """
        Update statistics.

        Args:
            arr: 2-dimensional numpy-array.
            metadata: CurrentAxesMetaData.
        """
        if metadata:
            self._metadata = metadata
        self.stats = self._get_stats_from_arr(arr)
        self._text_div.text = self._compile_text(self.stats)

    def _get_stats_from_arr(self, arr: np.ndarray) -> Dict[str, Union[str, float]]:
        flat_arr = arr.ravel()
        pixel_count = len(flat_arr)
        if pixel_count > self._max_calc_size:
            mean = std = median = iqr = "2ManyVals"
        elif len(flat_arr[~np.isnan(flat_arr)]) == 0:
            mean = std = median = iqr = "No data"
        else:
            flat_arr = flat_arr[~np.isnan(flat_arr)]
            mean = np.mean(flat_arr)
            std = np.std(flat_arr)
            median = np.median(flat_arr)
            iqr = np.subtract(*np.percentile(flat_arr, [75, 25]))

        x_unit = self._metadata.x.unit
        y_unit = self._metadata.y.unit
        x_length = self._metadata.x.length
        y_length = self._metadata.y.length
        x_size = self._metadata.x.size
        y_size = self._metadata.y.size
        area = (arr.shape[1] * x_length/x_size) *\
               (arr.shape[0] * y_length/y_size)
        area_unit = f"{x_unit}²" if x_unit == y_unit else f"{x_unit}*{y_unit}"
        return dict({"mean": mean, "median": median, "std": std, "iqr": iqr, "pixel_count": pixel_count, "area": area, "area_unit": area_unit})

    @staticmethod
    def _compile_text(stats: Dict[str, Union[str, float]]) -> str:
        return f"""
        <table class='statistics-table'><tbody>
        <tr><td>Mean</td><td>{format_(stats["mean"])}</td></tr>
        <tr><td>Median</td><td>{format_(stats["median"])}</td></tr>
        <tr><td>Standard deviation</td><td>{format_(stats["std"])}</td></tr>
        <tr><td>IQR</td><td>{format_(stats["iqr"])}</td></tr>
        <tr><td>Amount Pixel</td><td>{stats["pixel_count"]}</td></tr>
        <tr><td>Area</td><td>{stats["area"]:.1f} {stats["area_unit"]}</td></tr>
        """
