"""
Page 4: ZIP relationships
"""

import streamlit as st

from src.charts.exploratory import build_zip_311_vs_yelp_scatter, build_zip_mismatch_rank
from src.processing import load_data


st.title("ZIP Relationships")

data = load_data()
dfs = data["dataframes"]

st.markdown(
    """
## Complain Burden and Yelp Rating

"""
)

min_restaurants = st.slider("Minimum restaurants per ZIP", min_value=1, max_value=20, value=3)
show_mismatch_rank = True

scatter = build_zip_311_vs_yelp_scatter(dfs["metrics_by_zip"], min_restaurants=min_restaurants)
st.markdown("### Exploratory Chart: ZIP 311 vs Yelp Scatter")
st.altair_chart(scatter, width="stretch")
st.caption("Chart observations: ZIP codes with heavier 311 cleanliness complaint burdens tend to have slightly lower weighted Yelp ratings, but the relationship is weak and highly dispersed.")

if show_mismatch_rank:
    st.markdown("### Exploratory Chart: ZIP Mismatch Ranking")
    rank_chart = build_zip_mismatch_rank(
        dfs["metrics_by_zip"],
        min_restaurants=min_restaurants,
        top_n=20,
    )
    st.altair_chart(rank_chart, width="stretch")
    st.caption("Chart observations: This ranking highlights the ZIP codes where Yelp perception diverges most strongly from what complaint burden would predict. High positive mismatch values indicate places where restaurant ratings are stronger than expected given complaint pressure, making these ZIPs useful targets for closer investigation.")

st.divider()

st.markdown(
    """
## Analysis 

There is a minor negative link between complaint burden and Yelp rating, as demonstrated by our first direct test. The Yelp rating declines as the number of complaints per restaurant in a ZIP code increases. Nonetheless, the scatter and slope are both broad. This indicates that the variance in restaurant impression can only be partially explained by the 311 complaint burden.

Our mismatch ranking shows the ZIP codes with the largest differences between Yelp's restaurant ratings and the 311 cleanliness complaint burden. The top positive mismatches, where Yelp ratings are higher than 311 complaints would predict, are in 19176 and 19107. These ZIP codes show the strongest gaps between the two standardized measures, with values close to 1 indicating a considerable difference. ZIP codes at the bottom of the ranking show the reverse situation, where complaint burden is lower relative to Yelp perception. These outliers help pinpoint neighborhoods where signals of cleanliness and restaurant perception are diverging.

A limitation of both metrics is that they are subject to reporting and aggregation bias. 311 complaints rely on resident responses, and averages at the ZIP level obscure within-neighborhood variation.
"""
)
