
import streamlit
from streamlit_folium import st_folium
import folium

import pandas as pd
import geopandas as gpd

ref_point_lon = 9.6929923
ref_point_lat = 62.5931427

m = folium.Map(location=[62.5931427,9.6929923], zoom_start=10)
folium.Marker(
    location=[62.5931427,9.6929923],
    popup= 'Test' ,
    tooltip='test'
    ).add_to(m)

st_data = st_folium(m)

# st_folium(mymap, width=375)
