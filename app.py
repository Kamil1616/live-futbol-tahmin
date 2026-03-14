import streamlit as st
import requests
from difflib import SequenceMatcher

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
    .odds-row { display: flex; gap: 6px; margin: 6px 0; flex-wrap: wrap; }
    .odds-box { background: #21262d; border-radius: 6px; padding: 5px 10px; text-align: center; flex: 1; font-size: 12px; min-width: 60px; }
    .odds-down { background: #1a3a1a; color: #3fb950; font-weight: bold; }
    .odds-up   { background: #3a1a1a; color: #f85149; }
    h1 { color: #58a6ff !important; }
    .stButton > button { background: #238636; color: white; border: none; border-radius: 8px; padding: 8px 20px; }
    .badge { background: #21262d; border-radius: 4px; padding: 2px 8px; font-size: 12px; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Canlı Futbol Tahmin Sinyalleri")

LS_KEY    = "lD0xMVlUGwip7fzY"
LS_SECRET = "C7b6mK3wocmicEDxhD44zqYfWhF3we19"
ODDS_KEY  = "ac0551df534e175a4f312681465cffcc"
LS_BASE   = "https://livescore-api.com/api-client"
ODDS_BASE = "https://api.the-odds-api.com/v4"

MIN_SINYAL = 15  # Sinyaller kaçıncı dakikadan itibaren üretilsin

# ── API çağrıları ─────────────────────────────────────────

@st.cache_data(ttl=60)
def getir_canli_maclar():
    url = f"{LS_BASE}/matches/live.json?key={LS_KEY}&secret={LS_SECRET}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                maclar = (data.get("data") or {}).get("match") or []
                return [m for m in maclar if m.get("status") == "IN PLAY"]
            else:
                st.error(f"LiveScore API hatası: {data.get('error', '?')}")
        else:
            st.error(f"LiveScore HTTP hatası: {resp.status_code}")
    except Exception as e:
        st.error(f"Bağlantı sorunu: {str(e)}")
    return []

@st.cache_data(ttl=10)
def getir_stats(match_id):
    try:
        url = f"{LS_BASE}/matches/stats.json?match_id={match_id}&key={LS_KEY}&secret={LS_SECRET}"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                result = data.get("data")
                if isinstance(result, dict):
                    return result
    except:
        pass
    return {}

@st.cache_data(ttl=15)
def getir_odds():
    url = (
        f"{ODDS_BASE}/sports/soccer/odds/"
        f"?apiKey={ODDS_KEY}&regions=eu&markets=h2h,totals"
        f"&oddsFormat=decimal&bookmakers=betsson"
    )
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            maclar = resp.json()
            sonuc = {}
            for mac in maclar:
                home_team  = mac.get("home_team", "")
                away_team  = mac.get("away_team", "")
                pinnacle   = next((b for b in (mac.get("bookmakers") or []) if b.get("key") == "betsson"), None)
                if not pinnacle:
                    continue

                h2h_data    = {"home": 0, "draw": 0, "away": 0}
                totals_data = {}

                for market in (pinnacle.get("markets") or []):
                    key = market.get("key")
                    if key == "h2h":
                        for o in (market.get("outcomes") or []):
                            name  = o.get("name", "")
                            price = float(o.get("price") or 0)
                            if name == home_team:   h2h_data["home"] = price
                            elif name == away_team: h2h_data["away"] = price
                            elif name == "Draw":    h2h_data["draw"] = price
                    elif key == "totals":
                        for o in (market.get("outcomes") or []):
                            name  = o.get("name", "")
                            point = o.get("point")
                            price = float(o.get("price") or 0)
                            if point is not None:
                                point = float(point)
                                if point not in totals_data:
                                    totals_data[point] = {"over": 0, "under": 0}
                                if name == "Over":   totals_data[point]["over"]  = price
                                elif name == "Under": totals_data[point]["under"] = price

                if h2h_data["home"] or totals_data:
                    sonuc[f"{home_team}|{away_team}"] = {"h2h": h2h_data, "totals": totals_data}
            return sonuc
        else:
            st.warning(f"Odds API HTTP hatası: {resp.status_code}")
    except Exception as e:
        st.warning(f"Odds API sorunu: {str(e)}")
    return {}

# ── Yardımcı fonksiyonlar ─────────────────────────────────

def benzerlik(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def odds_eslestir(home, away, odds_dict):
    en_iyi, en_skor = None, 0.6
    for anahtar, odds in odds_dict.items():
        parca = anahtar.split("|")
        if len(parca) != 2: continue
        oh, oa = parca
        skor = (benzerlik(home, oh) + benzerlik(away, oa)) / 2
        if skor > en_skor:
            en_skor = skor
            en_iyi = odds
    return en_iyi

def parse_stat(val):
    try:
        if val is None: return 0, 0
        h, a = str(val).split(":")
        return int(h), int(a)
    except:
        return 0, 0

def parse_minute(minute):
    try:
        return int(str(minute).replace('+', '').split('+')[0])
    except:
        return 0

def hesapla_baski(stats, taraf="home"):
    if not stats or not isinstance(stats, dict): return 0
    skor = 0.0
    ph, pa = parse_stat(stats.get("possesion"))
    if ph + pa > 0: skor += ((ph if taraf == "home" else pa) / 100) * 30
    sh, sa = parse_stat(stats.get("shots_on_target"))
    if sh + sa > 0: skor += ((sh if taraf == "home" else sa) / (sh + sa)) * 25
    ah, aa = parse_stat(stats.get("attempts_on_goal"))
    if ah + aa > 0: skor += ((ah if taraf == "home" else aa) / (ah + aa)) * 25
    ch, ca = parse_stat(stats.get("corners"))
    if ch + ca > 0: skor += ((ch if taraf == "home" else ca) / (ch + ca)) * 20
    return round(skor)

def pct_change(pre, live):
    if pre and pre > 0 and live and live > 0:
        return round((live - pre) / pre * 100, 1)
    return None

def odds_renk(chg):
    if chg is None: return "odds-box"
    if chg <= -6:   return "odds-box odds-down"
    if chg >= 6:    return "odds-box odds-up"
    return "odds-box"

def stat_renk(h, a, taraf):
    if taraf == "home": return "stat-home" if h > a else ("stat-away" if h < a else "")
    return "stat-home" if a > h else ("stat-away" if a < h else "")

# ── Sinyal üretimi ────────────────────────────────────────

def sinyal_uret(match, odds_dict):
    try:
        match_id    = match.get("id")
        home        = (match.get("home") or {}).get("name", "Ev Sahibi")
        away        = (match.get("away") or {}).get("name", "Deplasman")
        score       = (match.get("scores") or {}).get("score", "? - ?")
        ht_score    = (match.get("scores") or {}).get("ht_score", "")
        minute      = match.get("time", "?")
        competition = (match.get("competition") or {}).get("name", "")
        country     = (match.get("country") or {}).get("name", "")

        ls_pre   = (match.get("odds") or {}).get("pre") or {}
        home_pre = float(ls_pre.get("1") or 0)
        draw_pre = float(ls_pre.get("X") or 0)
        away_pre = float(ls_pre.get("2") or 0)

        eslesen     = odds_eslestir(home, away, odds_dict)
        h2h_live    = (eslesen or {}).get("h2h") or {}
        totals_live = (eslesen or {}).get("totals") or {}

        home_live = h2h_live.get("home") or 0
        draw_live = h2h_live.get("draw") or 0
        away_live = h2h_live.get("away") or 0

        home_chg = pct_change(home_pre, home_live)
        draw_chg = pct_change(draw_pre, draw_live)
        away_chg = pct_change(away_pre, away_live)

        min_int    = parse_minute(minute)
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

        # Sinyal üretme eşiği
        if min_int < MIN_SINYAL:
            signals.append(("Sinyal yok", "signal-low"))
            return _sonuc(home, away, score, ht_score, minute, competition, country,
                          signals, priority, stats, home_baski, away_baski,
                          home_pre, draw_pre, away_pre, home_live, draw_live, away_live,
                          home_chg, draw_chg, away_chg, totals_live, toplam_gol, eslesen)

        # ── KURAL 1: Alt/Üst oran sinyalleri ──
        for cizgi in sorted(totals_live.keys()):
            ou = totals_live[cizgi]
            over_price = ou.get("over") or 0
            if not over_price or toplam_gol > cizgi:
                continue
            if over_price <= 1.25:
                signals.append((f"🔥 {cizgi} Üst oranı {over_price:.2f} — Gol çok yakın! ({min_int}. dak.)", "signal-high"))
                priority = max(priority, 3)
            elif over_price <= 1.45:
                signals.append((f"⚡ {cizgi} Üst oranı {over_price:.2f} — Gol beklentisi yüksek ({min_int}. dak.)", "signal-med"))
                priority = max(priority, 2)
            elif over_price <= 1.65 and min_int >= 60:
                signals.append((f"📊 {cizgi} Üst oranı {over_price:.2f} — Takip et ({min_int}. dak.)", "signal-med"))
                priority = max(priority, 2)

        # ── KURAL 2: 1X2 oran düşüşü ──
        if home_chg is not None and home_chg <= -20:
            signals.append((f"🔥 Ev sahibi oranı sert düştü: {home_pre:.2f} → {home_live:.2f} ({home_chg:+.1f}%)", "signal-high"))
            priority = max(priority, 3)
        elif home_chg is not None and home_chg <= -10:
            signals.append((f"📉 Ev sahibi oranı düştü: {home_pre:.2f} → {home_live:.2f} ({home_chg:+.1f}%)", "signal-med"))
            priority = max(priority, 2)

        if away_chg is not None and away_chg <= -20:
            signals.append((f"🔥 Deplasman oranı sert düştü: {away_pre:.2f} → {away_live:.2f} ({away_chg:+.1f}%)", "signal-high"))
            priority = max(priority, 3)
        elif away_chg is not None and away_chg <= -10:
            signals.append((f"📉 Deplasman oranı düştü: {away_pre:.2f} → {away_live:.2f} ({away_chg:+.1f}%)", "signal-med"))
            priority = max(priority, 2)

        # ── KURAL 3: Baskı + oran kombinasyonu ──
        if home_baski >= 60:
            if home_chg is not None and home_chg <= -7:
                signals.append((f"🔥 Ev sahibi baskısı ({home_baski}/100) + oran düştü ({home_chg:+.1f}%) → GÜÇLÜ SİNYAL", "signal-high"))
                priority = max(priority, 3)
            elif min_int >= 60:
                signals.append((f"⚡ Ev sahibi baskı yapıyor ({home_baski}/100) — {min_int}. dak.", "signal-med"))
                priority = max(priority, 2)

        if away_baski >= 60:
            if away_chg is not None and away_chg <= -7:
                signals.append((f"🔥 Deplasman baskısı ({away_baski}/100) + oran düştü ({away_chg:+.1f}%) → GÜÇLÜ SİNYAL", "signal-high"))
                priority = max(priority, 3)
            elif min_int >= 60:
                signals.append((f"⚡ Deplasman baskı yapıyor ({away_baski}/100) — {min_int}. dak.", "signal-med"))
                priority = max(priority, 2)

        # ── KURAL 4: Golsüz maç ──
        if toplam_gol == 0:
            if min_int >= 80:
                signals.append(("🔥 80+ dak. GOLSÜZ — Güçlü gol beklentisi", "signal-high"))
                priority = max(priority, 3)
            elif min_int >= 70:
                signals.append(("⚡ 70+ dak. golsüz — Gol sinyali", "signal-med"))
                priority = max(priority, 2)
            elif min_int >= 15:
                signals.append((f"📊 {min_int}. dak. golsüz — Takip et", "signal-low"))
                priority = max(priority, 1)

        # ── KURAL 5: Geride kalan takım bastırıyor ──
        if h_gol < a_gol and home_baski >= 55 and min_int >= 45:
            signals.append((f"🔄 Ev sahibi geride ({score}) + baskı ({home_baski}/100) → Geri dönüş beklentisi", "signal-med"))
            priority = max(priority, 2)
        if a_gol < h_gol and away_baski >= 55 and min_int >= 45:
            signals.append((f"🔄 Deplasman geride ({score}) + baskı ({away_baski}/100) → Geri dönüş beklentisi", "signal-med"))
            priority = max(priority, 2)

        if not signals:
            signals.append(("Sinyal yok", "signal-low"))

        return _sonuc(home, away, score, ht_score, minute, competition, country,
                      signals, priority, stats, home_baski, away_baski,
                      home_pre, draw_pre, away_pre, home_live, draw_live, away_live,
                      home_chg, draw_chg, away_chg, totals_live, toplam_gol, eslesen)

    except Exception as e:
        return _sonuc("?", "?", "?", "", "?", "", "",
                      [(f"Veri hatası: {str(e)}", "signal-low")], 0, {}, 0, 0,
                      0, 0, 0, 0, 0, 0, None, None, None, {}, 0, None)

def _sonuc(home, away, score, ht_score, minute, competition, country,
           signals, priority, stats, home_baski, away_baski,
           home_pre, draw_pre, away_pre, home_live, draw_live, away_live,
           home_chg, draw_chg, away_chg, totals_live, toplam_gol, eslesen):
    return {
        "home": home, "away": away, "score": score, "ht_score": ht_score,
        "minute": minute, "competition": competition, "country": country,
        "signals": signals, "priority": priority, "stats": stats,
        "home_baski": home_baski, "away_baski": away_baski,
        "odds_pre":    {"home": home_pre,  "draw": draw_pre,  "away": away_pre},
        "odds_live":   {"home": home_live, "draw": draw_live, "away": away_live},
        "odds_chg":    {"home": home_chg,  "draw": draw_chg,  "away": away_chg},
        "totals_live": totals_live, "toplam_gol": toplam_gol,
        "odds_eslesti": eslesen is not None,
    }

# ── Ana akış ─────────────────────────────────────────────
maclar = getir_canli_maclar()

if not maclar:
    st.warning("⏳ Şu an aktif canlı maç yok.")
    st.info("Büyük liglerin maç saatlerinde (akşam 18:00–23:00) tekrar dene.")
else:
    with st.spinner("Betsson oranları ve istatistikler yükleniyor..."):
        odds_dict = getir_odds()
        veriler   = [sinyal_uret(m, odds_dict) for m in maclar]

    veriler.sort(key=lambda x: x["priority"], reverse=True)

    sinyalli = sum(1 for d in veriler if d["priority"] >= 2)
    eslesmis = sum(1 for d in veriler if d["odds_eslesti"])
    st.success(f"🔴 **{len(veriler)} canlı maç** • 🟢 **{sinyalli} sinyalli** • 📊 **{eslesmis} maçta Betsson oranı eşleşti**")

    cols = st.columns(3)
    for idx, data in enumerate(veriler):
        with cols[idx % 3]:
            card_cls = "card card-signal" if data["priority"] >= 3 else ("card card-med" if data["priority"] == 2 else "card")
            st.markdown(f'<div class="{card_cls}">', unsafe_allow_html=True)
            st.markdown(f'🔴 <span class="badge">{data["competition"]} • {data["country"]}</span>', unsafe_allow_html=True)
            st.subheader(f"{data['home']} vs {data['away']}")
            st.metric("Skor", f"{data['score']} — {data['minute']}'")
            if data["ht_score"]:
                st.caption(f"İY: {data['ht_score']}")

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

            op = data["odds_pre"]
            ol = data["odds_live"]
            oc = data["odds_chg"]
            has_live = any([ol["home"], ol["draw"], ol["away"]])
            has_pre  = any([op["home"], op["draw"], op["away"]])

            if has_live:
                def fmt(val, chg, lbl):
                    chg_str = f"<br><small>{chg:+.0f}%</small>" if chg is not None else ""
                    return f'<div class="{odds_renk(chg)}"><small>{lbl}</small><br><b>{val:.2f}</b>{chg_str}</div>'
                st.markdown(
                    f'<div class="odds-row">'
                    f'{fmt(ol["home"], oc["home"], "1 Betsson")}'
                    f'{fmt(ol["draw"], oc["draw"], "X Betsson")}'
                    f'{fmt(ol["away"], oc["away"], "2 Betsson")}'
                    f'</div>', unsafe_allow_html=True
                )
            if has_pre:
                st.markdown(
                    f'<div class="odds-row">'
                    f'<div class="odds-box"><small>1 Öncesi</small><br>{op["home"] if op["home"] else "—"}</div>'
                    f'<div class="odds-box"><small>X Öncesi</small><br>{op["draw"] if op["draw"] else "—"}</div>'
                    f'<div class="odds-box"><small>2 Öncesi</small><br>{op["away"] if op["away"] else "—"}</div>'
                    f'</div>', unsafe_allow_html=True
                )

            tl = data["totals_live"]
            tg = data["toplam_gol"]
            if tl:
                st.caption("⚖️ Alt / Üst — Betsson")
                satirlar = []
                for cizgi in sorted(tl.keys()):
                    over  = tl[cizgi].get("over") or 0
                    under = tl[cizgi].get("under") or 0
                    gecti = tg > cizgi
                    etiket = f"✅ {cizgi}" if gecti else f"{cizgi}"
                    renk = "odds-down" if (not gecti and over > 0 and over <= 1.50) else ""
                    satirlar.append(
                        f'<div class="odds-box {renk}"><small>{etiket}</small><br>'
                        f'Ü <b>{over:.2f}</b><br><small>A {under:.2f}</small></div>'
                    )
                st.markdown(f'<div class="odds-row">{"".join(satirlar)}</div>', unsafe_allow_html=True)

            if not has_live and not tl:
                st.caption("⚠️ Betsson bu maç için oran vermedi")

            for (sig_text, sig_cls) in data["signals"]:
                st.markdown(f'<div class="signal {sig_cls}">{sig_text}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Şimdi Yenile"):
    st.cache_data.clear()
    st.rerun()

st.caption("Veri: livescore-api.com (istatistik 10sn) + Betsson via the-odds-api.com (1X2 + Alt/Üst 15sn) • ⚠️ Odds API: 500 istek/ay limiti")
