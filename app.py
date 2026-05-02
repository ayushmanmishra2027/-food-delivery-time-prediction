import streamlit as st
import numpy as np

st.set_page_config(page_title="FoodRush AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: #03010A !important; font-family: 'Outfit', sans-serif; color: #fff; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Animated gradient BG blobs */
.bg-blobs {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.blob {
    position: absolute; border-radius: 50%;
    filter: blur(80px); opacity: 0.35;
    animation: float 8s ease-in-out infinite;
}
.blob1 { width:500px;height:500px; background:#FF2D78; top:-100px; left:-100px; animation-delay:0s; }
.blob2 { width:400px;height:400px; background:#7B2FFF; top:30%; right:-100px; animation-delay:-3s; }
.blob3 { width:350px;height:350px; background:#00E5FF; bottom:-80px; left:35%; animation-delay:-5s; }
@keyframes float {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(30px,-30px) scale(1.08); }
}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-radius: 24px;
}

/* Layout */
.wrap { position: relative; z-index: 1; padding: 40px 48px; }

/* Hero */
.hero-wrap { text-align: center; margin-bottom: 48px; padding: 60px 20px 20px; }
.hero-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(255,45,120,0.2), rgba(123,47,255,0.2));
    border: 1px solid rgba(255,45,120,0.4);
    color: #FF6EB0; font-size: 12px; font-weight: 600;
    letter-spacing: 3px; text-transform: uppercase;
    padding: 8px 20px; border-radius: 50px; margin-bottom: 24px;
}
.hero-title {
    font-size: 72px; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #fff 0%, #FF2D78 40%, #7B2FFF 80%, #00E5FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 16px;
    text-shadow: none;
}
.hero-sub { color: rgba(255,255,255,0.45); font-size: 17px; font-weight: 300; }

/* Grid */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }

