# -*- coding: utf-8 -*-
"""카드 중개 메타 수집기 (API/SSR 직접 호출 + 일일 변경감지).
- 운영: GitHub Actions에서 requests로 각 플랫폼 호출 → meta.db 적재 → JSON export.
- 데모: --demo (네트워크 없이 주입 데이터로 변경감지 시연).
원칙: 사실 데이터(상품ID·리워드 금액·기간)만 저장. 소개 문구 미저장.
"""
import os, re, sqlite3, json, datetime, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)                          # 용각류 모듈(같은 폴더) import 보장
DB = os.path.join(BASE, "meta.db")
PLATFORMS = {"toss":"토스 카드라운지","cardgorilla":"카드고릴라","banksalad":"뱅크샐러드","ajungdang":"아정당"}

# 카드고릴라 카드사별 캐시백 이벤트 그룹 페이지 ID(웹사이트 /event/detail/{id} 라우팅·작은 고정 id). API 이벤트 idx와 다른 id 공간.
CG_GROUP={"삼성카드":"1","신한카드":"2","KB국민카드":"3","롯데카드":"4","우리카드":"5","현대카드":"7","하나카드":"8","NH농협카드":"9","IBK기업은행":"10"}

def plat_url(plat, pid):
    """플랫폼 product id로 실제 카드/이벤트 랜딩 URL 생성(검증된 패턴).
    네이버는 id만으로 못 만들어(카드사·발급사 필요) 별도 url을 그대로 사용."""
    pid=str(pid or "").strip()
    if not pid: return None
    return {
        "cardgorilla": "https://www.card-gorilla.com/card/detail/"+pid,   # /event/detail은 빈 허브 → /card/detail
        "banksalad":   "https://www.banksalad.com/product/cards/"+pid,
        "toss":        "https://card-lounge.toss.im/card/"+pid,
        "ajungdang":   "https://www.ajd.co.kr/card/event/detail/"+pid,
    }.get(plat)

# ── 용각류 파서 모듈 분리(2026-06): 공통=cardutil / 플랫폼별 파서 ──
from cardutil import _nk, parse_won, _fmt_man, is_june2026, parse_breakdown   # 공통 유틸
from brachio import parse_cardgorilla                        # 카드고릴라
from apato import parse_banksalad                            # 뱅크샐러드
from diplo import parse_toss                                 # 토스
from bronto import parse_ajd_rsc                             # 아정당
from mamenchi import parse_naver
from stego import parse_meta_from_text, parse_meta_from_json  # 메타(연회비·혜택·전월실적)                             # 네이버페이

# ---------- 라이브 수집(Actions용; requests 필요) ----------
def fetch(url, headers=None, timeout=20):
    import requests
    h={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
       "Accept":"application/json, text/plain, */*","Accept-Language":"ko-KR,ko;q=0.9"}
    if "card-gorilla.com" in url:                 # 목록 API는 referer/origin 필요
        h["Referer"]="https://www.card-gorilla.com/"; h["Origin"]="https://www.card-gorilla.com"
    if "banksalad.com" in url or "card-lounge.toss.im" in url:
        h["Accept"]="text/html,application/xhtml+xml,*/*"
    if headers: h.update(headers)
    r = requests.get(url, headers=h, timeout=timeout)
    r.raise_for_status(); return r

def collect_platform(plat, info):
    pid = info["id"]
    try:
        if plat=="cardgorilla":
            _cg_j=fetch(f"https://api.card-gorilla.com/v1/cards/{pid}").json()
            try:
                _m=parse_meta_from_json(_cg_j, json.dumps(_cg_j, ensure_ascii=False))
                if _m: CARD_META[("cardgorilla",str(pid))]=_m
            except: pass
            return parse_cardgorilla(_cg_j, pid)
        if plat=="banksalad":
            _bs_h=fetch(f"https://www.banksalad.com/product/cards/{pid}").text
            try:
                _m=parse_meta_from_text(_bs_h)
                if _m: CARD_META[("banksalad",str(pid))]=_m
            except: pass
            return parse_banksalad(_bs_h, pid)
        if plat=="toss":
            _ts_h=fetch(f"https://card-lounge.toss.im/card/{pid}").text
            try:
                _m=parse_meta_from_text(_ts_h)
                if _m: CARD_META[("toss",str(pid))]=_m
            except: pass
            return parse_toss(_ts_h, pid)
        if plat=="naver":
            co=info.get("company","CCNH"); iss=info.get("issuer",co)
            promo=info.get("promotionId"); prod=info.get("productId") or pid
            if promo:
                api=f"https://card.pay.naver.com/home/promotion.json?cardCompanyId={co}&cardIssuerCode={iss}&promotionId={promo}&from=pc_financetab"
                page=api.replace("promotion.json","promotion")
            else:
                api=f"https://card.pay.naver.com/home/detail.json?cardCompanyId={co}&cardIssuerCode={iss}&productId={prod}&from=pc_financetab"
                page=api.replace("detail.json","detail")
            ev=None
            try: ev=parse_naver(fetch(api).text, page)
            except Exception as e: print("  ! naver api err", e)
            if not ev:                                   # 헤드리스 폴백(Actions)
                try:
                    import headless; html=headless.render_html(page, wait_selector="body", referer="https://card.pay.naver.com/")
                    if html: ev=parse_naver(html, page)
                except Exception as e: print("  ! naver headless err", e)
            return ev
        if plat=="ajungdang":
            page=f"https://www.ajd.co.kr/card/event/detail/{pid}"
            ev=None
            try: ev=parse_ajd_rsc(fetch(page, headers={"RSC":"1","User-Agent":"Mozilla/5.0","Accept":"text/x-component"}).text, pid)
            except Exception as e: print("  ! ajd rsc err", e)
            if not ev:                                   # 헤드리스 폴백(Actions)
                try:
                    import headless; html=headless.render_html(page, wait_selector="main,section,body", referer="https://www.ajd.co.kr/")
                    if html: ev=parse_ajd_rsc(html, pid)
                except Exception as e: print("  ! ajd headless err", e)
            return ev
    except Exception as e:
        print(f"  ! {plat}/{pid} fetch err: {e}")
    return None

