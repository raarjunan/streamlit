# pages/1_Basic_Charts.py
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from load_data import load_dataset
from utils import section_title

section_title("📊 Basic Charts")
data = load_dataset()
data['month'] = data['date'].dt.strftime('%B')

st.subheader("Bar Chart")
st.plotly_chart(
    px.bar(data.groupby('product_category')['sales'].sum().reset_index(), x='product_category', y='sales'),
    use_container_width=True
)

st.subheader("Stacked Bar Chart")
st.plotly_chart(
    px.bar(data, x='month', y='sales', color='region', barmode='stack'),
    use_container_width=True
)

st.subheader("Line Chart")
st.plotly_chart(
    px.line(data, x='date', y='sales', color='region'),
    use_container_width=True
)

st.subheader("Area Chart")
st.area_chart(data.set_index('date')['sales'])

st.subheader("Box-and-Whisker Plot")
st.plotly_chart(
    px.box(data, x='product_category', y='sales', color='product_category'),
    use_container_width=True
)

st.subheader("Heat Map (Correlation)")
corr = data.select_dtypes(include='number').corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)

st.subheader("Histogram of Sales")
st.plotly_chart(px.histogram(data, x='sales', nbins=30), use_container_width=True)

st.subheader("Strip Plot of Sales by Category")
st.plotly_chart(px.strip(data, x='product_category', y='sales', color='product_category', stripmode='overlay'), use_container_width=True)

st.subheader("Violin Plot of Revenue by Region")
st.plotly_chart(px.violin(data, x='region', y='revenue', box=True, points="all"), use_container_width=True)

st.subheader("Sales vs Revenue (Scatter)")
st.plotly_chart(px.scatter(data, x='sales', y='revenue', size='customer_count', color='region'), use_container_width=True)

st.subheader("Revenue vs Customer Count (Density Contour)")
st.plotly_chart(px.density_contour(data, x='revenue', y='customer_count', color='region'), use_container_width=True)
