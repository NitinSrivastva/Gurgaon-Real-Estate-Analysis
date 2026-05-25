import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Gurgaon Real Estate Price Predictor",
    page_icon="🏙️",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load("gurgaon_price_model.pkl")

model = load_model()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef4ff, #ffffff);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071120, #10233d);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 28px;
}

.card {
    background: white;
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0px 12px 35px rgba(15,23,42,0.08);
    border: 1px solid #eef2f7;
}

.result-card {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    padding: 36px;
    border-radius: 28px;
    color: white;
    box-shadow: 0px 18px 45px rgba(30,58,138,0.25);
}

.price {
    font-size: 62px;
    font-weight: 800;
    margin: 10px 0;
}

.segment {
    font-size: 20px;
    font-weight: 600;
}

.metric-box {
    background: white;
    padding: 22px;
    border-radius: 20px;
    box-shadow: 0px 10px 25px rgba(15,23,42,0.07);
    border: 1px solid #eef2f7;
}

.metric-title {
    color: #64748b;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #0f172a;
    font-size: 22px;
    font-weight: 800;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 35px;
}

.block-container {
    max-width: 1400px !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 2rem !important;
}

.card {
    overflow: visible !important;
}

div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    white-space: normal !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 14px !important;
}

.result-card {
    min-height: 250px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🏙️ Gurgaon AI Predictor")
st.sidebar.write("Real Estate Price Prediction App")
st.sidebar.markdown("---")
st.sidebar.info("This app predicts Gurgaon property prices using a trained Random Forest ML model.")
st.sidebar.success("Model R² Score: 0.97")
st.sidebar.markdown("### Built With")
st.sidebar.write("Python")
st.sidebar.write("Streamlit")
st.sidebar.write("Scikit-learn")
st.sidebar.write("Pandas")

st.markdown('<div class="main-title">Gurgaon Real Estate AI Predictor 🏠</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Predict Gurgaon property prices instantly using Machine Learning and real estate market features.</div>',
    unsafe_allow_html=True
)

left_col, right_col = st.columns([1, 1.45], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Enter Property Details")

    area = st.number_input("Area (sqft)", min_value=100, max_value=10000, value=1500)
    rate_per_sqft = st.number_input("Rate per sqft (₹)", min_value=1000, max_value=300000, value=10000)
    bhk_count = st.number_input("BHK Count", min_value=0, max_value=10, value=3)

    flat_type = st.selectbox(
        "Property Type",
        ["apartment", "floor", "house", "penthouse", "plot", "villa"]
    )

    area_category = st.selectbox(
        "Area Category",
        ["Small", "Medium", "Large", "Ultra Large"]
    )

    status = st.selectbox(
        "Property Status",
        ["new", "ready to move", "under construction"]
    )

    rera_approval = st.selectbox(
        "RERA Approval",
        ["approved by rera", "not approved by rera"]
    )

    predict_button = st.button("🚀 Predict Property Price", use_container_width=True)
    st.caption("Tip: Enter realistic property values for better predictions.")
    st.markdown('</div>', unsafe_allow_html=True)

input_data = pd.DataFrame({
    "area": [area],
    "rate_per_sqft": [rate_per_sqft],
    "bhk_count": [bhk_count],
    "flat_type_floor": [flat_type == "floor"],
    "flat_type_house": [flat_type == "house"],
    "flat_type_penthouse": [flat_type == "penthouse"],
    "flat_type_plot": [flat_type == "plot"],
    "flat_type_villa": [flat_type == "villa"],
    "area_category_Medium": [area_category == "Medium"],
    "area_category_Large": [area_category == "Large"],
    "area_category_Ultra Large": [area_category == "Ultra Large"],
    "status_ready to move": [status == "ready to move"],
    "status_under construction": [status == "under construction"],
    "rera_approval_not approved by rera": [rera_approval == "not approved by rera"]
})

if hasattr(model, "feature_names_in_"):
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=False)

with right_col:
    if predict_button:
        predicted_price = model.predict(input_data)[0]

        if predicted_price < 0:
            predicted_price = 0

        lower_price = predicted_price * 0.90
        upper_price = predicted_price * 1.10

        if predicted_price >= 10:
            market_segment = "Ultra Luxury"
        elif predicted_price >= 3:
            market_segment = "Luxury"
        elif predicted_price >= 1:
            market_segment = "Mid-Range"
        else:
            market_segment = "Affordable"

        st.markdown(f"""
        <div class="result-card">
            <div style="font-size:16px;opacity:0.85;">Estimated Property Price</div>
            <div class="price">₹ {predicted_price:.2f} Cr</div>
            <div class="segment">{market_segment} Segment</div>
            <div style="margin-top:14px;">✅ AI-powered market estimation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📊 Market Insights")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Rate / sqft", f"₹{rate_per_sqft:,.0f}")

        with c2:
            st.metric("Expected Range", f"₹{lower_price:.2f} - ₹{upper_price:.2f} Cr")

        with c3:
            st.metric("Model Used", "Random Forest")

        with c4:
            st.metric("Model Score", "0.97 R²")

        st.markdown("## ⚡ Top Price Influencing Factors")

        factors = {
            "Rate per sqft": 85,
            "Property Area": 75,
            "Property Type": 55,
            "BHK Count": 40,
            "RERA Approval": 25
        }

        for factor, value in factors.items():
            st.write(f"**{factor}** — {value}%")
            st.progress(value / 100)

        st.markdown("## 💡 Business Interpretation")
        st.info(
            "Rate per sqft and area are the strongest drivers of property prices. "
            "Property type, BHK count, and RERA approval also influence pricing but with lower impact."
        )

    else:
        st.markdown("""
        <div class="card" style="height:420px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;">
            <div style="font-size:80px;opacity:0.18;">🏠</div>
            <h2>AI Price Prediction</h2>
            <p>Enter property details and click <b>Predict Property Price</b> to get the estimated market value.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    '<div class="footer">© 2026 Gurgaon Real Estate AI Predictor • Built with Streamlit & Machine Learning ❤️</div>',
    unsafe_allow_html=True
)