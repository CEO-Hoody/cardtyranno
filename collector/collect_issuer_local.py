# -*- coding: utf-8 -*-
"""
카드사 자체 이벤트 로컬 수집기 — 거주지 IP(회원님 맥)에서 실행.

배경: 각 카드사(삼성·현대·KB국민·신한·롯데·우리·하나·NH농협·IBK) 자체 사이트의 '발급 캐시백/프로모션'
이벤트는 카드고릴라·토스 등 중개 플랫폼과 별개다. 카드사 사이트는 (1) 데이터센터 IP에서 차단되거나
(2) 클라이언트 렌더(SPA)라 plain HTTP로는 빈 셸만 받는다. 그래서 collect_ajd_local.py와 동일하게
**거주지 IP + Playwright 헤드리스 렌더**로 수집한다.

흐름(제네릭, 카드사 무관):
  1) issuer_event_urls.json 의 카드사별 '이벤트 리스트 URL' 렌더
  2) 리스트에서 이벤트 상세 링크 발견(공통 이벤트 URL 패턴) — 없으면 리스트 페이지 자체를 파싱
  3) 각 상세(또는 리스트) 렌더 → 텍스트에서
       · 전체 캐시백 = '최대 N만원(캐시백/혜택/받기)' 헤드라인 최대값
       · 주요 = 'N만원 이상/쓰면/결제 시 M만원' 첫 보상(결제 캐시백) · 부가 = 전체 - 주요
       · 카드 = **우리 카드 유니버스(해당 발급사)를 텍스트에 역매칭** (카드명 추출 대신, ajd와 동일 철학)
  4) issuer_seed.json 저장 (collector.py가 네이버/아정당 시드와 동일 패턴으로 주입)

준비:  pip3 install playwright && python3 -m playwright install chromium
실행:  python3 collector/collect_issuer_local.py            # 수집만
       python3 collector/collect_issuer_local.py --push     # 수집 + git add/commit/push
       python3 collector/collect_issuer_local.py --only 삼성카드   # 특정 카드사만(디버그)

⚠ 카드사 이벤트 리스트 URL은 사이트 개편으로 바뀐다. 처음 실행 후 '0건'인 카드사는
   브라우저에서 그 카드사 '이벤트' 메뉴 URL을 복사해 issuer_event_urls.json 에서 교체하세요.
   (SETUP.md 참고. 삼성카드 URL은 2026-06 기준 확인됨.)
"""
import json, re, os, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))            # collector/
sys.path.insert(0, HERE)                                     # headless 모듈
SEED = os.path.join(HERE, "issuer_seed.json")
URLS_CFG = os.path.join(HERE, "issuer_event_urls.json")

ISSUERS = ["삼성카드","현대카드","KB국민카드","신한카드","롯데카드","우리카드","하나카드","NH농협카드","IBK기업은행"]

# 이벤트 상세 링크로 볼 만한 공통 URL 조각(카드사별 상이 → 느슨하게)
DETAIL_HINT = re.compile(r"(event|evnt|evt|/ev/|cms_id=|eventId=|seq=|notiId=|prmtn|promotion|EVENT)", re.I)
# 보상 금액 패턴
AMT_HEAD = re.compile(r"최대\s*([\d,]+(?:\.\d+)?)\s*만\s*원?")                 # 헤드라인 최대 N만원
TIER_MAIN = re.compile(r"(\d[\d,]*)\s*만\s*원?\s*(?:이상|쓰면|쓰고|결제\s*시|이용\s*시)\D{0,12}?(\d[\d,]*)\s*만\s*원?")  # N만원 쓰면 M만원

def _nk(s):
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def render(url):
    import headless
    return headless.render_html(url, wait_selector="body", timeout=40000) or ""

def universe_by_issuer():
    """발급사 → { _nk(카드명): 카드명 }. cross-issuer 오매칭 방지 위해 발급사로 분리."""
    by = {}
    try:
        cg = json.load(open(os.path.join(HERE, "cg_seed.json"), encoding="utf-8")).get("cards", [])
        for r in cg:                                  # [id, name, issuer]
            if isinstance(r, list) and len(r) >= 3 and r[1]:
                by.setdefault(r[2], {})[_nk(r[1])] = r[1]
    except Exception as e:
        print("cg_seed universe", e)
    try:
        for p in json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8")):
            if p.get("name") and p.get("issuer"):
                by.setdefault(p["issuer"], {})[_nk(p["name"])] = p["name"]
    except Exception as e:
        print("products universe", e)
    return by

def _alias(issuer):
    """issuer_event_urls.json 키와 유니버스 발급사명 매칭용(예: 'KB국민카드'↔'KB국민')."""
    return issuer.replace("카드","").replace("기업은행","").replace("농협","").strip()

