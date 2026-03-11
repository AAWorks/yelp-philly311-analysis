"""
Page 6: Mismatch causes
"""

import streamlit as st

from src.charts.exploratory import (
    build_mismatch_vs_coverage_chart,
    build_complaint_composition_chart,
    build_yelp_weighted_vs_simple_chart,
    build_restaurant_type_heatmap,
    build_restaurant_type_scatter,
)
from src.processing import load_data

from src.charts.common.transforms import get_restaurant_type_options


st.title("Mismatch Drivers")

data = load_data()
dfs = data["dataframes"]
geojson = data["geojson"]

st.markdown(
    """
## Why Do Complaints and Perception Diverge?

The mismatch between 311 complaint burden and Yelp ratings may reflect more than simple disagreement. 
These two signals are produced by different people and may capture different aspects of neighborhood 
experience. This section looks at four possible drivers of divergence: 311 complaint composition, restaurant 
coverage, the structure of the Yelp signal, and the types of restaurants in each ZIP.
"""
)

min_restaurants = st.slider("Minimum restaurants per ZIP", min_value=1, max_value=20, value=10)

st.markdown("### 1. Are the biggest mismatches concentrated in low-coverage ZIPs?")
coverage_chart = build_mismatch_vs_coverage_chart(
    dfs["metrics_by_zip"],
    min_restaurants=min_restaurants,
)
st.altair_chart(coverage_chart, width="stretch")
st.caption(
    "Chart observations: The largest mismatch magnitudes are concentrated in ZIP codes with relatively small restaurant bases, especially among the strongest negative mismatches. This pattern suggests that some of the most extreme divergences may reflect instability in low-coverage ZIPs rather than broad neighborhood-wide differences alone."
)

st.markdown("### 2. Do top mismatch ZIPs have a different complaint mix?")
composition_chart = build_complaint_composition_chart(
    dfs["metrics_by_zip"],
    dfs["complaints_311"],
    min_restaurants=min_restaurants,
    top_n_each=5,
)
st.altair_chart(composition_chart, width="stretch")
st.caption(
    "Chart observations: The complaint mix differs noticeably across the two mismatch groups. ZIPs where Yelp ratings are higher than complaint burden would predict tend to have a larger graffiti share, while ZIPs where ratings are lower than expected show relatively larger trash, lighting, and illegal dumping shares, suggesting that the type of neighborhood disorder may matter as much as the overall complaint volume."
)

st.markdown("### 3. Is the Yelp signal broad, or dominated by heavily reviewed restaurants?")
yelp_structure_chart = build_yelp_weighted_vs_simple_chart(
    dfs["metrics_by_zip"],
    dfs["yelp"],
    min_restaurants=min_restaurants,
    top_n_each=5,
)
st.altair_chart(yelp_structure_chart, width="stretch")
st.caption(
    "Chart observations: The weighted and simple Yelp averages are very close in most top mismatch ZIPs. This indicates that the ZIP-level Yelp signal is not being driven by just a few heavily reviewed restaurants. Where gaps do appear, they are modest, suggesting that review concentration may matter at the margin but does not fully explain the broader mismatch pattern."
)

st.markdown("### 4. Does restaurant mix help explain the mismatch?")

restaurant_type_options = get_restaurant_type_options(
    dfs["metrics_by_zip"],
    dfs["yelp"],
    min_restaurants=min_restaurants,
    top_n_each=5,
    min_type_count=2,
)

restaurant_type_heatmap = build_restaurant_type_heatmap(
    dfs["metrics_by_zip"],
    dfs["yelp"],
    min_restaurants=min_restaurants,
    top_n_each=5,
    min_type_count=2,
    max_types=10,
)

st.altair_chart(restaurant_type_heatmap, width="stretch")
st.caption(
    "Chart observations: The restaurant mix differs across the two mismatch groups rather than lining up around a single dominant cuisine profile. ZIPs with higher than expected ratings tend to show heavier concentrations in categories like American, coffee/bakery, and bars/pub food, while several negative-mismatch ZIPs lean more toward pizza, fast food/burgers, and seafood, suggesting that local dining composition may shape how restaurant perception diverges from complaint burden."
)

selected_restaurant_type = st.selectbox(
    "Restaurant type for scatter plot",
    restaurant_type_options,
    index=0,
)

restaurant_type_scatter = build_restaurant_type_scatter(
    dfs["metrics_by_zip"],
    dfs["yelp"],
    selected_type=selected_restaurant_type,
    min_restaurants=min_restaurants,
    top_n_each=5,
    min_type_count=2,
    max_types=10,
)

st.markdown("##### Does Restaurant Share Track Mismatch?")
st.altair_chart(restaurant_type_scatter, width="stretch")
st.caption(
    "Chart observations: Across cuisine types, the two mismatch groups are only partially mixed. Positive-mismatch ZIPs tend to appear at higher shares of coffee/bakery, bars/pub food, Chinese, Japanese, Italian, and seafood, while negative-mismatch ZIPs are more concentrated at higher pizza and fast-food shares. This suggests that restaurant composition may help explain why Yelp perception diverges from complaint burden in some ZIPs. Because this comparison is based on a small set of top mismatch ZIPs, these cuisine patterns should be treated as directional rather than conclusive."
)

st.divider()

st.markdown(
    """
## Analysis 

The 311 complaint and Yelp ratings are produced by different people and may capture different aspects of a neighborhood experience. This section analyzes potential drivers of this mismatch, including complaint composition, restaurant type, and the structure of the Yelp signal within each ZIP.

There are several patterns that remain stable across several charts above. The scatter plot of mismatch vs. restaurant count shows that the largest mismatches occur in ZIPs with fewer restaurants. This discrepancy shows that small sample sizes may amplify differences between the two signals. In addition, the weighted and simple Yelp averages within top mismatch ZIPs remain fairly close, indicating that the Yelp signal is not strongly dominated by a single highly reviewed restaurant.

When examining total complaints, some ZIPs appear to have an extremely high burden simply because they contain many restaurants and more activity. When complaints are viewed by restaurant or broken down by type, the picture becomes more detailed. In several ZIP codes where Yelp ratings are higher than expected given the complaint volume, graffiti accounts for a larger share of complaints. Graffiti may not always be interpreted as a negative signal, and in some neighborhoods can even be associated with a trendy or artistic environment. In contrast, ZIP codes where Yelp ratings fall below what complaint levels would predict tend to have a larger share of trash and recycling complaints. Issues related to trash are more likely to signal poor sanitation conditions and may directly affect how people perceive nearby food establishments.

Taken together, the patterns noted above suggest that the mismatch between complaints and Yelp ratings results from multiple variables rather than a single explanation. The differences in restaurant coverage and type, and in the composition of recorded complaints, may both influence average Yelp ratings relative to the 311 complaint burden. Because this is not a definitive statistical relationship, the results should be interpreted cautiously.
"""
)
