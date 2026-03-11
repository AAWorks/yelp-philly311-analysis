"""
Exploratory map: Yelp weighted rating by ZIP.
"""

import altair as alt
import pandas as pd

from ..common.layout import with_thin_spacer
from ..common.theme import COLOR_SCHEME_CONTINUOUS, MAP_HEIGHT, MAP_PROJECTION, MAP_WIDTH


def build_chart(geojson: dict, metrics_by_zip: pd.DataFrame) -> alt.Chart:
    lookup_df = metrics_by_zip.copy()
    zip_geo = alt.Data(values=geojson["features"])

    chart = (
        alt.Chart(zip_geo)
        .mark_geoshape(stroke="#333333", strokeWidth=0.4)
        .project(type=MAP_PROJECTION)
        .transform_lookup(
            lookup="properties.zip_code",
            from_=alt.LookupData(lookup_df, "zip_code", ["yelp_rating_wtd", "n_restaurants"]),
        )
        .transform_calculate(zip_code="datum.properties.zip_code")
        .encode(
            color=alt.Color(
                "yelp_rating_wtd:Q",
                title="Weighted Yelp rating",
                scale=alt.Scale(scheme=COLOR_SCHEME_CONTINUOUS),
            ),
            tooltip=[
                alt.Tooltip("zip_code:N", title="ZIP"),
                alt.Tooltip("yelp_rating_wtd:Q", title="Weighted Yelp rating"),
                alt.Tooltip("n_restaurants:Q", title="Restaurants"),
            ],
        )
        .properties(width=MAP_WIDTH, height=MAP_HEIGHT, title="Yelp Restaurant Perception")
    )
    return with_thin_spacer(chart)
