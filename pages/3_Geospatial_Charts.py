# pages/3_Geospatial_Charts.py
import streamlit as st
import pydeck as pdk
import plotly.express as px
from load_data import load_dataset
from utils import section_title
import pandas as pd

section_title("📍 Geospatial Charts")
data = load_dataset()

st.subheader("Choropleth Map (Simulated by Region)")
choropleth_data = data.groupby("region")["sales"].sum().reset_index()
region_map = {
    'North': 'NY',  # New York
    'South': 'TX',  # Texas
    'East': 'FL',   # Florida
    'West': 'CA'    # California
}
choropleth_data['state_code'] = choropleth_data['region'].map(region_map)

fig = px.choropleth(
    choropleth_data,
    locations="state_code",
    locationmode="USA-states",
    color="sales",
    scope="usa"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Symbol Map (Scatterplot Layer)")
symbol_data = data.dropna(subset=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(latitude=37.5, longitude=-122.3, zoom=4),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=symbol_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=1000,  # Increase radius
            pickable=True
        )
    ]
))

st.subheader("Heatmap (Density Layer)")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=pdk.ViewState(latitude=37.5, longitude=-122.3, zoom=4, pitch=50),
    layers=[pdk.Layer(
        "HeatmapLayer",
        data=data.dropna(subset=['lat', 'lon']),
        get_position='[lon, lat]',
        aggregation='MEAN')
    ]
))


st.subheader("Bubble Map (Sales by Location)")
fig = px.scatter_geo(
    symbol_data,
    lat='lat',
    lon='lon',
    size='sales',
    color='region',
    hover_name='region',
    scope='usa',
    title="Sales by Geo Location (Bubble Size)"
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("3D Hexagon Density Layer")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=pdk.ViewState(latitude=37.5, longitude=-122.3, zoom=5, pitch=40),
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=symbol_data,
            get_position='[lon, lat]',
            radius=2000,
            elevation_scale=50,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        )
    ]
))


st.subheader("Clustered Sales Map")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(latitude=37.5, longitude=-122.3, zoom=4),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=symbol_data,
            get_position='[lon, lat]',
            get_color='[0, 140, 255, 140]',
            get_radius='sales',
            pickable=True
        )
    ],
    tooltip={"text": "Region: {region}\nSales: {sales}"}
))


st.subheader("Curved Line Between Two Points (ArcLayer)")

arc_data = pd.DataFrame({
    "from_lat": [37.7749],      # San Francisco
    "from_lon": [-122.4194],
    "to_lat": [34.0522],        # Los Angeles
    "to_lon": [-118.2437],
    "source": ["San Francisco"],
    "target": ["Los Angeles"]
})

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=36.0,
        longitude=-120.0,
        zoom=5,
        pitch=0
    ),
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=arc_data,
            get_source_position='[from_lon, from_lat]',
            get_target_position='[to_lon, to_lat]',
            get_source_color=[0, 128, 200],
            get_target_color=[255, 0, 0],
            auto_highlight=True,
            width_scale=0.5,
            get_width=5,
            pickable=True
        )
    ],
    tooltip={"text": "From: {source}\nTo: {target}"}
))
