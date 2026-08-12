import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📍 Incident Map")

@st.cache_data
def load_data():
    df = pd.read_csv("geocodio_results.csv")
    # Resetting index is important here so the click event matches the correct row
    return df.dropna(subset=['lat', 'lon']).reset_index(drop=True) 

df = load_data()

fig = px.scatter_mapbox(
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

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 1. Add on_select="rerun" to capture the user's click on the map
event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

# 2. Check if the user clicked a point
if len(event.selection.get("points", [])) > 0:
    # Get the row number of the point they clicked
    point_index = event.selection["points"][0]["pointIndex"]
    
    # Extract that specific row from your dataframe
    selected_data = df.iloc[point_index]
    
    st.divider()
    st.subheader("📋 Selected Incident Details")
    
    # Print the data in a clean, easily copyable markdown block
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
