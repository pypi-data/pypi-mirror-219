from bokeh.core.properties import Seq, Float
from bokeh.models import LogColorMapper


class OffsetLogColorMapper(LogColorMapper):
    """
    Allow logarithmic colormapping for negative intervals.

    Works exactly the same as its base class, however
    OffsetLogColorMapper also allows mapping datasets
    with negative values. This does not work like mpl's
    symlog but instead we use a standard natural log on
    an interval [1, 10] (unless otherwise specified), which
    the input data interval, e.g, [-5, 51] is then mapped to.

    See Also:
        OffsetLogTickFormatter
    """

    #__implementation__ = 'offset_log_color_mapper.ts'

    log_span = Seq(Float, default=[1, 10], help="""
            This is used to determine the steepness of
            the log-scale.
        """)


if __name__ == '__main__':
    import numpy as np
    from offset_log_tick_formatter import OffsetLogTickFormatter
    from bokeh.models import HoverTool
    from bokeh.palettes import turbo
    from bokeh.models import ColorBar
    from bokeh.plotting import figure
    from bokeh.io import show
    from bokeh.settings import settings
    settings.minified = False
    palette = turbo(256)
    #data_arr = [list(np.arange(-20, -10, 0.1)) for j in range(-10, 10)]
    #data_arr = [list(np.arange(-20, -1, 0.1)) for j in range(-10, 10)]
    data_arr = [list(np.arange(-505, 523, 1)) for j in range(-10, 10)]

    lg = OffsetLogColorMapper(palette)

    c = ColorBar(color_mapper=lg, formatter=OffsetLogTickFormatter(low=np.min(data_arr), high=np.max(data_arr)))
    fig = figure(width=500, height=500, tools=[])
    fig.image(image=[data_arr], x=0, y=0, dw=500, dh=500, color_mapper=lg)
    fig.add_tools(HoverTool(tooltips="@image"))
    fig.add_layout(c, "right")
    show(fig)