/* Card */
.card { padding: 32px; margin-bottom: 0; }
.card-title {
    font-size: 11px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; margin-bottom: 28px;
    background: linear-gradient(90deg, #FF2D78, #7B2FFF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Streamlit overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important; color: #fff !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(255,45,120,0.5) !important;
}
div[data-baseweb="popover"] { background: #1A0A2E !important; }

/* Slider track */
div[data-testid="stSlider"] div[role="slider"] {
    background: linear-gradient(135deg, #FF2D78, #7B2FFF) !important;
    box-shadow: 0 0 12px rgba(255,45,120,0.6) !important;
}

/* Button */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #FF2D78 0%, #7B2FFF 100%) !important;
    color: white !important; border: none !important;
    border-radius: 16px !important; padding: 18px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 16px !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    box-shadow: 0 8px 40px rgba(255,45,120,0.4) !important;
    margin-top: 20px !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 12px 60px rgba(255,45,120,0.7) !important;
    transform: translateY(-2px) !important;
}

/* Result big number */
.result-wrap {
    text-align: center; padding: 40px 20px;
    position: relative;
}
.result-glow {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 280px; height: 280px;
    border-radius: 50%; filter: blur(60px);
    opacity: 0.25; pointer-events: none;
}
.result-num {
    font-size: 110px; font-weight: 900; line-height: 1;
    position: relative; z-index: 1;
}
.result-unit { font-size: 20px; color: rgba(255,255,255,0.4); font-weight: 300; margin-top: -8px; }
.result-badge {
    display: inline-block; padding: 10px 28px;
    border-radius: 50px; font-size: 13px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; margin-top: 20px;
}

/* Stat pills */
.stats-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; }
.stat-pill {
    flex: 1; min-width: 100px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 16px 12px; text-align: center;
}
.stat-pill-num { font-size: 20px; font-weight: 700; }
.stat-pill-lbl { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

/* Factor bars */
.factor-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.factor-name { font-size: 11px; color: rgba(255,255,255,0.4); width: 75px; text-align: right; flex-shrink: 0; }
.bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 3px; }
.factor-val { font-size: 12px; font-weight: 600; width: 52px; flex-shrink: 0; }

/* Insight chips */
.insight { 
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #FF2D78;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px; margin-bottom: 10px;
    font-size: 13px; color: rgba(255,255,255,0.7); line-height: 1.5;
}

/* idle state */
.idle {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; min-height: 380px; text-align: center; opacity: 0.3;
}
.idle-icon { font-size: 72px; margin-bottom: 16px; }
.idle-txt { font-size: 18px; font-weight: 700; }
.idle-sub { font-size: 13px; margin-top: 8px; font-weight: 300; }

/* footer */
.footer {
    text-align: center; padding: 32px;
    font-size: 12px; color: rgba(255,255,255,0.2);
    position: relative; z-index: 1;
}
.footer span { color: #FF2D78; }
</style>

<div class="bg-blobs">
  <div class="blob blob1"></div>
  <div class="blob blob2"></div>
  <div class="blob blob3"></div>
</div>
""", unsafe_allow_html=True)

# ── HERO
st.markdown("""
<div class="hero-wrap">
    <div class="hero-pill">⚡ AI-Powered · Real-Time</div>
    <div class="hero-title">FoodRush AI</div>
    <div class="hero-sub">Predict delivery time before the order even leaves the kitchen</div>
</div>
""", unsafe_allow_html=True)

# ── INPUTS + OUTPUT
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass card"><div class="card-title">⚙ Delivery Parameters</div>', unsafe_allow_html=True)
    weather       = st.selectbox("🌦 Weather", ["Clear", "Cloudy", "Windy", "Fog", "Sandstorms", "Stormy"])
    traffic       = st.selectbox("🚦 Traffic Level", ["Low", "Medium", "High", "Jam"])
    vehicle       = st.selectbox("🛵 Vehicle", ["Motorcycle", "Scooter", "Electric Scooter", "Bicycle"])
    order_priority= st.selectbox("📦 Priority", ["High", "Medium", "Low"])
    distance      = st.slider("📍 Distance (km)", 0.5, 20.0, 5.0, 0.5)
    experience    = st.slider("👨‍💼 Agent Experience (yrs)", 0, 10, 3)
    order_hour    = st.slider("⏰ Order Hour", 0, 23, 12)
    predict       = st.button("⚡  PREDICT NOW")
    st.markdown('</div>', unsafe_allow_html=True)

# ── CALC
weather_map   = {"Clear":0,"Cloudy":2,"Windy":3,"Fog":6,"Sandstorms":8,"Stormy":12}
traffic_map   = {"Low":0,"Medium":4,"High":9,"Jam":16}
vehicle_map   = {"Motorcycle":0,"Electric Scooter":1,"Scooter":2,"Bicycle":5}
priority_map  = {"High":0,"Medium":1,"Low":3}

w_pen = weather_map[weather]; t_pen = traffic_map[traffic]
v_pen = vehicle_map[vehicle]; p_pen = priority_map[order_priority]
exp_s = experience * 0.8
rush  = 7 if (8<=order_hour<=10 or 18<=order_hour<=21) else 0
base  = distance * 3.2
pred  = max(10, round(base + w_pen + t_pen + v_pen + p_pen - exp_s + rush, 1))
fast  = pred <= 35
sc    = "#00E5A0" if fast else "#FF2D78"
label = "ON TIME" if fast else "DELAYED"

factors = {"Distance":round(base,1),"Traffic":t_pen,"Weather":w_pen,"Rush":rush,"Vehicle":v_pen,"Exp":-round(exp_s,1)}
mx = max(abs(v) for v in factors.values()) or 1
fcolors = {"Distance":"#00E5FF","Traffic":"#FF2D78","Weather":"#FFB800","Rush":"#7B2FFF","Vehicle":"#FF6B35","Exp":"#00E5A0"}

with col2:
    if predict:
        # result
        st.markdown(f"""
        <div class="glass card">
          <div class="result-wrap">
            <div class="result-glow" style="background:{sc};"></div>
            <div class="result-num" style="background:linear-gradient(135deg,#fff,{sc});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{pred}</div>
            <div class="result-unit">minutes</div>
            <div class="result-badge" style="background:{'rgba(0,229,160,0.12)' if fast else 'rgba(255,45,120,0.12)'};color:{sc};border:1px solid {'rgba(0,229,160,0.3)' if fast else 'rgba(255,45,120,0.3)'};">
              {'✅ ' if fast else '🔴 '}{label}
            </div>
          </div>

          <div class="stats-row">
            <div class="stat-pill"><div class="stat-pill-num" style="color:#00E5FF;">{distance}km</div><div class="stat-pill-lbl">Distance</div></div>
            <div class="stat-pill"><div class="stat-pill-num" style="color:#FFB800;">{'Rush ⚡' if rush else 'Normal'}</div><div class="stat-pill-lbl">Hour Type</div></div>
            <div class="stat-pill"><div class="stat-pill-num" style="color:#7B2FFF;">{experience}yr</div><div class="stat-pill-lbl">Experience</div></div>
          </div>

          <div class="card-title">Factor Impact</div>
        """, unsafe_allow_html=True)

        bars = ""
        for name, val in factors.items():
            pct = min(abs(val)/mx*100, 100)
            sign = "−" if val < 0 else "+"
            col_c = fcolors.get(name, "#fff")
            bars += f"""
            <div class="factor-row">
              <div class="factor-name">{name}</div>
              <div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{col_c};box-shadow:0 0 8px {col_c}88;"></div></div>
              <div class="factor-val" style="color:{col_c};">{sign}{abs(val)}m</div>
            </div>"""
        st.markdown(bars + "</div>", unsafe_allow_html=True)

        # insights
        tips = []
        if traffic in ["High","Jam"]: tips.append("🚦 Heavy traffic — reroute via alternate streets")
        if weather in ["Stormy","Fog","Sandstorms"]: tips.append("🌧 Bad weather — proactively notify customer")
        if rush: tips.append("⚡ Rush hour — assign fastest available rider")
        if experience < 3: tips.append("👨‍💼 New agent — enable GPS assist mode")
        if not tips: tips.append("✅ All clear — optimal dispatch conditions")

        st.markdown('<div class="glass card"><div class="card-title">💡 Operational Insights</div>', unsafe_allow_html=True)
        for t in tips:
            st.markdown(f'<div class="insight">{t}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass card" style="height:100%;min-height:500px;">
          <div class="idle">
            <div class="idle-icon">⚡</div>
            <div class="idle-txt">Ready to Predict</div>
            <div class="idle-sub">Configure parameters & hit Predict Now</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Built by <span>Ayushman Mishra</span> · Food Delivery Time Prediction · Python · Scikit-learn · Streamlit
</div>
""", unsafe_allow_html=True)
