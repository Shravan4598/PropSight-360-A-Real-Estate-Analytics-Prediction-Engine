# app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PropSight 360",
    page_icon="🏠",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
with open("Notebook/pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# =========================
# TITLE
# =========================
st.title("🏠 PropSight 360")
st.subheader("Real Estate Analytics & Prediction Engine")

st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Navigation")
st.sidebar.success("Page 1 : Price Prediction")

# =========================
# PAGE HEADER
# =========================
st.header("💰 Property Price Prediction")

st.write("Fill all property details to predict the estimated property price.")

# =========================
# INPUT SECTION
# =========================
with open('Notebook/df.pkl', 'rb') as file:
    df=pickle.load(file)
col1, col2, col3 = st.columns(3)

with col1:

    property_type = st.selectbox(
        'Property Type',
        sorted(df['property_type'].unique().tolist())
    )

    sector = st.selectbox(
        'Sector',
        sorted(df['sector'].unique().tolist())
    )

    bedrooms = float(
        st.selectbox(
            'Number of Bedroom',
            sorted(df['bedRoom'].unique().tolist())
        )
    )

    bathroom = float(
        st.selectbox(
            'Number of Bathrooms',
            sorted(df['bathroom'].unique().tolist())
        )
    )

with col2:

    balcony = float(
        st.selectbox(
            'Balconies',
            sorted(df['balcony'].unique().tolist())
        )
    )

    property_age = st.selectbox(
        'Property Age',
        sorted(df['agePossession'].unique().tolist())
    )

    built_up_area = float(
        st.number_input('Built Up Area')
    )

    servant_room = float(
        st.selectbox(
            'Servant Room',
            [0.0, 1.0]
        )
    )

with col3:

    store_room = float(
        st.selectbox(
            'Store Room',
            [0.0, 1.0]
        )
    )

    furnishing_type = float(
        st.selectbox(
            'Furnishing Type',
            sorted(df['furnishing_type'].unique().tolist())
        )
    )

    luxury_category = st.selectbox(
        'Luxury Category',
        sorted(df['luxury_category'].unique().tolist())
    )

    floor_category = st.selectbox(
        'Floor Category',
        sorted(df['floor_category'].unique().tolist())
    )
# =========================
# PREDICT BUTTON
# =========================

if st.button("🔍 Predict Price"):

    # Create dataframe
    input_df = pd.DataFrame([[
    property_type,
    sector,
    bedrooms,
    bathroom,
    balcony,
    property_age,
    built_up_area,
    servant_room,
    store_room,
    furnishing_type,
    luxury_category,
    floor_category
]], columns=[
    'property_type',
    'sector',
    'bedRoom',
    'bathroom',
    'balcony',
    'agePossession',
    'built_up_area',
    'servant room',
    'store room',
    'furnishing_type',
    'luxury_category',
    'floor_category'
])
    # Prediction
    prediction = np.expm1(pipeline.predict(input_df))[0]

    crore=prediction
    low = prediction-0.11
    high = prediction+0.11
    st.markdown("---")

    st.success("Prediction Completed")

    st.metric(
    label="Estimated Property Price",
    value=f"₹ {crore:.2f} Cr"
)

    st.info(
    f"📌 The estimated price range is between ₹ {low:.2f} Cr and ₹ {high:.2f} Cr"
)

    st.write("### 📄 Input Summary")
    st.dataframe(input_df)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("PropSight 360 © 2026 | AI Powered Real Estate Prediction System")
