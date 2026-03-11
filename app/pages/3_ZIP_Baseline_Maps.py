"""
Page 3: ZIP baseline maps
"""

import streamlit as st

from src.charts.exploratory import build_zip_311_burden_map, build_zip_yelp_rating_map
from src.processing import load_data


st.title("ZIP Baseline Maps")

data = load_data()
dfs = data["dataframes"]
geojson = data["geojson"]

st.markdown(
    """
## Complaints, Yelp Perception, Restaurant Count Maps

Before testing the relationship between complaints and ratings directly, it helps to see where each signal 
is strongest. Complaint burden, Yelp perception, and restaurant count all vary across Philadelphia, but 
they do not trace  the same geography exactly. That spatial mismatch motivates the analysis that follows.
"""
)

metric = st.selectbox(
    "311 map metric",
    ["complaints_per_restaurant", "complaints"],
    index=0,
)

map_311 = build_zip_311_burden_map(geojson, dfs["metrics_by_zip"], value_col=metric)
map_yelp = build_zip_yelp_rating_map(geojson, dfs["metrics_by_zip"])


st.markdown("### Exploratory Chart: ZIP 311 Burden Map")
st.altair_chart(map_311, width="stretch")
st.caption("Chart observations: ZIP-level 311 cleanliness complaint burden is highest in a cluster of central Philadelphia ZIP codes, with lower burdens across much of the city’s outer areas. This map establishes that resident-reported sanitation pressure is spatially concentrated rather than evenly distributed.")

st.markdown("### Exploratory Chart: ZIP Yelp Rating Map")
st.altair_chart(map_yelp, width="stretch")
st.caption("Chart observations: Weighted Yelp restaurant ratings are generally strongest in several western, central, and southern ZIP codes, while a smaller number of peripheral areas show weaker perceived restaurant quality.")

st.divider()

st.markdown(
    """    
## Analysis

An interesting spatial pattern is visible in the 311 cleanliness burden map. The darkest blue areas show significantly higher complaint rates per restaurant, and the highest complaint burdens are concentrated in a few central ZIP codes. Lighter colors reflect lower complaint levels in many outer ZIP codes, especially in the far north and far south. As a result, lower-burden areas encircle a visible, center-weighted cluster of complaints.

The Yelp perception map at the ZIP level shows two spatial patterns. Higher weighted Yelp ratings are concentrated in a number of central and southern ZIP codes; ratings near four stars are indicated by the darkest blue areas. The southernmost ZIP code and a few western ZIP codes, on the other hand, have significantly lower ratings, which are shown in lighter shades. A large portion of the city's northern region falls in the middle range, suggesting that rather than sharp variation, restaurant perceptions are generally similar across many ZIP codes.

A comparison of the two maps reveals some areas where Yelp perception and complaint burden don't seem to match. Some central ZIP codes have both a high complaint burden and relatively strong Yelp perceptions, while some outer ZIP codes have lower complaint burdens, although only moderate levels of perceived restaurant quality. These obvious mismatches will be points of interest later in the notebook when complaint burden and perception metrics are compared directly.
"""
)
