import streamlit as st
import requests
import time
import json
from datetime import datetime

st.set_page_config(page_title="Canlı Futbol Sinyalleri ⚽", layout="wide", page_icon="⚽", initial_sidebar_state="expanded")

# Karanlık tema + custom CSS (analiz.onrender tarzı)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    .card { background: #1e1e2e; border-radius: 12px; padding: 16px; margin: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
    .signal-green { background: #0f6; color: black; font-weight: bold; padding: 8px 12px; border-radius: 8px; display: inline-block; }
    .signal-yellow { background: #ffcc00; color: black; font-weight: bold; padding: 8px 12px; border-radius: 8px; display: inline-block; }
    .signal-red { background: #ff4444; color: white; font-weight: bold; padding: 8px 12px; border-radius: 8px; display: inline-block; }
    .progress { height: 20px; background: #333; border-radius: 10px; overflow: hidden; margin: 8px 0; }
    .progress-bar { height: 100%; background: linear-gradient(90deg, #0f6, #00cc66); transition: width 0.5s; }
    h1, h2, h3 { color: #00ff99 !important; }
    .stButton > button { background: #00cc66; color: black; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Canlı Futbol Tahmin Sinyalleri")
st.markdown("**Tüm ligler** • Sofascore canlı verileri • Her 30 sn yenilenir • Gerçek istatistik + sinyal")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/"
}

BASE_URL = "https://api.sofascore.com/api/v1"

@st.cache_data(ttl=30)
def getir_canli_maclar():
    url = f"{BASE_URL}/sport/football/events/live"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("events", [])
    except:
        pass
    return []

def getir_mac_istatistik(event_id):
    url = f"{BASE_URL}/event/{event_id}/statistics"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def sinyal_uret(event, stats=None):
    home = event.get("homeTeam", {}).get("name", "Ev")
    away = event.get("awayTeam", {}).get("name", "Dep")
    score_h = event.get("homeScore", {}).get("current", "?")
    score_a = event.get("awayScore", {}).get("current", "?")
    period = event.get("currentPeriod", "Unknown")
    minute = event.get("currentPeriodStartTimestamp", 0)  # Yaklaşık dakika için

    signals = []
    strength = "Düşük"
    color_class = "signal-red"

    if stats:
        # Possession, shots vs. çek (Sofascore stats yapısı: periods içinde)
        possession_home = 50  # Varsayılan
        shots_home = 0
        xg_home = 0.0
        for period_stats in stats.get("statistics", []):
            if period_stats.get("period") == "ALL":
                for group in period_stats.get("groups", []):
                    if group["groupName"] == "Possession":
                        possession_home = group["statisticsItems"][0]["homeValue"] or 50
                    if group["groupName"] == "Shots":
                        shots_home = group["statisticsItems"][0]["homeValue"] or 0
                    if group["groupName"] == "Expected goals (xG)":
                        xg_home = float(group["statisticsItems"][0]["homeValue"] or 0.0)

        if possession_home > 62 and shots_home > 5 and xg_home > 0.7 and minute > 60:
            signals.append("Ev Sahibi Baskın / Kazanma Sinyali")
            strength = "Yüksek"
            color_class = "signal-green"
        if (xg_home + (stats.get("xg_away", 0) or 0)) > 1.2 and score_h == score_a and minute > 70:
            signals.append("0.5 Üst / Gol Beklentisi")
            strength = "Orta-Yüksek"
            color_class = "signal-yellow"

    if not signals:
        signals.append("Henüz güçlü sinyal yok")

    return {
        "home": home,
        "away": away,
        "score": f"{score_h} - {score_a}",
        "minute": f"{minute // 60}'" if minute else "Canlı",
        "signals": signals,
        "strength": strength,
        "color_class": color_class,
        "possession_home": possession_home if stats else None
    }

maclar = getir_canli_maclar()

if not maclar:
    st.error("Canlı maç yok veya Sofascore erişim sorunu. Birkaç dakika sonra dene.")
else:
    st.success(f"Şu an **{len(maclar)} canlı maç** • Tüm ligler kapsanıyor")
    
    cols = st.columns(3)
    for i, event in enumerate(maclar[:12]):  # İlk 12 maç göster (daha fazla olursa sayfala)
        with cols[i % 3]:
            stats = getir_mac_istatistik(event.get("id"))
            data = sinyal_uret(event, stats)
            
            with st.container():
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.subheader(f"{data['home']} vs {data['away']}")
                st.metric("Skor / Dakika", f"{data['score']} • {data['minute']}")
                
                # Possession bar (eğer veri varsa)
                if data['possession_home']:
                    poss = data['possession_home']
                    st.markdown(f"Ev Sahibi Topa Sahip Olma: **{poss}%**")
                    st.markdown(f'<div class="progress"><div class="progress-bar" style="width: {poss}%;"></div></div>', unsafe_allow_html=True)
                
                # Sinyaller (yıldırım + renkli badge)
                for sig in data["signals"]:
                    st.markdown(f'<span class="{data["color_class"]}">⚡ {sig} ({data["strength"]})</span>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# Yenile butonu + auto-refresh simülasyonu
if st.button("🔄 Şimdi Yenile"):
    st.rerun()

time.sleep(0.5)  # Küçük delay
st.caption("Veri: Sofascore unofficial • Prototip • İyileştirmeler devam ediyor")
