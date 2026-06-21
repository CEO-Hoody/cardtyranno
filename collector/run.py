# -*- coding: utf-8 -*-
"""카드티라노 콜렉터 — 토스 카드라운지 어댑터 구현 + 매일 실행 파이프라인.
운영/CI(네트워크 가능 환경)에서 실행:  python collector/run.py
흐름: 스크래핑 → cardtyrano.db(card/event) 갱신 → build_data.py가 site/*.json export → git push → Netlify 자동배포.

설계
- 소스별 어댑터 분리. 현재 '토스' 어댑터는 SSR(서버렌더)이라 표준 urllib로 동작.
  아정당/카드고릴라/뱅크샐러드/카드사 공식은 JS 렌더링이라 Playwright 어댑터로 확장(자리만 마련).
- 카드명 정규화 dedup. 동일 카드가 여러 소스에 있으면 '카드사 공식' 우선.
"""
import re, time, json, sqlite3, urllib.request, urllib.error

UA = {"User-Agent": "Mozilla/5.0 (cardtyrano-collector)"}
TOSS = "https://card-lounge.toss.im"
BRANDS = {"삼성카드":"SAMSUNG","현대카드":"HYUNDAI","신한카드":"SHINHAN","KB국민카드":"KB","롯데카드":"LOTTE",
          "우리카드":"WOORI","하나카드":"HANA","NH농협카드":"NH","BC카드":"BC","IBK기업":"IBK"}
SKIP = re.compile(r"(발급\s*중단|발급\s*종료|BIZ|법인|패밀리|후불\s*하이패스|화물|공무원연금)")

def _get(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code == 429:        # rate limit → backoff
                time.sleep(5 * (i + 1)); continue
            return ""
        except Exception:
            time.sleep(2); continue
    return ""

# ---- 토스 어댑터 ----
CARD_LINK = re.compile(r"card/(\d+)")
FEE_RE = re.compile(r"연회비(.+?)전월실적")
def fetch_toss_search(brand_code):
    """검색 페이지 SSR → [{id, name, fee, url}] (인기순 전체)."""
    html = _get(f"{TOSS}/search?filters={brand_code}&sortType=POPULARITY")
    out, seen = [], set()
    # 각 카드 항목: [{name}비교함 담기{tag}{name}연회비 ... 월 최대 혜택 ...](.../card/{id}?...)
    for m in re.finditer(r"\[([^\]]+?)비교함 담기([^\]]*?)\]\((https://card-lounge\.toss\.im/card/(\d+)[^\)]*)\)", html):
        name = m.group(1).strip()
        cid = m.group(4)
        if cid in seen or SKIP.search(name): continue
        seen.add(cid)
        fee = ""
        fm = FEE_RE.search(m.group(2))
        if fm:
            fee = re.split(r"전월실적", fm.group(1))[0].strip()
        out.append({"id": cid, "name": name, "fee": fee, "url": f"{TOSS}/card/{cid}"})
    return out

IMG_RE = re.compile(r"!\[[^\]]*카드 이미지\]\((https://static\.toss\.im/assets/credit-card/[^\)]+?)\)")
def fetch_toss_image(card_id):
    """상세 페이지 → 첫 '카드 이미지' 실제 src (없으면 '')."""
    html = _get(f"{TOSS}/card/{card_id}")
    m = IMG_RE.search(html)
    return m.group(1) if m else ""

def collect_toss(limit_per_issuer=40, sleep=0.6):
    result = {}
    for issuer, code in BRANDS.items():
        cards = fetch_toss_search(code)[:limit_per_issuer]
        rows = []
        for c in cards:
            img = fetch_toss_image(c["id"]); time.sleep(sleep)
            if not img:   # 이미지 없으면 스킵(임의생성 금지)
                continue
            rows.append({"issuer": issuer, "name": c["name"], "img": img, "fee": c["fee"],
                         "benefit": "", "url": c["url"]})
        result[issuer] = rows
        print(f"  토스 {issuer}: {len(rows)}장")
    return result

# ---- 확장 어댑터 자리 (Playwright 필요) ----
def collect_issuer_official(issuer): return []      # 카드사 공식(우선 소스)
def collect_events(): return []                     # 아정당/카드고릴라/뱅크샐러드/카카오 이벤트

# ---- dedup (카드사 우선) ----
def norm(n): return re.sub(r"[\s()（）·\-_/+]+", "", n).lower()
def merge(issuer_rows, toss_rows):
    by = {norm(c["name"]): c for c in toss_rows}
    for c in issuer_rows:               # 카드사 소스로 덮어쓰기(우선)
        by[norm(c["name"])] = {**by.get(norm(c["name"]), {}), **c}
    return list(by.values())

# ---- DB 적재 ----
def upsert(con, cards):
    cur = con.cursor()
    cur.execute("DELETE FROM card")
    for c in cards:
        cur.execute("INSERT INTO card(issuer,name,img,fee,benefit,source_url) VALUES(?,?,?,?,?,?)",
                    (c["issuer"], c["name"], c.get("img",""), c.get("fee",""), c.get("benefit",""), c.get("url","")))
    con.commit()

def main():
    print("카드티라노 콜렉터 시작 (토스 어댑터)")
    toss = collect_toss()
    all_cards = []
    for issuer in BRANDS:
        all_cards += merge(collect_issuer_official(issuer), toss.get(issuer, []))
    print(f"총 카드 {len(all_cards)}장 수집")
    try:
        con = sqlite3.connect("cardtyrano.db"); upsert(con, all_cards); con.close()
        print("DB 갱신 완료 → build_data.py export → 배포 단계로")
    except Exception as e:
        print("DB 미연결(스키마 먼저 생성 필요):", e)

if __name__ == "__main__":
    main()
