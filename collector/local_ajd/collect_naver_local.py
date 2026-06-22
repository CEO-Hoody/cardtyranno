# -*- coding: utf-8 -*-
"""
네이버페이 카드 로컬 수집기 — 거주지 IP(회원님 맥)에서 실행.

배경: 네이버 card.pay.naver.com 의 .json API는 데이터센터(GitHub Actions) IP엔 404를 줍니다.
     회원님 맥(거주지 IP)에선 정상이라, 여기서 수집해 결과를 깃에 올립니다(아정당과 동일 패턴).

확인된 엔드포인트(회원님 네트워크 캡처):
  - 프로모션 목록: https://card.pay.naver.com/home/api/promotionsList?formedYn=y  (★진입점: 전체 6월 이벤트)
  - 카드 목록:    https://card.pay.naver.com/home/api/productsList  (프로모션 대상 카드)
  - 프로모션상세: https://card.pay.naver.com/home/promotion.json?promotionId=..&cardCompanyId=..&cardIssuerCode=..
  - 카드상세:     https://card.pay.naver.com/home/detail.json?cardCompanyId=..&cardIssuerCode=..&productId=..
  발급사 코드 예: CCLG=롯데, CCWR=우리, CCNH=NH농협

동작:
  1) 위 엔드포인트들을 호출해 **원본 응답을 naver_raw.json 으로 덤프**(필드 구조 확인용)
  2) 가능한 범위에서 카드명↔(company/productId/promotionId)+리워드를 추출해 naver_seed.json 작성
  3) (옵션) --push 로 git add/commit/push

준비:  pip3 install requests
실행:
  python3 collect_naver_local.py            # 수집 + 원본 덤프
  python3 collect_naver_local.py --push     # 수집 + git push

※ 1차 실행 후 naver_raw.json 을 Claude에게 주시면, 응답 구조에 맞춰 파서를 확정해 드립니다.
"""
import json, re, os, sys, subprocess, datetime
import urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # collector/
SEED = os.path.join(BASE, "naver_seed.json")
RAW  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "naver_raw.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
H = {"User-Agent": UA, "Referer": "https://card.pay.naver.com/",
     "Accept": "application/json, text/plain, */*", "X-Requested-With": "XMLHttpRequest"}

EVENT_URLS = ["https://card.pay.naver.com/home/api/promotionsList?formedYn=y",
              "https://card.pay.naver.com/home/api/event.json"]
PRODUCTS_URLS = ["https://card.pay.naver.com/home/api/productsList"]
PROMO = "https://card.pay.naver.com/home/promotion.json"

def get(url, params=None, data=None):
    if params: url = url + "?" + urllib.parse.urlencode(params)
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=dict(H, **({"Content-Type":"application/json"} if data else {})))
    with urllib.request.urlopen(req, timeout=20) as r:
        t = r.read().decode("utf-8", "ignore")
    try: return json.loads(t)
    except Exception: return {"_nonjson": t[:500], "_status": "parse_fail"}

def deep_find(o, keyset):
    """중첩 구조에서 keyset 중 하나라도 키로 가진 dict들을 수집."""
    out = []
    def w(x):
        if isinstance(x, dict):
            if any(k in x for k in keyset): out.append(x)
            for v in x.values(): w(v)
        elif isinstance(x, list):
            for v in x: w(v)
    w(o); return out

def _nk(s): return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def our_universe():
    uni = {}
    for fn, k in [("cg_seed.json","cards"),("products.json",None)]:
        try:
            data = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
            rows = data.get("cards", []) if k else data
            for r in rows:
                nm = r[1] if isinstance(r, list) else r["name"]
                uni[_nk(nm)] = nm
        except Exception: pass
    return uni

def main():
    raw = {"as_of": datetime.date.today().isoformat(), "events": None, "products": [], "promotions": []}
    # 1) 이벤트 목록
    events = None
    for u in EVENT_URLS:
        try:
            j = get(u);
            if isinstance(j, (list, dict)) and "_nonjson" not in (j if isinstance(j,dict) else {}):
                events = j; raw["events_url"] = u; break
        except Exception as e:
            raw.setdefault("event_err", []).append(f"{u}: {e}")
    raw["events"] = events

    # 이벤트에서 (promotionId, cardCompanyId, cardIssuerCode) 추출
    promos = deep_find(events or {}, ["promotionId"])
    seen = set(); plist = []
    for p in promos:
        pid = str(p.get("promotionId") or "")
        if not pid or pid in seen: continue
        seen.add(pid)
        plist.append({"promotionId": pid,
                      "cardCompanyId": p.get("cardCompanyId") or p.get("companyId"),
                      "cardIssuerCode": p.get("cardIssuerCode") or p.get("issuerCode")})
    raw["promo_ids"] = plist[:30]

    # 2) 각 프로모션의 대상 카드 + 리워드
    uni = our_universe(); cards = {}
    for pr in plist[:30]:
        for pu in PRODUCTS_URLS:
            for call in ("get", "post"):
                try:
                    j = get(pu, params=pr) if call=="get" else get(pu, data=pr)
                    if isinstance(j, dict) and "_nonjson" in j: continue
                    raw["products"].append({"promotionId": pr["promotionId"], "resp_keys": list(j.keys()) if isinstance(j,dict) else "list"})
                    # 카드 추출
                    for c in deep_find(j, ["productId"]):
                        nm = c.get("cardName") or c.get("name") or c.get("productName")
                        prod = str(c.get("productId") or "")
                        if not nm or not prod: continue
                        ourname = uni.get(_nk(nm))
                        if ourname:
                            cards[ourname] = {"company": pr.get("cardCompanyId"), "issuer": pr.get("cardIssuerCode"),
                                              "productId": prod, "promotionId": pr["promotionId"]}
                    break
                except Exception as e:
                    raw.setdefault("products_err", []).append(f"{pr['promotionId']} {call}: {str(e)[:60]}")
            else: continue
            break
        # 프로모션 리워드
        try:
            pj = get(PROMO, params=pr)
            raw["promotions"].append({"promotionId": pr["promotionId"], "keys": list(pj.keys()) if isinstance(pj,dict) else "list",
                                      "sample": json.dumps(pj, ensure_ascii=False)[:400]})
        except Exception as e:
            raw.setdefault("promo_err", []).append(str(e)[:60])

    json.dump(raw, open(RAW, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"as_of": datetime.date.today().strftime("%Y-%m"), "cards": cards},
              open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"원본 덤프: {RAW}")
    print(f"네이버 시드: {SEED}  (매칭 {len(cards)}건)")
    print("※ naver_raw.json 을 Claude에게 주시면 파서를 확정합니다.")

    if "--push" in sys.argv:
        try:
            subprocess.run(["git","-C",BASE,"add","naver_seed.json","local_ajd/naver_raw.json"], check=True)
            subprocess.run(["git","-C",BASE,"commit","-m",f"naver local collect {datetime.date.today()}"], check=True)
            subprocess.run(["git","-C",BASE,"push"], check=True)
            print("git push 완료")
        except subprocess.CalledProcessError as e:
            print("git 실패(변경 없음/인증 필요):", e)

if __name__ == "__main__":
    main()
