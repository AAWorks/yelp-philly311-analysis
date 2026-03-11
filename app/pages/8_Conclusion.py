"""
Page 8: Conclusion
"""

import streamlit as st


st.markdown(
    """
## Conclusion 


While at first glance there appears to be only a weak relationship between local 311 complaints and Yelp ratings, after further
analysis of the data, other factors like differing restaurant types and complaint compositions may have obscured the relationship. 
In this analysis, we found that a several of the ZIP codes we looked at had a large gap between the rating our model predicted based
on the number of complaints per restaurant in the ZIP code and the observed rating average for the ZIP from the Yelp data set. 

Zip codes with a higher proportion of bars/pubs, American food, and coffee shops/bakeries tended to have higher ratings than the model
predicted while those with lower than predicted ratings often had higher proportions of pizza and fast food restaurants. The Zip codes 
with lower ratings also often had a smaller number of restaurants. This could mean there is a problem with the sample size or that there
are less restaurants in that area because the area is already not conducive to restaurants which could affect our results. In addition to
restaurant type and restaurant count in the Zip code, complaint composition differed starkly between those Zips with higher than expected ratings
and those with lower ratings. The Zips in the first category have a higher share of graffiti while those in the lower rating category have higher 
concentrations of trash, illegal dumping, and poor lighting.

Beyond looking at potential reasons for the mismatch in those Zip codes, we checked the robustness of our choice of the 311 data set by also 
examining data from the Litter index which confirmed that cleanliness varies substantially across the city of Philadelphia. This suggests that 
this factor is varied enough to potentially pose an issue for restaurants.

This project is limited by several factors, namely the small sample size of restaurants in some zips, especially those that have average ratings
lower than expected. However, it would be interesting to potentially examine if there is a causal mechanism at play here with unclean neighborhoods
driving out restaurants and shrinking the sample size. Also, the ability to merge the Litter index into the data geographically to even more strongly validate using the 311 
complaints would have enhanced robustness of the analysis. Ultimately, this work should not be used to make causal claims and is only exploring association
so nothing more than speculation can be made. In the future, a study able to combine more data using geographical markers and also potentially examining the 
qualitative substance of each review to perhaps determine the reason reviewers are rating restaurants the way they do would significantly build on and improve 
what has been explored here.
"""
)

st.divider()

st.markdown(
    """
# Citations 

Yelp dataset: https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/data?select=yelp_academic_dataset_business.json 

311 requests dataset: https://opendataphilly.org/datasets/311-service-and-information-requests/  

Litter Index: https://opendataphilly.org/datasets/litter-index/

Philadelphia geojson: https://github.com/opendataphilly/open-geo-data/blob/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson 
"""
)
