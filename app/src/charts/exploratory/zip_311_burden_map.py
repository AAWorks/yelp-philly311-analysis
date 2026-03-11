"""
Exploratory map: 311 complaint burden by ZIP.
"""

import altair as alt
import pandas as pd

from ..common.layout import with_thin_spacer
from ..common.theme import COLOR_SCHEME_CONTINUOUS, MAP_HEIGHT, MAP_PROJECTION, MAP_WIDTH


def build_chart(
    geojson: dict,
    metrics_by_zip: pd.DataFrame,
    value_col: str = "complaints_per_restaurant",
) -> alt.Chart:
    lookup_df = metrics_by_zip.copy()
    zip_geo = alt.Data(values=geojson["features"])

    chart = (
        alt.Chart(zip_geo)
        .mark_geoshape(stroke="#333333", strokeWidth=0.4)
        .project(type=MAP_PROJECTION)
        .transform_lookup(
            lookup="properties.zip_code",
            from_=alt.LookupData(
                lookup_df,
                "zip_code",
                [value_col, "complaints", "n_restaurants"],
            ),
        )
        .transform_calculate(zip_code="datum.properties.zip_code")
        .encode(
            color=alt.Color(
                f"{value_col}:Q",
                title="311 complaints per restaurant",
                scale=alt.Scale(scheme=COLOR_SCHEME_CONTINUOUS),
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("complaints:Q", title="311 complaints"),
                alt.Tooltip("n_restaurants:Q", title="Restaurants"),
                alt.Tooltip("complaints_per_restaurant:Q", title="311 complaints per restaurant"),
            ],
        )
        .properties(
            width=MAP_WIDTH,
            height=MAP_HEIGHT,
            title="311 Cleanliness Complaint Burden",
        )
    )
    return with_thin_spacer(chart)
