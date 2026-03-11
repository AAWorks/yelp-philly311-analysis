"""
Shared layout helpers for charts.
"""

import altair as alt

from .theme import MAP_HEIGHT


def with_thin_spacer(chart: alt.Chart, spacer_width: int = 2) -> alt.HConcatChart:
    spacer = (
        alt.Chart(alt.Data(values=[]))
        .mark_geoshape(fillOpacity=0, strokeOpacity=0)
        .properties(width=spacer_width, height=MAP_HEIGHT)
    )
    return chart | spacer
