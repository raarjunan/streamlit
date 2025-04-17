# pages/8_Storytelling_Visuals.py
import streamlit as st
import plotly.express as px
import pandas as pd
from load_data import load_dataset
from utils import section_title

section_title("📋 Storytelling & Narrative Visuals")
data = load_dataset()

st.subheader("Annotated Line Chart")
st.markdown("**Insight:** Sales dropped in Q2 across most regions, especially in the East.")
st.plotly_chart(px.line(data, x='date', y='sales', color='region'), use_container_width=True)

st.subheader("Step-by-Step Scrollytelling")
with st.expander("Step 1: Understand sales trend"):
    st.line_chart(data.set_index("date")["sales"])
with st.expander("Step 2: Dive into conversion rate"):
    st.line_chart(data.set_index("date")["conversion_rate"])
with st.expander("Step 3: Explore region breakdown"):
    st.plotly_chart(px.bar(data, x="region", y="sales", color="region"))
