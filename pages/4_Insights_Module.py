import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Insights Engine",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# LOAD FILES & CACHE
# =========================================================
@st.cache_data
def load_data():
    # Ensure these paths are correct relative to your app root
    coef_df = pickle.load(open("Notebook/coef_df.pkl", "rb"))
    feature_names = pickle.load(open("Notebook/feature_names.pkl", "rb"))
    return coef_df, feature_names

try:
    coef_df, feature_names = load_data()
except FileNotFoundError:
    st.error("Model files not found. Please check 'Notebook/' directory.")
    st.stop()

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%);
        color: white;
    }
    .main-title {
        font-size: 50px; font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle { color: #cbd5e1; font-size: 18px; margin-bottom: 40px; }
    .metric-card {
        background: linear-gradient(135deg, rgba(37,99,235,0.2), rgba(124,58,237,0.2));
        border-radius: 28px; padding: 35px; text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    .metric-value { font-size: 64px; font-weight: 800; color: white; }
    .feature-card {
        background: rgba(255,255,255,0.05); border-radius: 20px;
        padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08);
        transition: 0.3s; height: 100%;
    }
    .feature-card:hover { transform: translateY(-5px); background: rgba(255,255,255,0.08); }
    .positive { color: #4ade80; }
    .negative { color: #f87171; }
    .section-title { font-size: 28px; font-weight: 700; margin: 30px 0 15px 0; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="main-title">AI Property Insights Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Simulate property configurations and discover key price drivers using Explainable AI.</div>', unsafe_allow_html=True)

# =========================================================
# INTERACTIVE SIMULATOR
# =========================================================
st.markdown('<div class="section-title">🎛 Interactive Property Simulator</div>', unsafe_allow_html=True)

# Extract Sectors efficiently
sector_features = [col for col in feature_names if col.startswith("sector_")]
sector_names = sorted([col.replace("sector_", "") for col in sector_features])

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        property_type = st.selectbox("🏠 Property Type", ["flat", "house"])
        bedroom = st.slider("🛏 Bedrooms", 1, 10, 3)
        bathroom = st.slider("🚿 Bathrooms", 1, 10, 3)
        builtup = st.number_input("📐 Area (sq.ft)", 500, 50000, 2500, 50)
    
    with col2:
        furnishing = st.selectbox("🛋 Furnishing", ["unfurnished", "semi-furnished", "furnished"])
        luxury = st.selectbox("✨ Luxury Category", ["Low", "Medium", "High"])
        servant = st.selectbox("👨‍🍳 Servant Room", [0, 1])
        age = st.selectbox("🏗 Age Possession", ["new", "old"])
    
    with col3:
        selected_sector = st.selectbox("📍 Select Sector", sector_names)

# =========================================================
# DATA ENCODING & PREDICTION (Mathematical Logic)
# =========================================================
# Prepare input dictionary mapping directly to feature names
input_dict = {feat: 0 for feat in feature_names}

input_dict.update({
    "bedRoom": bedroom,
    "bathroom": bathroom,
    "built_up_area": builtup,
    "servant room": servant,
    "property_type": 1 if property_type == "house" else 0,
    "furnishing_type": {"unfurnished": 0, "semi-furnished": 1, "furnished": 2}[furnishing],
    "luxury_category": {"Low": 0, "Medium": 1, "High": 2}[luxury],
    f"agePossession_{age}": 1,
    f"sector_{selected_sector}": 1
})

# Vectorized Calculation for Speed
input_series = pd.Series(input_dict)
# Align coef_df with input features and multiply
aligned_coefs = coef_df.set_index('feature')['original_coef']
total_effect = (input_series * aligned_coefs).sum()

# Log-Linear transformation formula: Price Change % = (exp(coeff) - 1) * 100
price_change = (np.exp(total_effect) - 1) * 100

# =========================================================
# RESULTS DISPLAY
# =========================================================
st.markdown(f"""
    <div class="metric-card">
        <div style="color: #cbd5e1; font-size: 20px;">Estimated Impact on Property Price</div>
        <div class="metric-value">{price_change:+.2f}%</div>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# VISUAL ANALYSIS
# =========================================================
tab1, tab2 = st.tabs(["📊 Impact Analysis", "🤖 AI Insights"])

with tab1:
    st.markdown('<div class="section-title">Feature Impact Waterfall</div>', unsafe_allow_html=True)
    chart_df = coef_df.sort_values("price_impact_percent").tail(20)
    fig = px.bar(
        chart_df, x="price_impact_percent", y="feature",
        orientation="h", template="plotly_dark",
        color="price_impact_percent",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=600)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">Top Value Drivers</div>', unsafe_allow_html=True)
    top_pos = coef_df.nlargest(6, "price_impact_percent").reset_index()
    cols = st.columns(3)
    for i, row in top_pos.iterrows():
        with cols[i % 3]:
            st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight:700;">{row['feature']}</div>
                    <div class="positive" style="font-size:30px; font-weight:800;">+{row['price_impact_percent']:.2f}%</div>
                    <p style="font-size:14px; color:#94a3b8;">Increases value per unit.</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Value Reducers</div>', unsafe_allow_html=True)
    top_neg = coef_df.nsmallest(3, "price_impact_percent").reset_index()
    cols_neg = st.columns(3)
    for i, row in top_neg.iterrows():
        with cols_neg[i % 3]:
             st.markdown(f"""
                <div class="feature-card">
                    <div style="font-weight:700;">{row['feature']}</div>
                    <div class="negative" style="font-size:30px; font-weight:800;">{row['price_impact_percent']:.2f}%</div>
                    <p style="font-size:14px; color:#94a3b8;">Decreases value per unit.</p>
                </div>
            """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("<br><hr><center style='color:#64748b; font-size:12px;'>Built with ❤️ using Streamlit & Plotly</center>", unsafe_allow_html=True)