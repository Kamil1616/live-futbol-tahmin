import streamlit as st
import requests
from difflib import SequenceMatcher

st.set_page_config(page_title="Canlı Sinyal", layout="wide", page_icon="⚽")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
* { box-sizing: border-box; }
.stApp {
    background: #06090f;
    background-image: radial-gradient(ellipse at 10% 0%, #0a1a2e 0%, transparent 60%),
                      radial-gradient(ellipse at 90% 100%, #0a1f0e 0%, transparent 60%);
    color: #e2e8f0; font-family: 'Inter', sans-serif;
}
/* KART */
.kart { background: #0d1520; border: 1px solid #1a2535; border-radius: 14px; margin-bottom: 14px; overflow: hidden; }
.kart.sy { border-color: #22c55e; box-shadow: 0 0 24px rgba(34,197,94,0.18); }
.kart.so { border-color: #f97316; box-shadow: 0 0 18px rgba(249,115,22,0.15); }
/* KART ÜST */
.kust { padding: 10px 14px; background: #0a1018; border-bottom: 1px solid #1a2535;
        display: flex; justify-content: space-between; align-items: center; }
.lig  { font-size: 10px; color: #4a6080; letter-spacing: 1px; text-transform: uppercase; }
.dak  { background: #dc2626; color: #fff; font-size: 11px; font-weight: 700;
        padding: 2px 10px; border-radius: 20px; font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.7} }
/* SKOR BÖLÜMÜ */
.sbol { padding: 12px 14px 8px; display: flex; justify-content: space-between; align-items: flex-start; }
.tbl  { flex: 1; }
.tev  { font-family: 'Rajdhani', sans-serif; font-size: 17px; font-weight: 700; color: #f1f5f9; line-height: 1.2; }
.tdep { font-family: 'Rajdhani', sans-serif; font-size: 15px; font-weight: 600; color: #64748b; line-height: 1.2; }
.sblok { text-align: right; }
.skor { font-family: 'Rajdhani', sans-serif; font-size: 32px; font-weight: 700; color: #fff; line-height: 1; }
.iyskor { font-size: 10px; color: #3a5070; margin-top: 2px; }
/* İSTATİSTİK */
.sgrid { display: grid; grid-template-columns: repeat(4,1fr); gap: 5px; padding: 6px 14px; }
.si { background: #08111c; border-radius: 7px; padding: 7px 4px; text-align: center; border: 1px solid #141f2e; }
.sl { font-size: 9px; color: #3a5070; margin-bottom: 3px; letter-spacing: 0.5px; text-transform: uppercase; }
.sv { font-size: 12px; font-weight: 600; }
.ev { color: #22c55e; } .dep { color: #ef4444; } .esit { color: #64748b; }
.brow { padding: 2px 14px 8px; display: flex; gap: 8px; align-items: center; }
.btext { font-size: 10px; color: #3a5070; white-space: nowrap; }
.bbar { flex: 1; height: 3px; background: #1a2535; border-radius: 2px; overflow: hidden; }
.bfill { height: 100%; background: linear-gradient(90deg,#22c55e,#15803d); border-radius: 2px; }
/* BÖLÜM AYRAÇ */
.ayrac { border-top: 1px solid #1a2535; }
.bbol { padding: 8px 14px; }
.bbas { font-size: 9px; color: #3a5070; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px;
        display: flex; align-items: center; gap: 6px; }
.bbas::after { content:''; flex:1; height:1px; background:#1a2535; }
/* ORANLAR */
.ogrid3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 5px; }
.ok { background: #08111c; border: 1px solid #141f2e; border-radius: 7px; padding: 7px 4px; text-align: center; }
.ok.d { background: #071510; border-color: #166534; }
.ok.y { background: #150708; border-color: #991b1b; }
.ol { font-size: 9px; color: #3a5070; margin-bottom: 2px; }
.od { font-size: 14px; font-weight: 700; font-family: 'Rajdhani',sans-serif; color: #e2e8f0; }
.od.d { color: #22c55e; } .od.y { color: #ef4444; }
.oc { font-size: 9px; margin-top: 1px; }
/* ALT/ÜST - karşılaştırmalı tablo */
.total-tablo { width: 100%; border-collapse: collapse; font-size: 12px; }
.total-tablo th { font-size: 9px; color: #3a5070; font-weight: 600; letter-spacing: 1px;
                  text-transform: uppercase; padding: 4px 8px; text-align: center; }
.total-tablo td { padding: 5px 8px; text-align: center; border-top: 1px solid #141f2e; }
.total-tablo .cizgi { font-family: 'Rajdhani',sans-serif; font-weight: 700; color: #64748b; text-align: left; }
.total-tablo .gecti { color: #22c55e; font-weight: 700; }
.total-tablo .oran  { font-family: 'Rajdhani',sans-serif; font-weight: 600; color: #e2e8f0; }
.total-tablo .oran.sicak { color: #eab308; font-weight: 700; }
.total-tablo .oran.dusuk { color: #22c55e; }
/* SİNYAL */
.sinyalb { padding: 8px 14px 12px; border-top: 1px solid #1a2535; }
.sh { background: linear-gradient(135deg,#052e16,#14532d); color: #86efac;
      border: 1px solid #166534; border-radius: 7px; padding: 7px 11px;
      margin-bottom: 4px; font-size: 12px; font-weight: 600; }
.sm { background: linear-gradient(135deg,#1c0a02,#431407); color: #fdba74;
      border: 1px solid #7c2d12; border-radius: 7px; padding: 7px 11px;
      margin-bottom: 4px; font-size: 12px; font-weight: 600; }
.sl2 { background: #080f18; color: #3a5070; border: 1px solid #141f2e;
       border-radius: 7px; padding: 7px 11px; margin-bottom: 4px; font-size: 12px; }
.stButton>button {
    background: linear-gradient(135deg,#1d4ed8,#1e40af) !important;
    color: white !important; border: none !important; border-radius: 9px !important;
    padding: 9px 22px !important; font-weight: 600 !important; letter-spacing: .5px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:14px 0 22px;border-bottom:1px solid #1a2535;margin-bottom:22px">
  <span style="font-size:2.2rem">⚽</span>
  <div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:1.7rem;font-weight:700;letter-spacing:3px;color:#fff;line-height:1">CANLI SİNYAL</div>
    <div style="font-size:10px;color:#3a5070;letter-spacing:2px;margin-top:2px">PINNACLE + MATCHBOOK • CANLI ORAN & İSTATİSTİK</div>
  </div>
</div>
""", unsafe_allow_html=True)

LS_KEY    = "lD0xMVlUGwip7fzY"
LS_SECRET = "C7b6mK3wocmicEDxhD44zqYfWhF3we19"
ODDS_KEY  = "ac0551df534e175a4f312681465cffcc"
LS_BASE   = "https://livescore-api.com/api-client"
ODDS_BASE = "https://api.the-odds-api.com/v4"
MIN_SINYAL = 15
BOOKMAKERS = [("pinnacle","Pinnacle"), ("matchbook","Matchbook")]

@st.cache_data(ttl=60)
def getir_canli_maclar():
    try:
        resp = requests.get(f"{LS_BASE}/matches/live.json?key={LS_KEY}&secret={LS_SECRET}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                return [m for m in ((data.get("data") or {}).get("match") or []) if m.get("status") == "IN PLAY"]
    except: pass
    return []

@st.cache_data(ttl=10)
def getir_stats(match_id):
    try:
        resp = requests.get(f"{LS_BASE}/matches/stats.json?match_id={match_id}&key={LS_KEY}&secret={LS_SECRET}", timeout=8)
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
    Pinnacle: h2h + totals (dinamik çizgiler)
    Matchbook:  h2h only
    """
    url = (f"{ODDS_BASE}/sports/soccer/odds/"
           f"?apiKey={ODDS_KEY}&regions=eu&markets=h2h,totals&oddsFormat=decimal"
           f"&bookmakers=pinnacle,matchbook")
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200: return {}
        sonuc = {}
        for mac in resp.json():
            ht = mac.get("home_team",""); at = mac.get("away_team","")
            mac_data = {}
            for bm in (mac.get("bookmakers") or []):
                bk = bm.get("key","")
                if bk not in [b[0] for b in BOOKMAKERS]: continue
                h2h = {"home":0,"draw":0,"away":0}
                tots = {}  # { point: {"over":x,"under":x} }
                for mkt in (bm.get("markets") or []):
                    mk = mkt.get("key")
                    if mk == "h2h":
                        for o in (mkt.get("outcomes") or []):
                            nm=o.get("name",""); pr=float(o.get("price") or 0)
                            if pr<=0 or pr>500: continue
                            if nm==ht: h2h["home"]=pr
                            elif nm==at: h2h["away"]=pr
                            elif nm=="Draw": h2h["draw"]=pr
                    elif mk == "totals":
                        for o in (mkt.get("outcomes") or []):
                            nm=o.get("name",""); pt=o.get("point"); pr=float(o.get("price") or 0)
                            if pt is None or pr<=0: continue
                            pt=float(pt)
                            if pt not in tots: tots[pt]={"over":0,"under":0}
                            if nm=="Over": tots[pt]["over"]=pr
                            elif nm=="Under": tots[pt]["under"]=pr
                if h2h["home"] or tots:
                    mac_data[bk] = {"h2h":h2h,"totals":tots}
            if mac_data:
                sonuc[f"{ht}|{at}"] = mac_data
        return sonuc
    except: return {}

def benzerlik(a,b): return SequenceMatcher(None,a.lower(),b.lower()).ratio()

def eslestir(home,away,od):
    en,sk=None,0.6
    for k,v in od.items():
        p=k.split("|")
        if len(p)!=2: continue
        s=(benzerlik(home,p[0])+benzerlik(away,p[1]))/2
        if s>sk: sk=s; en=v
    return en

def parse_stat(val):
    try:
        if val is None: return 0,0
        h,a=str(val).split(":"); return int(h),int(a)
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
    if pre and pre>0 and live and live>0: return round((live-pre)/pre*100,1)
    return None

def sr(h,a,t):
    if t=="home": return "ev" if h>a else ("dep" if h<a else "esit")
    return "ev" if a>h else ("dep" if a<h else "esit")

def sinyal_uret(match, od):
    try:
        mid =match.get("id")
        home=(match.get("home") or {}).get("name","Ev Sahibi")
        away=(match.get("away") or {}).get("name","Deplasman")
        scr =(match.get("scores") or {}).get("score","? - ?")
        hts =(match.get("scores") or {}).get("ht_score","")
        mn  =match.get("time","?")
        comp=(match.get("competition") or {}).get("name","")
        cntry=(match.get("country") or {}).get("name","")
        lspre=(match.get("odds") or {}).get("pre") or {}
        hp=float(lspre.get("1") or 0); dp=float(lspre.get("X") or 0); ap=float(lspre.get("2") or 0)

        esl=eslestir(home,away,od)
        bmo={}
        for bk,_ in BOOKMAKERS:
            bd=(esl or {}).get(bk) or {}
            h2h=bd.get("h2h") or {}; tots=bd.get("totals") or {}
            hl=h2h.get("home") or 0; dl=h2h.get("draw") or 0; al=h2h.get("away") or 0
            bmo[bk]={"home":hl,"draw":dl,"away":al,"hc":pct(hp,hl),"dc":pct(dp,dl),"ac":pct(ap,al),"totals":tots}

        # Pinnacle ref
        pin=bmo.get("pinnacle",{})
        hc=pin.get("hc"); ac_=pin.get("ac")
        tl=pin.get("totals") or {}

        mint=parse_min(mn)
        st_d=getir_stats(mid) if mid else {}
        hb=baski(st_d,"home"); ab=baski(st_d,"away")

        try: hg,ag=map(int,scr.replace(" ","").split("-")); tg=hg+ag
        except: hg=ag=tg=0

        sigs=[]; pri=0

        if mint<MIN_SINYAL:
            sigs.append(("Sinyal yok","sl2"))
        else:
            # Totals sinyali
            for cz,ou in sorted(tl.items()):
                ov=ou.get("over") or 0
                if not ov or tg>cz: continue
                if ov<=1.25:
                    sigs.append((f"🔥 {cz} Üst {ov:.2f} — Gol çok yakın! ({mint}. dak.)","sh")); pri=max(pri,3)
                elif ov<=1.45:
                    sigs.append((f"⚡ {cz} Üst {ov:.2f} — Gol beklentisi yüksek ({mint}. dak.)","sm")); pri=max(pri,2)
                elif ov<=1.65 and mint>=60:
                    sigs.append((f"📊 {cz} Üst {ov:.2f} — Takip et ({mint}. dak.)","sm")); pri=max(pri,2)

            # 1X2 oran düşüşü
            hl2=pin.get("home") or 0; al2=pin.get("away") or 0
            if hc is not None and hc<=-20:
                sigs.append((f"🔥 Ev sahibi oranı sert düştü: {hp:.2f}→{hl2:.2f} ({hc:+.1f}%)","sh")); pri=max(pri,3)
            elif hc is not None and hc<=-10:
                sigs.append((f"📉 Ev sahibi oranı düştü: {hp:.2f}→{hl2:.2f} ({hc:+.1f}%)","sm")); pri=max(pri,2)
            if ac_ is not None and ac_<=-20:
                sigs.append((f"🔥 Deplasman oranı sert düştü: {ap:.2f}→{al2:.2f} ({ac_:+.1f}%)","sh")); pri=max(pri,3)
            elif ac_ is not None and ac_<=-10:
                sigs.append((f"📉 Deplasman oranı düştü: {ap:.2f}→{al2:.2f} ({ac_:+.1f}%)","sm")); pri=max(pri,2)

            # Baskı
            if hb>=60:
                if hc is not None and hc<=-7:
                    sigs.append((f"🔥 Ev sahibi baskı ({hb}/100) + oran düştü → GÜÇLÜ SİNYAL","sh")); pri=max(pri,3)
                elif mint>=60:
                    sigs.append((f"⚡ Ev sahibi baskı yapıyor ({hb}/100) — {mint}. dak.","sm")); pri=max(pri,2)
            if ab>=60:
                if ac_ is not None and ac_<=-7:
                    sigs.append((f"🔥 Deplasman baskı ({ab}/100) + oran düştü → GÜÇLÜ SİNYAL","sh")); pri=max(pri,3)
                elif mint>=60:
                    sigs.append((f"⚡ Deplasman baskı yapıyor ({ab}/100) — {mint}. dak.","sm")); pri=max(pri,2)

            # Golsüz
            if tg==0:
                if mint>=80: sigs.append(("🔥 80+ dak. GOLSÜZ — Güçlü gol beklentisi","sh")); pri=max(pri,3)
                elif mint>=70: sigs.append(("⚡ 70+ dak. golsüz — Gol sinyali","sm")); pri=max(pri,2)
                elif mint>=15: sigs.append((f"📊 {mint}. dak. golsüz","sl2")); pri=max(pri,1)

            # Geride + baskı
            if hg<ag and hb>=55 and mint>=45:
                sigs.append((f"🔄 Ev sahibi geride ({scr}) + baskı ({hb}/100)","sm")); pri=max(pri,2)
            if ag<hg and ab>=55 and mint>=45:
                sigs.append((f"🔄 Deplasman geride ({scr}) + baskı ({ab}/100)","sm")); pri=max(pri,2)

            if not sigs: sigs.append(("Sinyal yok","sl2"))

        return dict(home=home,away=away,score=scr,ht_score=hts,minute=mn,
                    comp=comp,country=cntry,sigs=sigs,pri=pri,stats=st_d,
                    hb=hb,ab=ab,hp=hp,dp=dp,ap=ap,bmo=bmo,tl=tl,tg=tg,esl=esl is not None)
    except Exception as e:
        return dict(home="?",away="?",score="?",ht_score="",minute="?",comp="",country="",
                    sigs=[(f"Hata:{e}","sl2")],pri=0,stats={},hb=0,ab=0,hp=0,dp=0,ap=0,
                    bmo={},tl={},tg=0,esl=False)

def ok_html(val, chg, lbl):
    rc = "d" if (chg is not None and chg<=-6) else "y" if (chg is not None and chg>=6) else ""
    chg_html = ""
    if chg is not None:
        clr = "#22c55e" if chg<0 else "#ef4444"
        chg_html = f'<div class="oc" style="color:{clr}">{chg:+.0f}%</div>'
    return f'<div class="ok {rc}"><div class="ol">{lbl}</div><div class="od {rc}">{val:.2f}</div>{chg_html}</div>'

def render(d):
    kls = "kart" + (" sy" if d["pri"]>=3 else " so" if d["pri"]==2 else "")
    ph,pa=parse_stat(d["stats"].get("possesion")) if d["stats"] else (0,0)
    sh,sa=parse_stat(d["stats"].get("shots_on_target")) if d["stats"] else (0,0)
    ah,aa=parse_stat(d["stats"].get("attempts_on_goal")) if d["stats"] else (0,0)
    ch,ca=parse_stat(d["stats"].get("corners")) if d["stats"] else (0,0)

    p = []
    p.append(f'<div class="{kls}">')

    # Üst bar
    p.append(f'<div class="kust"><span class="lig">🔴 {d["comp"]} • {d["country"]}</span><span class="dak">{d["minute"]}</span></div>')

    # Skor
    iytxt = f'<div class="iyskor">İY: {d["ht_score"]}</div>' if d["ht_score"] else ""
    p.append(f'''<div class="sbol">
<div class="tbl"><div class="tev">{d["home"]}</div><div class="tdep">vs {d["away"]}</div></div>
<div class="sblok"><div class="skor">{d["score"]}</div>{iytxt}</div>
</div>''')

    # İstatistik
    if d["stats"]:
        p.append(f'''<div class="sgrid">
<div class="si"><div class="sl">TOP</div><div class="sv"><span class="{sr(ph,pa,'home')}">{ph}%</span><span style="color:#1a2535"> – </span><span class="{sr(ph,pa,'away')}">{pa}%</span></div></div>
<div class="si"><div class="sl">İSABETLİ ŞUT</div><div class="sv"><span class="{sr(sh,sa,'home')}">{sh}</span><span style="color:#1a2535"> – </span><span class="{sr(sh,sa,'away')}">{sa}</span></div></div>
<div class="si"><div class="sl">ATAK</div><div class="sv"><span class="{sr(ah,aa,'home')}">{ah}</span><span style="color:#1a2535"> – </span><span class="{sr(ah,aa,'away')}">{aa}</span></div></div>
<div class="si"><div class="sl">KORNER</div><div class="sv"><span class="{sr(ch,ca,'home')}">{ch}</span><span style="color:#1a2535"> – </span><span class="{sr(ch,ca,'away')}">{ca}</span></div></div>
</div>
<div class="brow">
<span class="btext">{d["home"][:12]} {d["hb"]}/100</span>
<div class="bbar"><div class="bfill" style="width:{d['hb']}%"></div></div>
<span class="btext">{d["ab"]}/100 {d["away"][:12]}</span>
</div>''')

    # Pinnacle + Matchbook 1X2 karşılaştırmalı
    p.append('<div class="ayrac"></div><div class="bbol">')
    p.append('<div class="bbas">1X2 — Canlı Oranlar</div>')
    p.append('<div class="ogrid3">')
    p.append(f'<div class="ok" style="background:#06080d;border-color:#0f1a2a"><div class="ol">—</div><div class="od" style="font-size:10px;color:#22c55e">Pinnacle</div></div>')
    p.append(f'<div class="ok" style="background:#06080d;border-color:#0f1a2a"><div class="ol">—</div><div class="od" style="font-size:10px;color:#f97316">Matchbook</div></div>')
    p.append(f'<div class="ok" style="background:#06080d;border-color:#0f1a2a"><div class="ol">—</div><div class="od" style="font-size:10px;color:#64748b">Öncesi</div></div>')
    p.append('</div>')

    for lbl, idx in [("1","home"),("X","draw"),("2","away")]:
        pv = d["bmo"].get("pinnacle",{}).get(idx,0)
        bv = d["bmo"].get("matchbook",{}).get(idx,0)
        pc_ = d["bmo"].get("pinnacle",{}).get(f"{idx[0]}c" if idx!="draw" else "dc", None)
        # fix: get correct chg key
        chg_map = {"home":"hc","draw":"dc","away":"ac"}
        pc_ = d["bmo"].get("pinnacle",{}).get(chg_map[idx], None)
        bc_ = d["bmo"].get("matchbook",{}).get(chg_map[idx], None)
        pre = d["hp"] if idx=="home" else (d["dp"] if idx=="draw" else d["ap"])

        prc = "d" if (pc_ and pc_<=-6) else "y" if (pc_ and pc_>=6) else ""
        brc = "d" if (bc_ and bc_<=-6) else "y" if (bc_ and bc_>=6) else ""
        pc_txt = f'<div class="oc" style="color:{"#22c55e" if pc_ and pc_<0 else "#ef4444"}">{pc_:+.0f}%</div>' if pc_ is not None else ""
        bc_txt = f'<div class="oc" style="color:{"#22c55e" if bc_ and bc_<0 else "#ef4444"}">{bc_:+.0f}%</div>' if bc_ is not None else ""

        pv_str = f"{pv:.2f}" if pv else "—"
        bv_str = f"{bv:.2f}" if bv else "—"
        pre_str = f"{pre:.2f}" if pre else "—"
        p.append(f'<div class="ogrid3" style="margin-top:4px">')
        p.append(f'<div class="ok {prc}"><div class="ol">{lbl} — PIN</div><div class="od {prc}">{pv_str}</div>{pc_txt}</div>')
        p.append(f'<div class="ok {brc}"><div class="ol">{lbl} — MB</div><div class="od {brc}">{bv_str}</div>{bc_txt}</div>')
        p.append(f'<div class="ok"><div class="ol">{lbl} — Öncesi</div><div class="od">{pre_str}</div></div>')
        p.append('</div>')

    p.append('</div>')  # bbol

    # Alt/Üst (Pinnacle dinamik çizgiler)
    if d["tl"]:
        p.append('<div class="ayrac"></div><div class="bbol">')
        p.append('<div class="bbas">Alt / Üst — Pinnacle</div>')
        p.append('<table class="total-tablo"><thead><tr><th style="text-align:left">Çizgi</th><th>Üst</th><th>Alt</th><th>Durum</th></tr></thead><tbody>')
        for cz in sorted(d["tl"].keys()):
            ov = d["tl"][cz].get("over",0)
            un = d["tl"][cz].get("under",0)
            gecti = d["tg"] > cz
            if gecti:
                p.append(f'<tr><td class="cizgi gecti">✅ {cz}</td><td class="oran gecti">GEÇTİ</td><td>—</td><td class="gecti">✓</td></tr>')
            else:
                oc = "sicak" if ov<=1.50 else ("dusuk" if ov<=1.70 else "")
                p.append(f'<tr><td class="cizgi">{cz} Üst</td><td class="oran {oc}">{ov:.2f}</td><td class="oran">{un:.2f}</td><td style="font-size:10px;color:#3a5070">Açık</td></tr>')
        p.append('</tbody></table></div>')

    # Sinyaller
    p.append('<div class="sinyalb">')
    for txt,cls in d["sigs"]:
        p.append(f'<div class="{cls}">{txt}</div>')
    p.append('</div>')

    p.append('</div>')
    return "".join(p)

# ── Ana akış ─────────────────────────────────────────────
maclar = getir_canli_maclar()

if not maclar:
    st.markdown('<div style="text-align:center;padding:60px;color:#3a5070"><div style="font-size:3rem">⏳</div><div style="font-family:Rajdhani,sans-serif;font-size:1.4rem;margin-top:10px;color:#64748b">Şu an canlı maç yok</div><div style="font-size:12px;margin-top:6px">Akşam 18:00–23:00 arası tekrar dene</div></div>', unsafe_allow_html=True)
else:
    with st.spinner("Yükleniyor..."):
        odds_dict = getir_odds()
        veriler   = [sinyal_uret(m,odds_dict) for m in maclar]

    veriler.sort(key=lambda x: x["pri"], reverse=True)
    sinyalli=sum(1 for d in veriler if d["pri"]>=2)
    eslesmis=sum(1 for d in veriler if d["esl"])

    c1,c2,c3=st.columns(3)
    c1.metric("🔴 Canlı Maç",len(veriler))
    c2.metric("🟢 Sinyalli",sinyalli)
    c3.metric("📊 Oran Eşleşti",eslesmis)
    st.markdown("<br>",unsafe_allow_html=True)

    cols=st.columns(3)
    for i,d in enumerate(veriler):
        with cols[i%3]:
            st.markdown(render(d), unsafe_allow_html=True)

if st.button("🔄 Yenile"):
    st.cache_data.clear()
    st.rerun()
st.markdown('<div style="font-size:10px;color:#1a2535;margin-top:8px">İstatistik 10sn • Oranlar 15sn • livescore-api + the-odds-api (Pinnacle+Matchbook)</div>', unsafe_allow_html=True)
