import streamlit as st
import pandas as pd
import numpy as np
import pickle
import math

st.set_page_config(page_title="Food Delivery Time Predictor", page_icon="🍕", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0f0f0f; }
    .stApp { background-color: #0f0f0f; color: #f0f0f0; }
    h1 { color: #FF6B35; font-family: 'Georgia', serif; }
    h3 { color: #FF6B35; }
    .result-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #FF6B35;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-top: 20px;
    }
    .stSelectbox label, .stSlider label, .stNumberInput label { color: #f0f0f0 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🍕 Food Delivery Time Predictor")
st.markdown("#### Predict if your delivery will be **Fast** or **Delayed** — and get the estimated minutes.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📍 Location")
    distance = st.slider("Distance (km)", 0.5, 20.0, 5.0, step=0.5)
    
    st.markdown("### 🌦️ Conditions")
    weather = st.selectbox("Weather", ["Clear", "Fog", "Stormy", "Sandstorms", "Windy", "Cloudy"])
    traffic = st.selectbox("Traffic", ["Low", "Medium", "High", "Jam"])

with col2:
    st.markdown("### 🛵 Delivery Info")
    vehicle = st.selectbox("Vehicle Type", ["Bicycle", "Scooter", "Motorcycle", "Electric Scooter"])
    experience = st.slider("Delivery Person Experience (yrs)", 0, 10, 3)
    
    st.markdown("### ⏰ Order Info")
    order_hour = st.slider("Order Hour (0-23)", 0, 23, 12)
    order_priority = st.selectbox("Order Priority", ["Low", "Medium", "High"])

st.markdown("---")

# Feature engineering
weather_map = {"Clear": 0, "Cloudy": 1, "Windy": 2, "Fog": 3, "Sandstorms": 4, "Stormy": 5}
traffic_map = {"Low": 0, "Medium": 1, "High": 2, "Jam": 3}
vehicle_map = {"Bicycle": 0, "Electric Scooter": 1, "Motorcycle": 2, "Scooter": 3}
priority_map = {"Low": 0, "Medium": 1, "High": 2}

is_rush_hour = 1 if (8 <= order_hour <= 10 or 18 <= order_hour <= 21) else 0

# Simple rule-based prediction (replace with your trained model via pickle)
base_time = distance * 3.2
weather_penalty = [0, 2, 3, 6, 8, 12][weather_map[weather]]
traffic_penalty = [0, 4, 9, 16][traffic_map[traffic]]
vehicle_bonus = [5, 2, 0, 1][vehicle_map[vehicle]]
experience_bonus = experience * 0.8
rush_penalty = 7 if is_rush_hour else 0
priority_bonus = [3, 1, 0][priority_map[order_priority]]

predicted_time = base_time + weather_penalty + traffic_penalty + vehicle_bonus - experience_bonus + rush_penalty + priority_bonus
predicted_time = max(10, round(predicted_time, 1))

threshold = 35
status = "Delayed 🔴" if predicted_time > threshold else "Fast ✅"
status_color = "#FF4444" if predicted_time > threshold else "#44FF88"

if st.button("🚀 Predict Delivery Time", use_container_width=True):
    st.markdown(f"""
        <div class="result-box">
            <h2 style="color:{status_color}; margin:0;">{status}</h2>
            <h1 style="color:#FF6B35; font-size:56px; margin:8px 0;">{predicted_time} min</h1>
            <p style="color:#aaa; margin:0;">Rush Hour: {"Yes ⚡" if is_rush_hour else "No"} &nbsp;|&nbsp; Distance: {distance} km</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Feature Impact")
    impacts = {
        "Distance": round(distance * 3.2, 1),
        "Weather": weather_penalty,
        "Traffic": traffic_penalty,
        "Vehicle": vehicle_bonus,
        "Experience": -round(experience_bonus, 1),
        "Rush Hour": rush_penalty,
    }
    impact_df = pd.DataFrame(list(impacts.items()), columns=["Factor", "Time Impact (min)"])
    st.bar_chart(impact_df.set_index("Factor"))

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Food Delivery Time Prediction Project")
