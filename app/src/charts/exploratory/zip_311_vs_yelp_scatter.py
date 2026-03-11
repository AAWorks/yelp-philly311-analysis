"""
Exploratory scatter: 311 burden vs Yelp rating.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH


def build_chart(metrics_by_zip: pd.DataFrame, min_restaurants: int = 1) -> alt.Chart:
    plot_df = metrics_by_zip.loc[metrics_by_zip["n_restaurants"] >= min_restaurants].copy()

    points = (
        alt.Chart(plot_df)
        .mark_circle(size=70, opacity=0.7)
        .encode(
            x=alt.X("complaints_per_restaurant:Q", title="311 complaints per restaurant"),
            y=alt.Y("yelp_rating_wtd:Q", title="Weighted Yelp rating"),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("complaints_per_restaurant:Q", format=".2f"),
                alt.Tooltip("yelp_rating_wtd:Q", format=".2f"),
                alt.Tooltip("n_restaurants:Q"),
            ],
        )
    )

    trend = points.transform_regression("complaints_per_restaurant", "yelp_rating_wtd").mark_line()

    return (points + trend).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="311 Burden vs Yelp Rating",
    )
