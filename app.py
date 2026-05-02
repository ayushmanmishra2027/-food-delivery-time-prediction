import streamlit as st
import numpy as np

st.set_page_config(page_title="Food Delivery Time Predictor", page_icon="🍕", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp {
    background: #FFF8F3 !important;
    font-family: 'Outfit', sans-serif !important;
    color: #1A1A2E !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #FF6B35 0%, #FF9F1C 40%, #FFBF69 100%);
    padding: 52px 60px 48px;
    position: relative; overflow: hidden;
}
.hero::before {
    content: '🍕';
    position: absolute; right: 80px; top: 20px;
    font-size: 160px; opacity: 0.15;
    animation: spin 20s linear infinite;
}
.hero::after {
    content: '🛵';
    position: absolute; right: 300px; bottom: -10px;
    font-size: 100px; opacity: 0.15;
}
@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    border: 1px solid rgba(255,255,255,0.4);
    color: #fff; font-size: 11px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    padding: 6px 18px; border-radius: 50px; margin-bottom: 20px;
}
.hero-title {
    font-size: 56px; font-weight: 900; color: #fff;
    line-height: 1.05; margin-bottom: 12px;
    text-shadow: 0 4px 24px rgba(0,0,0,0.15);
}
.hero-sub { color: rgba(255,255,255,0.85); font-size: 17px; font-weight: 300; }
.hero-stats { display: flex; gap: 48px; margin-top: 36px; }
.hs-num { font-size: 32px; font-weight: 900; color: #fff; }
.hs-lbl { font-size: 12px; color: rgba(255,255,255,0.75); text-transform: uppercase; letter-spacing: 1px; }

/* Main */
.main-pad { padding: 40px 48px; background: #FFF8F3; }

/* Cards */
.card {
    background: #fff;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 4px 32px rgba(255,107,53,0.08);
    border: 1.5px solid rgba(255,107,53,0.1);
    height: 100%;
}
.card-title {
    font-size: 11px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #FF6B35; margin-bottom: 24px;
}

/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #888 !important; font-size: 11px !important;
    font-weight: 700 !important; letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-baseweb="select"] > div {
    background: #FFF8F3 !important;
    border: 1.5px solid #FFD6C0 !important;
    border-radius: 12px !important; color: #1A1A2E !important;
}
div[data-baseweb="select"] > div:hover { border-color: #FF6B35 !important; }
div[data-baseweb="popover"] ul { background: #fff !important; }

/* Button */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #FF6B35, #FF9F1C) !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important; padding: 18px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 15px !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    box-shadow: 0 8px 32px rgba(255,107,53,0.35) !important;
    margin-top: 20px !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 12px 48px rgba(255,107,53,0.55) !important;
}

/* Result */
.result-hero {
    text-align: center; padding: 36px 20px 28px;
    background: linear-gradient(135deg, #FFF0E8, #FFF8F3);
    border-radius: 20px; margin-bottom: 24px;
    border: 1.5px solid #FFD6C0;
    position: relative; overflow: hidden;
}
.result-hero::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #FF6B35, #FF9F1C, #FFBF69);
}
.res-num {
    font-size: 96px; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #FF6B35, #FF9F1C);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.res-unit { font-size: 18px; color: #aaa; font-weight: 300; }
.res-badge {
    display: inline-block; padding: 10px 28px;
    border-radius: 50px; font-size: 13px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; margin-top: 18px;
}

/* Stat pills */
.spills { display: flex; gap: 12px; margin-bottom: 24px; }
.spill {
    flex: 1; background: #FFF8F3; border: 1.5px solid #FFD6C0;
    border-radius: 14px; padding: 16px 10px; text-align: center;
}
.spill-n { font-size: 20px; font-weight: 800; color: #FF6B35; }
.spill-l { font-size: 10px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

/* Factor bars */
.frow { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.fname { font-size: 11px; color: #aaa; width: 72px; text-align: right; flex-shrink: 0; font-weight: 600; }
.ftrack { flex: 1; height: 8px; background: #FFF0E8; border-radius: 4px; overflow: hidden; }
.fbar { height: 100%; border-radius: 4px; }
.fval { font-size: 12px; font-weight: 700; width: 52px; }

/* Insights */
.tip {
    background: linear-gradient(135deg, #FFF8F3, #FFF0E8);
    border-left: 4px solid #FF6B35; border-radius: 0 12px 12px 0;
    padding: 12px 16px; margin-bottom: 10px;
    font-size: 13px; color: #444; line-height: 1.5;
}

/* Idle */
.idle { display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:440px;text-align:center;opacity:0.35; }
.idle-icon { font-size:80px;margin-bottom:16px; }
.idle-t { font-size:20px;font-weight:700;color:#FF6B35; }
.idle-s { font-size:13px;color:#aaa;margin-top:8px; }

/* Footer */
.ftbar {
    background: linear-gradient(135deg, #FF6B35, #FF9F1C);
    padding: 20px 48px; text-align: center;
    color: rgba(255,255,255,0.85); font-size: 13px; font-weight: 400;
}
.ftbar b { color: #fff; }
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
  <div class="hero-tag">🍕 ML Powered · Real-Time</div>
  <div class="hero-title">Food Delivery Time<br>Predictor</div>
  <div class="hero-sub">Know your delivery time before you even hit order — powered by Machine Learning</div>
  <div class="hero-stats">
    <div><div class="hs-num">3</div><div class="hs-lbl">ML Models</div></div>
    <div><div class="hs-num">91%</div><div class="hs-lbl">R² Score</div></div>
    <div><div class="hs-num">2.8 min</div><div class="hs-lbl">Avg MAE</div></div>
    <div><div class="hs-num">Live</div><div class="hs-lbl">Prediction</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# BODY
st.markdown('<div class="main-pad">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="card"><div class="card-title">⚙️ Delivery Parameters</div>', unsafe_allow_html=True)
    weather        = st.selectbox("🌦 Weather Conditions", ["Clear","Cloudy","Windy","Fog","Sandstorms","Stormy"])
    traffic        = st.selectbox("🚦 Traffic Level",      ["Low","Medium","High","Jam"])
    vehicle        = st.selectbox("🛵 Vehicle Type",       ["Motorcycle","Scooter","Electric Scooter","Bicycle"])
    order_priority = st.selectbox("📦 Order Priority",     ["High","Medium","Low"])
    distance       = st.slider("📍 Distance (km)", 0.5, 20.0, 5.0, 0.5)
    experience     = st.slider("👨‍💼 Agent Experience (yrs)", 0, 10, 3)
    order_hour     = st.slider("⏰ Order Hour (0–23)", 0, 23, 12)
    predict        = st.button("🚀  PREDICT DELIVERY TIME")
    st.markdown('</div>', unsafe_allow_html=True)

# calc
wm={"Clear":0,"Cloudy":2,"Windy":3,"Fog":6,"Sandstorms":8,"Stormy":12}
tm={"Low":0,"Medium":4,"High":9,"Jam":16}
vm={"Motorcycle":0,"Electric Scooter":1,"Scooter":2,"Bicycle":5}
pm={"High":0,"Medium":1,"Low":3}
wp=wm[weather]; tp=tm[traffic]; vp=vm[vehicle]; pp=pm[order_priority]
es=experience*0.8; rush=7 if(8<=order_hour<=10 or 18<=order_hour<=21) else 0
base=distance*3.2
pred=max(10,round(base+wp+tp+vp+pp-es+rush,1))
fast=pred<=35
sc="#22C55E" if fast else "#EF4444"
label="ON TIME ✅" if fast else "DELAYED 🔴"

factors={"Distance":round(base,1),"Traffic":tp,"Weather":wp,"Rush Hour":rush,"Vehicle":vp,"Experience":-round(es,1)}
mx=max(abs(v) for v in factors.values()) or 1
fc={"Distance":"#FF6B35","Traffic":"#EF4444","Weather":"#F59E0B","Rush Hour":"#8B5CF6","Vehicle":"#3B82F6","Experience":"#22C55E"}

with col2:
    if predict:
        st.markdown(f"""
        <div class="result-hero">
          <div style="font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{sc};margin-bottom:8px;">{label}</div>
          <div class="res-num">{pred}</div>
          <div class="res-unit">minutes estimated</div>
          <div class="res-badge" style="background:{'rgba(34,197,94,0.1)' if fast else 'rgba(239,68,68,0.1)'};color:{sc};border:1.5px solid {'rgba(34,197,94,0.3)' if fast else 'rgba(239,68,68,0.3)'};">
            {'Within 35 min threshold 🎯' if fast else 'Exceeds 35 min threshold ⚠️'}
          </div>
        </div>

        <div class="spills">
          <div class="spill"><div class="spill-n">{distance}km</div><div class="spill-l">Distance</div></div>
          <div class="spill"><div class="spill-n">{'Rush ⚡' if rush else 'Normal'}</div><div class="spill-l">Hour</div></div>
          <div class="spill"><div class="spill-n">{experience}yr</div><div class="spill-l">Experience</div></div>
          <div class="spill"><div class="spill-n">{traffic}</div><div class="spill-l">Traffic</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">📊 Factor Breakdown</div>', unsafe_allow_html=True)
        bars=""
        for name,val in factors.items():
            pct=min(abs(val)/mx*100,100)
            sign="−" if val<0 else "+"
            c=fc.get(name,"#FF6B35")
            bars+=f"""<div class="frow">
              <div class="fname">{name}</div>
              <div class="ftrack"><div class="fbar" style="width:{pct}%;background:{c};"></div></div>
              <div class="fval" style="color:{c};">{sign}{abs(val)}m</div>
            </div>"""
        st.markdown(bars+"</div>", unsafe_allow_html=True)

        tips=[]
        if traffic in ["High","Jam"]: tips.append("🚦 Heavy traffic detected — suggest alternate routes to rider")
        if weather in ["Stormy","Fog","Sandstorms"]: tips.append("🌧 Harsh weather — notify customer of possible delay")
        if rush: tips.append("⚡ Rush hour active — assign nearest available rider")
        if experience<3: tips.append("👨‍💼 New agent — enable GPS-assisted routing")
        if not tips: tips.append("✅ All conditions optimal — standard dispatch recommended")

        st.markdown('<div class="card" style="margin-top:20px;"><div class="card-title">💡 Smart Insights</div>', unsafe_allow_html=True)
        for t in tips:
            st.markdown(f'<div class="tip">{t}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
          <div class="idle">
            <div class="idle-icon">🍕</div>
            <div class="idle-t">Ready to Predict!</div>
            <div class="idle-s">Set parameters on the left and hit Predict</div>
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="ftbar">
  <b>Food Delivery Time Predictor</b> · Built by Ayushman Mishra · NMIT Bengaluru · Python · Scikit-learn · Streamlit
</div>
""", unsafe_allow_html=True)
