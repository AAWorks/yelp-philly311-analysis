"""
Exploratory ranking: mismatch between 311 burden and Yelp rating.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH, COLOR_SCHEME_DIVERGING
from ..common.transforms import add_mismatch_score


def build_chart(metrics_by_zip: pd.DataFrame, min_restaurants: int = 1, top_n: int = 20) -> alt.Chart:
    ranked = add_mismatch_score(metrics_by_zip)
    ranked = ranked.loc[ranked["n_restaurants"] >= min_restaurants].copy()
    ranked = ranked.sort_values("mismatch_311_vs_yelp", ascending=False).head(top_n)

    return (
        alt.Chart(ranked)
        .mark_bar()
        .encode(
            y=alt.Y("zip_code:N", sort="-x", title="ZIP"),
            x=alt.X("mismatch_311_vs_yelp:Q", title="Mismatch (z_yelp - z_complaints)"),
            color=alt.Color(
                "mismatch_311_vs_yelp:Q",
                scale=alt.Scale(scheme=COLOR_SCHEME_DIVERGING),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("mismatch_311_vs_yelp:Q", format=".2f"),
                alt.Tooltip("yelp_rating_wtd:Q", format=".2f"),
                alt.Tooltip("complaints_per_restaurant:Q", format=".2f"),
            ],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Top ZIP Mismatch Ranking")
    )
