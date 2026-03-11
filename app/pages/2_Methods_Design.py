"""
Data page for exploring processed tables
"""

import streamlit as st

from src.processing import load_data


st.title("Methods and Design Choices")
# st.caption("Processed tables from `src/processing` only.")

# data = load_data()
# dfs = data["dataframes"]
# geojson = data["geojson"]

# tables = {
#     "complaints_311 (filtered default)": dfs["complaints_311"],
#     "complaints_311_all": dfs["complaints_311_all"],
#     "complaints_311_by_zip": dfs["complaints_311_by_zip"],
#     "yelp (default)": dfs["yelp"],
#     "yelp_by_zip": dfs["yelp_by_zip"],
#     "litter_index (latest default)": dfs["litter_index"],
#     "litter_by_division": dfs["litter_by_division"],
#     "litter_trend": dfs["litter_trend"],
#     "geo_features": dfs["geo_features"],
#     "metrics_by_zip": dfs["metrics_by_zip"],
#     "geo_with_metrics": dfs["geo_with_metrics"],
# }

# selected = st.selectbox("Choose a processed table", list(tables.keys()))
# df = tables[selected]

# left, right = st.columns(2)
# with left:
#     st.metric("Rows", f"{len(df):,}")
# with right:
#     st.metric("Columns", f"{len(df.columns):,}")

# st.write("Columns:")
# st.code(", ".join(df.columns.tolist()))

# st.dataframe(df, width="stretch")

# st.divider()
# st.subheader("GeoJSON Preview")
# st.write("Feature count:", len(geojson.get("features", [])))

# if geojson.get("features"):
#     st.write("First feature properties:")
#     st.json(geojson["features"][0].get("properties", {}))

st.markdown(
    """
## Methodology
Our approach creates a single ZIP-level analysis table by combining cleaned 311 service requests, Yelp business records,
and ZIP boundary geometry. As an additional benchmark, we employ the city Litter Index in its original geography based on 
splitting the city into divisions. We aggregate Yelp stars using review count weights, filter 311 records to sanitation-related 
complaints, and normalize ZIP codes across sources. Companies with high review volumes contribute proportionately because Yelp uses a weighted 
rating system. We also compare raw complaints and complaints_per_restaurant (complaints / n_restaurants) for the cleanliness burden. 
In order to identify areas where perception and complaint pressure diverge following standardization, we calculate a mismatch score 
as z_yelp_rating - z_complaints_burden. The most commong difficulties we faced were dealing with unit mismatch (ZIP vs. division), keyword-based
311 filtering, and uneven restaurant coverage across ZIPs.

"""
)

st.divider()

st.markdown(
    """
## Design Choices - Baseline Maps

The spatial patterns of 311 cleanliness burden and Yelp restaurant perception across ZIP codes were displayed using two
choropleth maps. In order to make it easy for viewers to compare relative intensity across areas without confusing different
palettes, we encoded these metrics using the same sequential color scale, progressing from lighter shades to dark blue. 
Darker blues draw attention to ZIP codes with stronger signals, while lighter hues indicate lower values. To keep the map 
area clear, the legend is positioned to the side of the map. Interactive brushing gives the viewer more context by revealing
extra details like the number of restaurants in each ZIP code.
"""
)

st.markdown(
    """
## Design Choices - Relationships

Users can filter ZIP codes by minimum number of restaurants using the slider in the 311 vs Yelp scatter graphic. This enables users to determine whether
the trend persists when restricting to ZIP codes with more restaurant coverage, as well as to filter out ZIPs with low restaurant counts where averages may be
more erratic due to a small sample size. We chose to use a scatter plot since we believed it would make it easiest for readers to notice clusters, outliers,
and the overall trend as well as the relationship between complaint burden and Yelp ratings at the ZIP code level.

To make it easy for visitors to identify which ZIP codes had the most discrepancy between 311 complaints and Yelp perception, we employed a sorted horizontal 
bar chart for the mismatch ranking. The direction of the mismatch is displayed using a diverging color scale from blue to red.

"""
)

st.markdown(
    """
## Design Choices - Mismatch Explorer
The mismatch explorer scatter plot allows users to switch between complaints per restaurant and total complaints on the x axis. This design helps us analyze how the 
interpretation of complaint burden changes depending on whether restaurant density is taken into account. The points are also colored by mismatch score using a 
blue to red scale, which highlights where Yelp ratings are higher or lower than complaint levels would predict. This makes it easier to see clusters and outliers
while simultaneously understanding the direction of divergence.

The mismatch map uses a choropleth design to show where these divergences occur geographically across Philadelphia. We use the same color scale, allowing for continuity
between charts and letting the viewer quickly identify spatial clusters of bigger differences between complaints and perception. The map 
complements the scatter by adding geographic context, helping users see whether mismatches are concentrated in particular parts of the city rather than appearing
randomly across ZIP codes.

"""
)


st.markdown(
    """
## Design Choices - Mismatch Drivers

This page seeks to examine different potential causes of the mismatch observed on the relationship page. The rating mismatch vs. coverage 
scatter places zip restaurant count on the x-axis and magnitude of the mismatch on the y-axis. Here, color encodes the signed mismatch value 
so that direction and size are visible at the same time. Being able to see both size and direction simultaneously makes it easier to see 
whether mismatch is concentrated in the lower-coverage ZIPs.

The complaint composition charts were created with stacked bars because their goal is to compare the share of complaint types within each ZIP 
rather than the raw totals alone. Splitting the charts into positive and negative mismatch groups makes the contrast easier to read. 
The weighted vs. simple Yelp chart makes use of paired points so that small gaps between the two rating measures are visible within 
each ZIP. Finally, the restaurant-type heatmap uses color to encode cuisine share across ZIPs, while the cuisine scatterplots place 
restaurant-type share on the x-axis and mismatch score on the y-axis, with point size showing the number of restaurants in the ZIP.

"""
)


st.markdown(
    """
## Design Choices - Litter Benchmark

The Litter Index page uses charts that match the summarized division-level structure of the benchmark data. The first chart is a histogram, as it shows the overall spread of 2018 litter scores across divisions. Here we represent litter score via the x-axis and # of divisions per bin via the y-axis. This allows the reader to better distinguish where most divisions are concentrated. The second chart employs a scatterplot to compare the average litter score and the historical score range for each division. The position on the x-axis indicates average conditions, the position on the y-axis shows variability, and point size encodes the division area. This allows for the distinction of divisions that are worse on average from those that are simply more volatile over time. The third chart uses a min-mean-max range display, where horizontal position shows litter score and the connecting line shows the historical spread for each division. Sorting divisions by range makes the most variable cases easier to identify.
"""
)
