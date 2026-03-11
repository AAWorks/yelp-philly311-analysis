"""
Interactive-style robustness comparison charts.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH


def build_view(metrics_by_zip: pd.DataFrame, min_restaurants: int = 1) -> alt.VConcatChart:
    data = metrics_by_zip.loc[metrics_by_zip["n_restaurants"] >= min_restaurants].copy()

    by_burden = (
        alt.Chart(data)
        .mark_circle(size=65, opacity=0.75)
        .encode(
            x=alt.X("complaints_per_restaurant:Q", title="Complaints per restaurant"),
            y=alt.Y("yelp_rating_wtd:Q", title="Weighted Yelp rating"),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("complaints_per_restaurant:Q", format=".2f"),
                alt.Tooltip("yelp_rating_wtd:Q", format=".2f"),
            ],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Metric A: Per-Restaurant Burden")
    )

    by_raw = (
        alt.Chart(data)
        .mark_circle(size=65, opacity=0.75)
        .encode(
            x=alt.X("complaints:Q", title="Raw complaints"),
            y=alt.Y("yelp_rating_wtd:Q", title="Weighted Yelp rating"),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("complaints:Q", format=".0f"),
                alt.Tooltip("yelp_rating_wtd:Q", format=".2f"),
            ],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Metric B: Raw Complaints")
    )

    return by_burden & by_raw
