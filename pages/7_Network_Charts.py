# pages/7_Network_Charts.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from load_data import load_dataset
from utils import section_title
from load_data import load_network_graph, load_bipartite_graph

section_title("🌐 Network & Relationship Charts")
data = load_dataset()

st.subheader("Force-Directed Graph")

G = load_network_graph()
B = load_bipartite_graph()

fig, ax = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='skyblue', with_labels=True, node_size=500, ax=ax)
st.pyplot(fig)

st.subheader("Adjacency Matrix")
adj = nx.to_pandas_adjacency(G)
st.dataframe(adj.style.background_gradient(cmap='Blues'))

st.subheader("Bipartite Graph")
B = nx.Graph()
B.add_nodes_from(['A1', 'A2', 'A3'], bipartite=0)
B.add_nodes_from(['B1', 'B2'], bipartite=1)
B.add_edges_from([('A1', 'B1'), ('A2', 'B2'), ('A3', 'B1')])
fig, ax = plt.subplots()
pos = nx.bipartite_layout(B, nodes=['A1', 'A2', 'A3'])
nx.draw(B, pos, with_labels=True, ax=ax, node_color='lightgreen')
st.pyplot(fig)
