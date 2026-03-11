"""
Interactive-style ZIP map metric switcher.
"""

import altair as alt
import pandas as pd

from ..common.layout import with_thin_spacer
from ..common.theme import (
    COLOR_SCHEME_CONTINUOUS,
    COLOR_SCHEME_DIVERGING,
    MAP_HEIGHT,
    MAP_PROJECTION,
    MAP_WIDTH,
)
from ..common.transforms import add_mismatch_score


METRIC_CONFIG = {
    "complaints": ("311 complaints", ".0f"),
    "complaints_per_restaurant": ("311 complaints per restaurant", ".2f"),
    "yelp_rating_wtd": ("Weighted Yelp rating", ".2f"),
    "mismatch_311_vs_yelp": ("Mismatch (z_yelp - z_complaints)", ".2f"),
}

def build_chart(geojson: dict, metrics_by_zip: pd.DataFrame, metric: str) -> alt.Chart:
    if metric not in METRIC_CONFIG:
        raise ValueError(f"Unsupported metric: {metric}")

    data = add_mismatch_score(metrics_by_zip)
    title, fmt = METRIC_CONFIG[metric]
    zip_geo = alt.Data(values=geojson["features"])
    scale = (
        alt.Scale(scheme=COLOR_SCHEME_DIVERGING, domainMid=0)
        if metric == "mismatch_311_vs_yelp"
        else alt.Scale(scheme=COLOR_SCHEME_CONTINUOUS)
    )

    chart = (
        alt.Chart(zip_geo)
        .mark_geoshape(stroke="#333333", strokeWidth=0.4)
        .project(type=MAP_PROJECTION)
        .transform_lookup(
            lookup="properties.zip_code",
            from_=alt.LookupData(data, "zip_code", [metric]),
        )
        .transform_calculate(zip_code="datum.properties.zip_code")
        .encode(
            color=alt.Color(f"{metric}:Q", title=title, scale=scale),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip(f"{metric}:Q", title=title, format=fmt),
            ],
        )
        .properties(width=MAP_WIDTH, height=MAP_HEIGHT, title=f"ZIP Map: {title}")
    )
    return with_thin_spacer(chart)
