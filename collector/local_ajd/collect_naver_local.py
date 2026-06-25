# -*- coding: utf-8 -*-
"""
네이버페이 카드 로컬 수집기 (v2 · Playwright 렌더링 텍스트 방식) — 거주지 IP(회원님 맥)에서 실행.

배경
  - card.pay.naver.com 의 .json API는 데이터센터(GitHub Actions) IP엔 404.
  - Claude의 브라우저(Claude in Chrome)도 이 결제 도메인은 안전제한으로 차단됨.
  → 회원님 맥에서 도는 Playwright(헤드리스 크롬)엔 이런 제한이 없으므로 여기서 수집한다.
    (뱅크샐러드·프테라노돈에서 검증된 '렌더링된 화면 텍스트 읽기' 방식과 동일)

동작
  1) 프로모션 목록을 가져온다.
     - 1순위: 브라우저 컨텍스트에서 promotionsList API(JSON) 로드(거주지 IP+쿠키라 정상 응답).
     - 실패 시: 이벤트 허브 페이지의 렌더링 텍스트/HTML에서 promotionId 추출.
  2) 각 프로모션 페이지를 열어 **렌더링된 본문 텍스트**를 읽고
     - 우리 카드 유니버스(cg_seed.json/products.json)에 있는 카드명이 텍스트에 등장하면 매칭
     - '최대 N만원' 등 금액을 추출 → reward_won
  3) naver_seed.json 작성(스키마는 collector.py가 읽는 형식과 동일):
        cards: { "카드명": {reward_won, reward_text, company, promotionId, url} }
  4) 진단용 naver_raw.json 도 함께 저장(프로모션별 원본 텍스트). 1차 실행 후 매칭이 적으면
     이 파일을 Claude에게 주면 파서를 그 구조에 맞게 확정한다.
  5) --push 면 git add/commit/push (아정당 로컬 수집과 동일 패턴).

준비(최초 1회)
  pip3 install playwright
  python3 -m playwright install chromium

실행
  python3 collector/local_ajd/collect_naver_local.py            # 수집 + 진단 덤프
  python3 collector/local_ajd/collect_naver_local.py --headed    # 브라우저 띄워 눈으로 확인
  python3 collector/local_ajd/collect_naver_local.py --push      # 수집 + git push
"""
import json, re, os, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))      # collector/local_ajd/
BASE = os.path.dirname(HERE)                            # collector/
SEED = os.path.join(BASE, "naver_seed.json")
RAW  = os.path.join(HERE, "naver_raw.json")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

HUB        = "https://card.pay.naver.com/home/promotion/event"
PROMO_LIST = "https://card.pay.naver.com/home/api/promotionsList?formedYn=y"
PROMO_PAGE = ("https://card.pay.naver.com/home/promotion"
              "?promotionId={pid}&cardCompanyId={cc}&cardIssuerCode={ic}")

# 카드사 코드 → 표기명 (reward_text 용). 미확인 코드는 렌더링 텍스트에서 보강된다.
ISSUER = {"CCKM": "KB국민", "CCKB": "KB국민", "CCWR": "우리", "CCNH": "NH농협",
          "CCLG": "롯데", "CCLO": "롯데", "CCSS": "삼성", "CCSH": "신한",
          "CCHN": "하나", "CCBC": "비씨", "CCHD": "현대", "CCDI": "현대"}

def _nk(s):  # 정규화(공백/기호 제거, 소문자)
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def our_universe():
    """우리 사이트가 다루는 카드명 집합 → {정규화명: 표기명}."""
    uni = {}
    for fn, key in [("cg_seed.json", "cards"), ("products.json", None)]:
        try:
            data = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
            rows = data.get("cards", []) if key else data
            for r in rows:
                nm = r[1] if isinstance(r, list) else (r.get("name") if isinstance(r, dict) else None)
                if nm:
                    uni[_nk(nm)] = nm
        except Exception:
            pass
    return uni

_AMT = re.compile(r"(?:최대\s*)?([0-9][0-9,]*)\s*만\s*원")
_AMT_WON = re.compile(r"([0-9][0-9,]{3,})\s*원")

def best_won(text):
    """텍스트에서 가장 큰 '만원' 금액을 원 단위로. 없으면 가장 큰 '원' 금액."""
    best = 0
    for m in _AMT.finditer(text):
        v = int(m.group(1).replace(",", "")) * 10000
        if v > best: best = v
    if best:
        return best
    for m in _AMT_WON.finditer(text):
        v = int(m.group(1).replace(",", ""))
        if 10000 <= v <= 5000000 and v > best:
            best = v
    return best

def parse_promo_list_json(txt):
    """promotionsList 응답(JSON 문자열)에서 (promotionId, cardCompanyId, cardIssuerCode) 추출."""
    try:
        j = json.loads(txt)
    except Exception:
        return []
    out, seen = [], set()
    def walk(x):
        if isinstance(x, dict):
            pid = x.get("promotionId")
            if pid and str(pid) not in seen:
                seen.add(str(pid))
                out.append({"pid": str(pid),
                            "cc": x.get("cardCompanyId") or x.get("companyId") or "",
                            "ic": x.get("cardIssuerCode") or x.get("issuerCode") or
                                  x.get("cardCompanyId") or ""})
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(j)
    return out