# ---------- DB ----------
def init_db(con):
    con.executescript(open(os.path.join(BASE,"schema.sql"),encoding="utf-8").read())
    for c,n in PLATFORMS.items():
        con.execute("INSERT OR IGNORE INTO platform(code,name) VALUES(?,?)",(c,n))
    con.commit()

def upsert_product(con, p, today):
    nk=_nk(p["name"]); cur=con.cursor()
    row=cur.execute("SELECT id FROM card_product WHERE name_norm=?",(nk,)).fetchone()
    if row: pid=row[0]
    else:
        cur.execute("INSERT INTO card_product(name,name_norm,issuer) VALUES(?,?,?)",(p["name"],nk,p.get("issuer")))
        pid=cur.lastrowid
    for plat,info in p.get("platforms",{}).items():
        _u=info.get("url") or plat_url(plat,info.get("id"))
        cur.execute("""INSERT INTO product_platform(card_product_id,platform,platform_product_id,url,first_seen,last_seen)
            VALUES(?,?,?,?,?,?) ON CONFLICT(card_product_id,platform) DO UPDATE SET last_seen=excluded.last_seen, active=1,
            platform_product_id=excluded.platform_product_id, url=COALESCE(excluded.url, product_platform.url)""",
            (pid,plat,str(info["id"]),_u,today,today))
    con.commit(); return pid

def record_event(con, pid, plat, fetched, today):
    """변경감지: 신규=NEW, 금액/내용 변경=UPDATE(이전 active CLOSED 후 신규), 없음=CLOSED, 동일=SAME."""
    cur=con.cursor()
    act=cur.execute("SELECT id,reward_won,reward_text FROM event WHERE card_product_id=? AND platform=? AND status='active' ORDER BY id DESC",(pid,plat)).fetchall()
    def snap(eid,ft,fw,ct):
        cur.execute("INSERT INTO event_snapshot(event_id,card_product_id,platform,captured_date,reward_text,reward_won,change_type) VALUES(?,?,?,?,?,?,?)",(eid,pid,plat,today,ft,fw,ct))
    if fetched is None:
        for e in act:
            cur.execute("UPDATE event SET status='closed',last_seen=? WHERE id=?",(today,e[0])); snap(e[0],e[2],e[1],"CLOSED")
        con.commit(); return "CLOSED" if act else "NONE"
    fw,ft=fetched["reward_won"],fetched["reward_text"]
    if not act:
        cur.execute("""INSERT INTO event(card_product_id,platform,reward_text,reward_won,period_start,period_end,source_url,status,first_seen,last_seen)
            VALUES(?,?,?,?,?,?,?,'active',?,?)""",(pid,plat,ft,fw,fetched["period_start"],fetched["period_end"],fetched["url"],today,today))
        snap(cur.lastrowid,ft,fw,"NEW"); con.commit(); return "NEW"
    e=act[0]
    if e[1]==fw and e[2]==ft:
        cur.execute("UPDATE event SET last_seen=? WHERE id=?",(today,e[0])); snap(e[0],ft,fw,"SAME"); con.commit(); return "SAME"
    # 변경: 기존 active 전부 종료(1상품 2이벤트면 이전 중단) 후 신규 활성
    for ee in act: cur.execute("UPDATE event SET status='closed',last_seen=? WHERE id=?",(today,ee[0]))
    cur.execute("""INSERT INTO event(card_product_id,platform,reward_text,reward_won,period_start,period_end,source_url,status,first_seen,last_seen)
        VALUES(?,?,?,?,?,?,?,'active',?,?)""",(pid,plat,ft,fw,fetched["period_start"],fetched["period_end"],fetched["url"],today,today))
    snap(cur.lastrowid,ft,fw,"UPDATE"); con.commit(); return "UPDATE"

SITE = os.path.join(os.path.dirname(BASE), "site")

