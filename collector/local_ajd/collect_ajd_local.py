# -*- coding: utf-8 -*-
"""
아정당(ajd) 로컬 수집기 — 거주지 IP(회원님 맥)에서 실행.

배경: 아정당은 데이터센터 IP(GitHub Actions)를 차단. 회원님 맥(가정/사무실 IP)은 정상 수집됩니다.
모델: 아정당 카드 이벤트는 '발급사 단위'(예: 신한카드 최대 54만원). /card 랜딩에서 이번 달 이벤트 id를
      자동 발견 → 각 이벤트 상세에서 발급사·최대금액·대상카드 추출 → 우리 카드명과 매칭 →
      collector/ajd_seed.json 저장 → (옵션) git push. 클라우드 콜렉터가 이를 읽어 병합합니다.

준비(최초 1회):  pip3 install requests
실행:           python3 collect_ajd_local.py            # 수집만
               python3 collect_ajd_local.py --push     # 수집 + git add/commit/push
"""
import json, re, os, sys, subprocess, datetime
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # collector/
SEED = os.path.join(BASE, "ajd_seed.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
LANDING = "https://www.ajd.co.kr/card"
DETAIL = "https://www.ajd.co.kr/card/event/detail/%s"

HEAD_RE = re.compile(r"([가-힣A-Za-z0-9·\s]+?카드)[^최]*?최대\s*([\d.,]+)\s*만원\s*이벤트")
TITLE_RE = re.compile(r'<h4[^>]*view-list--content--title[^>]*>\s*([^<]+?)\s*</h4>')

def _nk(s):  # 정규화(콜렉터 _nk와 동일 규칙: 공백/특수문자 제거 + 소문자)
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko-KR"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")

def discover_event_ids(html):
    return sorted(set(re.findall(r"/card/event/detail/(\d+)", html)), key=int)

def parse_event(html):
    m = HEAD_RE.search(re.sub(r"<[^>]+>", " ", html))   # 헤딩 "발급사 최대 N만원 이벤트"
    issuer = m.group(1).strip() if m else ""
    won = int(float(m.group(2).replace(",", "")) * 10000) if m else 0
    cards = [re.sub(r"\s+", " ", t).strip() for t in TITLE_RE.findall(html)]
    return issuer, won, list(dict.fromkeys(cards))

def our_universe():
    uni = {}
    for fn, key in [("cg_seed.json", "cards"), ("products.json", None)]:
        try:
            data = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
            rows = data.get("cards", []) if key else data
            for r in rows:
                nm = r[1] if isinstance(r, list) else r["name"]
                uni[_nk(nm)] = nm
        except Exception as e:
            print("universe load", fn, e)
    return uni

def fmt_won(w):
    m = w / 10000
    return str(int(m)) if m == int(m) else ("%.1f" % m)

def main():
    uni = our_universe()
    landing = get(LANDING)
    ids = discover_event_ids(landing)
    print(f"이벤트 {len(ids)}개 발견: {ids}")
    cards = {}
    for eid in ids:
        try:
            issuer, won, clist = parse_event(get(DETAIL % eid))
        except Exception as e:
            print(f"  ✗ event {eid}: {e}"); continue
        if not won:
            continue
        wtxt = f"최대 {fmt_won(won)}만원 (아정당 {issuer} 발급 이벤트)"
        hit = 0
        for c in clist:
            nm = uni.get(_nk(c))
            if not nm:                       # 느슨한 매칭(부분일치)
                for nk, name in uni.items():
                    if len(nk) > 6 and (nk in _nk(c) or _nk(c) in nk):
                        nm = name; break
            if nm:
                cards[nm] = {"ajd_id": eid, "reward_won": won, "reward_text": wtxt,
                             "url": DETAIL % eid}
                hit += 1
        print(f"  ✓ {issuer:<10} 최대 {fmt_won(won)}만원  대상 {len(clist)}장 → 매칭 {hit}")
    json.dump({"as_of": datetime.date.today().strftime("%Y-%m"), "cards": cards},
              open(SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n저장: {SEED}  (매칭 {len(cards)}건)")

    if "--push" in sys.argv:
        try:
            subprocess.run(["git", "-C", BASE, "add", "ajd_seed.json"], check=True)
            subprocess.run(["git", "-C", BASE, "commit", "-m",
                            f"ajd local collect {datetime.date.today()}"], check=True)
            subprocess.run(["git", "-C", BASE, "push"], check=True)
            print("git push 완료")
        except subprocess.CalledProcessError as e:
            print("git 단계 실패(변경 없음이거나 인증 필요):", e)

if __name__ == "__main__":
    main()
