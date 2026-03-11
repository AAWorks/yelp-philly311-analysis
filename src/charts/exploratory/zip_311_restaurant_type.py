"""
Exploratory chart: Heatmap comparing restaurant types and scatter examining restaurant type and mismatch.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH
from ..common.transforms import _prepare_restaurant_type_panel_df


def build_restaurant_type_heatmap(
    metrics_by_zip: pd.DataFrame,
    yelp_df: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
    min_type_count: int = 2,
    max_types: int = 10,
) -> alt.Chart:
    plot_df, type_order = _prepare_restaurant_type_panel_df(
        metrics_by_zip=metrics_by_zip,
        yelp_df=yelp_df,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
        min_type_count=min_type_count,
        max_types=max_types,
    )

    def make_group_chart(group_name: str, ascending: bool) -> alt.Chart:
        group_df = plot_df.loc[plot_df["mismatch_group"] == group_name].copy()

        zip_order = (
            group_df[["zip_code", "mismatch_311_vs_yelp"]]
            .drop_duplicates()
            .sort_values("mismatch_311_vs_yelp", ascending=ascending)["zip_code"]
            .tolist()
        )

        base = (
            alt.Chart(group_df)
            .mark_rect(stroke="white", strokeWidth=1)
            .encode(
                x=alt.X(
                    "restaurant_type:N",
                    title="Restaurant type",
                    sort=type_order,
                    axis=alt.Axis(labelAngle=-55),
                ),
                y=alt.Y(
                    "zip_code:N",
                    title="ZIP",
                    sort=zip_order,
                ),
                color=alt.Color(
                    "type_share:Q",
                    title="Share of restaurants",
                    scale=alt.Scale(scheme="blues"),
                ),
                tooltip=[
                    alt.Tooltip("zip_code:N", title="ZIP"),
                    alt.Tooltip("restaurant_type:N", title="Restaurant type"),
                    alt.Tooltip("type_restaurants:Q", title="Restaurants of type"),
                    alt.Tooltip("total_restaurants:Q", title="Total restaurants"),
                    alt.Tooltip("type_share:Q", title="Share", format=".1%"),
                    alt.Tooltip("type_avg_rating:Q", title="Avg type rating", format=".2f"),
                    alt.Tooltip("overall_zip_rating:Q", title="Overall ZIP rating", format=".2f"),
                    alt.Tooltip("mismatch_311_vs_yelp:Q", title="Mismatch", format=".2f"),
                ],
            )
            .properties(
                width=480,
                height=max(160, 38 * len(zip_order)),
                title=group_name,
            )
        )

        text = (
            alt.Chart(group_df.loc[group_df["type_restaurants"] > 0])
            .mark_text(fontSize=10)
            .encode(
                x=alt.X("restaurant_type:N", sort=type_order),
                y=alt.Y("zip_code:N", sort=zip_order),
                text=alt.Text("type_restaurants:Q"),
                color=alt.value("black"),
            )
        )

        return base + text

    left = make_group_chart(
        "Yelp higher than complaints predict",
        ascending=False,
    )

    right = make_group_chart(
        "Yelp lower than complaints predict",
        ascending=True,
    )

    return (
        alt.vconcat(left, right, spacing=30)
        .resolve_scale(color="shared")
        .properties(title="Restaurant-Type Composition in Top Mismatch ZIPs")
    )


def build_restaurant_type_scatter(
    metrics_by_zip: pd.DataFrame,
    yelp_df: pd.DataFrame,
    selected_type: str,
    min_restaurants: int = 3,
    top_n_each: int = 5,
    min_type_count: int = 2,
    max_types: int = 10,
) -> alt.Chart:
    plot_df, _ = _prepare_restaurant_type_panel_df(
        metrics_by_zip=metrics_by_zip,
        yelp_df=yelp_df,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
        min_type_count=min_type_count,
        max_types=max_types,
    )

    scatter_df = (
        plot_df.loc[plot_df["restaurant_type"] == selected_type]
        .copy()
        .drop_duplicates(subset=["zip_code"])
    )

    scatter_df["abs_mismatch"] = scatter_df["mismatch_311_vs_yelp"].abs()

    labels_df = scatter_df.nlargest(6, "abs_mismatch").copy()

    zero_rule = (
        alt.Chart(pd.DataFrame({"y": [0]}))
        .mark_rule(strokeDash=[6, 4], color="gray")
        .encode(y="y:Q")
    )

    points = (
        alt.Chart(scatter_df)
        .mark_circle(opacity=0.85)
        .encode(
            x=alt.X(
                "type_share:Q",
                title=f"Share of restaurants that are {selected_type}",
                axis=alt.Axis(format="%"),
            ),
            y=alt.Y(
                "mismatch_311_vs_yelp:Q",
                title="Mismatch score",
            ),
            size=alt.Size(
                "total_restaurants:Q",
                title="Total restaurants in ZIP",
                scale=alt.Scale(range=[80, 700]),
            ),
            color=alt.Color(
                "mismatch_group:N",
                title=None,
                scale=alt.Scale(
                    domain=[
                        "Yelp higher than complaints predict",
                        "Yelp lower than complaints predict",
                    ],
                    range=["#1f77b4", "#d62728"],
                ),
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("restaurant_type:N", title="Restaurant type"),
                alt.Tooltip("type_restaurants:Q", title=f"{selected_type} restaurants"),
                alt.Tooltip("total_restaurants:Q", title="Total restaurants"),
                alt.Tooltip("type_share:Q", title="Type share", format=".1%"),
                alt.Tooltip("type_avg_rating:Q", title=f"Avg {selected_type} rating", format=".2f"),
                alt.Tooltip("overall_zip_rating:Q", title="Overall ZIP rating", format=".2f"),
                alt.Tooltip("mismatch_311_vs_yelp:Q", title="Mismatch", format=".2f"),
            ],
        )
    )

    labels = (
        alt.Chart(labels_df)
        .mark_text(dx=8, dy=-6, fontSize=11)
        .encode(
            x="type_share:Q",
            y="mismatch_311_vs_yelp:Q",
            text="zip_code:N",
        )
    )

    chart = (
    (zero_rule + points + labels)
    .properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        )
    )
  
    return chart
