"""
Overview page
"""

import streamlit as st

from src.processing import load_data


st.title("Overview")

data = load_data()
dfs = data["dataframes"]

st.markdown(
    """
## Project Framing
As digital ordering and reservation platforms have become more central to restaurant demand, Yelp ratings are now more 
critical than ever in determining customer traffic. However, a restaurant's food, service, and interior are not the only 
components evaluated in a Yelp rating. Reviewers also take into account the environments in the neighborhood and cleanliness.
While some neighborhoods consistently receive high sanitation ratings, others frequently receive complaints regarding cleanliness. The goal 
of this project is to determine how/if a neighborhood's cleanliness and sanitation are associated with the Yelp ratings that restaurants recieve. 

"""
)

st.markdown(
    """
## Big Question
How do ZIP-level cleanliness complaint burdens relate to Yelp restaurant perception in Philadelphia,
and how does the district-level Litter Index compare as a benchmark?
"""
)

st.markdown(
    """
## Sub-Questions
1. Do higher ZIP-level complaint burdens align with lower Yelp ratings?
2. Where do complaint-vs-perception mismatches appear?
3. What does the Litter Index show in its native division unit?
4. Which findings are robust to metric choices?
"""
)

st.subheader("Current Data Snapshot")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("311 Filtered Rows", f"{len(dfs['complaints_311']):,}")
with col2:
    st.metric("Yelp Rows", f"{len(dfs['yelp']):,}")
with col3:
    st.metric("ZIP Metrics Rows", f"{len(dfs['metrics_by_zip']):,}")
with col4:
    st.metric("Litter Rows (Latest)", f"{len(dfs['litter_index']):,}")

st.markdown(
    """
## Narrative Placement

Our analysis centers on four subquestions to direct an organized investigation of the relationship between restaurant perception
and neighborhood cleanliness throughout Philadelphia. We first check whether ZIP codes with higher complaint burdens also have 
lower Yelp ratings. Second, we take a look at areas where customer perception and public cleanliness are at odds by identifying 
areas where complaint levels and restaurant perception are mismatched (i.e. diverge). Third, we look at the Litter Index to see 
how different districts have different levels of cleanliness throughout the city. Additionally, the analysis determines whether 
the patterns we see hold true when various metrics or aggregation options are applied.
"""
)
