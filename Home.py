# main_app.py
import streamlit as st
from load_data import load_dataset
from utils import section_title

# st.set_page_config(layout="wide")
st.set_page_config(page_title="My App", page_icon="📊", layout="wide")


st.title("📊 Streamlit Chart Gallery – Modular Version")
data = load_dataset()

st.sidebar.title("Navigation")
st.sidebar.markdown("Use the pages on the left to explore chart types.")

section_title("Welcome")
st.markdown("""
This dashboard showcases a variety of chart types for different use cases:
- Basic bar, line, area, and pie charts
- Time-series analysis
- Geospatial maps
- Advanced statistical and business visuals
- Custom interactive and storytelling components
""")

