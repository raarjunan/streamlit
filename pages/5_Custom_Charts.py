# pages/5_Custom_Charts.py
import streamlit as st
import plotly.express as px
from load_data import load_dataset
from utils import section_title

section_title("🧠 Custom / Interactive Charts")
data = load_dataset()

st.subheader("Dynamic Metric Chart")
metric = st.selectbox("Select metric to plot", ['sales', 'revenue', 'customer_count'])
st.line_chart(data.set_index("date")[metric])

st.subheader("KPI Cards / Scorecards")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{data['sales'].sum():,.0f}")
col2.metric("Total Revenue", f"${data['revenue'].sum():,.2f}")
col3.metric("Avg Conversion Rate", f"{data['conversion_rate'].mean() * 100:.2f}%")

st.subheader("Small Multiples (Trellis Chart)")
st.plotly_chart(px.line(data, x="date", y="sales", facet_col="region", color="product_category"), use_container_width=True)

st.subheader("Sankey Diagram")
sankey_data = data.groupby(['channel', 'status']).size().reset_index(name='count')
labels = list(set(sankey_data['channel']) | set(sankey_data['status']))
label_index = {label: idx for idx, label in enumerate(labels)}

st.subheader("Correlation Matrix (Interactive)")
corr_metric = st.selectbox("Select metric to correlate", ['sales', 'revenue', 'customer_count'])
corr_df = data.select_dtypes(include='number').corr()[[corr_metric]].sort_values(by=corr_metric, ascending=False)
st.dataframe(corr_df.style.background_gradient(cmap='Blues'))

st.subheader("Drilldown Table by Region")
selected_region = st.selectbox("Choose Region", data['region'].unique())
drill = data[data['region'] == selected_region].groupby('product_category')[['sales', 'revenue']].sum().reset_index()
st.dataframe(drill.style.format({'sales': '{:,.0f}', 'revenue': '${:,.2f}'}))

st.subheader("Interactive Bubble Chart")
fig = px.scatter(data, x='sales', y='revenue', size='customer_count', color='region', hover_name='product_category')
st.plotly_chart(fig, use_container_width=True)




