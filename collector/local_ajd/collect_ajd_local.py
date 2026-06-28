# -*- coding: utf-8 -*-
"""
아정당(ajd) 로컬 수집기 v2 — 거주지 IP(회원님 맥)에서 실행.

배경: 아정당은 데이터센터 IP(GitHub Actions) 차단 + **Next.js 클라이언트 렌더**라 plain HTTP(urllib)로는
빈 셸만 받는다(v1이 8이벤트 중 2장만 매칭한 원인). v2는 headless(playwright)로 렌더한 뒤
RSC 페이로드에서 발급사·최대금액을 뽑고, 카드명은 비정형이라(카드의정석2/7CORE 등) 추출 대신
**우리 카드 유니버스를 이벤트 텍스트에 역매칭**한다(residential_meta와 동일 철학).

흐름: /card 랜딩 렌더 → 이벤트 id 발견 → 각 이벤트 상세 렌더 →
      발급사("CASHBACK","<발급사> N종") + 헤드라인 최대금액 + 유니버스 매칭 카드 → ajd_seed.json.

준비:  pip3 install playwright && python3 -m playwright install chromium
실행:  python3 collect_ajd_local.py            # 수집만
       python3 collect_ajd_local.py --push     # 수집 + git add/commit/push
"""
import json, re, os, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))                  # collector/local_ajd/
BASE = os.path.dirname(HERE)                                       # collector/
sys.path.insert(0, BASE)                                           # headless 모듈 import
SEED = os.path.join(BASE, "ajd_seed.json")
LANDING = "https://www.ajd.co.kr/card"
DETAIL  = "https://www.ajd.co.kr/card/event/detail/%s"

ISS_RE  = re.compile(r'"CASHBACK","[^"]+?종\s*",?\d*,"([^"]+카드)"')          # 발급사
HEAD_RE = re.compile(r'최대\s*([\d,]+(?:\.\d+)?)\s*만\s*(?:([\d,]+)\s*천\s*)?원[^"]{0,6}(?:캐시백|혜택)')

def _nk(s):  # 콜렉터 _nk와 동일(공백/특수문자 제거 + 소문자)
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def get(url):
    """headless(playwright)로 렌더한 HTML. ajd는 클라이언트 렌더라 필수."""
    import headless
    return headless.render_html(url, wait_selector="body", timeout=40000) or ""

def discover_event_ids(html):
    return sorted(set(re.findall(r"/card/event/detail/(\d+)", html)), key=int)

def parse_event(html, uni):
    """발급사 + 헤드라인 최대금액(헤더 직후 범위) + 유니버스 역매칭 카드."""
    mi = ISS_RE.search(html)
    issuer = mi.group(1).strip() if mi else ""
    won = 0
    if mi:
        win = html[mi.end():mi.end() + 1500]                       # CASHBACK 헤더 직후(타 이벤트 금액 오염 방지)
        hm = HEAD_RE.search(win)
        if hm:
            man = float(hm.group(1).replace(",", ""))
            cheon = int(hm.group(2).replace(",", "")) if hm.group(2) else 0
            won = int(man * 10000) + cheon * 1000
    nt = _nk(re.sub(r"<[^>]+>", " ", html))
    cards = [name for nk, name in uni.items() if len(nk) >= 5 and nk in nt]   # 우리 카드 역매칭
    return issuer, won, cards

def our_universe():
    uni = {}
    for fn, key in [("cg_seed.json", "cards"), ("products.json", None)]:
        try:
            data = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
            rows = data.get("cards", []) if key else data
            for r in rows:
                nm = r[1] if isinstance(r, list) else r["name"]
                if nm: uni[_nk(nm)] = nm
        except Exception as e:
            print("universe load", fn, e)
    return uni

def fmt_won(w):
    m = w / 10000
    return str(int(m)) if m == int(m) else ("%.1f" % m)

def main():
    uni = our_universe()
    print(f"우리 카드 유니버스 {len(uni)}개")
    ids = discover_event_ids(get(LANDING))
    print(f"이벤트 {len(ids)}개 발견: {ids}")
    cards = {}
    for eid in ids:
        try:
            issuer, won, clist = parse_event(get(DETAIL % eid), uni)
        except Exception as e:
            print(f"  ✗ event {eid}: {str(e)[:50]}"); continue
        if not won or not issuer:
            print(f"  - event {eid}: 발급사/금액 미검출 → 스킵"); continue
        wtxt = f"최대 {fmt_won(won)}만원 (아정당 {issuer} 발급 이벤트)"
        for nm in clist:
            # 더 큰 금액 우선(같은 카드가 여러 이벤트에 걸칠 때)
            if nm not in cards or won > cards[nm]["reward_won"]:
                cards[nm] = {"ajd_id": eid, "reward_won": won, "reward_text": wtxt, "url": DETAIL % eid}
        print(f"  ✓ {issuer:<10} 최대 {fmt_won(won)}만원  → 매칭 {len(clist)}")
    json.dump({"as_of": datetime.date.today().strftime("%Y-%m"), "cards": cards},
              open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n저장: {SEED}  (매칭 {len(cards)}건)")

    if "--push" in sys.argv:
        try:
            subprocess.run(["git", "-C", BASE, "add", "ajd_seed.json"], check=True)
            subprocess.run(["git", "-C", BASE, "commit", "-m", f"ajd local collect {datetime.date.today()}"], check=True)
            subprocess.run(["git", "-C", BASE, "push"], check=True)
            print("git push 완료")
        except subprocess.CalledProcessError as e:
            print("git 단계 실패(변경 없음이거나 인증 필요):", e)

if __name__ == "__main__":
    main()
