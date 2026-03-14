import streamlit as st
import requests

st.set_page_config(page_title="Canlı Futbol Sinyalleri ⚽", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin: 12px 0; box-shadow: 0 6px 16px rgba(0,0,0,0.4); }
    .signal { padding: 10px 16px; border-radius: 8px; font-weight: bold; margin: 8px 0; display: inline-block; }
    .signal-high { background: #238636; color: white; }
    .signal-med { background: #db6d28; color: white; }
    .signal-low { background: #c94e4e; color: white; }
    h1, h2 { color: #58a6ff !important; }
    .stButton > button { background: #238636; color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Canlı Futbol Tahmin Sinyalleri")
st.markdown("Tüm ligler • Canlı skor + oran hareketi + sinyal • Her 30 sn yenile")

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
            if data.get("success"):
                maclar = data.get("data", {}).get("match", [])
                # Sadece canlı olanları döndür
                return [m for m in maclar if m.get("status") == "IN PLAY"]
            else:
                st.error(f"API hatası: {data.get('error', 'Bilinmeyen hata')}")
                return []
        else:
            st.error(f"HTTP Hatası: {resp.status_code}")
            return []
    except Exception as e:
        st.error(f"Bağlantı sorunu: {str(e)}")
        return []

def sinyal_uret(match):
    home = match.get("home", {}).get("name", "Ev Sahibi")
    away = match.get("away", {}).get("name", "Deplasman")
    score = match.get("scores", {}).get("score", "? - ?")
    ht_score = match.get("scores", {}).get("ht_score", "")
    minute = match.get("time", "?")
    competition = match.get("competition", {}).get("name", "")
    country = match.get("country", {}).get("name", "")

    odds_live = match.get("odds", {}).get("live", {})
    odds_pre = match.get("odds", {}).get("pre", {})

    home_live = float(odds_live.get("1") or 0)
    draw_live = float(odds_live.get("X") or 0)
    away_live = float(odds_live.get("2") or 0)
    home_pre  = float(odds_pre.get("1") or 0)
    draw_pre  = float(odds_pre.get("X") or 0)
    away_pre  = float(odds_pre.get("2") or 0)

    odds_drop_home = round(home_pre - home_live, 2) if home_pre > 0 and home_live > 0 else 0
    odds_drop_away = round(away_pre - away_live, 2) if away_pre > 0 and away_live > 0 else 0

    try:
        min_int = int(minute) if str(minute).replace('.', '', 1).isdigit() else 0
    except:
        min_int = 0

    signals = []
    sig_class = "signal-low"
    strength = "Düşük"

    # 70+ dakika 0-0 → gol beklentisi
    if min_int >= 70 and score in ["0 - 0", "0-0"]:
        signals.append("⚡ 0.5 Üst — 70+ dak. golsüz")
        strength = "Yüksek"
        sig_class = "signal-high"

    # Ev sahibi oran düşüşü
    if odds_drop_home >= 0.15:
        signals.append(f"📉 Ev sahibi oranı sert düştü ({home_pre} → {home_live})")
        strength = "Yüksek"
        sig_class = "signal-high"
    elif odds_drop_home >= 0.05:
        signals.append(f"📉 Ev sahibi oranında düşüş ({home_pre} → {home_live})")
        if sig_class != "signal-high":
            strength = "Orta"
            sig_class = "signal-med"

    # Deplasman oran düşüşü
    if odds_drop_away >= 0.15:
        signals.append(f"📉 Deplasman oranı sert düştü ({away_pre} → {away_live})")
        if sig_class != "signal-high":
            strength = "Yüksek"
            sig_class = "signal-high"
    elif odds_drop_away >= 0.05:
        signals.append(f"📉 Deplasman oranında düşüş ({away_pre} → {away_live})")
        if sig_class == "signal-low":
            strength = "Orta"
            sig_class = "signal-med"

    # Geride kalan takım baskısı
    try:
        home_goals, away_goals = map(int, score.replace(" ", "").split("-"))
        if home_goals < away_goals and min_int >= 60 and odds_drop_home >= 0.05:
            signals.append("🔄 Ev sahibi geride + oran düşüyor — baskı artıyor")
            if sig_class == "signal-low":
                sig_class = "signal-med"
                strength = "Orta"
        elif away_goals < home_goals and min_int >= 60 and odds_drop_away >= 0.05:
            signals.append("🔄 Deplasman geride + oran düşüyor — baskı artıyor")
            if sig_class == "signal-low":
                sig_class = "signal-med"
                strength = "Orta"
    except:
        pass

    if not signals:
        signals.append("Henüz güçlü sinyal yok")

    return {
        "home": home,
        "away": away,
        "score": score,
        "ht_score": ht_score,
        "minute": minute,
        "competition": competition,
        "country": country,
        "signals": signals,
        "sig_class": sig_class,
        "strength": strength,
        "odds_pre": {"home": home_pre, "draw": draw_pre, "away": away_pre},
        "odds_live": {"home": home_live, "draw": draw_live, "away": away_live},
    }

maclar = getir_canli_maclar()

if not maclar:
    st.warning("Şu an aktif canlı maç yok.")
    st.info("Büyük liglerin maç saatlerinde (akşam 18:00–23:00) tekrar dene.")
else:
    st.success(f"🔴 **{len(maclar)} canlı maç** tespit edildi")

    cols = st.columns(3)
    for idx, match in enumerate(maclar):
        with cols[idx % 3]:
            data = sinyal_uret(match)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"🔴 **CANLI** • {data['competition']} ({data['country']})")
            st.subheader(f"{data['home']} vs {data['away']}")
            st.metric("Skor / Dakika", f"{data['score']} • {data['minute']}'")
            if data["ht_score"]:
                st.caption(f"İY: {data['ht_score']}")

            op = data["odds_pre"]
            ol = data["odds_live"]
            if any([op["home"], op["draw"], op["away"]]):
                st.caption(f"Maç öncesi: 1={op['home']} X={op['draw']} 2={op['away']}")
            if any([ol["home"], ol["draw"], ol["away"]]):
                st.caption(f"Canlı oran:  1={ol['home']} X={ol['draw']} 2={ol['away']}")

            for sig in data["signals"]:
                st.markdown(f'<div class="signal {data["sig_class"]}">{sig} ({data["strength"]})</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Şimdi Yenile"):
    st.cache_data.clear()
    st.rerun()

st.caption("Veri: live-score-api.com • Her 30 sn otomatik güncellenir")
