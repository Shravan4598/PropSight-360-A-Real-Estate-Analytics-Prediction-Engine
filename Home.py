import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PropSight 360 | Home",
    page_icon="🏠",
    layout="wide"
)

# =========================
# CUSTOM PREMIUM CSS
# =========================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Hero Section */
    .hero-container {
        padding: 80px 40px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        text-align: center;
        margin-bottom: 50px;
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-size: 80px;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #c084fc, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .sub-title {
        font-size: 24px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    /* Card Styling */
    .module-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease;
        height: 100%;
    }
    
    .module-card:hover {
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.08);
        border-color: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero-container">
    <div class="main-title">PropSight 360</div>
    <div class="sub-title">A Real Estate Analytics & Prediction Engine</div>
    <p style="max-width: 800px; margin: 0 auto; color: #cbd5e1; font-size: 18px;">
        Harnessing advanced Machine Learning and Geospatial Analytics to decode the Gurgaon 
        property market. Predict values, explore trends, and find your next investment with precision.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# FEATURE GRID
# =========================
st.markdown("### 🛠 Explore our AI Modules")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown("""
    <div class="module-card">
        <h3>💰 Price Predictor</h3>
        <p>Input property specs to get an instant valuation driven by our Random Forest pipeline with 95% accuracy.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Spacer

with col2:
    st.markdown("""
    <div class="module-card">
        <h3>📊 Analytics Dashboard</h3>
        <p>Interactive heatmaps, Voronoi tessellations, and price distribution charts for every sector in Gurgaon.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

with col3:
    st.markdown("""
    <div class="module-card">
        <h3>🤖 Smart Recommender</h3>
        <p>Found something you like? Our similarity engine finds the closest matches based on luxury, area, and amenities.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="module-card">
        <h3>📈 Impact Insights</h3>
        <p>Ever wondered what adds the most value? See the mathematical weight of every feature like BHK, area, and sector.</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR NAVIGATION INFO
# =========================
st.sidebar.title("💎 Navigation")
st.sidebar.info("Select a page above to launch a specific module.")
