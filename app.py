import streamlit as st
import requests
import time

st.set_page_config(page_title="Canlı Futbol Sinyalleri ⚽", layout="wide", page_icon="⚽")

# Karanlık tema + modern CSS (analiz.onrender benzeri)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin: 12px 0; box-shadow: 0 6px 16px rgba(0,0,0,0.4); }
    .signal { padding: 10px 16px; border-radius: 8px; font-weight: bold; margin: 8px 0; display: inline-block; }
    .signal-high { background: #238636; color: white; }
    .signal-med { background: #db6d28; color: white; }
    .signal-low { background: #c94e4e; color: white; }
    .progress { height: 24px; background: #21262d; border-radius: 12px; overflow: hidden; margin: 10px 0; }
    .progress-fill { height: 100%; background: linear-gradient(90deg, #238636, #2ea043); transition: width 0.6s ease; }
    h1, h2 { color: #58a6ff !important; }
    .stButton > button { background: #238636; color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Canlı Futbol Tahmin Sinyalleri")
st.markdown("**live-score-api.com** trial • Tüm ligler • Canlı skor + oran hareketi + sinyal • Her 30 sn yenile")

API_KEY = "lD0xMVlUGwip7fzY"
API_SECRET = "C7b6mK3wocmicEDxhD44zqYfWhF3we19"

BASE_URL = "https://livescore-api.com/api-client"

@st.cache_data(ttl=30)
def getir_canli_maclar():
    url = f"{BASE_URL}/matches/live.json?key={API_KEY}&secret={API_SECRET}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success") == 1:
                return data.get("data", {}).get("match", [])
            else:
                st.error(f"API cevabı başarısız: {data.get('error', 'Bilinmeyen hata')}")
                return []
        else:
            st.error(f"HTTP Hatası: {resp.status_code} - {resp.text[:200]}...")
            return []
    except Exception as e:
        st.error(f"Bağlantı sorunu: {str(e)}")
        return []

def sinyal_uret(match):
    home = match.get("home", {}).get("name", "Ev Sahibi")
    away = match.get("away", {}).get("name", "Deplasman")
    score = match.get("scores", {}).get("score", "? - ?")
    minute = match.get("time", "?")
    status = match.get("status", "Bilinmiyor")
    
    odds_live = match.get("odds", {}).get("live", {})
    odds_pre = match.get("odds", {}).get("pre", {})
    home_odds_live = float(odds_live.get("1", 0)) if odds_live.get("1") else 0
    home_odds_pre = float(odds_pre.get("1", 0)) if odds_pre.get("1") else 0
    odds_drop = home_odds_pre - home_odds_live if home_odds_pre > 0 and home_odds_live > 0 else 0
    
    signals = []
    sig_class = "signal-low"
    strength = "Düşük"
    
    try:
        min_int = int(minute) if minute.replace('.', '', 1).isdigit() else 0
    except:
        min_int = 0
    
    if "IN PLAY" in status or status == "HALF TIME" or min_int > 0:
        if min_int > 70 and score == "0 - 0":
            signals.append("0.5 Üst / Gol Beklentisi Yüksek")
            strength = "Orta-Yüksek"
            sig_class = "signal-med"
        if odds_drop > 0.05:
            signals.append("Ev Sahibi Kazanır / Oran Düşüş Sinyali")
            strength = "Yüksek"
            sig_class = "signal-high"
    
    if not signals:
        signals.append("Henüz güçlü sinyal yok")
    
    return {
        "home": home,
        "away": away,
        "score": score,
        "minute": minute,
        "status": status,
        "signals": signals,
        "sig_class": sig_class,
        "strength": strength,
        "odds_drop": odds_drop
    }

maclar = getir_canli_maclar()

if not maclar:
    st.warning("Şu anda canlı maç görünmüyor veya API erişim sorunu var (trial aktif mi? Gece/az maç saatinde olabilir). 30 sn sonra yenile.")
    st.info("Süper Lig, Premier League gibi büyük liglerin maç saatlerinde dene.")
else:
    st.success(f"**{len(maclar)} canlı maç** tespit edildi • Trial dönemi • Oran düşüşü + dakika bazlı sinyal")
    
    cols = st.columns(3)
    for idx, match in enumerate(maclar):
        with cols[idx % 3]:
            data = sinyal_uret(match)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"{data['home']} vs {data['away']}")
            st.metric("Skor / Dakika", f"{data['score']} • {data['minute']}'")
            st.caption(data['status'])
            
            # Sinyaller
            for sig in data["signals"]:
                st.markdown(f'<div class="signal {data["sig_class"]}">⚡ {sig} ({data["strength"]})</div>', unsafe_allow_html=True)
            
            # Placeholder progress bar (possession için ileride gerçek veri)
            st.markdown('<div class="progress"><div class="progress-fill" style="width: 60%;"></div></div>', unsafe_allow_html=True)
            st.caption("Tahmini Üstünlük / İstatistik yakında gerçek olacak")
            
            st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Şimdi Yenile"):
    st.rerun()

st.caption("Veri kaynağı: live-score-api.com • 14 gün trial • Key/Secret güncellendi")
