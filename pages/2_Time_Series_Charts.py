# pages/2_Time_Series_Charts.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from load_data import load_dataset
from utils import section_title
from statsmodels.tsa.holtwinters import ExponentialSmoothing

section_title("📈 Time-Series Charts")
data = load_dataset()

st.subheader("Line Chart - Sales Over Time")
st.line_chart(data.set_index("date")["sales"])

st.subheader("Moving Average (14-day)")
data_sorted = data.sort_values("date")
data_sorted["sales_rolling"] = data_sorted["sales"].rolling(window=14).mean()
st.line_chart(data_sorted.set_index("date")["sales_rolling"])

st.subheader("Sales Forecast (30 Days)")
sales_ts = data.set_index("date")["sales"].resample("D").mean().ffill()
model = ExponentialSmoothing(sales_ts, trend="add", seasonal=None).fit()
forecast = model.forecast(30)
forecast_df = pd.DataFrame({"date": forecast.index, "forecast": forecast.values})
st.line_chart(pd.concat([sales_ts, forecast_df.set_index("date")], axis=1))

st.subheader("Calendar Heatmap")
calendar_data = data.groupby("date")["sales"].sum().reset_index()
calendar_data["day"] = calendar_data["date"].dt.day
calendar_data["month"] = calendar_data["date"].dt.month_name()
st.plotly_chart(px.density_heatmap(calendar_data, x="day", y="month", z="sales", histfunc="avg"), use_container_width=True)

from statsmodels.tsa.seasonal import seasonal_decompose

st.subheader("Seasonal Decomposition")
decomp = seasonal_decompose(sales_ts, model='additive', period=30)
fig = go.Figure()
fig.add_trace(go.Scatter(x=decomp.trend.index, y=decomp.trend, name='Trend'))
fig.add_trace(go.Scatter(x=decomp.seasonal.index, y=decomp.seasonal, name='Seasonal'))
fig.add_trace(go.Scatter(x=decomp.resid.index, y=decomp.resid, name='Residual'))
st.plotly_chart(fig, use_container_width=True)



st.subheader("Interactive Sales Time Series")
fig = px.line(data, x='date', y='sales')
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Sales vs Revenue Over Time")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['date'], y=data['sales'], name='Sales', yaxis='y1'))
fig.add_trace(go.Scatter(x=data['date'], y=data['revenue'], name='Revenue', yaxis='y2'))

fig.update_layout(
    yaxis=dict(title='Sales'),
    yaxis2=dict(title='Revenue', overlaying='y', side='right'),
    xaxis=dict(title='Date')
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales Anomalies (Z-score method)")
from scipy.stats import zscore
data['z_score'] = zscore(data['sales'])
anomalies = data[data['z_score'].abs() > 2]
fig = px.line(data, x='date', y='sales')
fig.add_scatter(x=anomalies['date'], y=anomalies['sales'], mode='markers', marker=dict(color='red', size=10), name='Anomaly')
st.plotly_chart(fig, use_container_width=True)
