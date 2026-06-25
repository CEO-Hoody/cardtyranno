# -*- coding: utf-8 -*-
"""
프테라노돈(pteranodon) — 결제처(가맹점)별 카드 결제할인 수집기.

용각류(brachio/apato/diplo/bronto/mamenchi)는 '카드 발급 캐시백'을 모으고,
프테라노돈은 '무신사·쿠팡·하이마트 등 결제처에서 특정 카드로 결제 시 받는 할인'을 모은다.

왜 거주지(로컬)인가:
  결제처/카드사 이벤트 페이지는 대부분 JS로 렌더링되고, 데이터센터 IP엔 다르게 응답하거나 막힌다.
  그래서 회원님 맥(거주지 IP)에서 헤드리스 브라우저(Playwright)로 '렌더링된 화면 텍스트'를 읽어
  (카드사 + 금액 + 할인유형)을 추출한다. — 카드 캐시백에서 검증된 방식과 동일.

산출물:
  collector/discount_seed.json   (site/data.json 과 동일한 항목 스키마)
  → build_data.py 가 이를 읽어 site/data.json 에 병합(merge) 한다.

준비(최초 1회):
  pip3 install playwright
  python3 -m playwright install chromium

실행:
  python3 collector/pteranodon.py            # 수집만(discount_seed.json 갱신)
  python3 collector/pteranodon.py --push      # 수집 + git add/commit/push
  python3 collector/pteranodon.py --dry        # 1개 결제처만 테스트 출력(브라우저 없이 파서 점검)
"""
import json, os, re, sys, subprocess, datetime

