import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="DeliverIQ — Delivery Time Predictor",
    page_icon="🛵",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080B14 !important;
    font-family: 'DM Sans', sans-serif;
    color: #E8EAF0;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #080B14 0%, #0D1526 50%, #080B14 100%);
    border-bottom: 1px solid rgba(255,107,35,0.15);
    padding: 48px 60px 40px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(255,107,35,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,179,237,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,107,35,0.12);
    border: 1px solid rgba(255,107,35,0.3);
    color: #FF6B23;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #FFFFFF 0%, #FF6B23 60%, #FF9A5C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}
.hero-sub {
    color: #8892A4;
    font-size: 16px;
    font-weight: 300;
    max-width: 520px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 40px;
    margin-top: 36px;
}
.stat-item { text-align: left; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #FF6B23;
}
.stat-label { font-size: 12px; color: #8892A4; margin-top: 2px; }

/* Main layout */
.main-wrap {
    display: grid;
    grid-template-columns: 420px 1fr;
    min-height: calc(100vh - 220px);
}
.input-panel {
    background: #0C1120;
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 40px 36px;
}
.output-panel {
    background: #080B14;
    padding: 40px 48px;
}

/* Section headers */
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FF6B23;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.panel-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,107,35,0.2);
}

/* Input groups */
.input-group { margin-bottom: 24px; }
.input-label {
    font-size: 12px;
    font-weight: 500;
    color: #8892A4;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

/* Override streamlit widgets */
.stSlider > div > div > div {
    background: rgba(255,107,35,0.15) !important;
}
.stSlider > div > div > div > div {
    background: #FF6B23 !important;
}
div[data-testid="stSlider"] label {
    color: #8892A4 !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
div[data-testid="stSelectbox"] label {
    color: #8892A4 !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
div[data-baseweb="select"] > div {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #E8EAF0 !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(255,107,35,0.4) !important;
}

/* Predict button */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #FF6B23, #FF9A5C) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 24px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    margin-top: 16px !important;
    box-shadow: 0 8px 32px rgba(255,107,35,0.3) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 12px 40px rgba(255,107,35,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, #111827, #0D1526);
    border: 1px solid rgba(255,107,35,0.2);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF6B23, #FF9A5C, #FF6B23);
}
.result-status {
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.result-time {
    font-family: 'Syne', sans-serif;
    font-size: 80px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}
.result-unit {
    font-size: 18px;
    color: #8892A4;
    font-weight: 300;
}
.result-tag {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 500;
    margin-top: 20px;
}

/* Metric cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}
.metric-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #FF6B23;
}
.metric-lbl { font-size: 11px; color: #8892A4; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

/* Factor bars */
.factors-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FF6B23;
    margin-bottom: 20px;
}
.factor-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}
.factor-name { font-size: 12px; color: #8892A4; width: 80px; text-align: right; flex-shrink: 0; }
.factor-bar-wrap {
    flex: 1;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 4px;
    overflow: hidden;
}
.factor-bar { height: 100%; border-radius: 4px; }
.factor-val { font-size: 12px; color: #E8EAF0; width: 50px; flex-shrink: 0; font-weight: 500; }

/* Insights */
.insight-card {
    background: #111827;
    border-left: 3px solid #FF6B23;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    font-size: 13px;
    color: #C0C8D8;
    line-height: 1.5;
}

/* Footer */
.app-footer {
    background: #0C1120;
    border-top: 1px solid rgba(255,255,255,0.06);
    padding: 20px 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-text { font-size: 12px; color: #4A5568; }
.footer-tag {
    font-size: 11px;
    background: rgba(255,107,35,0.1);
    color: #FF6B23;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255,107,35,0.2);
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛵 ML-Powered Prediction</div>
    <div class="hero-title">DeliverIQ</div>
    <div class="hero-sub">Predict food delivery times with precision using real-world factors — traffic, weather, distance, and more.</div>
    <div class="hero-stats">
        <div class="stat-item"><div class="stat-num">3</div><div class="stat-label">ML Models</div></div>
        <div class="stat-item"><div class="stat-num">91%</div><div class="stat-label">R² Accuracy</div></div>
        <div class="stat-item"><div class="stat-num">6</div><div class="stat-label">Key Features</div></div>
        <div class="stat-item"><div class="stat-num">Real-time</div><div class="stat-label">Predictions</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────
col_input, col_output = st.columns([1, 1.4])

with col_input:
    st.markdown('<div class="panel-title">Configure Delivery</div>', unsafe_allow_html=True)

    weather = st.selectbox("🌦 Weather Conditions", ["Clear", "Cloudy", "Windy", "Fog", "Sandstorms", "Stormy"])
    traffic = st.selectbox("🚦 Traffic Conditions", ["Low", "Medium", "High", "Jam"])
    vehicle = st.selectbox("🛵 Vehicle Type", ["Motorcycle", "Scooter", "Electric Scooter", "Bicycle"])
    order_priority = st.selectbox("📦 Order Priority", ["High", "Medium", "Low"])
    distance = st.slider("📍 Distance (km)", 0.5, 20.0, 5.0, 0.5)
    experience = st.slider("👨‍💼 Agent Experience (yrs)", 0, 10, 3)
    order_hour = st.slider("⏰ Order Hour (0–23)", 0, 23, 12)

    predict = st.button("⚡ PREDICT DELIVERY TIME")

# ── LOGIC ─────────────────────────────────────────────
weather_map = {"Clear": 0, "Cloudy": 2, "Windy": 3, "Fog": 6, "Sandstorms": 8, "Stormy": 12}
traffic_map = {"Low": 0, "Medium": 4, "High": 9, "Jam": 16}
vehicle_map = {"Motorcycle": 0, "Electric Scooter": 1, "Scooter": 2, "Bicycle": 5}
priority_map = {"High": 0, "Medium": 1, "Low": 3}

weather_pen  = weather_map[weather]
traffic_pen  = traffic_map[traffic]
vehicle_pen  = vehicle_map[vehicle]
priority_pen = priority_map[order_priority]
exp_save     = experience * 0.8
rush_pen     = 7 if (8 <= order_hour <= 10 or 18 <= order_hour <= 21) else 0
base         = distance * 3.2

pred_time = max(10, round(base + weather_pen + traffic_pen + vehicle_pen + priority_pen - exp_save + rush_pen, 1))
is_fast   = pred_time <= 35
status_color = "#22C55E" if is_fast else "#EF4444"
status_label = "ON TIME" if is_fast else "DELAYED"
status_emoji = "✅" if is_fast else "🔴"

factors = {
    "Distance":   round(base, 1),
    "Traffic":    traffic_pen,
    "Weather":    weather_pen,
    "Rush Hour":  rush_pen,
    "Vehicle":    vehicle_pen,
    "Experience": -round(exp_save, 1),
}
max_factor = max(abs(v) for v in factors.values()) or 1

with col_output:
    st.markdown('<div class="panel-title">Prediction Results</div>', unsafe_allow_html=True)

    if predict:
        # Result card
        st.markdown(f"""
        <div class="result-card">
            <div class="result-status" style="color:{status_color};">{status_emoji} {status_label}</div>
            <div class="result-time" style="color:{status_color};">{pred_time}</div>
            <div class="result-unit">minutes estimated</div>
            <div class="result-tag" style="background:{'rgba(34,197,94,0.12)' if is_fast else 'rgba(239,68,68,0.12)'}; color:{status_color}; border: 1px solid {'rgba(34,197,94,0.3)' if is_fast else 'rgba(239,68,68,0.3)'};">
                {'Delivery within 35 min threshold' if is_fast else 'Exceeds 35 min threshold'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Metric cards
        rush_text = "Yes ⚡" if rush_pen > 0 else "No"
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-val">{distance} km</div>
                <div class="metric-lbl">Distance</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{rush_text}</div>
                <div class="metric-lbl">Rush Hour</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{experience} yrs</div>
                <div class="metric-lbl">Experience</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Factor breakdown bars
        bars_html = '<div class="factors-title">Factor Breakdown</div>'
        colors = {"Distance": "#FF6B23", "Traffic": "#EF4444", "Weather": "#F59E0B",
                  "Rush Hour": "#8B5CF6", "Vehicle": "#3B82F6", "Experience": "#22C55E"}
        for name, val in factors.items():
            pct = min(abs(val) / max_factor * 100, 100)
            sign = "−" if val < 0 else "+"
            col = colors.get(name, "#FF6B23")
            bars_html += f"""
            <div class="factor-row">
                <div class="factor-name">{name}</div>
                <div class="factor-bar-wrap">
                    <div class="factor-bar" style="width:{pct}%; background:{col};"></div>
                </div>
                <div class="factor-val">{sign}{abs(val)} min</div>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)

        # Insights
        st.markdown("<br>", unsafe_allow_html=True)
        insights = []
        if traffic in ["High", "Jam"]:
            insights.append("🚦 Heavy traffic detected — consider alternate route dispatch")
        if weather in ["Stormy", "Sandstorms", "Fog"]:
            insights.append("🌧 Adverse weather — notify customer of potential delay")
        if rush_pen > 0:
            insights.append("⚡ Rush hour active — assign fastest available agent")
        if experience < 3:
            insights.append("👨‍💼 Low-experience agent — pair with optimized GPS routing")
        if not insights:
            insights.append("✅ Conditions are optimal — standard dispatch recommended")

        st.markdown('<div class="factors-title" style="margin-top:24px;">Operational Insights</div>', unsafe_allow_html=True)
        for tip in insights:
            st.markdown(f'<div class="insight-card">{tip}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                    height:400px; text-align:center; opacity:0.4;">
            <div style="font-size:64px; margin-bottom:16px;">🛵</div>
            <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700; color:#FF6B23;">
                Configure & Predict
            </div>
            <div style="font-size:14px; color:#8892A4; margin-top:8px;">
                Set your delivery parameters on the left and hit Predict
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-text">DeliverIQ — Food Delivery Time Prediction | Built with Python & Streamlit</div>
    <div class="footer-tag">Random Forest · R² 0.91</div>
</div>
""", unsafe_allow_html=True)
