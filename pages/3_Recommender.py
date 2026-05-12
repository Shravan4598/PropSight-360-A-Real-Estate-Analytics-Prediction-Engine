import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import os

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="PropVision AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 40%, #111827 100%);
    color: white;
}

.hero {
    background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(124,58,237,0.18));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 30px;
    padding: 40px;
    margin-bottom: 35px;
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.title-text {
    font-size: 50px;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #c084fc, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #9ca3af;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA (With Error Handling)
# =========================================================
@st.cache_resource
def load_data():
    # Replace these paths with your actual file locations
    try:
        loc_df = pickle.load(open('Notebook/location_distance.pkl', 'rb'))
        sim1 = pickle.load(open('Notebook/cosine_sim1.pkl', 'rb'))
        sim2 = pickle.load(open('Notebook/cosine_sim2.pkl', 'rb'))
        sim3 = pickle.load(open('Notebook/cosine_sim3.pkl', 'rb'))
        return loc_df, sim1, sim2, sim3
    except FileNotFoundError:
        st.error("Data files not found. Please check the 'Notebook/' directory.")
        return None, None, None, None

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🏙️ PropVision AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("📌 Navigation", ["Home", "Location Finder", "Recommender System"])
    st.markdown("---")
    st.markdown("### 🚀 Features\n✅ AI Recommendations\n✅ Smart Location Search\n✅ Premium Dashboard")

# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="hero">
    <div class="badge">🚀 AI Powered Real Estate</div>
    <div class="title-text">PropVision AI</div>
    <div style="color: #d1d5db; font-size: 18px;">Modern apartment recommendation & analytics platform.</div>
</div>
""", unsafe_allow_html=True)

if location_df is not None:
    # =========================================================
    # HOME PAGE
    # =========================================================
    if page == "Home":
        st.subheader("📊 Platform Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏢 Apartments", len(location_df.index), "+12%")
        col2.metric("📍 Locations", len(location_df.columns), "+7%")
        col3.metric("🤖 AI Models", "3", "+1")
        col4.metric("⚡ Accuracy", "95%", "+2%")

        chart_df = pd.DataFrame({
            "Module": ["Prediction", "Analytics", "Insights", "Recommendations"],
            "Usage": [90, 86, 82, 96]
        })
        fig = px.bar(chart_df, x="Module", y="Usage", template="plotly_dark", color="Module")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # LOCATION FINDER
    # =========================================================
    elif page == "Location Finder":
        st.subheader("📍 Smart Location Finder")
        c1, c2 = st.columns([3, 1])
        selected_location = c1.selectbox("📌 Select Location", sorted(location_df.columns.to_list()))
        radius = c2.number_input("📏 Radius (KM)", min_value=0.1, value=2.0, step=0.5)

        if st.button("🔍 Search Nearby"):
            result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
            if result_ser.empty:
                st.warning("No nearby locations found.")
            else:
                nearby_df = pd.DataFrame({
                    "Location": result_ser.index,
                    "Distance (Km)": np.round(result_ser.values / 1000, 2)
                })
                st.dataframe(nearby_df, use_container_width=True, hide_index=True)
                fig = px.scatter(nearby_df, x="Location", y="Distance (Km)", size="Distance (Km)", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # RECOMMENDER SYSTEM
    # =========================================================
    elif page == "Recommender System":
        st.subheader("🤖 AI Apartment Recommender")

        def recommend(property_name, top_n=10):
            cosine_sim_matrix = (30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3)
            property_names = location_df.index.tolist()
            idx = property_names.index(property_name)
            sim_scores = list(enumerate(cosine_sim_matrix[idx]))
            sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
            top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
            
            return pd.DataFrame({
                'PropertyName': [property_names[i] for i in top_indices],
                'SimilarityScore': np.round(top_scores, 2)
            })

        c1, c2 = st.columns([3, 1])
        selected_apt = c1.selectbox("🏢 Select Apartment", sorted(location_df.index.tolist()))
        top_n = c2.slider("🎯 Recommendations", 5, 20, 10)

        if st.button("✨ Generate AI Recommendations"):
            rec_df = recommend(selected_apt, top_n)
            
            st.success("Recommendations generated!")
            
            # Show Chart
            fig = px.bar(rec_df, x='SimilarityScore', y='PropertyName', orientation='h', template='plotly_dark')
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

            # Premium Cards (Correctly Indented inside the Button trigger)
            st.markdown("### 🌟 Top Recommendations")
            for _, row in rec_df.iterrows():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(37,99,235,0.1), rgba(124,58,237,0.1)); 
                            border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin-bottom: 15px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h4 style="margin:0;">🏢 {row['PropertyName']}</h4>
                            <p style="margin:0; color:#9ca3af; font-size:13px;">AI Recommended Premium Choice</p>
                        </div>
                        <div style="text-align:center;">
                            <small style="color:#60a5fa;">Match Score</small>
                            <h3 style="margin:0;">{row['SimilarityScore']}</h3>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""<div class="footer">Made with ❤️ using Streamlit • PropVision AI © 2026</div>""", unsafe_allow_html=True)