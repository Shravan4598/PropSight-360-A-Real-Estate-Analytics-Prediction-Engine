# pages/2_Analytics_Module.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from wordcloud import WordCloud

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Analytics Module",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("📊 Gurgaon Real Estate Analytics Module")

st.markdown("---")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Notebook/gurgaon_sector_coordinates.csv")

    return df

df = load_data()

# =========================================================
# LOAD WORDCLOUD TEXT
# =========================================================

@st.cache_data
def load_wordcloud():

    feature_text = pickle.load(
        open('Notebook/feature_text.pkl', 'rb')
    )

    return feature_text

feature_text = load_wordcloud()

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Filter Properties")

sector_options = sorted(
    df['sector'].dropna().unique()
)

selected_sector = st.sidebar.multiselect(
    "Select Sector",
    sector_options
)

property_options = sorted(
    df['property_type'].dropna().unique()
)

selected_property = st.sidebar.multiselect(
    "Select Property Type",
    property_options
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if len(selected_sector) > 0:

    filtered_df = filtered_df[
        filtered_df['sector'].isin(selected_sector)
    ]

if len(selected_property) > 0:

    filtered_df = filtered_df[
        filtered_df['property_type'].isin(selected_property)
    ]

# =========================================================
# MAP DATA
# =========================================================

map_df = filtered_df.drop_duplicates(
    subset='sector'
).copy()

# =========================================================
# CREATE CENTER COORDINATES
# =========================================================

map_df['latitude'] = (
    map_df['nw_lat'] +
    map_df['ne_lat'] +
    map_df['sw_lat'] +
    map_df['se_lat']
) / 4

map_df['longitude'] = (
    map_df['nw_lon'] +
    map_df['ne_lon'] +
    map_df['sw_lon'] +
    map_df['se_lon']
) / 4

# =========================================================
# CHOROPLETH MAP
# =========================================================

st.subheader("📍 Gurgaon Sector Price Heatmap")

features = []

for idx, row in map_df.iterrows():

    feature = {
        "type": "Feature",
        "id": row['sector'],
        "properties": {
            "sector": row['sector']
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[

                [row['nw_lon'], row['nw_lat']],
                [row['ne_lon'], row['ne_lat']],
                [row['se_lon'], row['se_lat']],
                [row['sw_lon'], row['sw_lat']],
                [row['nw_lon'], row['nw_lat']]

            ]]
        }
    }

    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

fig = px.choropleth_mapbox(
    map_df,

    geojson=geojson,

    locations='sector',

    featureidkey="properties.sector",

    color='price_per_sqft',

    hover_name='sector',

    color_continuous_scale='Turbo',

    mapbox_style='carto-positron',

    center={
        "lat": 28.4595,
        "lon": 77.0266
    },

    zoom=10,

    opacity=0.5
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# SCATTER GEO MAP
# =========================================================

st.subheader("🗺️ Sector Scatter Geo Map")

fig2 = px.scatter_mapbox(
    map_df,

    lat="latitude",
    lon="longitude",

    color="price_per_sqft",

    size="price_per_sqft",

    hover_name="sector",

    hover_data=[
        'price_per_sqft'
    ],

    zoom=10,

    height=700,

    mapbox_style="open-street-map",

    color_continuous_scale="YlOrRd"
)

fig2.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
# =========================================================
# VORONOI MAP
# =========================================================

st.subheader("🧭 Voronoi Sector Price Map")

# -----------------------------------
# Create Center Coordinates
# -----------------------------------

map_df['latitude'] = (
    map_df['nw_lat'] +
    map_df['ne_lat'] +
    map_df['sw_lat'] +
    map_df['se_lat']
) / 4

map_df['longitude'] = (
    map_df['nw_lon'] +
    map_df['ne_lon'] +
    map_df['sw_lon'] +
    map_df['se_lon']
) / 4

# -----------------------------------
# Create Points
# -----------------------------------

points = map_df[['longitude', 'latitude']].dropna().values

# -----------------------------------
# Voronoi Tessellation
# -----------------------------------

from scipy.spatial import Voronoi
from shapely.geometry import Polygon
import geopandas as gpd
import json

vor = Voronoi(points)

# -----------------------------------
# Convert Voronoi Regions to Polygons
# -----------------------------------

polygons = []

for region_index in vor.point_region:

    region = vor.regions[region_index]

    if -1 in region or len(region) == 0:

        polygons.append(None)

        continue

    polygon = Polygon([
        vor.vertices[i] for i in region
    ])

    polygons.append(polygon)

# -----------------------------------
# GeoDataFrame
# -----------------------------------

gdf = gpd.GeoDataFrame(
    map_df,
    geometry=polygons
)

# -----------------------------------
# Remove Invalid Polygons
# -----------------------------------

gdf = gdf[
    gdf.geometry.notnull()
]

# -----------------------------------
# Convert to GeoJSON
# -----------------------------------

geojson = json.loads(
    gdf.to_json()
)

# -----------------------------------
# Choropleth Voronoi Map
# -----------------------------------

fig_voronoi = px.choropleth_mapbox(
    gdf,

    geojson=geojson,

    locations=gdf.index,

    color='price_per_sqft',

    hover_name='sector',

    color_continuous_scale='YlOrRd',

    mapbox_style='carto-positron',

    center={
        "lat": 28.4595,
        "lon": 77.0266
    },

    zoom=10,

    opacity=0.75
)

fig_voronoi.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    height=750
)

