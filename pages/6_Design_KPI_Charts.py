# pages/6_Design_KPI_Charts.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from load_data import load_dataset
from utils import section_title
from load_data import load_kpi_spike_data
section_title("📊 Design-Focused KPI & Dashboard Elements")

data = load_kpi_spike_data()
data['month'] = data['date'].dt.strftime('%B')
value = data['conversion_rate'].mean() * 100

st.subheader("Thermometer Gauge")
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=value,
    title={'text': "Conversion Rate %"},
    gauge={
        'axis': {'range': [0, 15]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 5], 'color': "red"},
            {'range': [5, 10], 'color': "yellow"},
            {'range': [10, 15], 'color': "green"},
        ],
    }
))

st.plotly_chart(fig, use_container_width=True)

st.subheader("Progress Donut Chart")
fig = go.Figure(go.Pie(
    values=[value, 100 - value],
    hole=0.6,
    textinfo='none',
    marker_colors=['royalblue', 'lightgray']
))
fig.update_layout(
    showlegend=False,
    annotations=[dict(text=f'{value:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sparkline Chart (Monthly Sales Avg)")
spark_data = data.groupby('month')["sales"].mean().reset_index()
st.line_chart(spark_data.set_index('month'))


st.subheader("Conversion Rate Change")
last_month = data[data['date'].dt.month == data['date'].dt.month.max()]
prev_month = data[data['date'].dt.month == (data['date'].dt.month.max() - 1)]

current_val = last_month['conversion_rate'].mean() * 100
prev_val = prev_month['conversion_rate'].mean() * 100

st.metric("Current Conversion Rate", f"{current_val:.2f}%", delta=f"{(current_val - prev_val):+.2f}%")



