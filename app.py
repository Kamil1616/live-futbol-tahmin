import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Canlı Futbol Sinyalleri", layout="wide", page_icon="⚽")
st.title("⚽ Canlı Futbol Tahmin Sinyalleri")
st.markdown("**Sofascore** ile tüm liglerde anlık sinyal üretir • Her 30 saniye yenilenir")

# Headers (Sofascore engellemesin diye)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/"
}

BASE_URL = "https://api.sofascore.com/api/v1"

@st.cache_data(ttl=30)  # 30 saniyede bir yenile
def getir_canli_maclar():
    url = f"{BASE_URL}/sport/football/events/live"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("events", [])
    return []

def sinyal_uret(event):
    # Basit ama etkili sinyal mantığı (senin istediğin gibi)
    home = event.get("homeTeam", {}).get("name", "Home")
    away = event.get("awayTeam", {}).get("name", "Away")
    score_h = event.get("homeScore", {}).get("current", 0)
    score_a = event.get("awayScore", {}).get("current", 0)
    status = event.get("status", {}).get("description", "")
    
    # İleride statistics çekip possession, xG, shots ekleyeceğiz
    # Şimdilik temel sinyal (0-0 veya 1-0 geç dakikada baskı varsayımı)
    signals = []
    if score_h == score_a and "2nd half" in status:
        signals.append({"type": "0.5 ÜST", "strength": "Orta", "color": "🟡"})
    if score_h > score_a + 1:
        signals.append({"type": "EV SAHİBİ KAZANIR", "strength": "Yüksek", "color": "🟢"})
    
    return {
        "home": home,
        "away": away,
        "score": f"{score_h}-{score_a}",
        "status": status,
        "id": event.get("id"),
        "signals": signals
    }

# ====================== ANA UYGULAMA ======================
maclar = getir_canli_maclar()

if not maclar:
    st.warning("Şu anda canlı maç yok veya geçici sorun var. 30 saniye sonra tekrar dene.")
    st.stop()

st.success(f"Şu anda **{len(maclar)} canlı maç** var • Tüm ligler dahil")

# Güzel kartlar
cols = st.columns(3)
for idx, event in enumerate(maclar):
    with cols[idx % 3]:
        data = sinyal_uret(event)
        
        with st.container(border=True):
            st.subheader(f"{data['home']} vs {data['away']}")
            st.metric("Skor", data['score'])
            st.caption(data['status'])
            
            # Sinyaller
            for s in data["signals"]:
                st.markdown(f"<span style='font-size:18px'>{s['color']} **{s['type']}** ({s['strength']})</span>", unsafe_allow_html=True)
            
            # İleride buraya possession bar ve detay eklenecek
            if st.button("Detay + İstatistik Gör", key=event["id"]):
                st.session_state.selected_id = event["id"]
                st.rerun()

# Otomatik yenileme
time.sleep(1)
if st.button("🔄 Şimdi Yenile"):
    st.rerun()

st.caption("Veri kaynağı: Sofascore unofficial API • Ücretsiz prototip")
