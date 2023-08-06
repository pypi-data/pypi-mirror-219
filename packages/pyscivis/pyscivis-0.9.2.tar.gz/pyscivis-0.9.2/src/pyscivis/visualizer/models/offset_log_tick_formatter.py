from bokeh.models.formatters import LogTickFormatter
from bokeh.core.properties import Float, Seq


class OffsetLogTickFormatter(LogTickFormatter):
    """
    Format ticks for a logarithmic colormapper while taking negative intervals into account.

    The ticks within the range of logspan are re-mapped to the interval of [low, high].

    Note:
        This class is required to display correct ticks for the OffsetLogColorMapper.

    See Also:
        OffsetLogColorMapper
    """

    #__implementation__ = "offset_log_tick_formatter.ts"

    low = Float(default=0, help="""
        REQUIRED! Should be set to the ColorMapper's low value (equal to min(data) if unspecified)
    """)
    high = Float(default=0, help="""
        REQUIRED! Should be set to the ColorMapper's high value (equal to max(data) if unspecified)
    """)
    log_span = Seq(Float, default=[1, 10], help="""
        This value is used for determining the tick labels. This has only
        to be changed if you change the default log_span of the corresponding
        OffsetLogColorMapper!
    """)
