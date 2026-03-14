import streamlit as st
import requests
from difflib import SequenceMatcher

st.set_page_config(page_title="⚽ Canlı Sinyal", layout="wide", page_icon="⚽")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #080c12;
    background-image: radial-gradient(ellipse at 20% 0%, #0d2137 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 100%, #091a0e 0%, transparent 50%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

h1 { font-family: 'Rajdhani', sans-serif !important; font-size: 2rem !important;
     letter-spacing: 2px; color: #fff !important; margin-bottom: 0 !important; }

.header-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 0; border-bottom: 1px solid #1e2d3d; margin-bottom: 20px;
}
.live-dot { width:8px; height:8px; border-radius:50%; background:#ef4444;
            display:inline-block; margin-right:6px;
            box-shadow: 0 0 8px #ef4444; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* KART */
.mac-karti {
    background: linear-gradient(135deg, #0f1923 0%, #111d2b 100%);
    border: 1px solid #1e2d3d;
    border-radius: 16px;
    padding: 0;
    margin-bottom: 16px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.mac-karti:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
.mac-karti.sinyal-yuksek { border-color: #22c55e; box-shadow: 0 0 20px rgba(34,197,94,0.2); }
.mac-karti.sinyal-orta   { border-color: #f97316; box-shadow: 0 0 16px rgba(249,115,22,0.15); }

.kart-ust {
    padding: 14px 16px 10px;
    border-bottom: 1px solid #1e2d3d;
    display: flex; justify-content: space-between; align-items: center;
}
.lig-adi { font-size: 11px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }
.dakika-badge {
    background: #ef4444; color: white; font-size: 11px; font-weight: 700;
    padding: 2px 8px; border-radius: 20px; font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
}

.kart-orta { padding: 12px 16px; }
.takim-adi { font-family: 'Rajdhani', sans-serif; font-size: 17px; font-weight: 700;
             color: #f1f5f9; line-height: 1.2; }
.skor-blok { display:flex; align-items:center; gap:12px; margin-top:8px; }
.skor { font-family: 'Rajdhani', sans-serif; font-size: 28px; font-weight: 700; color:#fff; }
.iy-skor { font-size: 11px; color: #475569; }

/* İSTATİSTİK */
.stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; margin:10px 0; }
.stat-item { background:#0a1520; border-radius:8px; padding:8px 6px; text-align:center; }
.stat-label { font-size:10px; color:#475569; margin-bottom:4px; }
.stat-val { font-size:13px; font-weight:600; }
.ev { color:#22c55e; }
.dep { color:#ef4444; }
.esit { color:#94a3b8; }
.baski-bar { height:4px; border-radius:2px; background:#1e2d3d; margin:8px 0 4px; overflow:hidden; }
.baski-fill { height:100%; background:linear-gradient(90deg,#22c55e,#16a34a); border-radius:2px; }

/* ORANLAR */
.oran-bolum { padding:10px 16px; border-top:1px solid #1e2d3d; }
.oran-baslik { font-size:10px; color:#475569; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; }
.oran-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; }
.oran-kutu { background:#0a1520; border-radius:8px; padding:8px 4px; text-align:center; border:1px solid #1e2d3d; }
.oran-kutu.dusus { background:#0d2010; border-color:#22c55e; }
.oran-kutu.yukselis { background:#200d0d; border-color:#ef4444; }
.oran-label { font-size:10px; color:#475569; }
.oran-deger { font-size:15px; font-weight:700; font-family:'Rajdhani',sans-serif; color:#f1f5f9; }
.oran-deger.dusus { color:#22c55e; }
.oran-deger.yukselis { color:#ef4444; }
.oran-degisim { font-size:10px; margin-top:1px; }
.bm-etiket { font-size:9px; color:#334155; letter-spacing:0.5px; margin-top:2px; }

/* TOTALS */
.total-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-top:6px; }
.total-kutu { background:#0a1520; border-radius:8px; padding:8px 6px; text-align:center; border:1px solid #1e2d3d; }
.total-kutu.gecti { background:#0d2010; border-color:#22c55e; }
.total-kutu.sicak { background:#1a1200; border-color:#eab308; }
.total-cizgi { font-size:12px; font-weight:700; font-family:'Rajdhani',sans-serif; color:#94a3b8; }
.total-cizgi.gecti { color:#22c55e; }
.total-over { font-size:14px; font-weight:700; color:#f1f5f9; margin:2px 0; }
.total-under { font-size:10px; color:#475569; }

/* SİNYAL */
.sinyal-bolum { padding:10px 16px 14px; border-top:1px solid #1e2d3d; }
.sinyal-item { border-radius:8px; padding:8px 12px; margin-bottom:5px; font-size:13px; font-weight:600; }
.sinyal-high { background:linear-gradient(135deg,#14532d,#166534); color:#86efac; border:1px solid #22c55e; }
.sinyal-med  { background:linear-gradient(135deg,#431407,#7c2d12); color:#fdba74; border:1px solid #f97316; }
.sinyal-low  { background:#0f172a; color:#475569; border:1px solid #1e293b; }

.stButton>button {
    background:linear-gradient(135deg,#1d4ed8,#1e40af) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    padding:10px 24px !important; font-weight:600 !important; letter-spacing:0.5px !important;
}
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="header-bar">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="font-size:1.8rem">⚽</span>
    <div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:1.5rem;font-weight:700;letter-spacing:2px;color:#fff">
        CANLI SİNYAL
      </div>
      <div style="font-size:11px;color:#475569;letter-spacing:1px">
        Pinnacle + Betfair • Canlı Oran & İstatistik
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

LS_KEY    = "lD0xMVlUGwip7fzY"
LS_SECRET = "C7b6mK3wocmicEDxhD44zqYfWhF3we19"
ODDS_KEY  = "ac0551df534e175a4f312681465cffcc"
LS_BASE   = "https://livescore-api.com/api-client"
ODDS_BASE = "https://api.the-odds-api.com/v4"

MIN_SINYAL = 15
CIZGILER   = [0.5, 1.5, 2.5]
BOOKMAKERS = ["pinnacle", "betfair_ex_eu"]
BM_ETIKET  = {"pinnacle": "Pinnacle", "betfair_ex_eu": "Betfair"}

# ── API ───────────────────────────────────────────────────

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
            st.error(f"LiveScore hatası: {data.get('error','?')}")
        else:
            st.error(f"LiveScore HTTP: {resp.status_code}")
    except Exception as e:
        st.error(f"Bağlantı: {str(e)}")
    return []

@st.cache_data(ttl=10)
def getir_stats(match_id):
    try:
        url = f"{LS_BASE}/matches/stats.json?match_id={match_id}&key={LS_KEY}&secret={LS_SECRET}"
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                r = data.get("data")
                if isinstance(r, dict): return r
    except: pass
    return {}

@st.cache_data(ttl=15)
def getir_odds():
    """
    Pinnacle + Betfair için ayrı ayrı h2h + totals.
    Döndürür:
    {
      "Home|Away": {
        "pinnacle":      { "h2h": {...}, "totals": {...} },
        "betfair_ex_eu": { "h2h": {...}, "totals": {...} },
      }
    }
    """
    url = (
        f"{ODDS_BASE}/sports/soccer/odds/"
        f"?apiKey={ODDS_KEY}&regions=eu&markets=h2h,totals&oddsFormat=decimal"
        f"&bookmakers=pinnacle,betfair_ex_eu"
    )
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {}
        maclar = resp.json()
        sonuc = {}
        for mac in maclar:
            home_team  = mac.get("home_team","")
            away_team  = mac.get("away_team","")
            bms        = mac.get("bookmakers") or []
            if not bms: continue

            mac_data = {}
            for bm in bms:
                bm_key = bm.get("key","")
                if bm_key not in BOOKMAKERS: continue

                h2h_d    = {"home":0,"draw":0,"away":0}
                totals_d = {}

                for market in (bm.get("markets") or []):
                    mk = market.get("key")
                    if mk == "h2h":
                        for o in (market.get("outcomes") or []):
                            name  = o.get("name","")
                            price = float(o.get("price") or 0)
                            if price <= 0 or price > 500: continue
                            if name == home_team:   h2h_d["home"] = price
                            elif name == away_team: h2h_d["away"] = price
                            elif name == "Draw":    h2h_d["draw"] = price
                    elif mk == "totals":
                        for o in (market.get("outcomes") or []):
                            name  = o.get("name","")
                            point = o.get("point")
                            price = float(o.get("price") or 0)
                            if point is None or price <= 0: continue
                            point = float(point)
                            if point not in CIZGILER: continue
                            if point not in totals_d:
                                totals_d[point] = {"over":0,"under":0}
                            if name == "Over":    totals_d[point]["over"]  = price
                            elif name == "Under": totals_d[point]["under"] = price

                if h2h_d["home"] or totals_d:
                    mac_data[bm_key] = {"h2h": h2h_d, "totals": totals_d}

            if mac_data:
                sonuc[f"{home_team}|{away_team}"] = mac_data
        return sonuc
    except Exception as e:
        return {}

# ── Yardımcılar ───────────────────────────────────────────

def benzerlik(a,b):
    return SequenceMatcher(None,a.lower(),b.lower()).ratio()

def odds_eslestir(home,away,odds_dict):
    en_iyi,en_skor=None,0.6
    for anahtar,odds in odds_dict.items():
        p=anahtar.split("|")
        if len(p)!=2: continue
        oh,oa=p
        s=(benzerlik(home,oh)+benzerlik(away,oa))/2
        if s>en_skor: en_skor=s; en_iyi=odds
    return en_iyi

def parse_stat(val):
    try:
        if val is None: return 0,0
        h,a=str(val).split(":")
        return int(h),int(a)
    except: return 0,0

def parse_minute(minute):
    try: return int(str(minute).replace('+',' ').split()[0])
    except: return 0

def hesapla_baski(stats,taraf="home"):
    if not stats or not isinstance(stats,dict): return 0
    s=0.0
    ph,pa=parse_stat(stats.get("possesion"))
    if ph+pa>0: s+=((ph if taraf=="home" else pa)/100)*30
    sh,sa=parse_stat(stats.get("shots_on_target"))
    if sh+sa>0: s+=((sh if taraf=="home" else sa)/(sh+sa))*25
    ah,aa=parse_stat(stats.get("attempts_on_goal"))
    if ah+aa>0: s+=((ah if taraf=="home" else aa)/(ah+aa))*25
    ch,ca=parse_stat(stats.get("corners"))
    if ch+ca>0: s+=((ch if taraf=="home" else ca)/(ch+ca))*20
    return round(s)

def pct(pre,live):
    if pre and pre>0 and live and live>0:
        return round((live-pre)/pre*100,1)
    return None

def oran_renk_cls(chg):
    if chg is None: return ""
    if chg<=-6: return "dusus"
    if chg>=6:  return "yukselis"
    return ""

# ── Sinyal üretimi ────────────────────────────────────────

def sinyal_uret(match, odds_dict):
    try:
        match_id    = match.get("id")
        home        = (match.get("home") or {}).get("name","Ev Sahibi")
        away        = (match.get("away") or {}).get("name","Deplasman")
        score       = (match.get("scores") or {}).get("score","? - ?")
        ht_score    = (match.get("scores") or {}).get("ht_score","")
        minute      = match.get("time","?")
        competition = (match.get("competition") or {}).get("name","")
        country     = (match.get("country") or {}).get("name","")

        ls_pre   = (match.get("odds") or {}).get("pre") or {}
        home_pre = float(ls_pre.get("1") or 0)
        draw_pre = float(ls_pre.get("X") or 0)
        away_pre = float(ls_pre.get("2") or 0)

        eslesen = odds_eslestir(home,away,odds_dict)

        # Her bookmaker için ayrı oran al
        bm_oranlar = {}
        for bm_key in BOOKMAKERS:
            bm_data = (eslesen or {}).get(bm_key) or {}
            h2h = bm_data.get("h2h") or {}
            tot = bm_data.get("totals") or {}
            hl = h2h.get("home") or 0
            dl = h2h.get("draw") or 0
            al = h2h.get("away") or 0
            bm_oranlar[bm_key] = {
                "home": hl, "draw": dl, "away": al,
                "home_chg": pct(home_pre,hl),
                "draw_chg": pct(draw_pre,dl),
                "away_chg": pct(away_pre,al),
                "totals": tot,
            }

        # Sinyal için Pinnacle oranlarını ana referans al
        pin = bm_oranlar.get("pinnacle",{})
        home_chg = pin.get("home_chg")
        away_chg = pin.get("away_chg")
        totals_live = pin.get("totals") or {}
        # Betfair yoksa Pinnacle totals kullan
        for bm_key in BOOKMAKERS:
            if bm_oranlar[bm_key].get("totals"):
                totals_live = bm_oranlar[bm_key]["totals"]
                break

        min_int    = parse_minute(minute)
        stats      = getir_stats(match_id) if match_id else {}
        home_baski = hesapla_baski(stats,"home")
        away_baski = hesapla_baski(stats,"away")

        try:
            h_gol,a_gol = map(int,score.replace(" ","").split("-"))
            toplam_gol  = h_gol+a_gol
        except:
            h_gol,a_gol,toplam_gol = 0,0,0

        signals  = []
        priority = 0

        if min_int < MIN_SINYAL:
            signals.append(("Sinyal yok","sinyal-low"))
        else:
            # Totals sinyali
            for cizgi in CIZGILER:
                if cizgi not in totals_live or toplam_gol>cizgi: continue
                op = totals_live[cizgi].get("over") or 0
                if not op: continue
                if op<=1.25:
                    signals.append((f"🔥 {cizgi} Üst oranı {op:.2f} — Gol çok yakın! ({min_int}. dak.)","sinyal-high"))
                    priority=max(priority,3)
                elif op<=1.45:
                    signals.append((f"⚡ {cizgi} Üst {op:.2f} — Gol beklentisi yüksek ({min_int}. dak.)","sinyal-med"))
                    priority=max(priority,2)
                elif op<=1.65 and min_int>=60:
                    signals.append((f"📊 {cizgi} Üst {op:.2f} — Takip et ({min_int}. dak.)","sinyal-med"))
                    priority=max(priority,2)

            # 1X2 oran düşüşü
            if home_chg is not None and home_chg<=-20:
                signals.append((f"🔥 Ev sahibi oranı sert düştü: {home_pre:.2f}→{pin['home']:.2f} ({home_chg:+.1f}%)","sinyal-high"))
                priority=max(priority,3)
            elif home_chg is not None and home_chg<=-10:
                signals.append((f"📉 Ev sahibi oranı düştü: {home_pre:.2f}→{pin['home']:.2f} ({home_chg:+.1f}%)","sinyal-med"))
                priority=max(priority,2)

            if away_chg is not None and away_chg<=-20:
                signals.append((f"🔥 Deplasman oranı sert düştü: {away_pre:.2f}→{pin['away']:.2f} ({away_chg:+.1f}%)","sinyal-high"))
                priority=max(priority,3)
            elif away_chg is not None and away_chg<=-10:
                signals.append((f"📉 Deplasman oranı düştü: {away_pre:.2f}→{pin['away']:.2f} ({away_chg:+.1f}%)","sinyal-med"))
                priority=max(priority,2)

            # Baskı
            if home_baski>=60:
                if home_chg is not None and home_chg<=-7:
                    signals.append((f"🔥 Ev sahibi baskı ({home_baski}/100) + oran düştü → GÜÇLÜ SİNYAL","sinyal-high"))
                    priority=max(priority,3)
                elif min_int>=60:
                    signals.append((f"⚡ Ev sahibi baskı yapıyor ({home_baski}/100) — {min_int}. dak.","sinyal-med"))
                    priority=max(priority,2)

            if away_baski>=60:
                if away_chg is not None and away_chg<=-7:
                    signals.append((f"🔥 Deplasman baskı ({away_baski}/100) + oran düştü → GÜÇLÜ SİNYAL","sinyal-high"))
                    priority=max(priority,3)
                elif min_int>=60:
                    signals.append((f"⚡ Deplasman baskı yapıyor ({away_baski}/100) — {min_int}. dak.","sinyal-med"))
                    priority=max(priority,2)

            # Golsüz
            if toplam_gol==0:
                if min_int>=80:
                    signals.append(("🔥 80+ dak. GOLSÜZ — Güçlü gol beklentisi","sinyal-high"))
                    priority=max(priority,3)
                elif min_int>=70:
                    signals.append(("⚡ 70+ dak. golsüz — Gol sinyali","sinyal-med"))
                    priority=max(priority,2)
                elif min_int>=15:
                    signals.append((f"📊 {min_int}. dak. golsüz","sinyal-low"))
                    priority=max(priority,1)

            # Geride + baskı
            if h_gol<a_gol and home_baski>=55 and min_int>=45:
                signals.append((f"🔄 Ev sahibi geride ({score}) + baskı ({home_baski}/100)","sinyal-med"))
                priority=max(priority,2)
            if a_gol<h_gol and away_baski>=55 and min_int>=45:
                signals.append((f"🔄 Deplasman geride ({score}) + baskı ({away_baski}/100)","sinyal-med"))
                priority=max(priority,2)

            if not signals:
                signals.append(("Sinyal yok","sinyal-low"))

        return {
            "home":home,"away":away,"score":score,"ht_score":ht_score,
            "minute":minute,"competition":competition,"country":country,
            "signals":signals,"priority":priority,"stats":stats,
            "home_baski":home_baski,"away_baski":away_baski,
            "home_pre":home_pre,"draw_pre":draw_pre,"away_pre":away_pre,
            "bm_oranlar":bm_oranlar,"totals_live":totals_live,
            "toplam_gol":toplam_gol,"eslendi":eslesen is not None,
        }
    except Exception as e:
        return {
            "home":"?","away":"?","score":"?","ht_score":"","minute":"?",
            "competition":"","country":"",
            "signals":[(f"Hata: {str(e)}","sinyal-low")],"priority":0,
            "stats":{},"home_baski":0,"away_baski":0,
            "home_pre":0,"draw_pre":0,"away_pre":0,
            "bm_oranlar":{},"totals_live":{},"toplam_gol":0,"eslendi":False,
        }

# ── HTML Yardımcıları ─────────────────────────────────────

def stat_renk(h,a,taraf):
    if taraf=="home": return "ev" if h>a else ("dep" if h<a else "esit")
    return "ev" if a>h else ("dep" if a<h else "esit")

def render_kart(data):
    priority = data["priority"]
    kart_cls = "mac-karti"
    if priority>=3: kart_cls+=" sinyal-yuksek"
    elif priority==2: kart_cls+=" sinyal-orta"

    s = data["stats"]
    ph,pa=parse_stat(s.get("possesion")) if s else (0,0)
    sh,sa=parse_stat(s.get("shots_on_target")) if s else (0,0)
    ah,aa=parse_stat(s.get("attempts_on_goal")) if s else (0,0)
    ch,ca=parse_stat(s.get("corners")) if s else (0,0)

    hb = data["home_baski"]
    ab = data["away_baski"]

    html = f"""
    <div class="{kart_cls}">
      <div class="kart-ust">
        <span class="lig-adi">🔴 {data['competition']} • {data['country']}</span>
        <span class="dakika-badge">{data['minute']}'</span>
      </div>
      <div class="kart-orta">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div style="flex:1">
            <div class="takim-adi">{data['home']}</div>
            <div class="takim-adi" style="color:#94a3b8">vs {data['away']}</div>
          </div>
          <div style="text-align:right">
            <div class="skor">{data['score']}</div>
            {"<div class='iy-skor'>İY: "+data['ht_score']+"</div>" if data['ht_score'] else ""}
          </div>
        </div>
    """

    # İstatistik
    if s:
        html += f"""
        <div class="stat-grid">
          <div class="stat-item">
            <div class="stat-label">TOP</div>
            <div class="stat-val">
              <span class="{stat_renk(ph,pa,'home')}">{ph}%</span>
              <span style="color:#334155"> – </span>
              <span class="{stat_renk(ph,pa,'away')}">{pa}%</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-label">İSABETLİ ŞUT</div>
            <div class="stat-val">
              <span class="{stat_renk(sh,sa,'home')}">{sh}</span>
              <span style="color:#334155"> – </span>
              <span class="{stat_renk(sh,sa,'away')}">{sa}</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-label">ATAK</div>
            <div class="stat-val">
              <span class="{stat_renk(ah,aa,'home')}">{ah}</span>
              <span style="color:#334155"> – </span>
              <span class="{stat_renk(ah,aa,'away')}">{aa}</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-label">KORNER</div>
            <div class="stat-val">
              <span class="{stat_renk(ch,ca,'home')}">{ch}</span>
              <span style="color:#334155"> – </span>
              <span class="{stat_renk(ch,ca,'away')}">{ca}</span>
            </div>
          </div>
        </div>
        <div style="font-size:10px;color:#475569;margin-bottom:2px">
          Baskı → {data['home'][:12]}: {hb}/100 | {data['away'][:12]}: {ab}/100
        </div>
        <div class="baski-bar"><div class="baski-fill" style="width:{hb}%"></div></div>
        """
    html += "</div>"  # kart-orta

    # Her bookmaker için ayrı oran satırı
    for bm_key in BOOKMAKERS:
        bm = data["bm_oranlar"].get(bm_key,{})
        hl = bm.get("home",0)
        dl = bm.get("draw",0)
        al = bm.get("away",0)
        hc = bm.get("home_chg")
        dc = bm.get("draw_chg")
        ac = bm.get("away_chg")
        etiket = BM_ETIKET.get(bm_key,bm_key)

        if not hl:
            html += f"""
            <div class="oran-bolum">
              <div class="oran-baslik">{etiket}</div>
              <div style="font-size:11px;color:#334155">Oran yok</div>
            </div>"""
            continue

        def kutu(val,chg,lbl):
            rc = oran_renk_cls(chg)
            dc_str = f"<div class='oran-degisim' style='color:{'#22c55e' if chg and chg<0 else '#ef4444' if chg and chg>0 else '#475569'}'>{chg:+.0f}%</div>" if chg is not None else ""
            return f"""<div class="oran-kutu {rc}">
              <div class="oran-label">{lbl}</div>
              <div class="oran-deger {rc}">{val:.2f}</div>
              {dc_str}
            </div>"""

        html += f"""
        <div class="oran-bolum">
          <div class="oran-baslik">{etiket} — Canlı</div>
          <div class="oran-grid">
            {kutu(hl,hc,'1')}
            {kutu(dl,dc,'X')}
            {kutu(al,ac,'2')}
          </div>
        </div>"""

    # Maç öncesi
    hp,dp,ap = data["home_pre"],data["draw_pre"],data["away_pre"]
    if hp or dp or ap:
        html += f"""
        <div class="oran-bolum" style="padding-top:6px">
          <div class="oran-baslik">Maç Öncesi</div>
          <div class="oran-grid">
            <div class="oran-kutu"><div class="oran-label">1</div><div class="oran-deger">{hp if hp else '—'}</div></div>
            <div class="oran-kutu"><div class="oran-label">X</div><div class="oran-deger">{dp if dp else '—'}</div></div>
            <div class="oran-kutu"><div class="oran-label">2</div><div class="oran-deger">{ap if ap else '—'}</div></div>
          </div>
        </div>"""

    # Alt/Üst
    tl = data["totals_live"]
    tg = data["toplam_gol"]
    if tl:
        html += """<div class="oran-bolum"><div class="oran-baslik">Alt / Üst</div><div class="total-grid">"""
        for cizgi in CIZGILER:
            gecti = tg > cizgi
            if gecti:
                html += f"""<div class="total-kutu gecti">
                  <div class="total-cizgi gecti">✅ {cizgi} Üst</div>
                  <div style="font-size:11px;color:#22c55e;margin-top:4px">GEÇTİ</div>
                </div>"""
            elif cizgi in tl:
                ov = tl[cizgi].get("over",0)
                un = tl[cizgi].get("under",0)
                sicak = ov>0 and ov<=1.50
                html += f"""<div class="total-kutu {'sicak' if sicak else ''}">
                  <div class="total-cizgi">{cizgi} Üst</div>
                  <div class="total-over">Ü {ov:.2f}</div>
                  <div class="total-under">A {un:.2f}</div>
                </div>"""
            else:
                html += f"""<div class="total-kutu">
                  <div class="total-cizgi">{cizgi} Üst</div>
                  <div class="total-under" style="margin-top:8px">—</div>
                </div>"""
        html += "</div></div>"

    # Sinyaller
    html += '<div class="sinyal-bolum">'
    for txt,cls in data["signals"]:
        html += f'<div class="sinyal-item {cls}">{txt}</div>'
    html += "</div>"

    html += "</div>"  # mac-karti
    return html

# ── Ana akış ─────────────────────────────────────────────
maclar = getir_canli_maclar()

if not maclar:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#475569">
      <div style="font-size:3rem">⏳</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;margin-top:10px">
        Şu an aktif canlı maç yok
      </div>
      <div style="font-size:13px;margin-top:6px">Akşam 18:00–23:00 arası tekrar dene</div>
    </div>""", unsafe_allow_html=True)
else:
    with st.spinner("Yükleniyor..."):
        odds_dict = getir_odds()
        veriler   = [sinyal_uret(m,odds_dict) for m in maclar]

    veriler.sort(key=lambda x: x["priority"], reverse=True)
    sinyalli = sum(1 for d in veriler if d["priority"]>=2)
    eslesmis = sum(1 for d in veriler if d["eslendi"])

    col1,col2,col3 = st.columns(3)
    with col1: st.metric("🔴 Canlı Maç", len(veriler))
    with col2: st.metric("🟢 Sinyalli", sinyalli)
    with col3: st.metric("📊 Oran Eşleşti", eslesmis)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, data in enumerate(veriler):
        with cols[idx%3]:
            st.markdown(render_kart(data), unsafe_allow_html=True)

col1, col2 = st.columns([1,4])
with col1:
    if st.button("🔄 Yenile"):
        st.cache_data.clear()
        st.rerun()
st.markdown("<div style='font-size:11px;color:#1e2d3d;margin-top:8px'>İstatistik 10sn • Oranlar 15sn • livescore-api + the-odds-api</div>", unsafe_allow_html=True)
