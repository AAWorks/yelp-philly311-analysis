"""
Exploratory chart: Restaurant count by mismatch score.
"""
import altair as alt
import pandas as pd
import numpy as np

from ..common.theme import CHART_HEIGHT, CHART_WIDTH
from ..common.transforms import add_mismatch_score, get_top_mismatch_zips, classify_complaint_detail

def build_chart(
    metrics_by_zip: pd.DataFrame,
    min_restaurants: int = 3,
) -> alt.Chart:
    df = add_mismatch_score(metrics_by_zip)
    df = df.loc[df["n_restaurants"] >= min_restaurants].copy()
    df["abs_mismatch"] = df["mismatch_311_vs_yelp"].abs()
    df["mismatch_direction"] = np.where(
        df["mismatch_311_vs_yelp"] >= 0,
        "Yelp higher than complaints predict",
        "Yelp lower than complaints predict",
    )

    top = df.nlargest(6, "abs_mismatch").copy()

    base = alt.Chart(df)

    points = base.mark_circle(size=85, opacity=0.8).encode(
        x=alt.X("n_restaurants:Q", title="Restaurants in ZIP"),
        y=alt.Y("abs_mismatch:Q", title="Absolute mismatch magnitude"),
        color=alt.Color(
            "mismatch_311_vs_yelp:Q",
            title="Mismatch",
            scale=alt.Scale(scheme="redblue", reverse=True),
        ),
        tooltip=[
            alt.Tooltip("zip_code:N", title="ZIP"),
            alt.Tooltip("n_restaurants:Q", title="Restaurants"),
            alt.Tooltip("complaints:Q", title="311 complaints"),
            alt.Tooltip("complaints_per_restaurant:Q", title="Complaints per restaurant", format=".2f"),
            alt.Tooltip("yelp_rating_wtd:Q", title="Weighted Yelp rating", format=".2f"),
            alt.Tooltip("mismatch_311_vs_yelp:Q", title="Mismatch", format=".2f"),
        ],
    )

    labels = alt.Chart(top).mark_text(
        align="left",
        baseline="middle",
        dx=7,
        fontSize=11,
    ).encode(
        x="n_restaurants:Q",
        y="abs_mismatch:Q",
        text="zip_code:N",
    )

    return (points + labels).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        title="Mismatch vs. Restaurant Coverage",
    )