def export_json(con):
    rows=con.cursor().execute("SELECT id,name,issuer FROM card_product ORDER BY id").fetchall()  # 먼저 materialize(커서 재사용 버그 방지)
    out=[]; c=con.cursor()
    # 이미지 폴백 맵: cards.json(빌드 카탈로그·toss CDN 등 안정 443 URL)에서 이름→이미지.
    # 카드고릴라 :8080 card_img가 실패(데이터센터 timeout)해도 저장된 URL로 플레이트를 채운다.
    CARDS_IMG={}
    try:
        _cj=json.load(open(os.path.join(SITE,"cards.json"),encoding="utf-8"))
        def _wimg(o):
            if isinstance(o,dict):
                if o.get("name") and o.get("img"): CARDS_IMG[_nk(o["name"])]=o["img"]
                for v in o.values(): _wimg(v)
            elif isinstance(o,list):
                for v in o: _wimg(v)
        _wimg(_cj); print(f"이미지 폴백맵(cards.json) {len(CARDS_IMG)}개")
    except Exception as _e: print("cards.json 이미지맵 로드 실패:", str(_e)[:60])
    for pid,name,issuer in rows:
        maps={r[0]:{"id":r[1],"url":r[2]} for r in c.execute("SELECT platform,platform_product_id,url FROM product_platform WHERE card_product_id=?",(pid,)).fetchall()}
        for _pl,_m in maps.items():           # url 누락(과거 ON CONFLICT 미갱신 등) 시 id로 정확 랜딩 URL 보정
            if not _m.get("url"): _m["url"]=plat_url(_pl,_m.get("id"))
        evs=[]
        for r in c.execute("SELECT platform,reward_text,reward_won,period_end,source_url FROM event WHERE card_product_id=? AND status='active' ORDER BY reward_won DESC",(pid,)).fetchall():
            mw,bw,comps=parse_breakdown(r[1],r[2])   # reward_text→메인/부가 분해
            ov=BREAKDOWN.get((name,r[0]))            # 거주지 수집 이벤트상세 분해값 우선
            if ov: mw,bw=ov["main"],ov["bonus"]
            e={"platform":r[0],"reward_text":r[1],"reward_won":r[2],"period_end":r[3],"url":r[4],
               "main_won":mw,"bonus_won":bw}
            if comps and bw>0: e["breakdown"]=comps   # 부가가 실제 있을 때만 첨부
            evs.append(e)
        cgid=str((maps.get("cardgorilla") or {}).get("id") or "")
        img=CG_IMG.get(cgid) or CARDS_IMG.get(_nk(name))   # 8080 실패 시 cards.json 저장 이미지로 폴백
        out.append({"id":pid,"name":name,"issuer":issuer,"img":img,"platforms":maps,"events":evs})
    os.makedirs(SITE,exist_ok=True)
    MONTH="2026-06"
    json.dump({"updated":datetime.date.today().isoformat(),"month":MONTH,"products":out},
              open(os.path.join(SITE,"platform_events.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → site/platform_events.json ({len(out)} products)")
    # ── 발급이벤트 목록(events.json) = platform_events 평탄화(5개 플랫폼·네이버 포함). 구형 build_data 산출물(네이버 0건) 대체 ──
    PN={"cardgorilla":"카드고릴라","banksalad":"뱅크샐러드","toss":"토스","naver":"네이버페이","ajungdang":"아정당","kakaopay":"카카오페이"}
    def _man(w):
        if not w: return ""
        return (str(round(w/1000)/10).replace(".0","")+"만원") if w>=10000 else (f"{w:,}원")
    items=[]; iss_max={}
    for p in out:
        iss=p.get("issuer") or "기타"
        for e in p.get("events",[]):
            pl=e.get("platform"); url=e.get("url") or (p.get("platforms",{}).get(pl) or {}).get("url") or ""
            w=e.get("reward_won") or 0
            ben=("최대 "+_man(w)+" 캐시백") if w>0 else (e.get("reward_text") or "")
            pe=e.get("period_end")
            items.append({"issuer":iss,"card":p["name"],"platform":PN.get(pl,pl),"benefit":ben,
                          "period":("~"+str(pe)[5:].replace("-","/")) if pe else "","url":url,"won":w})
            iss_max[iss]=max(iss_max.get(iss,0),w)
    order=sorted(iss_max,key=lambda k:-iss_max[k])
    json.dump({"updated":datetime.date.today().isoformat(),"month":MONTH,"order":order,"items":items},
              open(os.path.join(SITE,"events.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → site/events.json ({len(items)} items, {len(order)} issuers)")
    # ── 월간 스냅샷(전월 대비 비교 기반: 7월에 6월과 diff) ──
    issuers={}; cardsnap=[]
    for p in out:
        pl={}
        for e in p.get("events",[]):
            w=e.get("reward_won") or 0
            if w>pl.get(e["platform"],0): pl[e["platform"]]=w
        if not pl: continue
        iss=p.get("issuer") or "기타"; issuers.setdefault(iss,{})
        for pk,w in pl.items():
            if w>issuers[iss].get(pk,0): issuers[iss][pk]=w
        cardsnap.append({"name":p["name"],"issuer":iss,"platforms":pl,"max":max(pl.values())})
    hist=os.path.join(SITE,"history"); os.makedirs(hist,exist_ok=True)
    json.dump({"month":MONTH,"updated":datetime.date.today().isoformat(),"issuers":issuers,"cards":cardsnap},
              open(os.path.join(hist,MONTH+".json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    # 추이차트용 월 인덱스(존재하는 스냅샷 월 목록) — 프론트가 이걸 읽어 각 월 파일을 로드
    months=sorted([f[:-5] for f in os.listdir(hist) if f.endswith(".json") and f[0].isdigit()])
    json.dump({"months":months,"updated":datetime.date.today().isoformat()},
              open(os.path.join(hist,"index.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → site/history/{MONTH}.json + index.json ({len(months)} months)")
    # ── 추천 테이블 기반(reco.json): 카드별 교차 최대혜택 + 플랫폼 + 발급사 (향후 유저 추천용) ──
    reco=[]
    for p in out:
        evs=p.get("events",[])
        if not evs: continue
        best=max(evs,key=lambda e:e.get("reward_won") or 0)
        reco.append({"id":p["id"],"name":p["name"],"issuer":p.get("issuer"),"img":p.get("img"),
                     "maxCashbackWon":best.get("reward_won") or 0,"maxCashbackText":best.get("reward_text"),
                     "bestPlatform":best.get("platform"),"periodEnd":best.get("period_end"),
                     "platforms":sorted(set(e["platform"] for e in evs)),
                     "platformCount":len(set(e["platform"] for e in evs)),
                     "events":[{"platform":e["platform"],"reward_won":e.get("reward_won"),"reward_text":e.get("reward_text"),"period_end":e.get("period_end"),"main_won":e.get("main_won"),"bonus_won":e.get("bonus_won")} for e in evs]})
    reco.sort(key=lambda r:r["maxCashbackWon"],reverse=True)
    json.dump({"month":MONTH,"updated":datetime.date.today().isoformat(),"count":len(reco),"cards":reco},
              open(os.path.join(SITE,"reco.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → history/{MONTH}.json ({len(cardsnap)} cards), reco.json ({len(reco)} cards)")

def run(products, today, injected=None, june_only=True):
    con=sqlite3.connect(DB); init_db(con)
    for p in products:
        pid=upsert_product(con,p,today)
        for plat,info in p.get("platforms",{}).items():
            fetched = (injected or {}).get((p["name"],plat), "LIVE") if injected else "LIVE"
            if fetched=="LIVE": fetched=collect_platform(plat,info)
            if june_only and fetched and not is_june2026(fetched): fetched=None  # 6월 이벤트 우선
            res=record_event(con,pid,plat,fetched,today)
            amt=fetched["reward_text"] if fetched else "-"
            print(f"  [{today}] {p['name'][:18]:<18} {plat:<11} {res:<7} {amt}")
    export_json(con); con.close()

def _cards_from(j):
    """카드고릴라 목록 응답에서 카드 배열 추출(여러 shape 방어)."""
    if isinstance(j, list): return j
    for k in ("data","result","results","cards","list","items"):
        v=j.get(k) if isinstance(j, dict) else None
        if isinstance(v, list): return v
        if isinstance(v, dict):
            for kk in ("data","list","cards","items"):
                if isinstance(v.get(kk), list): return v[kk]
    return []

def _load_seed():
    """cg_seed.json(브라우저로 확정한 6월 CBK 카드 128개) → 발굴 폴백/시드."""
    try:
        s=json.load(open(os.path.join(BASE,"cg_seed.json"),encoding="utf-8"))
        return [{"name":n,"issuer":iss,"platforms":{"cardgorilla":{"id":str(cid)}}}
                for cid,n,iss in s.get("cards",[])]
    except Exception as e:
        print("seed load err", e); return []

def _cg_catalog():
    """idx→{name,issuer,img}. cards?type=CBK&is_live=true 전체 카탈로그.
    :8080 응답엔 card_img(플레이트 이미지)가 포함됨 → 우선 사용, 실패 시 무포트 폴백."""
    cat={}
    # cards 카탈로그(card_img 포함)는 응답이 커서 20s로는 타임아웃 → 60s + 재시도. :8080 우선(card_img 제공).
    for url in ("https://api.card-gorilla.com:8080/v1/cards?type=CBK&is_live=true",
                "https://api.card-gorilla.com/v1/cards?type=CBK&is_live=true"):
        for attempt in range(3):
            try:
                cj=fetch(url, timeout=60).json()
                for c in _cards_from(cj):
                    if isinstance(c,dict) and c.get("idx"):
                        corp=c.get("corp") or {}
                        cat[str(c["idx"])]={"name":c.get("name"),
                                            "issuer":corp.get("name") if isinstance(corp,dict) else None,
                                            "img":(c.get("card_img") or {}).get("url")}   # 카드 플레이트 이미지(CloudFront)
                n_img=sum(1 for v in cat.values() if v.get("img"))
                print(f"catalog({url.split('//')[1][:30]}) → {len(cat)} cards, {n_img} with img (try {attempt+1})")
                if cat: return cat
            except Exception as e:
                print("catalog err", url[:40], "try", attempt+1, str(e)[:60])
    return cat

CG_EVENTS={}   # cardgorilla_id → {subject(=카드고릴라 자체 이벤트 라벨), title, start, end}
CG_IMG={}      # cardgorilla_id → 카드 플레이트 이미지 URL(상품 메타 매핑)
BREAKDOWN={}   # (카드명, 플랫폼) →
CARD_META={}    # (platform, pid) → {annual_fee, benefits, spending_req} 메타정보
# (카드명, 플랫폼) → {"main":원, "bonus":원}  거주지 수집 이벤트상세 분해값(메인/부가 override)

def discover_products(limit=400):
    """카드고릴라 events?type=CBK(현재 진행 캐시백 이벤트) → 매핑 카드 자동 발굴.
    각 이벤트의 card_idxs를 카탈로그(이름·발급사)와 조인. subject(이벤트 라벨)도 CG_EVENTS에 적재.
    라이브 실패 시 cg_seed.json 폴백."""
    out={}
    try:
        ev=fetch("https://api.card-gorilla.com/v1/events?type=CBK").json()
        events=ev.get("data") if isinstance(ev,dict) else ev
        cat=_cg_catalog()
        for e in (events or []):
            if not isinstance(e,dict): continue
            corpn=e.get("corp_name")
            for cid in (e.get("card_idxs") or []):
                cid=str(cid); meta=cat.get(cid) or {}
                name=meta.get("name") or (e.get("title") or "").strip()
                if not name: continue
                out[_nk(name)]={"name":name,"issuer":meta.get("issuer") or corpn,
                                "platforms":{"cardgorilla":{"id":cid}}}
                if meta.get("img"): CG_IMG[cid]=meta["img"]
                CG_EVENTS[cid]={"subject":(e.get("subject") or "").strip(),
                                "title":(e.get("title") or "").strip(),"idx":e.get("idx"),
                                "start":e.get("evt_start_time"),"end":e.get("evt_end_time")}
        print(f"discover(live events?type=CBK) → {len(out)} cards, {len(CG_EVENTS)} events")
    except Exception as e:
        print("discover live err", e)
    if not out:                                   # 라이브 차단 시 시드로 보장
        for p in _load_seed(): out[_nk(p["name"])]=p
        print(f"discover(seed fallback) → {len(out)} cards")
    return list(out.values())[:limit]

def diagnose():
    """진단 덤프 → site/_debug.json (Actions 로그 대신 커밋 파일로 관찰)."""
    dbg={"playwright":False,"cg_events":{},"cg_cards":{}}
    try:
        import playwright; dbg["playwright"]=getattr(playwright,"__version__","yes")
    except Exception as e: dbg["playwright"]="ERR:"+str(e)[:60]
    try:
        r=fetch("https://api.card-gorilla.com/v1/events?type=CBK")
        j=r.json(); d=j.get("data") if isinstance(j,dict) else j
        dbg["cg_events"]={"st":r.status_code,"len":len(r.text),"n":len(d or []),
                          "cardIdxs":sum(len(e.get("card_idxs") or []) for e in (d or []))}
    except Exception as e: dbg["cg_events"]="ERR:"+str(e)[:120]
    try:
        r=fetch("https://api.card-gorilla.com/v1/cards?type=CBK&is_live=true")
        j=r.json(); d=j.get("data") if isinstance(j,dict) else j
        dbg["cg_cards"]={"st":r.status_code,"n":len(d or [])}
    except Exception as e: dbg["cg_cards"]="ERR:"+str(e)[:120]
    os.makedirs(SITE,exist_ok=True)
    json.dump(dbg,open(os.path.join(SITE,"_debug.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("diagnose →", {k:(v if isinstance(v,str) else "...") for k,v in dbg.items()})

def _apply_event_schemes(platform, schemes_file, injected, products):
    """세이스모(토스/카카오페이) 이벤트 페이지 랜딩 스킴 주입(공통).
    schemes_file(예: toss_event_schemes.json)의 events[]를 issuer+금액 근접으로 해당 platform 이벤트에 1:1 배정.
    매칭 규칙: 같은 issuer 내에서 (이벤트 reward_won, 없으면 0) ↔ scheme.headline_won 차이가 작은 쌍부터 그리디 매칭(중복 배정 금지).
    매칭되면 injected[(name,platform)]["url"] 과 products[i].platforms[platform]["url"] 을 스킴으로 덮어쓴다.
    파일이 없으면 조용히 0건 반환. 반환=주입(덮어쓴) 건수."""
    try:
        sch=json.load(open(os.path.join(BASE,schemes_file),encoding="utf-8"))
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"{platform} scheme load err", e); return 0
    schemes=sch.get("events",[])
    if not schemes: return 0
    # 이름→상품 빠른 조회
    bynk={_nk(p["name"]):p for p in products}
    # 현재 이 platform 을 가진 이벤트 후보 수집: (name, issuer, won)
    cands=[]
    for p in products:
        plats=p.get("platforms",{})
        if platform not in plats: continue
        won=0
        inj=injected.get((p["name"],platform))
        if isinstance(inj,dict):
            if inj.get("url"): continue                 # 시드에 정확한 이벤트 url이 이미 박혀 있으면 재매칭 제외(스크램블 방지)
            won=inj.get("reward_won") or 0
        cands.append({"name":p["name"],"issuer":(p.get("issuer") or "").strip(),"won":won})
    # issuer 별 그리디 매칭: scheme(headline_won 내림차순) ↔ candidate(won 내림차순)
    from collections import defaultdict
    sch_by=defaultdict(list); cand_by=defaultdict(list)
    for s in schemes:
        sch_by[(s.get("issuer") or "").strip()].append(s)
    for c in cands:
        cand_by[c["issuer"]].append(c)
    used_names=set(); n=0
    for iss, slist in sch_by.items():
        clist=[c for c in cand_by.get(iss,[]) if c["name"] not in used_names]
        # 금액 내림차순 그리디
        for s in sorted(slist, key=lambda x:-(x.get("headline_won") or 0)):
            avail=[c for c in clist if c["name"] not in used_names]
            if not avail: break
            hw=s.get("headline_won") or 0
            best=min(avail, key=lambda c:abs((c["won"] or 0)-hw))
            url=s.get("url")
            if not url: continue
            used_names.add(best["name"])
            inj=injected.get((best["name"],platform))
            if isinstance(inj,dict): inj["url"]=url
            p=bynk.get(_nk(best["name"]))
            if p:
                p.setdefault("platforms",{}).setdefault(platform,{"id":""})["url"]=url
            n+=1
    return n


def _merge_seismo_seed(platform, seed_file, injected, products):
    """선택적 세이스모 시드(kakaopay_seed.json 동일 스키마: platform/events[].cards/reward_won/...)를
    해당 platform 으로 병합 주입. 단, 라이브가 이미 있는 (name,platform) 이벤트는 라이브 우선(금액 유지),
    없는 카드만 시드로 보강한다(병합). 미존재 카드는 신규 상품 생성. 파일 없으면 조용히 skip. 반환=보강 건수."""
    try:
        sd=json.load(open(os.path.join(BASE,seed_file),encoding="utf-8"))
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"{platform} seismo seed err", e); return 0
    bynk={_nk(p["name"]):p for p in products}; n=0; nnew=0
    for ev in sd.get("events",[]):
        rw=ev.get("reward_won") or 0; rtext=ev.get("reward_text"); eurl=ev.get("url","")
        ps=ev.get("period_start"); pe=ev.get("period_end"); iss=ev.get("issuer") or ""
        for cn in ev.get("cards",[]):
            p=bynk.get(_nk(cn))
            if not p:
                continue                                   # 우리 시드/DB에 없는 카드는 제외(신규 상품 생성 안 함)
            had_live = platform in p.get("platforms",{})   # 이미 라이브 매핑이 붙어 있던 카드
            p.setdefault("platforms",{}).setdefault(platform,{"id":"","url":""})
            key=(p["name"],platform)
            # 시드에 이벤트 스킴 url이 있으면(캡처 기반 정확값) 라이브보다 우선. url 없을 때만 라이브 우선.
            if had_live and isinstance(injected.get(key),dict) and not eurl:
                continue
            if rw:
                cur=injected.get(key) if isinstance(injected.get(key),dict) else {}
                u=eurl or cur.get("url","")
                injected[key]={"reward_won":rw,"reward_text":rtext,"period_start":ps,"period_end":pe,"url":u}
                if u: p["platforms"][platform]["url"]=u
                n+=1
    if n or nnew: print(f"세이스모({platform}) 시드 보강 {n}건 (신규상품 {nnew}건)")
    return n


# ---------- 토스 카드라운지 연회비 스크래퍼 (ID 기반) ----------
# 토스 발급사별 검색 페이지를 playwright로 렌더 → 각 카드의 고유 id(/card/{id})와 연회비를 파싱.
# 이름 매칭이 아니라 toss 카드 id 기준으로 fee를 적재(scrape/toss_fees.json) → build_data가 카드의
# toss source id(우선) 또는 정규화 이름(폴백)으로 병합.
TOSS_FEE_FILTERS = ["SAMSUNG","HYUNDAI","LOTTE","SHINHAN","KB","WOORI","HANA","NH","IBK","BC"]
def _toss_shortfee(s):
    if not s: return ""
    if "없음" in s: return "없음"
    m=re.search(r"([\d,]+)\s*원", s); return (m.group(1)+"원") if m else ""
def _toss_clean_name(nm):
    nm=re.sub(r"\s+"," ",(nm or "")).strip()
    nm=re.sub(r"^(?:할인|적립|마일리지|·|\s)+","",nm).strip()
    return nm
def scrape_toss_fees():
    """토스 카드라운지에서 카드 id↔연회비를 수집해 scrape/toss_fees.json 작성."""
    try: import headless
    except Exception as e:
        print("toss fee: headless 미가용", e); return
    SCR=os.path.join(os.path.dirname(BASE),"scrape"); os.makedirs(SCR,exist_ok=True)
    byId={}; byName={}
    for code in TOSS_FEE_FILTERS:
        url=f"https://card-lounge.toss.im/search?filters={code}"
        html=None
        try: html=headless.render_html(url, wait_selector="a[href*='/card/']", timeout=35000)
        except Exception as e: print("  toss fee render err", code, e)
        if not html: continue
        parts=re.split(r'href="(?:https://card-lounge\.toss\.im)?/card/(\d+)"', html)
        n0=len(byId)
        for i in range(1, len(parts)-1, 2):
            cid=parts[i]; block=parts[i+1]
            txt=re.sub(r"<[^>]+>"," ",block); txt=re.sub(r"\s+"," ",txt).strip()
            mf=re.search(r"연회비\s*(.*?)\s*전월실적", txt)
            fee=_toss_shortfee(mf.group(1)) if mf else ""
            if not fee: continue
            mn=re.search(r"([가-힣A-Za-z0-9().,/&+\-\s]{2,70}?)\s*연회비", txt)
            nm=_toss_clean_name(mn.group(1) if mn else "")
            if cid not in byId: byId[cid]={"name":nm,"fee":fee}
            if nm: byName.setdefault(_nk(nm), fee)
        print(f"  toss fee {code}: +{len(byId)-n0}")
    if byId:
        json.dump({"_updated":datetime.date.today().isoformat(),"byId":byId,"byName":byName},
                  open(os.path.join(SCR,"toss_fees.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"toss fees → scrape/toss_fees.json (byId {len(byId)}, byName {len(byName)})")
    else:
        print("toss fees: 수집 0건 — 기존 파일 유지")

def export_card_meta(products):
    """수집된 카드 메타정보를 scrape/card_meta.json으로 저장."""
    SCR=os.path.join(os.path.dirname(BASE),"scrape"); os.makedirs(SCR,exist_ok=True)
    by_name={}
    for p in products:
        nk=_nk(p["name"]); entry={"name":p["name"],"issuer":p.get("issuer","")}
        for plat,info in p.get("platforms",{}).items():
            pid=str(info.get("id",""))
            m=CARD_META.get((plat,pid))
            if m:
                for k in ("annual_fee","benefits","spending_req"):
                    if m.get(k) and not entry.get(k): entry[k]=m[k]
        if any(entry.get(k) for k in ("annual_fee","benefits","spending_req")):
            by_name[nk]=entry
    json.dump({"_updated":datetime.date.today().isoformat(),"cards":by_name},
              open(os.path.join(SCR,"card_meta.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"card meta → scrape/card_meta.json ({len(by_name)} cards)")

if __name__=="__main__":
    today=datetime.date.today().isoformat()
    try: scrape_toss_fees()
    except Exception as e: print("toss fee scrape err", e)
    try: diagnose()
    except Exception as e: print("diagnose err", e)
    curated=json.load(open(os.path.join(BASE,"products.json"),encoding="utf-8"))
    by={_nk(p["name"]):p for p in curated}
    discovered=discover_products()                # 라이브 events?type=CBK
    seed=_load_seed()                             # 항상 시드 합집합(최소 128 보장)
    for d in discovered+seed:                      # 자동 발굴 + 큐레이션 매핑 병합
        k=_nk(d["name"])
        if k in by: by[k]["platforms"].setdefault("cardgorilla", d["platforms"]["cardgorilla"])
        else: by[k]=d
    products=list(by.values())
    # 토스: cards.json 매칭 시드(toss_seed.json) → toss 플랫폼 부착(라이브 parse_toss로 수집)
    try:
        ts=json.load(open(os.path.join(BASE,"toss_seed.json"),encoding="utf-8")).get("cards",{})
        _bt={_nk(p["name"]):p for p in products}; _tn=0
        for nm,info in ts.items():
            p=_bt.get(_nk(nm))
            if p and info.get("toss_id"):
                p.setdefault("platforms",{}).setdefault("toss",{"id":str(info["toss_id"])}); _tn+=1
        if _tn: print(f"토스 매핑 부착 {_tn}건")
    except FileNotFoundError: pass
    except Exception as e: print("toss seed err", e)
    # 아정당: 로컬 수집(거주지 IP) 결과 ajd_seed.json 을 주입(라이브 호출 없이 병합)
    injected={}
    try:
        aj=json.load(open(os.path.join(BASE,"ajd_seed.json"),encoding="utf-8")).get("cards",{})
        bynk={_nk(p["name"]):p for p in products}
        for nm,info in aj.items():
            p=bynk.get(_nk(nm))
            if not p or not info.get("reward_won"): continue
            p.setdefault("platforms",{})["ajungdang"]={"id":info.get("ajd_id",""),"url":info.get("url","")}
            injected[(p["name"],"ajungdang")]={"reward_won":info["reward_won"],"reward_text":info.get("reward_text"),
                                               "period_start":None,"period_end":None,"url":info.get("url","")}
        if injected: print(f"아정당 로컬 주입 {len(injected)}건")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("ajd seed 병합 err", e)
    # 네이버: 캡처/로컬 수집 결과 naver_seed.json 주입(네이버는 데이터센터 404 → 라이브 호출 없이 병합)
    try:
        nv=json.load(open(os.path.join(BASE,"naver_seed.json"),encoding="utf-8")).get("cards",{})
        _bn={_nk(p["name"]):p for p in products}; _nn=0; _nskip=0
        NAVER_MAX=1_000_000   # 1인 캐시백 현실 상한. 초과액은 '총 행사규모/최대적립한도' 마케팅 수치로 보고 금액 비표시
        for nm,info in nv.items():
            p=_bn.get(_nk(nm))
            if not p: continue
            rw=info.get("reward_won") or 0
            rtext=info.get("reward_text")
            if rw>NAVER_MAX:                       # 3600만원 등 비현실 금액 → 금액 숨기고 이벤트만 표기
                rw=0; rtext="네이버페이 카드 이벤트"; _nskip+=1
            # 네이버 상품 페이지 링크는 항상 부착(금액 신뢰 여부와 무관)
            if info.get("url"):
                p.setdefault("platforms",{})["naver"]={"id":info.get("productId",""),"url":info.get("url","")}
            if rw:                                  # 신뢰 가능한 금액만 교차비교 이벤트로 주입
                injected[(p["name"],"naver")]={"reward_won":rw,"reward_text":rtext,
                                               "period_start":None,"period_end":None,"url":info.get("url","")}
                if info.get("main_won") is not None or info.get("bonus_won"):   # 주(혜택1)/부가(추가혜택) 분해 반영
                    BREAKDOWN[(p["name"],"naver")]={"main":info.get("main_won") or 0,"bonus":info.get("bonus_won") or 0}
                _nn+=1
        if _nn or _nskip: print(f"네이버 주입 {_nn}건 (금액 비현실 제외 {_nskip}건)")
    except FileNotFoundError: pass
    except Exception as e: print("naver seed err", e)
    # 뱅크샐러드: 거주지 렌더링 텍스트로 보정한 banksalad_seed.json 주입(cashbackAmountKrw0f 파싱 오류 override)
    try:
        bs=json.load(open(os.path.join(BASE,"banksalad_seed.json"),encoding="utf-8")).get("cards",{})
        _bb={_nk(p["name"]):p for p in products}; _bn2=0
        for nm,info in bs.items():
            p=_bb.get(_nk(nm))
            if not p: continue
            if info.get("no_event") or not info.get("reward_won"):
                injected[(p["name"],"banksalad")]=None        # 이벤트 없음 → 종료(잘못된 라이브값 차단)
            else:
                # guid는 시드 우선(거주지 __NEXT_DATA__ productGuid), 없으면 기존 매핑. 둘 다 없으면 전체리스트(/cards/event) 대신 링크 생략
                bgid=str(info.get("id") or (p.get("platforms",{}).get("banksalad") or {}).get("id") or "")
                burl=("https://www.banksalad.com/product/cards/"+bgid) if bgid else ""   # 상품상세(p2). 리스트로 떨어뜨리지 않음
                # 기존 banksalad 매핑이 없던 카드도 플랫폼을 부착해야 run()이 주입을 적용한다(naver와 동일 패턴)
                p.setdefault("platforms",{}).setdefault("banksalad",{"id":bgid,"url":burl})
                injected[(p["name"],"banksalad")]={"reward_won":info["reward_won"],"reward_text":info.get("reward_text"),
                                                   "period_start":None,"period_end":None,"url":burl}
                if info.get("main_won") is not None or info.get("bonus_won"):
                    BREAKDOWN[(p["name"],"banksalad")]={"main":info.get("main_won") or 0,"bonus":info.get("bonus_won") or 0}
            _bn2+=1
        if _bn2: print(f"뱅샐 보정 주입 {_bn2}건")
    except FileNotFoundError: pass
    except Exception as e: print("banksalad seed err", e)
    # 세이스모(Seismosaurus): 카카오페이 앱 캡처를 비전분석한 kakaopay_seed.json 주입.
    # 카카오페이는 공개 웹 스크래핑 소스가 없어 앱 캡처 기반으로 적재(toss와 함께 세이스모 모듈이 담당).
    # reward_won=국내 이용 메인 캐시백(타 플랫폼과 비교 가능한 발급 캐시백). 공개 웹 URL이 없어 아웃링크는 비부착.
    try:
        kp=json.load(open(os.path.join(BASE,"kakaopay_seed.json"),encoding="utf-8"))
        _bk={_nk(p["name"]):p for p in products}; _kn=0; _knew=0
        for ev in kp.get("events",[]):
            rw=ev.get("headline_won") or ev.get("reward_won") or 0; rtext=ev.get("reward_text")   # 기준 통일: 전체 혜택(최대 헤드라인). 카카오페이포인트=원 1:1
            ps=ev.get("period_start"); pe=ev.get("period_end"); iss=ev.get("issuer") or ""
            eurl=ev.get("url","")                      # 카카오페이 이벤트 페이지 랜딩 스킴(fest.kakaopay.com 그룹)
            for cn in ev.get("cards",[]):
                p=_bk.get(_nk(cn))
                if not p:                              # 우리 시드/DB에 없는 카드는 제외(신규 상품 생성 안 함)
                    continue
                p.setdefault("platforms",{})["kakaopay"]={"id":"","url":eurl}
                if rw:
                    injected[(p["name"],"kakaopay")]={"reward_won":rw,"reward_text":rtext,
                        "period_start":ps,"period_end":pe,"url":eurl}
                    _kn+=1
        if _kn: print(f"세이스모(카카오페이) 주입 {_kn}건 (신규상품 {_knew}건)")
    except FileNotFoundError: pass
    except Exception as e: print("kakaopay seismo err", e)
    # 세이스모(토스): 선택적 toss_seismo_seed.json(kakaopay_seed.json 동일 스키마)로 toss 이벤트 보강.
    # 라이브 toss(=toss_seed 매핑→parse_toss)가 이미 금액을 가진 카드는 라이브 우선, 없는 카드만 시드로 보강.
    # 파일 없으면 조용히 skip(지금은 파일 없음). 그 뒤 아래 스킴 주입이 url을 입힌다.
    try:
        _merge_seismo_seed("toss","toss_seismo_seed.json",injected,products)
    except Exception as e: print("toss seismo merge err", e)
    # 토스 이벤트 페이지 스킴 주입: issuer+금액 근접 매칭으로 toss 이벤트 url을 toss.im/_m/... 스킴으로 덮어쓴다.
    # (라이브 toss는 reward_won 주입이 없으므로 won=0 기준 근접; 같은 issuer 다건이면 금액 내림차순 그리디 1:1)
    try:
        _tsn=_apply_event_schemes("toss","toss_event_schemes.json",injected,products)
    except Exception as e: _tsn=0; print("toss scheme err", e)
    print(f"토스 스킴 주입 {_tsn}건")
    # 카카오페이 스킴 주입(스캐폴드): 선택적 kakaopay_event_schemes.json 있으면 동일 매칭으로 url 덮어쓰기. 없으면 0건.
    try:
        _ksn=_apply_event_schemes("kakaopay","kakaopay_event_schemes.json",injected,products)
    except Exception as e: _ksn=0; print("kakaopay scheme err", e)
    print(f"카카오페이 스킴 주입 {_ksn}건")
    # 카드고릴라: 이벤트 라벨(subject)을 reward_text로 주입(상세 'card_detail_text'의 "연회비 캐시백"류 대신)
    cg_inj=0
    for p in products:
        cid=str((p.get("platforms",{}).get("cardgorilla") or {}).get("id") or "")
        ce=CG_EVENTS.get(cid)
        if not ce: continue
        subj=ce.get("subject") or ""
        if not subj: continue
        # 랜딩: /event/detail/{그룹ID}=카드사 캐시백 이벤트 그룹(주/부가 노출). 그룹ID는 카드사 단위 작은 id(웹사이트 라우팅)로,
        # API의 이벤트 idx(1288류)와는 다른 id 공간이라 그대로 쓰면 안 됨(엉뚱한 페이지로 떨어짐). 발급사→그룹ID 매핑 사용.
        gid=CG_GROUP.get((p.get("issuer") or "").strip())
        ev_url=(f"https://www.card-gorilla.com/event/detail/{gid}" if gid else f"https://www.card-gorilla.com/card/detail/{cid}")
        p.setdefault("platforms",{}).setdefault("cardgorilla",{"id":cid})["url"]=ev_url   # platforms.url에도 그룹페이지 반영
        injected[(p["name"],"cardgorilla")]={"reward_won":parse_won(subj),"reward_text":subj,
            "period_start":ce.get("start"),"period_end":ce.get("end"),
            "url":ev_url}
        cg_inj+=1
    if cg_inj: print(f"카드고릴라 이벤트 라벨 주입 {cg_inj}건")
    print(f"총 상품 {len(products)}개 수집 시작")
    run(products, today, injected=injected or None)
    try: export_card_meta(products)
    except Exception as e: print("card meta export err", e)