BASE = os.path.dirname(os.path.abspath(__file__))           # collector/
SEED = os.path.join(BASE, "discount_seed.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# ── 결제처 레지스트리 ────────────────────────────────────────────────────────
# plat: 결제처명 / domain / gubun(온라인·오프라인) / url: 결제할인을 렌더링하는 소스 페이지
#   - "own": 결제처 자체 이벤트 페이지(가장 깔끔)  /  "issuer": 카드사 행사 페이지(가맹점 행사 모음)
# 회원님이 항목을 추가/수정하면 그만큼 더 수집됩니다.
MERCHANTS = [
    {"plat": "무신사",     "domain": "musinsa.com",  "gubun": "온라인", "src": "own",
     "url": "https://www.musinsa.com/campaign/payevent/0"},
    {"plat": "롯데하이마트", "domain": "himart.co.kr", "gubun": "온라인", "src": "own",
     "url": "https://company.himart.co.kr/event/card"},
    {"plat": "GS샵",       "domain": "gsshop.com",   "gubun": "온라인", "src": "own",
     "url": "https://www.gsshop.com/shop/planCard.gs"},
    {"plat": "G마켓",      "domain": "gmarket.co.kr", "gubun": "온라인", "src": "own",
     "url": "https://www.gmarket.co.kr/n/showroom/samsungcard"},
    {"plat": "옥션",       "domain": "auction.co.kr", "gubun": "온라인", "src": "own",
     "url": "https://www.auction.co.kr/n/showroom/samsungcard"},
    {"plat": "교보문고",   "domain": "kyobobook.co.kr", "gubun": "온라인", "src": "own",
     "url": "https://event.kyobobook.co.kr/detail/204081"},
    {"plat": "11번가",     "domain": "11st.co.kr",   "gubun": "온라인", "src": "own",
     "url": "https://plan.11st.co.kr/plan/front/exhibitions/2014938/"},
    # 카드사 행사 페이지(여러 가맹점 결제할인 모음) — src=issuer
    {"plat": "KB국민카드 행사", "domain": "kbcard.com", "gubun": "온라인", "src": "issuer",
     "url": "https://card.kbcard.com/CRD/DVIEW/HCAMCXPRICAC0076"},
]
# ★ 결제처 전체 목록은 collector/discount_sources.json(레지스트리)에서 읽는다(43개 결제처).
#   위 MERCHANTS는 레지스트리가 없을 때의 폴백. 결제처 추가/수정은 discount_sources.json에서.
REGISTRY = os.path.join(BASE, "discount_sources.json")

def _load_registry():
    try:
        ms = json.load(open(REGISTRY, encoding="utf-8")).get("merchants") or []
        if ms:
            return ms
    except Exception as e:
        print("[프테라노돈] 레지스트리 로드 실패, 폴백 사용:", str(e)[:60])
    return MERCHANTS

# 할인을 식별하는 키워드
ISSUERS = ["삼성카드", "현대카드", "신한카드", "KB국민카드", "국민카드", "롯데카드", "우리카드",
           "하나카드", "NH농협카드", "농협카드", "BC카드", "IBK", "카카오뱅크", "카카오페이",
           "토스", "네이버페이", "씨티", "케이뱅크"]
ISSUER_NORM = {"국민카드": "KB국민카드", "농협카드": "NH농협카드"}
TYPE_KW = [("즉시할인", "즉시할인"), ("청구할인", "청구할인"), ("페이백", "페이백"),
           ("캐시백", "캐시백"), ("적립", "적립"), ("쿠폰", "쿠폰할인"),
           ("바우처", "캐시백/바우처"), ("포인트", "포인트적립"), ("할인", "즉시할인")]
PERIOD_RE = re.compile(r"(\d{1,2})[.\-/](\d{1,2})\s*[~\-]\s*(\d{1,2})[.\-/](\d{1,2})")
AMT_RE = re.compile(r"(\d[\d,]*\s*원|\d{1,3}\s*%|\d[\d,]*\s*만원)")
MIN_RE = re.compile(r"([\d,]+\s*원)\s*이상")

def _nk(s): return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def _today(): return datetime.date.today().isoformat()

def _find_issuer(s):
    for k in ISSUERS:
        if k in s:
            return ISSUER_NORM.get(k, k)
    return None

def _find_type(s):
    for kw, label in TYPE_KW:
        if kw in s:
            return label
    return ""

def parse_discounts(text, merchant):
    """렌더링 텍스트 → 결제처 카드할인 항목 리스트(data.json 스키마).
    한 세그먼트(줄)에 '카드사 + 금액 + 할인유형'이 함께 있으면 한 항목으로 본다.
    완벽하진 않지만(결제처마다 마크업이 달라) 핵심 라인은 잡힌다. 결과를 보고 키워드/소스를 보강하면 정확해진다."""
    out = []
    if not text:
        return out
    segs = re.split(r"[\n\r]+|(?<=[원%])\s{2,}", text)
    period_global = None
    pg = PERIOD_RE.search(text)
    if pg:
        period_global = f"{int(pg.group(1)):02d}.{int(pg.group(2)):02d}~{int(pg.group(3)):02d}.{int(pg.group(4)):02d}"
    for s in segs:
        s = (s or "").strip()
        if not s or len(s) > 90:
            continue
        iss = _find_issuer(s)
        mn = MIN_RE.search(s)
        sclean = re.sub(r"[\d,]+\s*원\s*이상", " ", s)   # 임계금액('N원 이상')은 할인액이 아니므로 제거 후 추출
        amt = AMT_RE.search(sclean)
        if not iss or not amt:
            continue
        typ = _find_type(s)
        if not typ:
            continue
        pr = PERIOD_RE.search(s)
        period = (f"{int(pr.group(1)):02d}.{int(pr.group(2)):02d}~{int(pr.group(3)):02d}.{int(pr.group(4)):02d}"
                  if pr else (period_global or ""))
        out.append({
            "plat": merchant["plat"], "domain": merchant["domain"], "gubun": merchant["gubun"],
            "card": iss,                      # 카드명 상세가 없으면 카드사로(이후 보강)
            "tab": iss,
            "type": typ,
            "min": (mn.group(1).replace(" ", "") if mn else ""),
            "disc": amt.group(1).replace(" ", ""),
            "cond": "", "period": period,
            "conf": "중",                     # 자동수집은 신뢰도 '중'(수기검증 시 '상')
            "url": merchant["url"],
        })
    # 동일 (카드사+할인액+유형) 중복 제거
    seen, uniq = set(), []
    for d in out:
        k = (d["card"], d["disc"], d["type"])
        if k in seen:
            continue
        seen.add(k); uniq.append(d)
    return uniq

# ── 수집(Playwright 렌더링 텍스트) ───────────────────────────────────────────
def collect():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("[프테라노돈] Playwright 미설치 → 중단. 'pip3 install playwright && python3 -m playwright install chromium' 후 재실행")
        return []
    items = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        merchants = _load_registry()
        print(f"[프테라노돈] 결제처 {len(merchants)}곳 수집 시작")
        for m in merchants:
            try:
                page.goto(m["url"], wait_until="networkidle", timeout=35000)
                page.wait_for_timeout(1200)
                text = page.inner_text("body")
                got = parse_discounts(text, m)
                print(f"[프테라노돈] {m['plat']:<10} {len(got)}건")
                items.extend(got)
            except Exception as e:
                print(f"[프테라노돈] {m['plat']} 실패: {str(e)[:70]}")
        browser.close()
    # id 부여
    for i, d in enumerate(items):
        d["id"] = i
    return items

DATA = os.path.join(os.path.dirname(BASE), "site", "data.json")   # 사이트가 직접 읽는 결제처 할인

def write_seed(items):
    json.dump({"month": datetime.date.today().strftime("%Y-%m"), "updated": _today(),
               "source": "pteranodon(거주지 렌더링 텍스트 수집)", "items": items},
              open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장 → discount_seed.json ({len(items)}건, {len(set(d['plat'] for d in items))}개 결제처)")

def merge_into_data(items):
    """site/data.json 에 병합 — 수기 항목(conf '상')은 보존, 신규 자동수집 항목만 추가/갱신.
    중복키=(결제처+카드+할인액+유형). 거주지 실행만으로 사이트(discount.html)에 바로 반영된다."""
    try:
        doc = json.load(open(DATA, encoding="utf-8"))
    except Exception:
        doc = {"month": datetime.date.today().strftime("%Y-%m"), "source": "db", "items": []}
    seen = {(d["plat"], d.get("card"), d.get("disc"), d.get("type")) for d in doc["items"]}
    add = 0
    for it in items:
        k = (it["plat"], it.get("card"), it.get("disc"), it.get("type"))
        if k not in seen:
            doc["items"].append(it); seen.add(k); add += 1
    for i, d in enumerate(doc["items"]):
        d["id"] = i
    json.dump(doc, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"site/data.json 병합 +{add}건 (총 {len(doc['items'])}건)")

def git_push():
    try:
        subprocess.run(["git", "-C", os.path.dirname(BASE), "add", "collector/discount_seed.json", "site/data.json"], check=True)
        subprocess.run(["git", "-C", os.path.dirname(BASE), "commit", "-m", "pteranodon: 결제처 카드할인 수집 " + _today()], check=True)
        for _ in range(3):
            try:
                subprocess.run(["git", "-C", os.path.dirname(BASE), "pull", "--no-rebase", "-X", "ours", "--no-edit", "origin", "main"], check=True)
                subprocess.run(["git", "-C", os.path.dirname(BASE), "push", "origin", "main"], check=True)
                print("git push 완료"); return
            except subprocess.CalledProcessError:
                continue
    except subprocess.CalledProcessError as e:
        print("git push 실패(수동 필요):", e)

def main():
    if "--dry" in sys.argv:   # 파서 점검(샘플 텍스트)
        sample = ("무신사 페이 이벤트 06.01~06.30\n삼성카드 31,000원 이상 결제 시 30,000원 즉시할인\n"
                  "현대카드 10% 청구할인\n네이버페이 5,000원 적립")
        for d in parse_discounts(sample, MERCHANTS[0]):
            print(d)
        return
    items = collect()
    if items:
        write_seed(items)
        merge_into_data(items)
        if "--push" in sys.argv:
            git_push()
    else:
        print("[프테라노돈] 수집 0건 — 소스 페이지 구조 변동/차단 가능. MERCHANTS의 url 점검 필요.")

if __name__ == "__main__":
    main()
