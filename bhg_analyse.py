import pandas as pd
import geopandas as gpd

from shapely.geometry import Point

import streamlit as st
import folium
from streamlit_folium import folium_static

df = pd.read_excel('data.xlsx')

# Convert UTM coordinates to Point geometry
df['geometry'] = [Point(xy) for xy in zip(df.UTM_X, df.UTM_Y)]
# gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.set_crs(epsg=4326, inplace=True)


df['voksentetthet'] = df['Ant_ansatte']/df['Ant_barn']
ref_point_lon = '9.6929923'
ref_point_lat = '62.5931427'

ref_point = Point(ref_point_lon, ref_point_lat)

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.UTM_X, df.UTM_Y))

# Set CRS to WGS84 (if it's not already)
gdf = gdf.set_crs(epsg=4326)

# Find a suitable UTM zone CRS for your region and reproject
gdf = gdf.to_crs(epsg=32632)
ref_point = gpd.GeoSeries([ref_point], crs=4326).to_crs(epsg=32632)[0]

df['AvstandJernbane'] = gdf['geometry'].distance(ref_point)



# farger for å visualisere voksentetthet
def get_color(ratio):
    if ratio > 0.245:
        return 'green'
    elif 0.229 <= ratio < 0.245:
        return 'orange'
    else:
        return 'red'

map_center = [df['UTM_Y'].mean(), df['UTM_X'].mean()]
mymap = folium.Map(location=map_center, zoom_start=12)

# Add circles with colors
for idx, row in df.iterrows():
    folium.Circle(
        location=[row['UTM_Y'], row['UTM_X']],
        popup=f"{row['Barnehage']}<br>Barn: {row['Ant_barn']}<br>Ansatte: {row['Ant_ansatte']}<br>Voksentetthet: {row['voksentetthet']:.2f}",
        radius=row['Ant_barn'] * 10,  # Adjust as necessary
        color=get_color(row['voksentetthet']),
        fill=True,
        fill_color=get_color(row['voksentetthet'])
    ).add_to(mymap)

# Display the map
mymap


st.title('Kartanalyse barnehager')
folium_static(mymap)


