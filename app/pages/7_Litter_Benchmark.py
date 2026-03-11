"""
Exploratory distribution/trend for Litter Index.
"""

import streamlit as st

from src.processing import load_data
from src.charts.exploratory import build_litter_histogram
from src.charts.exploratory.litter_benchmark_story import (
    build_litter_mean_vs_range_scatter,
    build_litter_range_dumbbell,
)

st.title("Litter Benchmark")

data = load_data()
dfs = data["dataframes"]

st.markdown(
    """
The Litter Index provides an independent measure of neighborhood cleanliness, but it is recorded by sanitation division rather than ZIP code. That means it cannot be directly merged into the ZIP-level Yelp analysis. Still, it serves as a useful benchmark: if litter conditions also vary substantially across divisions, then the broader claim that cleanliness differs across Philadelphia looks more credible under a second measurement system.
"""
)

st.markdown("### 1. Distribution of litter scores in 2018")
histogram_chart = build_litter_histogram(dfs["litter_index"])
st.altair_chart(histogram_chart, width="stretch")
st.caption(
    "Chart observations: The 2018 Litter Index is concentrated in the lower-to-middle score range, with most divisions falling roughly between 1.4 and 2.3 and relatively few reaching the highest litter levels. This suggests that while extreme litter conditions are uncommon, cleanliness still varies meaningfully across divisions in the benchmark snapshot."
)

st.markdown("### 2. Which divisions are worse on average, and which are more variable over time?")
scatter_chart = build_litter_mean_vs_range_scatter(dfs["litter_by_division"], label_n=10)
st.altair_chart(scatter_chart, width="stretch")
st.caption(
    "Chart observations: Divisions with worse average litter conditions often also show more variation between their best and worst observed scores, though the relationship is far from perfect. Most divisions cluster in the lower-middle range of variability, while a smaller set of outliers like 6504, 5202, and 2229 combine relatively high average litter scores with unusually wide historical swings."
)

st.markdown("### 3. Which divisions showed the widest historical spread in highest and lowest litter conditions?")
dumbbell_chart = build_litter_range_dumbbell(dfs["litter_by_division"], top_n=12)
st.altair_chart(dumbbell_chart, width="stretch")
st.caption(
    "Chart observations: These divisions have the widest historical spread between their lowest and highest observed litter scores, indicating that litter conditions were especially volatile over time rather than consistently stable. Divisions such as 6504, 2417, and 3317 stand out not only for wide ranges but also for relatively high average litter levels, suggesting that some of the most variable divisions were also among the dirtiest on average."
)

st.divider()

st.markdown(
    """
### Analysis

The Litter Index does not directly validate the ZIP-level Yelp results because the geographies differ. But it points in the same broader direction as the 311 analysis: cleanliness conditions vary meaningfully across Philadelphia. That makes it increasingly plausible that the 311 complaint burden is capturing a real environmental signal rather than reporting noise.
"""
)
