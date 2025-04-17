# pages/9_Extra_Charts.py
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from statsmodels.graphics.mosaicplot import mosaic
from load_data import load_dataset
from utils import section_title
from load_data import load_text_blob
import plotly.express as px


section_title("✨ Extras & Bonus Charts")
data = load_dataset()

st.subheader("Word Cloud from Product Category")

text = load_text_blob()

wc = WordCloud(background_color='white').generate(text)
fig, ax = plt.subplots()
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

st.subheader("Butterfly (Tornado) Chart: North vs South")
bfly_data = data[data['region'].isin(['North', 'South'])]
bfly_grouped = bfly_data.groupby(['product_category', 'region'])['sales'].sum().unstack().fillna(0)
bfly_grouped['South'] = -bfly_grouped['South']

fig = go.Figure()
fig.add_trace(go.Bar(y=bfly_grouped.index, x=bfly_grouped['North'], name='North', orientation='h'))
fig.add_trace(go.Bar(y=bfly_grouped.index, x=bfly_grouped['South'], name='South', orientation='h'))
fig.update_layout(barmode='relative', title='Butterfly Chart: North vs South Sales', xaxis_title='Sales')
st.plotly_chart(fig, use_container_width=True)

st.subheader("Mosaic Plot: Region vs Product Category")
fig, _ = mosaic(data, ['region', 'product_category'], title='Mosaic: Region vs Category')
st.pyplot(fig)


st.subheader("Interactive Category Mosaic (via Treemap)")
fig = px.treemap(data, path=['region', 'product_category'], values='sales')
st.plotly_chart(fig, use_container_width=True)


st.subheader("Dumbbell Chart: Revenue Comparison")
revenue = data[data['region'].isin(['North', 'South'])].groupby(['product_category', 'region'])['revenue'].mean().unstack()
fig = go.Figure()
for idx, row in revenue.iterrows():
    fig.add_trace(go.Scatter(x=[row['North'], row['South']], y=[idx, idx], mode='lines+markers', name=idx))
st.plotly_chart(fig, use_container_width=True)

import streamlit.components.v1 as components

st.subheader("🧊 Interactive 3D Model")
components.html("""
  <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
  <model-viewer src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
                alt="A 3D model"
                auto-rotate
                camera-controls
                style="width: 100%; height: 500px;">
  </model-viewer>
""", height=550)

st.subheader("🚢 Norwegian Sun – Interactive 3D Model")

components.html("""
<div class="sketchfab-embed-wrapper">
  <iframe title="Norwegian Sun" frameborder="0"
    allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true"
    allow="autoplay; fullscreen; xr-spatial-tracking"
    xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share
    width="100%" height="500"
    src="https://sketchfab.com/models/258c3832b9474bfd8e54e2ff703df122/embed">
  </iframe>
</div>
""", height=520)

