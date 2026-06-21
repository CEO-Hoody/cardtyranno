# -*- coding: utf-8 -*-
"""카드 중개 메타 수집기 (API/SSR 직접 호출 + 일일 변경감지).
- 운영: GitHub Actions에서 requests로 각 플랫폼 호출 → meta.db 적재 → JSON export.
- 데모: --demo (네트워크 없이 주입 데이터로 변경감지 시연).
원칙: 사실 데이터(상품ID·리워드 금액·기간)만 저장. 소개 문구 미저장.
"""
import os, re, sqlite3, json, datetime, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "meta.db")
PLATFORMS = {"toss":"토스 카드라운지","cardgorilla":"카드고릴라","banksalad":"뱅크샐러드","ajungdang":"아정당"}

def _nk(n): return re.sub(r"[\s()（）·\-_/+.]+","",(n or "")).lower()

def parse_won(text):
    """'최대 57.9만원 혜택' -> 579000, '84만원' -> 840000. 여러 개면 최대값."""
    if not text: return None
    t = text.replace(",","")
    best = 0
    for m in re.finditer(r"([\d]+(?:\.\d+)?)\s*(억|만원|만|원)", t):
        v = float(m.group(1)); u = m.group(2)
        won = v*100000000 if u=="억" else v*10000 if u in("만원","만") else v
        best = max(best, int(won))
    return best or None

# ---------- 플랫폼 파서 (입력: 응답 본문 → 출력: {reward_text,reward_won,period_start,period_end,url}) ----------
def parse_cardgorilla(card_json, card_id):
    ev = (card_json or {}).get("event") or {}
    txt = ev.get("card_detail_text") or ev.get("subject")
    period = re.search(r"(20\d\d\.\d\d?\.\d\d?)\s*~\s*(20\d\d\.\d\d?\.\d\d?)", ev.get("detail","") or "")
    return {"reward_text":txt, "reward_won":parse_won(txt),
            "period_start":period.group(1) if period else None,
            "period_end":period.group(2) if period else None,
            "url":f"https://www.card-gorilla.com/card/{card_id}"} if txt else None

def parse_banksalad(html, prod_id):
    m = re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*캐시백", html or "")
    if not m: return None
    txt = "최대 "+m.group(1).replace(" ","")+" 캐시백"
    return {"reward_text":txt, "reward_won":parse_won(txt), "period_start":None,"period_end":None,
            "url":f"https://www.banksalad.com/product/cards/{prod_id}"}

def parse_toss(html, card_id):
    # 카드 자체 이벤트 배너: '카드 쓰고 최대 81만원 받는 이벤트'
    m = re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*받는\s*이벤트", html or "") \
        or re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*이벤트", html or "")
    if not m: return None
    txt = "최대 "+m.group(1).replace(" ","")+" 이벤트"
    return {"reward_text":txt, "reward_won":parse_won(txt), "period_start":None,"period_end":None,
            "url":f"https://card-lounge.toss.im/card/{card_id}"}

def parse_naver(text, url):
    # 네이버페이 detail.json/promotion.json 또는 page-data(dehydratedState) → 리워드/기간 generic 추출
    mt = re.search(r"(최대\s*[\d.,]+\s*(?:억|만원|원))", text)
    won = parse_won(mt.group(1)) if mt else parse_won(text)
    if not won: return None
    period = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", text)
    return {"reward_text":(mt.group(1) if mt else f"최대 {won//10000}만원"),"reward_won":won,
            "period_start":period.group(1).replace("-",".") if period else None,
            "period_end":period.group(2).replace("-",".") if period else None,"url":url}

def parse_ajd_rsc(text, evt_id):
    # 아정당 RSC(self.__next_f)/렌더 텍스트 → 리워드/기간 generic 추출
    mt = re.search(r"(최대\s*[\d.,]+\s*(?:억|만원|원))", text)
    won = parse_won(mt.group(1)) if mt else parse_won(text)
    if not won: return None
    period = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", text)
    return {"reward_text":(mt.group(1) if mt else f"최대 {won//10000}만원"),"reward_won":won,
            "period_start":period.group(1).replace("-",".") if period else None,
            "period_end":period.group(2).replace("-",".") if period else None,
            "url":f"https://www.ajd.co.kr/card/event/detail/{evt_id}"}

def is_june2026(ev):
    """6월(2026.06) 이벤트만 우선 필터."""
    if not ev: return False
    s = (ev.get("period_start") or "")+(ev.get("period_end") or "")+(ev.get("reward_text") or "")
    return ("2026.6" in s) or ("2026.06" in s) or ("2026-06" in s) or (not ev.get("period_start"))  # 기간 미표기는 현행으로 간주

# ---------- 라이브 수집(Actions용; requests 필요) ----------
def fetch(url, headers=None):
    import requests
    r = requests.get(url, headers=headers or {"User-Agent":"Mozilla/5.0","Accept":"*/*"}, timeout=15)
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
            return parse_naver(fetch(api).text, page)
        if plat=="ajungdang":
            r = fetch(f"https://www.ajd.co.kr/card/event/detail/{pid}", headers={"RSC":"1","User-Agent":"Mozilla/5.0","Accept":"text/x-component"})
            return parse_ajd_rsc(r.text, pid)
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
        evs=[{"platform":r[0],"reward_text":r[1],"reward_won":r[2],"period_end":r[3],"url":r[4]} for r in c.execute("SELECT platform,reward_text,reward_won,period_end,source_url FROM event WHERE card_product_id=? AND status='active' ORDER BY reward_won DESC",(pid,)).fetchall()]
        out.append({"id":pid,"name":name,"issuer":issuer,"platforms":maps,"events":evs})
    os.makedirs(SITE,exist_ok=True)
    json.dump({"updated":datetime.date.today().isoformat(),"month":"2026-06","products":out},
              open(os.path.join(SITE,"platform_events.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"export → site/platform_events.json ({len(out)} products)")

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

if __name__=="__main__":
    products=json.load(open(os.path.join(BASE,"products.json"),encoding="utf-8"))
    today=datetime.date.today().isoformat()
    run(products, today)
