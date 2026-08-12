import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📍 Incident Map")

@st.cache_data
def load_data():
    df = pd.read_csv("stream_map_material.csv")
    # Drop rows that failed to get coordinates so the map doesn't crash
    return df.dropna(subset=['lat', 'lon'])

df = load_data()

# Build the map with all requested columns in the tooltip
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="original", # This displays the original address as the bold title
    hover_data={
        "original": False, # Set to False here so it doesn't duplicate the title
        "found_address": True, 
        "lat": True, 
        "lon": True,
        "url": True,
        "classification2": True,
        "incident_type2": True,
        "location": True,
        "date2": True
    },
    zoom=10, 
    height=700
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)