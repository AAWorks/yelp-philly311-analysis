"""
Interactive linked view: ZIP map + scatter.
"""

import altair as alt
import pandas as pd

from ..common.layout import with_thin_spacer
from ..common.theme import (
    CHART_HEIGHT,
    CHART_WIDTH,
    COLOR_SCHEME_DIVERGING,
    MAP_HEIGHT,
    MAP_PROJECTION,
    MAP_WIDTH,
)
from ..common.transforms import add_mismatch_score


def _prepare_data(metrics_by_zip: pd.DataFrame, min_restaurants: int = 1) -> pd.DataFrame:
    data = add_mismatch_score(metrics_by_zip)
    data = data.loc[data["n_restaurants"] >= min_restaurants].copy()
    return data


def build_scatter(
    metrics_by_zip: pd.DataFrame,
    min_restaurants: int = 1,
    burden_metric: str = "complaints_per_restaurant",
) -> alt.Chart:
    data = _prepare_data(metrics_by_zip, min_restaurants=min_restaurants)
    if burden_metric not in {"complaints", "complaints_per_restaurant"}:
        raise ValueError(f"Unsupported burden metric: {burden_metric}")

    x_title = (
        "311 complaints per restaurant"
        if burden_metric == "complaints_per_restaurant"
        else "311 complaints"
    )
    burden_fmt = ".2f" if burden_metric == "complaints_per_restaurant" else ".0f"

    return (
        alt.Chart(data)
        .mark_circle(size=70, opacity=0.75)
        .encode(
            x=alt.X(f"{burden_metric}:Q", title=x_title),
            y=alt.Y("yelp_rating_wtd:Q", title="Weighted Yelp rating"),
            color=alt.Color(
                "mismatch_311_vs_yelp:Q",
                title="Mismatch",
                scale=alt.Scale(scheme=COLOR_SCHEME_DIVERGING),
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("mismatch_311_vs_yelp:Q", format=".2f"),
                alt.Tooltip(f"{burden_metric}:Q", title=x_title, format=burden_fmt),
                alt.Tooltip("yelp_rating_wtd:Q", format=".2f"),
            ],
        )
        .properties(width=CHART_WIDTH, height=CHART_HEIGHT, title="Mismatch Explorer: Scatter")
    )


def build_map(geojson: dict, metrics_by_zip: pd.DataFrame, min_restaurants: int = 1) -> alt.Chart:
    data = _prepare_data(metrics_by_zip, min_restaurants=min_restaurants)
    zip_geo = alt.Data(values=geojson["features"])
    chart = (
        alt.Chart(zip_geo)
        .mark_geoshape(stroke="#333333", strokeWidth=0.4)
        .project(type=MAP_PROJECTION)
        .transform_lookup(
            lookup="properties.zip_code",
            from_=alt.LookupData(data, "zip_code", ["zip_code", "mismatch_311_vs_yelp"]),
        )
        .transform_calculate(zip_code="datum.properties.zip_code")
        .encode(
            color=alt.Color(
                "mismatch_311_vs_yelp:Q",
                title="Mismatch",
                scale=alt.Scale(scheme=COLOR_SCHEME_DIVERGING, domainMid=0),
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("mismatch_311_vs_yelp:Q", format=".2f"),
            ],
        )
        .properties(width=MAP_WIDTH, height=MAP_HEIGHT, title="Mismatch Explorer: Map")
    )
    return with_thin_spacer(chart)


def build_view(
    geojson: dict,
    metrics_by_zip: pd.DataFrame,
    min_restaurants: int = 1,
    burden_metric: str = "complaints_per_restaurant",
) -> alt.HConcatChart:
    scatter = build_scatter(
        metrics_by_zip,
        min_restaurants=min_restaurants,
        burden_metric=burden_metric,
    )
    map_view = build_map(geojson, metrics_by_zip, min_restaurants=min_restaurants)
    return scatter | map_view
