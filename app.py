import streamlit as st
import requests

st.set_page_config(page_title="Canlı Futbol Sinyalleri ⚽", layout="wide", page_icon="⚽")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin: 12px 0; }
    .card-signal { border: 1px solid #238636 !important; box-shadow: 0 0 16px rgba(35,134,54,0.5); }
    .card-med    { border: 1px solid #db6d28 !important; box-shadow: 0 0 12px rgba(219,109,40,0.4); }
    .signal { padding: 10px 16px; border-radius: 8px; font-weight: bold; margin: 5px 0; display: block; font-size: 14px; }
    .signal-high { background: #238636; color: white; }
    .signal-med  { background: #db6d28; color: white; }
    .signal-low  { background: #2d333b; color: #8b949e; }
    .stat-row { display: flex; gap: 6px; margin: 8px 0; flex-wrap: wrap; }
    .stat-box { background: #21262d; border-radius: 6px; padding: 5px 10px; font-size: 12px; text-align: center; flex: 1; min-width: 60px; }
    .stat-home { color: #3fb950; font-weight: bold; }
    .stat-away { color: #f85149; font-weight: bold; }
    .odds-row { display: flex; gap: 6px; margin: 6px 0; }
    .odds-box { background: #21262d; border-radius: 6px; padding: 5px 10px; text-align: center; flex: 1; font-size: 12px; }
    .odds-down { background: #1a3a1a; color: #3fb950; font-weight: bold; }
    .odds-up   { background: #3a1a1a; color: #f85149; }
    h1 { color: #58a6ff !important; }
    .stButton > button { background: #238636; color: white; border: none; border-radius: 8px; padding: 8px 20px; }
    .badge { background: #21262d; border-radius: 4px; padding: 2px 8px; font-size: 12px; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Canlı Futbol Tahmin Sinyalleri")

API_KEY    = "lD0xMVlUGwip7fzY"
API_SECRET = "C7b6mK3wocmicEDxhD44zqYfWhF3we19"
BASE_URL   = "https://livescore-api.com/api-client"

@st.cache_data(ttl=30)
def getir_canli_maclar():
    url = f"{BASE_URL}/matches/live.json?key={API_KEY}&secret={API_SECRET}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                maclar = data.get("data", {}).get("match", [])
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

@st.cache_data(ttl=30)
def getir_stats(match_id):
    url = f"{BASE_URL}/matches/stats.json?match_id={match_id}&key={API_KEY}&secret={API_SECRET}"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                return data.get("data") or {}
        return {}
    except:
        return {}

def parse_stat(val):
    try:
        h, a = str(val).split(":")
        return int(h), int(a)
    except:
        return 0, 0

def parse_minute(minute):
    try:
        return int(str(minute).replace('+','').split('+')[0])
    except:
        return 0

def hesapla_baski(stats, taraf="home"):
    if not stats:
        return 0
    skor = 0
    ph, pa = parse_stat(stats.get("possesion"))
    if ph + pa > 0:
        pos = ph if taraf == "home" else pa
        skor += (pos / 100) * 30

    sh, sa = parse_stat(stats.get("shots_on_target"))
    toplam_sot = sh + sa
    if toplam_sot > 0:
        sot = sh if taraf == "home" else sa
        skor += (sot / toplam_sot) * 25

    ah, aa = parse_stat(stats.get("attempts_on_goal"))
    toplam_atk = ah + aa
    if toplam_atk > 0:
        atk = ah if taraf == "home" else aa
        skor += (atk / toplam_atk) * 25

    ch, ca = parse_stat(stats.get("corners"))
    toplam_cor = ch + ca
    if toplam_cor > 0:
        cor = ch if taraf == "home" else ca
        skor += (cor / toplam_cor) * 20

    return round(skor)

def sinyal_uret(match):
    match_id    = match.get("id")
    home        = (match.get("home") or {}).get("name", "Ev Sahibi")
    away        = (match.get("away") or {}).get("name", "Deplasman")
    score       = (match.get("scores") or {}).get("score", "? - ?")
    ht_score    = (match.get("scores") or {}).get("ht_score", "")
    minute      = match.get("time", "?")
    competition = (match.get("competition") or {}).get("name", "")
    country     = (match.get("country") or {}).get("name", "")

    odds_live = (match.get("odds") or {}).get("live") or {}
    odds_pre  = (match.get("odds") or {}).get("pre")  or {}

    home_live = float(odds_live.get("1") or 0)
    draw_live = float(odds_live.get("X") or 0)
    away_live = float(odds_live.get("2") or 0)
    home_pre  = float(odds_pre.get("1")  or 0)
    draw_pre  = float(odds_pre.get("X")  or 0)
    away_pre  = float(odds_pre.get("2")  or 0)

    def pct_change(pre, live):
        if pre > 0 and live > 0:
            return round((live - pre) / pre * 100, 1)
        return None

    home_chg = pct_change(home_pre, home_live)
    draw_chg = pct_change(draw_pre, draw_live)
    away_chg = pct_change(away_pre, away_live)

    min_int = parse_minute(minute)

    stats      = getir_stats(match_id) if match_id else {}
    home_baski = hesapla_baski(stats, "home")
    away_baski = hesapla_baski(stats, "away")

    try:
        h_gol, a_gol = map(int, score.replace(" ", "").split("-"))
        toplam_gol   = h_gol + a_gol
    except:
        h_gol, a_gol, toplam_gol = 0, 0, 0

    signals  = []
    priority = 0

    # KURAL 1: Baskı + oran hareketi kombinasyonu
    if min_int >= 60 and home_baski >= 60:
        if home_chg is not None and home_chg <= -7:
            signals.append((f"🔥 Ev sahibi baskısı ({home_baski}/100) + oran düşüyor → GÜÇLÜ SİNYAL", "signal-high"))
            priority = max(priority, 3)
        elif home_chg is not None and home_chg <= -3:
            signals.append((f"⚡ Ev sahibi baskısı ({home_baski}/100) + oran hafif düşüyor", "signal-med"))
            priority = max(priority, 2)
        elif toplam_gol == 0 and min_int >= 70:
            signals.append((f"⚡ Ev sahibi baskısı ({home_baski}/100) + golsüz maç", "signal-med"))
            priority = max(priority, 2)

    if min_int >= 60 and away_baski >= 60:
        if away_chg is not None and away_chg <= -7:
            signals.append((f"🔥 Deplasman baskısı ({away_baski}/100) + oran düşüyor → GÜÇLÜ SİNYAL", "signal-high"))
            priority = max(priority, 3)
        elif away_chg is not None and away_chg <= -3:
            signals.append((f"⚡ Deplasman baskısı ({away_baski}/100) + oran hafif düşüyor", "signal-med"))
            priority = max(priority, 2)

    # KURAL 2: 0-0 + dakika
    if toplam_gol == 0:
        if min_int >= 80:
            signals.append(("🔥 80+ dak. GOLSÜZ — Güçlü gol beklentisi", "signal-high"))
            priority = max(priority, 3)
        elif min_int >= 70:
            signals.append(("⚡ 70+ dak. golsüz — Gol sinyali", "signal-med"))
            priority = max(priority, 2)

    # KURAL 3: Sadece oran hareketi (istatistik yoksa)
    if not stats:
        if home_chg is not None and home_chg <= -12:
            signals.append((f"📉 Ev sahibi oranı sert düştü: {home_pre} → {home_live} ({home_chg:+.1f}%)", "signal-high"))
            priority = max(priority, 3)
        elif home_chg is not None and home_chg <= -6:
            signals.append((f"📉 Ev sahibi oranı düştü: {home_pre} → {home_live} ({home_chg:+.1f}%)", "signal-med"))
            priority = max(priority, 2)
        if away_chg is not None and away_chg <= -12:
            signals.append((f"📉 Deplasman oranı sert düştü: {away_pre} → {away_live} ({away_chg:+.1f}%)", "signal-high"))
            priority = max(priority, 3)

    # KURAL 4: Geride kalan takım baskısı
    if h_gol < a_gol and min_int >= 60 and home_baski >= 55:
        signals.append((f"🔄 Ev sahibi geride ({score}) + baskı yapıyor ({home_baski}/100)", "signal-med"))
        priority = max(priority, 2)
    if a_gol < h_gol and min_int >= 60 and away_baski >= 55:
        signals.append((f"🔄 Deplasman geride ({score}) + baskı yapıyor ({away_baski}/100)", "signal-med"))
        priority = max(priority, 2)

    if not signals:
        signals.append(("Sinyal yok", "signal-low"))

    return {
        "home": home,
        "away": away,
        "score": score,
        "ht_score": ht_score,
        "minute": minute,
        "competition": competition,
        "country": country,
        "signals": signals,
        "priority": priority,
        "stats": stats,
        "home_baski": home_baski,
        "away_baski": away_baski,
        "odds_pre":  {"home": home_pre,  "draw": draw_pre,  "away": away_pre},
        "odds_live": {"home": home_live, "draw": draw_live, "away": away_live},
        "odds_chg":  {"home": home_chg,  "draw": draw_chg,  "away": away_chg},
    }

def odds_renk(chg):
    if chg is None: return "odds-box"
    if chg <= -6:   return "odds-box odds-down"
    if chg >= 6:    return "odds-box odds-up"
    return "odds-box"

def stat_renk(h_val, a_val, taraf):
    if taraf == "home":
        return "stat-home" if h_val > a_val else ("stat-away" if h_val < a_val else "")
    else:
        return "stat-home" if a_val > h_val else ("stat-away" if a_val < h_val else "")

# ── Ana akış ─────────────────────────────────────────────
maclar = getir_canli_maclar()

if not maclar:
    st.warning("⏳ Şu an aktif canlı maç yok.")
    st.info("Büyük liglerin maç saatlerinde (akşam 18:00–23:00) tekrar dene.")
else:
    with st.spinner("İstatistikler yükleniyor..."):
        veriler = [sinyal_uret(m) for m in maclar]

    veriler.sort(key=lambda x: x["priority"], reverse=True)

    sinyalli = sum(1 for d in veriler if d["priority"] >= 2)
    st.success(f"🔴 **{len(veriler)} canlı maç** • 🟢 **{sinyalli} sinyalli maç**")

    cols = st.columns(3)
    for idx, data in enumerate(veriler):
        with cols[idx % 3]:
            if data["priority"] >= 3:
                card_cls = "card card-signal"
            elif data["priority"] == 2:
                card_cls = "card card-med"
            else:
                card_cls = "card"

            st.markdown(f'<div class="{card_cls}">', unsafe_allow_html=True)
            st.markdown(f'🔴 <span class="badge">{data["competition"]} • {data["country"]}</span>', unsafe_allow_html=True)
            st.subheader(f"{data['home']} vs {data['away']}")
            st.metric("Skor", f"{data['score']} — {data['minute']}'")
            if data["ht_score"]:
                st.caption(f"İY: {data['ht_score']}")

            # İstatistikler
            s = data["stats"]
            if s:
                ph, pa = parse_stat(s.get("possesion"))
                sh, sa = parse_stat(s.get("shots_on_target"))
                ah, aa = parse_stat(s.get("attempts_on_goal"))
                ch, ca = parse_stat(s.get("corners"))

                st.markdown(
                    f'<div class="stat-row">'
                    f'<div class="stat-box">Top<br><span class="{stat_renk(ph,pa,"home")}">{ph}%</span> – <span class="{stat_renk(ph,pa,"away")}">{pa}%</span></div>'
                    f'<div class="stat-box">İsabetli Şut<br><span class="{stat_renk(sh,sa,"home")}">{sh}</span> – <span class="{stat_renk(sh,sa,"away")}">{sa}</span></div>'
                    f'<div class="stat-box">Atak<br><span class="{stat_renk(ah,aa,"home")}">{ah}</span> – <span class="{stat_renk(ah,aa,"away")}">{aa}</span></div>'
                    f'<div class="stat-box">Korner<br><span class="{stat_renk(ch,ca,"home")}">{ch}</span> – <span class="{stat_renk(ch,ca,"away")}">{ca}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.caption(f"Baskı → {data['home'][:14]}: {data['home_baski']}/100 | {data['away'][:14]}: {data['away_baski']}/100")

            # Oranlar
            op = data["odds_pre"]
            ol = data["odds_live"]
            oc = data["odds_chg"]
            has_live = any([ol["home"], ol["draw"], ol["away"]])
            has_pre  = any([op["home"], op["draw"], op["away"]])

            if has_live:
                def fmt_live(val, chg, lbl):
                    chg_str = f"<br><small>{chg:+.0f}%</small>" if chg is not None else ""
                    return f'<div class="{odds_renk(chg)}"><small>{lbl}</small><br><b>{val if val else "—"}</b>{chg_str}</div>'
                st.markdown(
                    f'<div class="odds-row">'
                    f'{fmt_live(ol["home"], oc["home"], "1 Canlı")}'
                    f'{fmt_live(ol["draw"], oc["draw"], "X Canlı")}'
                    f'{fmt_live(ol["away"], oc["away"], "2 Canlı")}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            if has_pre:
                st.markdown(
                    f'<div class="odds-row">'
                    f'<div class="odds-box"><small>1 Öncesi</small><br>{op["home"] if op["home"] else "—"}</div>'
                    f'<div class="odds-box"><small>X Öncesi</small><br>{op["draw"] if op["draw"] else "—"}</div>'
                    f'<div class="odds-box"><small>2 Öncesi</small><br>{op["away"] if op["away"] else "—"}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Sinyaller
            for (sig_text, sig_cls) in data["signals"]:
                st.markdown(f'<div class="signal {sig_cls}">{sig_text}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Şimdi Yenile"):
    st.cache_data.clear()
    st.rerun()

st.caption("Veri: live-score-api.com • İstatistik + oran hareketi bazlı sinyal • 30 sn yenileme")
