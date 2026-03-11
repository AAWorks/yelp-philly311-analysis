"""
Page 5: Interactive mismatch explorer
"""

import streamlit as st

from src.charts.interactive import (
    build_mismatch_map,
    build_mismatch_scatter
)
from src.processing import load_data


st.title("Interactive Mismatch Explorer")

data = load_data()
dfs = data["dataframes"]
geojson = data["geojson"]

st.markdown(
    """
## Mismatch between complaints and ratings

The overall relationship between complaints and Yelp ratings is only part of the story. Some ZIP codes have much 
worse Yelp ratings than their complaint burden would suggest, while others perform better than expected. These 
mismatches matter because they show where neighborhood cleanliness and restaurant perception stop moving together.
"""
)

min_restaurants = st.slider("Minimum restaurants per ZIP", min_value=1, max_value=20, value=3)

scatter_metric = st.selectbox(
    "Mismatch scatter x-axis metric",
    ["complaints_per_restaurant", "complaints"],
    index=0,
)

scatter_view = build_mismatch_scatter(
    dfs["metrics_by_zip"],
    min_restaurants=min_restaurants,
    burden_metric=scatter_metric,
)
mismatch_map = build_mismatch_map(
    geojson,
    dfs["metrics_by_zip"],
    min_restaurants=min_restaurants,
)
st.markdown("### Interactive Chart: Mismatch Explorer (Scatter)")
st.altair_chart(scatter_view, width="stretch")
st.caption("Chart observations: Most ZIP codes cluster at relatively low complaint burdens with Yelp ratings between roughly 3.3 and 4.0, but mismatch still varies meaningfully within that range. As complaint burden rises, the points shift from mostly blue to mostly red, suggesting that high-burden ZIPs are more likely to have Yelp ratings that underperform what the broader pattern would predict.")

st.markdown("### Mismatch Map")
st.altair_chart(mismatch_map, width="stretch")
st.caption("Chart observations: Mismatch is not randomly scattered across Philadelphia. Several central ZIP codes show strongly negative mismatch, where Yelp ratings fall well below what complaint burden would predict, while parts of western and southern Philadelphia show positive mismatch, where restaurant ratings remain stronger than expected despite local complaint pressure.")

st.divider()

st.markdown(
    """
## Analysis 

When the raw complaint number and complaints per restaurant are changed, and when the minimum restaurant threshold is raised, several patterns hold true. Despite the vast range of complaints, the majority of ZIP codes still tend to cluster around Yelp scores between about 3.3 and 4.0. The fact that raising the minimum restaurant threshold has no impact implies that a small number of restaurants are not the primary cause of the discrepancy between cleanliness complaints and restaurant perception. On the map, a number of ZIP codes in the south and west continue to show greater positive mismatches, while a few in the center continue to show stronger negative mismatches.

Overall, the visualizations indicate that, despite significant differences in complaint burdens, restaurant assessment is relatively consistent across most ZIP codes. However, as restaurant density, ZIP level aggregation, and complaint reporting behavior can all affect the detected relationships, these trends should be evaluated with caution.
"""
)
