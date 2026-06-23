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

# ── 용각류 파서 모듈 분리(2026-06): 공통=cardutil / 플랫폼별 파서 ──
from cardutil import _nk, parse_won, _fmt_man, is_june2026, parse_breakdown   # 공통 유틸
from brachio import parse_cardgorilla                        # 카드고릴라
from apato import parse_banksalad                            # 뱅크샐러드
from diplo import parse_toss                                 # 토스
from bronto import parse_ajd_rsc                             # 아정당
from mamenchi import parse_naver                             # 네이버페이

# ---------- 라이브 수집(Actions용; requests 필요) ----------
def fetch(url, headers=None):
    import requests
    h={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
       "Accept":"application/json, text/plain, */*","Accept-Language":"ko-KR,ko;q=0.9"}
    if "card-gorilla.com" in url:                 # 목록 API는 referer/origin 필요
        h["Referer"]="https://www.card-gorilla.com/"; h["Origin"]="https://www.card-gorilla.com"
    if "banksalad.com" in url or "card-lounge.toss.im" in url:
        h["Accept"]="text/html,application/xhtml+xml,*/*"
    if headers: h.update(headers)
    r = requests.get(url, headers=h, timeout=20)
    r.raise_for_status(); return r

def collect_platform(plat, info):
    pid = info["id"]
    try:
        if plat=="cardgorilla":
            return parse_cardgorilla(fetch(f"https://api.card-gorilla.com/v1/cards/{pid}").json(), pid)
        if plat=="banksalad":
            return parse_banksalad(fetch(f"https://www.banksalad.com/product/cards/{pid}").text, pid)
        if plat=="toss":
            return parse_toss(fetch(f"https://card-lounge.toss.im/card/{pid}").text, pid)
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
        cur.execute("""INSERT INTO product_platform(card_product_id,platform,platform_product_id,url,first_seen,last_seen)
            VALUES(?,?,?,?,?,?) ON CONFLICT(card_product_id,platform) DO UPDATE SET last_seen=excluded.last_seen, active=1""",
            (pid,plat,str(info["id"]),info.get("url"),today,today))
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
    for pid,name,issuer in rows:
        maps={r[0]:{"id":r[1],"url":r[2]} for r in c.execute("SELECT platform,platform_product_id,url FROM product_platform WHERE card_product_id=?",(pid,)).fetchall()}
        evs=[]
        for r in c.execute("SELECT platform,reward_text,reward_won,period_end,source_url FROM event WHERE card_product_id=? AND status='active' ORDER BY reward_won DESC",(pid,)).fetchall():
            mw,bw,comps=parse_breakdown(r[1],r[2])   # reward_text→메인/부가 분해
            e={"platform":r[0],"reward_text":r[1],"reward_won":r[2],"period_end":r[3],"url":r[4],
               "main_won":mw,"bonus_won":bw}
            if comps and bw>0: e["breakdown"]=comps   # 부가가 실제 있을 때만 첨부
            evs.append(e)
        cgid=str((maps.get("cardgorilla") or {}).get("id") or "")
        img=CG_IMG.get(cgid)
        out.append({"id":pid,"name":name,"issuer":issuer,"img":img,"platforms":maps,"events":evs})
    os.makedirs(SITE,exist_ok=True)
    MONTH="2026-06"
    json.dump({"updated":datetime.date.today().isoformat(),"month":MONTH,"products":out},
              open(os.path.join(SITE,"platform_events.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → site/platform_events.json ({len(out)} products)")
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
    for url in ("https://api.card-gorilla.com:8080/v1/cards?type=CBK&is_live=true",
                "https://api.card-gorilla.com/v1/cards?type=CBK&is_live=true"):
        try:
            cj=fetch(url).json()
            for c in _cards_from(cj):
                if isinstance(c,dict) and c.get("idx"):
                    corp=c.get("corp") or {}
                    cat[str(c["idx"])]={"name":c.get("name"),
                                        "issuer":corp.get("name") if isinstance(corp,dict) else None,
                                        "img":(c.get("card_img") or {}).get("url")}   # 카드 플레이트 이미지(CloudFront)
            n_img=sum(1 for v in cat.values() if v.get("img"))
            print(f"catalog({url.split('//')[1][:30]}) → {len(cat)} cards, {n_img} with img")
            if cat: return cat
        except Exception as e:
            print("catalog err", url[:40], e)
    return cat

CG_EVENTS={}   # cardgorilla_id → {subject(=카드고릴라 자체 이벤트 라벨), title, start, end}
CG_IMG={}      # cardgorilla_id → 카드 플레이트 이미지 URL(상품 메타 매핑)

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

if __name__=="__main__":
    today=datetime.date.today().isoformat()
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
        _bn={_nk(p["name"]):p for p in products}; _nn=0
        for nm,info in nv.items():
            p=_bn.get(_nk(nm))
            if not p or not info.get("reward_won"): continue
            p.setdefault("platforms",{})["naver"]={"id":info.get("productId",""),"url":info.get("url","")}
            injected[(p["name"],"naver")]={"reward_won":info["reward_won"],"reward_text":info.get("reward_text"),
                                           "period_start":None,"period_end":None,"url":info.get("url","")}
            _nn+=1
        if _nn: print(f"네이버 주입 {_nn}건")
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
                injected[(p["name"],"banksalad")]={"reward_won":info["reward_won"],"reward_text":info.get("reward_text"),
                                                   "period_start":None,"period_end":None,
                                                   "url":"https://www.banksalad.com/product/cards/"+str((p.get("platforms",{}).get("banksalad") or {}).get("id") or "")}
            _bn2+=1
        if _bn2: print(f"뱅샐 보정 주입 {_bn2}건")
    except FileNotFoundError: pass
    except Exception as e: print("banksalad seed err", e)
    # 카드고릴라: 이벤트 라벨(subject)을 reward_text로 주입(상세 'card_detail_text'의 "연회비 캐시백"류 대신)
    cg_inj=0
    for p in products:
        cid=str((p.get("platforms",{}).get("cardgorilla") or {}).get("id") or "")
        ce=CG_EVENTS.get(cid)
        if not ce: continue
        subj=ce.get("subject") or ""
        if not subj: continue
        evidx=ce.get("idx")
        ev_url=f"https://www.card-gorilla.com/event/detail/{evidx}" if evidx else f"https://www.card-gorilla.com/card/{cid}"
        injected[(p["name"],"cardgorilla")]={"reward_won":parse_won(subj),"reward_text":subj,
            "period_start":ce.get("start"),"period_end":ce.get("end"),
            "url":ev_url}
        cg_inj+=1
    if cg_inj: print(f"카드고릴라 이벤트 라벨 주입 {cg_inj}건")
    print(f"총 상품 {len(products)}개 수집 시작")
    run(products, today, injected=injected or None)
