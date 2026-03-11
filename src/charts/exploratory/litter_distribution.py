"""
Exploratory distribution/trend for Litter Index.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH


def build_histogram(litter_index: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(litter_index)
        .mark_bar(opacity=0.8)
        .encode(
            x=alt.X("division_score:Q", bin=alt.Bin(maxbins=30), title="Division score"),
            y=alt.Y("count():Q", title="District count"),
            tooltip=[alt.Tooltip("count():Q", title="Count")],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Litter Index Distribution")
    )

def build_trend(litter_trend: pd.DataFrame, top_n: int = 25) -> alt.Chart:
    trend = litter_trend.copy()
    trend = trend.sort_values("division_score_delta", ascending=False).head(top_n)

    return (
        alt.Chart(trend)
        .mark_bar()
        .encode(
            y=alt.Y("division_num:N", sort="-x", title="Division"),
            x=alt.X("division_score_delta:Q", title="Score delta (latest - earliest)"),
            tooltip=[
                alt.Tooltip("division_num:N", title="Division"),
                alt.Tooltip("division_score_earliest:Q", format=".2f"),
                alt.Tooltip("division_score_latest:Q", format=".2f"),
                alt.Tooltip("division_score_delta:Q", format=".2f"),
            ],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Largest Litter Score Changes")
    )
