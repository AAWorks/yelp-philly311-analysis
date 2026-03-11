"""
Streamlit entrypoint with explicit page navigation.
"""

import streamlit as st


pg = st.navigation(
    [
        st.Page("pages/1_Overview.py", title="Overview"),
        st.Page("pages/2_Methods_Design.py", title="Methods & Design Choices"),
        st.Page("pages/3_ZIP_Baseline_Maps.py", title="ZIP Baseline Maps"),
        st.Page("pages/4_ZIP_Relationships.py", title="ZIP Relationships"),
        st.Page("pages/5_Interactive_Mismatch_Explorer.py", title="Mismatch Explorer"),
        st.Page("pages/6_Mismatch_Drivers.py", title="Mismatch Drivers"),
        st.Page("pages/7_Litter_Benchmark.py", title="Litter Benchmark"),
        st.Page("pages/8_Conclusion.py", title="Conclusion"),
    ]
)

pg.run()