def main():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("Playwright 미설치. → pip3 install playwright && python3 -m playwright install chromium")
        sys.exit(1)

    uni = our_universe()
    print(f"우리 카드 유니버스 {len(uni)}개 로드")
    headed = "--headed" in sys.argv
    raw = {"as_of": datetime.date.today().isoformat(), "promos": [], "events": []}
    cards = {}

    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=not headed)
        ctx = b.new_context(user_agent=UA, locale="ko-KR",
                            viewport={"width": 1280, "height": 1200})
        pg = ctx.new_page()

        # 0) 허브 먼저 열어 쿠키/세션 확보
        try:
            pg.goto(HUB, wait_until="networkidle", timeout=40000)
            pg.wait_for_timeout(1500)
            raw["hub_text"] = pg.inner_text("body")[:4000]
        except Exception as e:
            raw["hub_err"] = str(e)[:120]

        # 1) 프로모션 목록 (브라우저 컨텍스트에서 API JSON 로드)
        promos = []
        try:
            pg.goto(PROMO_LIST, wait_until="domcontentloaded", timeout=40000)
            pg.wait_for_timeout(800)
            txt = pg.inner_text("body")
            raw["promo_list_sample"] = txt[:800]
            promos = parse_promo_list_json(txt)
        except Exception as e:
            raw["promo_list_err"] = str(e)[:120]
        # 폴백: 허브 텍스트/HTML에서 promotionId 패턴 긁기
        if not promos:
            html = ""
            try: html = pg.content()
            except Exception: pass
            for pid in dict.fromkeys(re.findall(r"promotionId[\"'=:\s]+([0-9]{14,})", html)):
                promos.append({"pid": pid, "cc": "", "ic": ""})
        raw["promo_count"] = len(promos)
        print(f"프로모션 {len(promos)}건 발견")

        # 2) 각 프로모션 페이지 렌더링 텍스트 → 카드 매칭 + 금액
        for i, pr in enumerate(promos[:60]):
            url = PROMO_PAGE.format(pid=pr["pid"], cc=pr["cc"], ic=pr["ic"] or pr["cc"])
            try:
                pg.goto(url, wait_until="networkidle", timeout=40000)
                pg.wait_for_timeout(1200)
                t = pg.inner_text("body")
            except Exception as e:
                raw["events"].append({"pid": pr["pid"], "err": str(e)[:80]})
                continue
            won = best_won(t)
            iss = ISSUER.get(pr["cc"], "")
            # 카드 매칭: 유니버스 카드명이 페이지 텍스트에 등장하면 부착
            nt = _nk(t)
            hit = []
            for nk, name in uni.items():
                if len(nk) >= 4 and nk in nt:
                    hit.append(name)
            rtext = (f"최대 {won//10000}만원" if won else "이벤트") + \
                    (f" (네이버페이 {iss}카드 이벤트)" if iss else " (네이버페이 카드 이벤트)")
            for name in hit:
                # 더 큰 금액으로만 갱신(같은 카드가 여러 프로모션에 걸칠 때)
                if name not in cards or won > cards[name]["reward_won"]:
                    cards[name] = {"reward_won": won, "reward_text": rtext,
                                   "company": pr["cc"], "promotionId": pr["pid"], "url": url}
            raw["events"].append({"pid": pr["pid"], "cc": pr["cc"], "won": won,
                                  "matched": hit, "text": t[:600]})
            if (i + 1) % 10 == 0:
                print(f"  진행 {i+1}/{min(len(promos),60)}  (누적 매칭 {len(cards)})")

        b.close()

    # 3) 저장
    json.dump(raw, open(RAW, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = {"as_of": datetime.date.today().strftime("%Y-%m"),
           "source": "네이버페이 거주지 Playwright 렌더링 텍스트 수집(collect_naver_local.py v2)",
           "cards": cards}
    json.dump(out, open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n진단 덤프 : {RAW}")
    print(f"네이버 시드: {SEED}  (매칭 {len(cards)}건)")
    if len(cards) < 5:
        print("※ 매칭이 적습니다. naver_raw.json 을 Claude에게 주시면 페이지 구조에 맞게 파서를 확정합니다.")

    if "--push" in sys.argv:
        try:
            subprocess.run(["git", "-C", BASE, "add", "naver_seed.json", "local_ajd/naver_raw.json"], check=True)
            subprocess.run(["git", "-C", BASE, "commit", "-m",
                            f"naver local collect (rendered) {datetime.date.today()}"], check=True)
            subprocess.run(["git", "-C", BASE, "push"], check=True)
            print("git push 완료 → Cloudflare 자동 배포")
        except subprocess.CalledProcessError as e:
            print("git 실패(변경 없음/인증 필요):", e)

if __name__ == "__main__":
    main()
