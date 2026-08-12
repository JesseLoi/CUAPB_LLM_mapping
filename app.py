import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Incident Map")

@st.cache_data
def load_data():
    df = pd.read_csv("stream_map_material.csv")
    # Resetting index is important here so the click event matches the correct row
    return df.dropna(subset=['lat', 'lon']).reset_index(drop=True) 

df = load_data()

# 1. FIXED: Using scatter_map instead of scatter_mapbox
fig = px.scatter_map(
    df,
    lat="lat",
    lon="lon",
    hover_name="original",
    hover_data={
        "original": False, 
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

# 2. FIXED: Using map_style instead of mapbox_style
fig.update_layout(map_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 3. FIXED: Using width="stretch" instead of use_container_width=True
event = st.plotly_chart(fig, width="stretch", on_select="rerun")

if len(event.selection.get("points", [])) > 0:
    # 4. FIXED: Using 'point_index' instead of 'pointIndex'
    point_index = event.selection["points"][0]["point_index"]
    
    selected_data = df.iloc[point_index]
    
    st.divider()
    st.subheader("Selected Details")
    
    st.markdown(f"""
    **Original Input:** {selected_data['original']}  
    **Matched Address:** {selected_data['found_address']}  
    **Coordinates:** {selected_data['lat']}, {selected_data['lon']}  
    **Date:** {selected_data['date2']}  
    **Location:** {selected_data['location']}  
    **Classification:** {selected_data['classification2']}  
    **Incident Type:** {selected_data['incident_type2']}  
    **URL:** {selected_data['url']}  
    """)
