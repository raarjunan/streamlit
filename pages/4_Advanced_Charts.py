# pages/4_Advanced_Charts.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from load_data import load_dataset
from utils import section_title

section_title("💡 Advanced Charts")
data = load_dataset()
data['month'] = data['date'].dt.strftime('%B')


st.subheader("Pareto Chart")
pareto = data.groupby('product_category')['sales'].sum().sort_values(ascending=False).reset_index()
pareto['cum_perc'] = pareto['sales'].cumsum() / pareto['sales'].sum() * 100
fig = go.Figure()
fig.add_bar(x=pareto['product_category'], y=pareto['sales'], name='Sales')
fig.add_scatter(x=pareto['product_category'], y=pareto['cum_perc'], yaxis='y2', name='Cumulative %')
fig.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0, 110]))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Control Chart")
control_data = data.set_index('date').resample('D')['sales'].mean().dropna()
mean = control_data.mean()
std = control_data.std()
fig = go.Figure()
fig.add_trace(go.Scatter(x=control_data.index, y=control_data.values, mode='lines', name='Sales'))
fig.add_trace(go.Scatter(x=control_data.index, y=[mean]*len(control_data), name='Mean'))
fig.add_trace(go.Scatter(x=control_data.index, y=[mean+3*std]*len(control_data), name='Upper Limit', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=control_data.index, y=[mean-3*std]*len(control_data), name='Lower Limit', line=dict(dash='dash')))
st.plotly_chart(fig, use_container_width=True)


st.subheader("Bullet Chart (simulated)")
# Bullet-like chart using bar and scatter
metric = data.groupby('region')['sales'].sum().reset_index()
targets = {'North': 25000, 'South': 26000, 'East': 24000, 'West': 23000}
metric['target'] = metric['region'].map(targets)
fig = go.Figure()
fig.add_trace(go.Bar(x=metric['sales'], y=metric['region'], orientation='h', name='Sales'))
fig.add_trace(go.Scatter(x=metric['target'], y=metric['region'], mode='markers', marker=dict(color='red', size=12), name='Target'))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Radar / Spider Chart")
radar_data = data.groupby("region")[['sales', 'revenue', 'customer_count']].mean().reset_index()
categories = ['sales', 'revenue', 'customer_count']
fig = go.Figure()
for i, row in radar_data.iterrows():
    fig.add_trace(go.Scatterpolar(r=row[categories].values, theta=categories, fill='toself', name=row['region']))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sunburst Chart")
st.plotly_chart(px.sunburst(data, path=['parent_category', 'product_category', 'region'], values='sales'), use_container_width=True)


st.subheader("Lifecycle Funnel")
funnel = data.groupby('status')["conversion_rate"].mean().sort_values(ascending=False).reset_index()
st.plotly_chart(px.funnel(funnel, x='conversion_rate', y='status'), use_container_width=True)


st.subheader("Race Bar Chart")
race_data = data.groupby(['month', 'region'])['sales'].sum().reset_index()
st.plotly_chart(px.bar(race_data, x='region', y='sales', animation_frame='month', color='region', range_y=[0, race_data['sales'].max()]), use_container_width=True)

st.subheader("Animated Bubble Trail")
st.plotly_chart(px.scatter(data, x='sales', y='revenue', animation_frame='month', color='region', size='customer_count'), use_container_width=True)


st.subheader("Treemap (Category Breakdown)")
st.plotly_chart(
    px.treemap(data, path=['parent_category', 'product_category'], values='sales'),
    use_container_width=True
)


st.subheader("Waterfall Chart")
waterfall_data = pd.DataFrame({
    'Stage': ['Revenue', 'Cost', 'Profit'],
    'Value': [data['revenue'].sum(), -data['cost'].sum(), data['revenue'].sum() - data['cost'].sum()]
})
fig = go.Figure(go.Waterfall(
    x=waterfall_data['Stage'],
    y=waterfall_data['Value'],
    connector={"line": {"color": "rgb(63, 63, 63)"}}
))
st.plotly_chart(fig, use_container_width=True)

