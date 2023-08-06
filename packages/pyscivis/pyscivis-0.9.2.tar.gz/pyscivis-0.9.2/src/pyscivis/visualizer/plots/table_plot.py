from typing import Any, Dict, List, Optional

from bokeh.models import ColumnDataSource, DataTable, TableColumn, LayoutDOM

from pyscivis.visualizer.plots.base_plot import BasePlot
from pyscivis.visualizer.plots.components.loading_div import LoadingDiv


class TablePlot(BasePlot):
    """ Create a Table from the supplied column-dictionary. """
    def __init__(self,
                 column_dict: Dict[str, List[Any]],
                 loading_indicator: Optional[LoadingDiv] = None,
                 **kwargs: Any) -> None:
        """
        Set up CDS and Table-kwargs.

        Args:
            column_dict: Dictionary containing (column-name, List of values)-key-value pairs.
            loading_indicator: None in notebook, LoadingDiv in standalone, used to print messages in the Loading-screen.
            **kwargs: Additional keyword-arguments supplied to the Table.

        Notes:
            For a list of possible keyword-arguments see https://docs.bokeh.org/en/latest/docs/reference/models/widgets.tables.html#bokeh.models.widgets.tables.DataTable .
        """
        if loading_indicator is not None:
            loading_indicator.set_text("Filling table rows...")
        source = ColumnDataSource(data=column_dict)

        columns = [
            TableColumn(field=field_name, title=field_name.capitalize()) for field_name in column_dict
        ]

        self.table_kwargs = dict(source=source, columns=columns, **kwargs)

    def get_layout(self) -> LayoutDOM:
        """
        Fill table keyword-args into DataTable-Constructor.

        Returns:
            A bokeh-DataTable object.
        """
        return DataTable(sizing_mode="stretch_both", sortable=False, reorderable=False, **self.table_kwargs)
