"""
Exploratory chart: 311 complain composition for top and bottom mismatch zips.
"""
import altair as alt
import pandas as pd
import numpy as np

from ..common.layout import with_thin_spacer
from ..common.theme import COLOR_SCHEME_DIVERGING, CHART_HEIGHT, CHART_WIDTH
from ..common.transforms import add_mismatch_score, get_top_mismatch_zips, classify_complaint_detail

def build_chart(
    metrics_by_zip: pd.DataFrame,
    complaints_311: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
) -> alt.Chart:
    top = get_top_mismatch_zips(
        metrics_by_zip,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
    )[["zip_code", "mismatch_group", "mismatch_311_vs_yelp"]].copy()

    comp = complaints_311.copy()
    comp = comp.loc[comp["zip_code"].isin(top["zip_code"])].copy()

    comp["complaint_type_detail"] = comp.apply(
        lambda row: classify_complaint_detail(
            row.get("subject", ""),
            row.get("service_name", ""),
        ),
        axis=1,
    )

    plot_df = (
        comp.groupby(["zip_code", "complaint_type_detail"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .merge(top, on="zip_code", how="left")
    )

    if plot_df.empty:
        return (
            alt.Chart(pd.DataFrame({"text": ["No complaint composition data available."]}))
            .mark_text(size=16)
            .encode(text="text:N")
            .properties(width=500, height=60)
        )

    plot_df["zip_total"] = plot_df.groupby("zip_code")["count"].transform("sum")
    plot_df["share"] = plot_df["count"] / plot_df["zip_total"]

    def make_group_chart(group_name: str, ascending: bool) -> alt.Chart:
        group_df = plot_df.loc[plot_df["mismatch_group"] == group_name].copy()
        group_top = top.loc[top["mismatch_group"] == group_name].copy()

        if group_df.empty or group_top.empty:
            return (
                alt.Chart(pd.DataFrame({"text": [f"No data for: {group_name}"]}))
                .mark_text(size=14)
                .encode(text="text:N")
                .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title=group_name)
            )

        zip_order = (
            group_top.sort_values("mismatch_311_vs_yelp", ascending=ascending)["zip_code"]
            .tolist()
        )

        return (
            alt.Chart(group_df)
            .mark_bar()
            .encode(
                x=alt.X("zip_code:N", title="ZIP", sort=zip_order),
                y=alt.Y(
                    "share:Q",
                    title="Share of complaints",
                    axis=alt.Axis(format="%")
                ),
                color=alt.Color("complaint_type_detail:N", title="Complaint type"),
                tooltip=[
                    alt.Tooltip("zip_code:N", title="ZIP"),
                    alt.Tooltip("complaint_type_detail:N", title="Complaint type"),
                    alt.Tooltip("count:Q", title="Count"),
                    alt.Tooltip("share:Q", title="Share", format=".1%"),
                ],
            )
            .properties(
                width=CHART_WIDTH,
                height=CHART_HEIGHT,
                title=group_name,
            )
        )

    left_chart = make_group_chart(
        "Yelp higher than complaints predict",
        ascending=False,
    )

    right_chart = make_group_chart(
        "Yelp lower than complaints predict",
        ascending=True,
    )

    return (
        alt.vconcat(left_chart, right_chart, spacing=30)
        .resolve_scale(color="shared")
        .properties(title="Complaint Mix in Top Mismatch ZIPs")
    )