st.plotly_chart(
    fig_voronoi,
    use_container_width=True
)
# =========================================================
# WORD CLOUD
# =========================================================

st.subheader("☁️ Amenities WordCloud")

wordcloud = WordCloud(
    width=1200,
    height=600,

    background_color='white',

    stopwords=set(['s']),

    min_font_size=10
).generate(feature_text)

fig3, ax = plt.subplots(
    figsize=(15,8)
)

ax.imshow(
    wordcloud,
    interpolation='bilinear'
)

ax.axis("off")

st.pyplot(fig3)

# =========================================================
# AREA VS PRICE
# =========================================================

st.subheader("📈 Area Vs Price")

fig4 = px.scatter(
    filtered_df,

    x="built_up_area",
    y="price",

    color="bedRoom",

    title="Built Up Area Vs Price",

    hover_data=[
        'sector',
        'property_type'
    ]
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================================================
# PIE CHART
# =========================================================

st.subheader("🥧 BHK Distribution")

bhk_df = filtered_df[
    'bedRoom'
].value_counts().reset_index()

bhk_df.columns = [
    'BHK',
    'Count'
]

fig5 = px.pie(
    bhk_df,

    names='BHK',
    values='Count',

    title='BHK Distribution'
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# =========================================================
# BOX PLOT
# =========================================================

st.subheader("📦 BHK Price Range")

temp_df = filtered_df[
    filtered_df['bedRoom'] <= 4
]

fig6 = px.box(
    temp_df,

    x='bedRoom',
    y='price',

    color='bedRoom',

    title='BHK Price Distribution'
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# =========================================================
# PRICE DISTRIBUTION
# =========================================================

st.subheader("📊 Property Price Distribution")

fig7, ax = plt.subplots(
    figsize=(12,6)
)

sns.histplot(
    filtered_df[
        filtered_df['property_type'] == 'house'
    ]['price'],

    kde=True,

    label='House',

    ax=ax
)

sns.histplot(
    filtered_df[
        filtered_df['property_type'] == 'flat'
    ]['price'],

    kde=True,

    label='Flat',

    ax=ax
)

ax.legend()

st.pyplot(fig7)
# =========================================================
# SUNBURST CHART
# =========================================================

st.subheader("🌞 Property Type Distribution by Bedrooms")

fig8 = px.sunburst(
    filtered_df,

    path=['bedRoom', 'property_type'],

    values='price_per_sqft',

    title='Property Type Distribution by Bedrooms'
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# =========================================================
# DATA PREVIEW
# =========================================================

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head()
)
