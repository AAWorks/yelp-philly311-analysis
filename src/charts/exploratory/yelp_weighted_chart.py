"""
Exploratory chart: Simple average Yelp rating vs. weighted rating by restaurant size.
"""
import altair as alt
import pandas as pd
import numpy as np

from ..common.layout import with_thin_spacer
from ..common.theme import COLOR_SCHEME_DIVERGING, CHART_HEIGHT, CHART_WIDTH
from ..common.transforms import get_top_mismatch_zips

def build_chart(
    metrics_by_zip: pd.DataFrame,
    yelp_df: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
) -> alt.Chart:
    top = get_top_mismatch_zips(
        metrics_by_zip,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
    )[["zip_code", "mismatch_group", "mismatch_311_vs_yelp"]].copy()

    yelp = yelp_df.copy()
    yelp["stars"] = pd.to_numeric(yelp["stars"], errors="coerce")
    yelp["review_count"] = pd.to_numeric(yelp["review_count"], errors="coerce").fillna(0)
    yelp["weighted_stars"] = yelp["stars"] * yelp["review_count"]

    agg = (
        yelp.groupby("zip_code", as_index=False)
        .agg(
            simple_yelp_rating=("stars", "mean"),
            weighted_stars_sum=("weighted_stars", "sum"),
            total_reviews=("review_count", "sum"),
            n_restaurants=("business_id", "nunique"),
        )
    )

    agg["weighted_yelp_rating"] = (
        agg["weighted_stars_sum"] / agg["total_reviews"].replace(0, np.nan)
    )

    plot_df = agg.merge(top, on="zip_code", how="inner").copy()

    if plot_df.empty:
        return (
            alt.Chart(pd.DataFrame({"text": ["No ZIPs meet the current threshold."]}))
            .mark_text(size=16)
            .encode(text="text:N")
            .properties(width=700, height=60)
        )

    long_df = plot_df.melt(
        id_vars=[
            "zip_code",
            "mismatch_group",
            "mismatch_311_vs_yelp",
            "total_reviews",
            "n_restaurants",
        ],
        value_vars=["simple_yelp_rating", "weighted_yelp_rating"],
        var_name="rating_type",
        value_name="rating",
    )

    long_df["rating_type"] = long_df["rating_type"].replace(
        {
            "simple_yelp_rating": "Simple average",
            "weighted_yelp_rating": "Weighted average",
        }
    )

    def make_group_chart(group_name: str) -> alt.Chart:
        group_plot = plot_df.loc[plot_df["mismatch_group"] == group_name].copy()
        group_long = long_df.loc[long_df["mismatch_group"] == group_name].copy()

        if group_plot.empty:
            return (
                alt.Chart(pd.DataFrame({"text": [f"No ZIPs in group: {group_name}"]}))
                .mark_text(size=14)
                .encode(text="text:N")
                .properties(width=320, height=220, title=group_name)
            )

        zip_order = (
            group_plot.sort_values("mismatch_311_vs_yelp", ascending=False)["zip_code"]
            .tolist()
        )

        rules = (
            alt.Chart(group_plot)
            .mark_rule(color="#9E9E9E", strokeWidth=2)
            .encode(
                x=alt.X("simple_yelp_rating:Q", title="Yelp rating"),
                x2="weighted_yelp_rating:Q",
                y=alt.Y("zip_code:N", title="ZIP", sort=zip_order),
                tooltip=[
                    alt.Tooltip("zip_code:N", title="ZIP"),
                    alt.Tooltip("simple_yelp_rating:Q", title="Simple avg", format=".2f"),
                    alt.Tooltip("weighted_yelp_rating:Q", title="Weighted avg", format=".2f"),
                    alt.Tooltip("total_reviews:Q", title="Total reviews"),
                    alt.Tooltip("n_restaurants:Q", title="Restaurants"),
                    alt.Tooltip("mismatch_311_vs_yelp:Q", title="Mismatch", format=".2f"),
                ],
            )
        )

        points = (
            alt.Chart(group_long)
            .mark_circle(size=95)
            .encode(
                x=alt.X("rating:Q", title="Yelp rating"),
                y=alt.Y("zip_code:N", title="ZIP", sort=zip_order),
                color=alt.Color("rating_type:N", title=None),
                tooltip=[
                    alt.Tooltip("zip_code:N", title="ZIP"),
                    alt.Tooltip("rating_type:N", title="Metric"),
                    alt.Tooltip("rating:Q", title="Rating", format=".2f"),
                    alt.Tooltip("total_reviews:Q", title="Total reviews"),
                    alt.Tooltip("n_restaurants:Q", title="Restaurants"),
                    alt.Tooltip("mismatch_311_vs_yelp:Q", title="Mismatch", format=".2f"),
                ],
            )
        )

        return (rules + points).properties(
            width=320,
            height=220,
            title=group_name,
        )

    left = make_group_chart("Yelp higher than complaints predict")
    right = make_group_chart("Yelp lower than complaints predict")

    return alt.hconcat(left, right, spacing=30).resolve_scale(
        color="shared"
    ).properties(
        title="Weighted vs. Simple Yelp Ratings in Top Mismatch ZIPs"
    )