def discover_details(html, base):
    out = []
    for m in re.finditer(r'href="([^"#]+)"', html):
        u = m.group(1)
        if DETAIL_HINT.search(u):
            if u.startswith("/"):
                u = re.sub(r"(https?://[^/]+).*", r"\1", base) + u
            if u.startswith("http"): out.append(u)
    # 중복 제거, 너무 많으면 상위 40개
    seen = set(); uniq = [x for x in out if not (x in seen or seen.add(x))]
    return uniq[:40]

def parse_amounts(text):
    """전체(최대 N만원) + 주요(결제 캐시백) + 부가(전체-주요). 원 단위."""
    t = re.sub(r"\s+", " ", text)
    heads = [int(float(x.replace(",", "")) * 10000) for x in AMT_HEAD.findall(t)]
    heads = [w for w in heads if 0 < w <= 5_000_000]
    total = max(heads) if heads else 0
    main = 0
    tm = TIER_MAIN.search(t)
    if tm:
        main = int(tm.group(2).replace(",", "")) * 10000        # 받는 금액(둘째 수)
        if main > total and total: main = 0
    bonus = max(total - main, 0) if (main and total and main < total) else 0
    if not main and total: main = total                          # 분해 못 하면 주요=전체
    return total, main, bonus

def collect_issuer(issuer, urls, uni):
    cards = {}
    alias = _alias(issuer)
    ucards = {}
    for k, v in uni.items():                                     # 발급사명 느슨 매칭
        if alias and (alias in k.replace(" ", "") or alias in v):
            ucards.update(uni[k])
    if not ucards: ucards = uni.get(issuer, {})
    for list_url in urls:
        try:
            lh = render(list_url)
        except Exception as e:
            print(f"  ✗ {issuer} 리스트 렌더 실패 {str(e)[:40]}"); continue
        if not lh: continue
        details = discover_details(lh, list_url)
        targets = details if details else [list_url]            # 상세 못 찾으면 리스트 자체 파싱
        for du in targets:
            try:
                dh = render(du) if du != list_url else lh
            except Exception:
                continue
            txt = re.sub(r"<[^>]+>", " ", dh)
            total, main, bonus = parse_amounts(txt)
            if not total: continue
            nt = _nk(txt)
            hit = [name for nk, name in ucards.items() if len(nk) >= 5 and nk in nt]
            for nm in hit:
                cur = cards.get(nm)
                if not cur or total > cur["reward_won"]:
                    cards[nm] = {"issuer": issuer, "reward_won": total, "main_won": main,
                                 "bonus_won": bonus,
                                 "reward_text": f"최대 {_man(total)}만원 ({issuer} 발급 이벤트)",
                                 "url": du}
        print(f"  · {issuer}: 상세 {len(targets)}개 탐색 → 매칭 {sum(1 for c in cards.values() if c['issuer']==issuer)}건")
    return cards

def _man(w):
    m = w / 10000
    return str(int(m)) if m == int(m) else ("%.1f" % m)

def main():
    only = None
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        if i + 1 < len(sys.argv): only = sys.argv[i + 1]
    try:
        URLS = json.load(open(URLS_CFG, encoding="utf-8"))
    except Exception as e:
        print("issuer_event_urls.json 로드 실패 — 기본 템플릿을 만들어 주세요.", e); return
    uni = universe_by_issuer()
    print(f"유니버스 발급사 {len(uni)}곳")
    allcards = {}
    for issuer in ISSUERS:
        if only and issuer != only: continue
        urls = URLS.get(issuer) or []
        if not urls:
            print(f"  - {issuer}: URL 미설정 → 스킵 (issuer_event_urls.json 에 추가)"); continue
        try:
            allcards.update(collect_issuer(issuer, urls, uni))
        except Exception as e:
            print(f"  ✗ {issuer} 수집 오류 {str(e)[:60]}")
    out = {"as_of": datetime.date.today().strftime("%Y-%m"), "source": "issuer_local",
           "cards": allcards}
    json.dump(out, open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    by_iss = {}
    for c in allcards.values(): by_iss[c["issuer"]] = by_iss.get(c["issuer"], 0) + 1
    print(f"\n저장: {SEED}  (총 {len(allcards)}건)")
    for i in ISSUERS:
        print(f"   {i}: {by_iss.get(i,0)}건" + ("  ⚠ 0건 — issuer_event_urls.json URL 확인 필요" if not by_iss.get(i) and URLS.get(i) else ""))

    if "--push" in sys.argv:
        try:
            subprocess.run(["git", "-C", HERE, "add", "issuer_seed.json"], check=True)
            subprocess.run(["git", "-C", HERE, "commit", "-m", f"issuer local collect {datetime.date.today()}"], check=True)
            subprocess.run(["git", "-C", HERE, "push"], check=True)
            print("git push 완료 → Cloudflare 재배포(다음 빌드)")
        except subprocess.CalledProcessError as e:
            print("git 단계 실패(변경 없음이거나 인증 필요):", e)

if __name__ == "__main__":
    main()
