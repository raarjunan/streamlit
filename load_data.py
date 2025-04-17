import streamlit as st
from data_generator import generate_general_dataset, generate_network_data, generate_bipartite_data, generate_text_data, generate_kpi_spike_data

# @st.cache_data
def load_dataset():
    return generate_general_dataset()

@st.cache_data
def load_network_graph():
    return generate_network_data()

@st.cache_data
def load_bipartite_graph():
    return generate_bipartite_data()

@st.cache_data
def load_text_blob():
    return generate_text_data()

@st.cache_data
def load_kpi_spike_data():
    return generate_general_dataset()
