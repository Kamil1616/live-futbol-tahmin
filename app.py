import streamlit as st
import requests
from difflib import SequenceMatcher

st.set_page_config(page_title="Canlı Sinyal", layout="wide", page_icon="⚽")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
* { box-sizing: border-box; }
.stApp {
    background: #080c12;
    background-image: radial-gradient(ellipse at 20% 0%, #0d2137 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 100%, #091a0e 0%, transparent 50%);
    color: #e2e8f0; font-family: 'Inter', sans-serif;
}
.mac-karti {
    background: linear-gradient(135deg, #0f1923 0%, #111d2b 100%);
    border: 1px solid #1e2d3d; border-radius: 16px;
    margin-bottom: 16px; overflow: hidden;
}
.mac-karti.sy { border-color: #22c55e; box-shadow: 0 0 20px rgba(34,197,94,0.2); }
.mac-karti.so { border-color: #f97316; box-shadow: 0 0 16px rgba(249,115,22,0.15); }
.kust { padding: 12px 16px 10px; border-bottom: 1px solid #1e2d3d;
        display: flex; justify-content: space-between; align-items: center; }
.lig { font-size: 11px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; }
.dak { background: #ef4444; color: white; font-size: 11px; font-weight: 700;
       padding: 2px 10px; border-radius: 20px; font-family: 'Rajdhani', sans-serif; }
.korta { padding: 12px 16px; }
.tadi { font-family: 'Rajdhani', sans-serif; font-size: 18px; font-weight: 700; color: #f1f5f9; }
.tadi2 { font-family: 'Rajdhani', sans-serif; font-size: 16px; font-weight: 600; color: #64748b; }
.skor { font-family: 'Rajdhani', sans-serif; font-size: 30px; font-weight: 700; color: #fff; }
.iyskor { font-size: 11px; color: #475569; text-align: right; }
.sgrid { display: grid; grid-template-columns: repeat(4,1fr); gap: 6px; margin: 10px 0 6px; }
.si { background: #0a1520; border-radius: 8px; padding: 8px 4px; text-align: center; }
.sl { font-size: 9px; color: #475569; margin-bottom: 3px; letter-spacing: 0.5px; }
.sv { font-size: 13px; font-weight: 600; }
.ev { color: #22c55e; } .dep { color: #ef4444; } .esit { color: #94a3b8; }
.bbar { height: 3px; background: #1e2d3d; border-radius: 2px; margin: 4px 0 2px; overflow: hidden; }
.bfill { height: 100%; background: linear-gradient(90deg,#22c55e,#16a34a); border-radius: 2px; }
.btext { font-size: 10px; color: #334155; margin-bottom: 4px; }
.obol { padding: 10px 16px; border-top: 1px solid #1e2d3d; }
.obas { font-size: 10px; color: #475569; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; }
.ogrid { display: grid; grid-template-columns: repeat(3,1fr); gap: 6px; }
.ok { background: #0a1520; border-radius: 8px; padding: 8px 4px; text-align: center; border: 1px solid #1e2d3d; }
.ok.d { background: #0d2010; border-color: #22c55e; }
.ok.y { background: #200d0d; border-color: #ef4444; }
.ol { font-size: 10px; color: #475569; }
.od { font-size: 15px; font-weight: 700; font-family: 'Rajdhani',sans-serif; color: #f1f5f9; }
.od.d { color: #22c55e; } .od.y { color: #ef4444; }
.oc { font-size: 10px; margin-top: 1px; }
.tgrid { display: grid; grid-template-columns: repeat(3,1fr); gap: 6px; margin-top: 6px; }
.tk { background: #0a1520; border-radius: 8px; padding: 8px 6px; text-align: center; border: 1px solid #1e2d3d; }
.tk.g { background: #0d2010; border-color: #22c55e; }
.tk.s { background: #1a1200; border-color: #eab308; }
.tc { font-size: 12px; font-weight: 700; font-family: 'Rajdhani',sans-serif; color: #64748b; }
.tc.g { color: #22c55e; }
.to { font-size: 14px; font-weight: 700; color: #f1f5f9; margin: 2px 0; }
.tu { font-size: 10px; color: #475569; }
.sbol { padding: 10px 16px 14px; border-top: 1px solid #1e2d3d; }
.sh { background: linear-gradient(135deg,#14532d,#166534); color: #86efac;
      border: 1px solid #22c55e; border-radius: 8px; padding: 8px 12px;
      margin-bottom: 5px; font-size: 13px; font-weight: 600; }
.sm { background: linear-gradient(135deg,#431407,#7c2d12); color: #fdba74;
      border: 1px solid #f97316; border-radius: 8px; padding: 8px 12px;
      margin-bottom: 5px; font-size: 13px; font-weight: 600; }
.sl2 { background: #0f172a; color: #475569; border: 1px solid #1e293b;
       border-radius: 8px; padding: 8px 12px; margin-bottom: 5px; font-size: 13px; }
.stButton>button {
    background: linear-gradient(135deg,#1d4ed8,#1e40af) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 10px 24px !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;align-items:center;gap:10px;padding:12px 0 20px;border-bottom:1px solid #1e2d3d;margin-bottom:20px">
  <span style="font-size:2rem">⚽</span>
  <div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:1.6rem;font-weight:700;letter-spacing:2px;color:#fff">CANLI SİNYAL</div>
    <div style="font-size:11px;color:#475569;letter-spacing:1px">Pinnacle + Betfair • Canlı Oran ve İstatistik</div>
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
BOOKMAKERS = [("pinnacle","Pinnacle"), ("betfair_ex_eu","Betfair")]

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
    except: pass
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
    url = (f"{ODDS_BASE}/sports/soccer/odds/"
           f"?apiKey={ODDS_KEY}&regions=eu&markets=h2h,totals&oddsFormat=decimal"
           f"&bookmakers=pinnacle,betfair_ex_eu")
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200: return {}
        sonuc = {}
        for mac in resp.json():
            ht = mac.get("home_team","")
            at = mac.get("away_team","")
            bms = mac.get("bookmakers") or []
            if not bms: continue
            mac_data = {}
            for bm in bms:
                bk = bm.get("key","")
                if bk not in [b[0] for b in BOOKMAKERS]: continue
                h2h = {"home":0,"draw":0,"away":0}
                tots = {}
                for mkt in (bm.get("markets") or []):
                    mk = mkt.get("key")
                    if mk == "h2h":
                        for o in (mkt.get("outcomes") or []):
                            nm = o.get("name",""); pr = float(o.get("price") or 0)
                            if pr<=0 or pr>500: continue
                            if nm==ht: h2h["home"]=pr
                            elif nm==at: h2h["away"]=pr
                            elif nm=="Draw": h2h["draw"]=pr
                    elif mk == "totals":
                        for o in (mkt.get("outcomes") or []):
                            nm = o.get("name",""); pt = o.get("point"); pr = float(o.get("price") or 0)
                            if pt is None or pr<=0: continue
                            pt = float(pt)
                            if pt not in CIZGILER: continue
                            if pt not in tots: tots[pt] = {"over":0,"under":0}
                            if nm=="Over": tots[pt]["over"]=pr
                            elif nm=="Under": tots[pt]["under"]=pr
                if h2h["home"] or tots:
                    mac_data[bk] = {"h2h":h2h,"totals":tots}
            if mac_data:
                sonuc[f"{ht}|{at}"] = mac_data
        return sonuc
    except: return {}

def benzerlik(a,b):
    return SequenceMatcher(None,a.lower(),b.lower()).ratio()

def eslestir(home,away,odds_dict):
    en,sk = None, 0.6
    for k,v in odds_dict.items():
        p = k.split("|")
        if len(p)!=2: continue
        s = (benzerlik(home,p[0])+benzerlik(away,p[1]))/2
        if s>sk: sk=s; en=v
    return en

def parse_stat(val):
    try:
        if val is None: return 0,0
        h,a = str(val).split(":")
        return int(h),int(a)
    except: return 0,0

def parse_min(m):
    try: return int(str(m).replace("+"," ").split()[0])
    except: return 0

def baski(stats,taraf):
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

def sr(h,a,t):
    if t=="home": return "ev" if h>a else ("dep" if h<a else "esit")
    return "ev" if a>h else ("dep" if a<h else "esit")

def sinyal_uret(match, odds_dict):
    try:
        mid  = match.get("id")
        home = (match.get("home") or {}).get("name","Ev Sahibi")
        away = (match.get("away") or {}).get("name","Deplasman")
        scr  = (match.get("scores") or {}).get("score","? - ?")
        hts  = (match.get("scores") or {}).get("ht_score","")
        mn   = match.get("time","?")
        comp = (match.get("competition") or {}).get("name","")
        cntry= (match.get("country") or {}).get("name","")
        lspre= (match.get("odds") or {}).get("pre") or {}
        hp   = float(lspre.get("1") or 0)
        dp   = float(lspre.get("X") or 0)
        ap   = float(lspre.get("2") or 0)

        esl  = eslestir(home,away,odds_dict)
        bmo  = {}
        for bk,_ in BOOKMAKERS:
            bd   = (esl or {}).get(bk) or {}
            h2h  = bd.get("h2h") or {}
            tots = bd.get("totals") or {}
            hl=h2h.get("home") or 0; dl=h2h.get("draw") or 0; al=h2h.get("away") or 0
            bmo[bk] = {"home":hl,"draw":dl,"away":al,
                       "hc":pct(hp,hl),"dc":pct(dp,dl),"ac":pct(ap,al),"totals":tots}

        # Sinyal için Pinnacle ref
        pin = bmo.get("pinnacle",{})
        hc  = pin.get("hc"); ac = pin.get("ac")
        tl  = pin.get("totals") or {}
        if not tl:
            for bk,_ in BOOKMAKERS:
                if bmo[bk].get("totals"): tl=bmo[bk]["totals"]; break

        mint = parse_min(mn)
        st_d = getir_stats(mid) if mid else {}
        hb   = baski(st_d,"home"); ab = baski(st_d,"away")

        try:
            hg,ag = map(int,scr.replace(" ","").split("-")); tg=hg+ag
        except: hg=ag=tg=0

        sigs=[]; pri=0

        if mint < MIN_SINYAL:
            sigs.append(("Sinyal yok","sl2"))
        else:
            for cz in CIZGILER:
                if cz not in tl or tg>cz: continue
                ov = tl[cz].get("over") or 0
                if not ov: continue
                if ov<=1.25:
                    sigs.append((f"🔥 {cz} Üst {ov:.2f} — Gol çok yakın! ({mint}. dak.)","sh"))
                    pri=max(pri,3)
                elif ov<=1.45:
                    sigs.append((f"⚡ {cz} Üst {ov:.2f} — Gol beklentisi yüksek ({mint}. dak.)","sm"))
                    pri=max(pri,2)
                elif ov<=1.65 and mint>=60:
                    sigs.append((f"📊 {cz} Üst {ov:.2f} — Takip et ({mint}. dak.)","sm"))
                    pri=max(pri,2)

            hl2=pin.get("home") or 0; al2=pin.get("away") or 0
            if hc is not None and hc<=-20:
                sigs.append((f"🔥 Ev sahibi oranı sert düştü: {hp:.2f} → {hl2:.2f} ({hc:+.1f}%)","sh")); pri=max(pri,3)
            elif hc is not None and hc<=-10:
                sigs.append((f"📉 Ev sahibi oranı düştü: {hp:.2f} → {hl2:.2f} ({hc:+.1f}%)","sm")); pri=max(pri,2)
            if ac is not None and ac<=-20:
                sigs.append((f"🔥 Deplasman oranı sert düştü: {ap:.2f} → {al2:.2f} ({ac:+.1f}%)","sh")); pri=max(pri,3)
            elif ac is not None and ac<=-10:
                sigs.append((f"📉 Deplasman oranı düştü: {ap:.2f} → {al2:.2f} ({ac:+.1f}%)","sm")); pri=max(pri,2)

            if hb>=60:
                if hc is not None and hc<=-7:
                    sigs.append((f"🔥 Ev sahibi baskı ({hb}/100) + oran düştü → GÜÇLÜ SİNYAL","sh")); pri=max(pri,3)
                elif mint>=60:
                    sigs.append((f"⚡ Ev sahibi baskı yapıyor ({hb}/100) — {mint}. dak.","sm")); pri=max(pri,2)
            if ab>=60:
                if ac is not None and ac<=-7:
                    sigs.append((f"🔥 Deplasman baskı ({ab}/100) + oran düştü → GÜÇLÜ SİNYAL","sh")); pri=max(pri,3)
                elif mint>=60:
                    sigs.append((f"⚡ Deplasman baskı yapıyor ({ab}/100) — {mint}. dak.","sm")); pri=max(pri,2)

            if tg==0:
                if mint>=80: sigs.append(("🔥 80+ dak. GOLSÜZ — Güçlü gol beklentisi","sh")); pri=max(pri,3)
                elif mint>=70: sigs.append(("⚡ 70+ dak. golsüz — Gol sinyali","sm")); pri=max(pri,2)
                elif mint>=15: sigs.append((f"📊 {mint}. dak. golsüz","sl2")); pri=max(pri,1)

            if hg<ag and hb>=55 and mint>=45:
                sigs.append((f"🔄 Ev sahibi geride ({scr}) + baskı ({hb}/100)","sm")); pri=max(pri,2)
            if ag<hg and ab>=55 and mint>=45:
                sigs.append((f"🔄 Deplasman geride ({scr}) + baskı ({ab}/100)","sm")); pri=max(pri,2)

            if not sigs: sigs.append(("Sinyal yok","sl2"))

        return dict(home=home,away=away,score=scr,ht_score=hts,minute=mn,
                    comp=comp,country=cntry,sigs=sigs,pri=pri,stats=st_d,
                    hb=hb,ab=ab,hp=hp,dp=dp,ap=ap,bmo=bmo,tl=tl,tg=tg,
                    esl=esl is not None)
    except Exception as e:
        return dict(home="?",away="?",score="?",ht_score="",minute="?",
                    comp="",country="",sigs=[(f"Hata:{e}","sl2")],pri=0,
                    stats={},hb=0,ab=0,hp=0,dp=0,ap=0,bmo={},tl={},tg=0,esl=False)

def render(d):
    kls = "mac-karti" + (" sy" if d["pri"]>=3 else " so" if d["pri"]==2 else "")
    ph,pa=parse_stat(d["stats"].get("possesion")) if d["stats"] else (0,0)
    sh,sa=parse_stat(d["stats"].get("shots_on_target")) if d["stats"] else (0,0)
    ah,aa=parse_stat(d["stats"].get("attempts_on_goal")) if d["stats"] else (0,0)
    ch,ca=parse_stat(d["stats"].get("corners")) if d["stats"] else (0,0)

    # Kart üst
    parts = [f'<div class="{kls}">']
    parts.append(f'<div class="kust"><span class="lig">🔴 {d["comp"]} • {d["country"]}</span><span class="dak">{d["minute"]}</span></div>')

    # Orta
    iytxt = f'<div class="iyskor">İY: {d["ht_score"]}</div>' if d["ht_score"] else ""
    parts.append(f'''<div class="korta">
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div><div class="tadi">{d["home"]}</div><div class="tadi2">vs {d["away"]}</div></div>
  <div style="text-align:right"><div class="skor">{d["score"]}</div>{iytxt}</div>
</div>''')

    # İstatistik
    if d["stats"]:
        parts.append(f'''<div class="sgrid">
<div class="si"><div class="sl">TOP</div><div class="sv"><span class="{sr(ph,pa,"home")}">{ph}%</span><span style="color:#334155"> – </span><span class="{sr(ph,pa,"away")}">{pa}%</span></div></div>
<div class="si"><div class="sl">İSABETLİ ŞUT</div><div class="sv"><span class="{sr(sh,sa,"home")}">{sh}</span><span style="color:#334155"> – </span><span class="{sr(sh,sa,"away")}">{sa}</span></div></div>
<div class="si"><div class="sl">ATAK</div><div class="sv"><span class="{sr(ah,aa,"home")}">{ah}</span><span style="color:#334155"> – </span><span class="{sr(ah,aa,"away")}">{aa}</span></div></div>
<div class="si"><div class="sl">KORNER</div><div class="sv"><span class="{sr(ch,ca,"home")}">{ch}</span><span style="color:#334155"> – </span><span class="{sr(ch,ca,"away")}">{ca}</span></div></div>
</div>
<div class="btext">Baskı → {d["home"][:13]}: {d["hb"]}/100 | {d["away"][:13]}: {d["ab"]}/100</div>
<div class="bbar"><div class="bfill" style="width:{d["hb"]}%"></div></div>''')

    parts.append("</div>")  # korta

    # Bookmaker oranları
    for bk, betiket in BOOKMAKERS:
        bm = d["bmo"].get(bk, {})
        hl = bm.get("home", 0); dl = bm.get("draw", 0); al = bm.get("away", 0)
        hc = bm.get("hc"); dc = bm.get("dc"); ac = bm.get("ac")

        parts.append(f'<div class="obol"><div class="obas">{betiket} — Canlı</div>')
        if not hl:
            parts.append('<div style="font-size:11px;color:#334155;padding-bottom:4px">Oran yok</div>')
        else:
            def ok_html(val, chg, lbl):
                rc = "d" if (chg is not None and chg<=-6) else "y" if (chg is not None and chg>=6) else ""
                chg_html = ""
                if chg is not None:
                    clr = "#22c55e" if chg<0 else "#ef4444"
                    chg_html = f'<div class="oc" style="color:{clr}">{chg:+.0f}%</div>'
                return f'<div class="ok {rc}"><div class="ol">{lbl}</div><div class="od {rc}">{val:.2f}</div>{chg_html}</div>'

            parts.append(f'<div class="ogrid">{ok_html(hl,hc,"1")}{ok_html(dl,dc,"X")}{ok_html(al,ac,"2")}</div>')
        parts.append("</div>")

    # Maç öncesi
    if d["hp"] or d["dp"] or d["ap"]:
        hp_s = f'{d["hp"]:.2f}' if d["hp"] else "—"
        dp_s = f'{d["dp"]:.2f}' if d["dp"] else "—"
        ap_s = f'{d["ap"]:.2f}' if d["ap"] else "—"
        parts.append(f'''<div class="obol"><div class="obas">Maç Öncesi</div>
<div class="ogrid">
<div class="ok"><div class="ol">1</div><div class="od">{hp_s}</div></div>
<div class="ok"><div class="ol">X</div><div class="od">{dp_s}</div></div>
<div class="ok"><div class="ol">2</div><div class="od">{ap_s}</div></div>
</div></div>''')

    # Alt/Üst
    if d["tl"]:
        tg = d["tg"]
        parts.append('<div class="obol"><div class="obas">Alt / Üst</div><div class="tgrid">')
        for cz in CIZGILER:
            gecti = tg > cz
            if gecti:
                parts.append(f'<div class="tk g"><div class="tc g">✅ {cz} Üst</div><div style="font-size:11px;color:#22c55e;margin-top:4px">GEÇTİ</div></div>')
            elif cz in d["tl"]:
                ov = d["tl"][cz].get("over", 0)
                un = d["tl"][cz].get("under", 0)
                sc = "s" if (ov>0 and ov<=1.50) else ""
                parts.append(f'<div class="tk {sc}"><div class="tc">{cz} Üst</div><div class="to">Ü {ov:.2f}</div><div class="tu">A {un:.2f}</div></div>')
            else:
                parts.append(f'<div class="tk"><div class="tc">{cz} Üst</div><div class="tu" style="margin-top:8px">—</div></div>')
        parts.append("</div></div>")

    # Sinyaller
    parts.append('<div class="sbol">')
    for txt, cls in d["sigs"]:
        parts.append(f'<div class="{cls}">{txt}</div>')
    parts.append("</div>")

    parts.append("</div>")
    return "".join(parts)

# ── Ana akış ─────────────────────────────────────────────
maclar = getir_canli_maclar()

if not maclar:
    st.markdown('<div style="text-align:center;padding:60px;color:#475569"><div style="font-size:3rem">⏳</div><div style="font-family:Rajdhani,sans-serif;font-size:1.3rem;margin-top:10px">Şu an canlı maç yok</div><div style="font-size:13px;margin-top:6px">Akşam 18:00–23:00 arası tekrar dene</div></div>', unsafe_allow_html=True)
else:
    with st.spinner("Yükleniyor..."):
        odds_dict = getir_odds()
        veriler   = [sinyal_uret(m, odds_dict) for m in maclar]

    veriler.sort(key=lambda x: x["pri"], reverse=True)
    sinyalli = sum(1 for d in veriler if d["pri"]>=2)
    eslesmis = sum(1 for d in veriler if d["esl"])

    c1,c2,c3 = st.columns(3)
    c1.metric("🔴 Canlı Maç", len(veriler))
    c2.metric("🟢 Sinyalli", sinyalli)
    c3.metric("📊 Oran Eşleşti", eslesmis)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, d in enumerate(veriler):
        with cols[i%3]:
            st.markdown(render(d), unsafe_allow_html=True)

if st.button("🔄 Yenile"):
    st.cache_data.clear()
    st.rerun()
st.markdown('<div style="font-size:11px;color:#1e2d3d;margin-top:8px">İstatistik 10sn • Oranlar 15sn • livescore-api + the-odds-api</div>', unsafe_allow_html=True)
