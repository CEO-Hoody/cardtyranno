# -*- coding: utf-8 -*-
"""
카드티라노 통합 원장 수집기 — 거주지 IP(회원님 맥)에서 실행.

왜 로컬인가:
  네이버페이·아정당·카드고릴라 이미지/상세는 데이터센터 IP(GitHub Actions)에 막히거나 제한됩니다.
  회원님 맥(가정/사무실 IP)은 정상 접근됩니다. 그리고 뱅크샐러드처럼 SPA로 렌더링되는 사이트는
  '렌더링된 화면 텍스트'를 읽어야 정확한데, 이를 위해 헤드리스 브라우저(Playwright)를 씁니다.

무엇을 하나:
  - 각 플랫폼의 상품/이벤트 페이지를 방문해 '렌더링된 본문 텍스트'를 읽어
    상품명·이벤트금액·이벤트상세·상품상세를 수집합니다.
  - 프로덕트ID는 임의로 부여하고, 플랫폼 간 매핑은 '상품명(_nk)' 기준으로 합니다.
    ★ 규칙: "토스 미스터라이프카드" 와 "미스터라이프 카드" 는 서로 다른 상품으로 봅니다
       (_nk가 접두/코브랜드를 그대로 두므로 자동으로 분리됩니다).
  - 결과를 collector/ledger.json(통합 원장)과 collector/banksalad_seed.json(클라우드 콜렉터 보정용)에 저장.
  - --push 옵션이면 git add/commit/push 까지 수행 → 클라우드 콜렉터/사이트에 반영.

준비(최초 1회, 터미널에 그대로 붙여넣기):
  pip3 install playwright requests
  python3 -m playwright install chromium

실행:
  python3 collect_ledger.py            # 수집만(ledger.json/banksalad_seed.json 갱신)
  python3 collect_ledger.py --push     # 수집 + git push (사이트 반영)

매일 자동 실행: 같은 폴더 SETUP.md 의 launchd 안내 참고.
"""
import json, os, re, sys, subprocess, datetime
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # collector/
LEDGER = os.path.join(BASE, "ledger.json")
BS_SEED = os.path.join(BASE, "banksalad_seed.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# ── 공통 ──────────────────────────────────────────────────────────────────────
def _nk(s):
    """상품명 정규화 키(클라우드 콜렉터 _nk와 동일 규칙). 접두/코브랜드는 유지 → 변형은 별상품."""
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def _won(text):
    """'최대 23만원' → 230000, '84만원' → 840000. 여러 개면 최대값. '연회비 100%'는 0(별도 처리)."""
    if not text:
        return 0
    best = 0
    for m in re.finditer(r"([\d]+(?:\.\d+)?)\s*만\s*원?", text.replace(",", "")):
        best = max(best, int(float(m.group(1)) * 10000))
    return best

def _http_json(url, headers=None):
    h = {"User-Agent": UA, "Accept": "application/json", "Referer": "https://www.card-gorilla.com/"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

# ── 1) 카드고릴라: API(거주지/데이터센터 모두 OK). 카드명·발급사·플레이트·캐시백이벤트 ────────────
CG_CARDS = "https://api.card-gorilla.com:8080/v1/cards?type=CBK&is_live=true"
CG_EVENTS = "https://api.card-gorilla.com:8080/v1/events?type=CBK"

def collect_cardgorilla(ledger):
    try:
        cj = _http_json(CG_CARDS)
        cards = cj if isinstance(cj, list) else (cj.get("data") or cj.get("list") or [])
        cat = {}
        for c in cards:
            if isinstance(c, dict) and c.get("idx"):
                corp = c.get("corp") or {}
                cat[str(c["idx"])] = {
                    "name": c.get("name"),
                    "issuer": corp.get("name") if isinstance(corp, dict) else None,
                    "img": (c.get("card_img") or {}).get("url"),
                }
        ev = _http_json(CG_EVENTS)
        events = ev.get("data") if isinstance(ev, dict) else ev
        n = 0
        for e in (events or []):
            if not isinstance(e, dict):
                continue
            subj = (e.get("subject") or e.get("title") or "").strip()
            evidx = e.get("idx")
            for cid in (e.get("card_idxs") or []):
                meta = cat.get(str(cid)) or {}
                name = meta.get("name")
                if not name:
                    continue
                p = _ensure(ledger, name, meta.get("issuer"), meta.get("img"))
                p["platforms"]["cardgorilla"] = {
                    "event_text": subj, "event_won": _won(subj),
                    "url": f"https://www.card-gorilla.com/event/detail/{evidx}" if evidx else "",
                    "read_at": _today(),
                }
                n += 1
        print(f"[카드고릴라] 카탈로그 {len(cat)}장 · 캐시백이벤트 매핑 {n}건")
    except Exception as e:
        print("[카드고릴라] 오류:", e)

# ── 2) 뱅크샐러드: SPA → Playwright로 렌더링 텍스트 읽기 ───────────────────────────────────────
# 알려진 GUID(우리 데이터 기준). 회원님이 더 추가하면 그만큼 더 수집됩니다.
BANKSALAD_GUIDS = {
    "삼성 iD SELECT ALL 카드": "CARD004534",
    "삼성카드 & MILEAGE PLATINUM (스카이패스)": "CARD000081",
    "신한카드 Mr.Life": "CARD000004",
    "신한카드 Deep Oil": "CARD000118",
    "신한카드 처음(ANNIVERSE)": "CARD004343",
    "LOCA 365 카드": "CARD000037",
    "LOCA LIKIT 1.2 카드": "CARD000038",
    "K-패스 (신용)": "CARD004320",
    "KB국민 굿데이카드": "CARD000156",
    "KB국민 굿데이올림카드": "CARD000114",
    "KB국민 My WE:SH 카드": "CARD000128",
    "D4카드의정석 II": "CARD004420",
    "카드의정석 SHOPPING+": "CARD004419",
    "카드의정석 SHOPPING": "CARD003739",
}
BS_EVENT_RE = re.compile(r"(최대\s*[\d.,]+\s*만\s*원\s*캐시백|연회비\s*100%\s*캐시백)")

def collect_banksalad(ledger):
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("[뱅샐] Playwright 미설치 → 건너뜀. 'pip3 install playwright && python3 -m playwright install chromium' 후 재실행")
        return
    n = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(user_agent=UA)
        # (선택) 이벤트 차트에서 추가 상품 링크 자동발견 — 마크업 변동에 견디게 best-effort
        try:
            page.goto("https://www.banksalad.com/chart/cards?tab=event", wait_until="networkidle", timeout=30000)
            hrefs = page.eval_on_selector_all(
                'a[href*="/product/cards/"]', "els => els.map(e => e.getAttribute('href'))")
            for h in (hrefs or []):
                m = re.search(r"cards/([A-Z0-9]+)", h or "")
                if m:
                    BANKSALAD_GUIDS.setdefault("__auto_" + m.group(1), m.group(1))
        except Exception as e:
            print("[뱅샐] 차트 발견 단계 건너뜀:", e)
        for name, guid in list(BANKSALAD_GUIDS.items()):
            try:
                page.goto(f"https://www.banksalad.com/product/cards/{guid}",
                          wait_until="networkidle", timeout=30000)
                body = page.inner_text("body")
                title = page.title()
                real_name = title.split("|")[0].replace("뱅크샐러드", "").strip() or name
                # 이벤트 금액(렌더링 텍스트에서)
                ev_text, ev_won = "", 0
                for ln in body.split("\n"):
                    ln = ln.strip()
                    if len(ln) < 45 and BS_EVENT_RE.search(ln):
                        ev_text = BS_EVENT_RE.search(ln).group(1).replace(" ", "")
                        ev_won = _won(ev_text)
                        break
                p = _ensure(ledger, real_name, None, None)
                p["platforms"]["banksalad"] = {
                    "guid": guid, "event_text": ev_text, "event_won": ev_won,
                    "no_event": (ev_won == 0 and "연회비" not in ev_text),
                    "url": f"https://www.banksalad.com/product/cards/{guid}",
                    "read_at": _today(),
                }
                n += 1
            except Exception as e:
                print(f"[뱅샐] {name} 실패:", e)
        browser.close()
    print(f"[뱅샐] 렌더링 텍스트 수집 {n}건")

# ── 원장 빌드 / 저장 ──────────────────────────────────────────────────────────
def _today():
    return datetime.date.today().isoformat()

def _ensure(ledger, name, issuer, img):
    """name_key로 상품 찾기/생성. 임의ID 부여. 코브랜드 변형은 name_key가 달라 자동 분리."""
    k = _nk(name)
    prods = ledger["products"]
    if k not in prods:
        prods[k] = {
            "id": "P%04d" % (len(prods) + 1),   # 임의 식별자
            "name": name, "name_key": k, "issuer": issuer, "img": img,
            "platforms": {},
        }
    p = prods[k]
    if issuer and not p.get("issuer"):
        p["issuer"] = issuer
    if img and not p.get("img"):
        p["img"] = img
    return p

def write_outputs(ledger):
    ledger["updated"] = _today()
    json.dump(ledger, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 클라우드 콜렉터 보정용 banksalad_seed.json (override: cashbackAmountKrw0f 버그 차단)
    seed = {"as_of": _today(),
            "source": "거주지 렌더링 텍스트 수집(collect_ledger.py). 상품명 매핑.",
            "cards": {}}
    for p in ledger["products"].values():
        bs = p["platforms"].get("banksalad")
        if not bs:
            continue
        if bs.get("no_event"):
            seed["cards"][p["name"]] = {"reward_won": 0, "reward_text": "", "no_event": True}
        elif bs.get("event_won") or bs.get("event_text"):
            seed["cards"][p["name"]] = {"reward_won": bs.get("event_won") or 0,
                                        "reward_text": bs.get("event_text") or ""}
    json.dump(seed, open(BS_SEED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"저장 → ledger.json({len(ledger['products'])} 상품), banksalad_seed.json({len(seed['cards'])} 카드)")

def git_push():
    try:
        subprocess.run(["git", "-C", BASE, "add", "ledger.json", "banksalad_seed.json"], check=True)
        subprocess.run(["git", "-C", BASE, "commit", "-m", "ledger: 거주지 렌더링 텍스트 수집 " + _today()], check=True)
        for _ in range(3):
            try:
                subprocess.run(["git", "-C", BASE, "pull", "--no-rebase", "-X", "ours", "--no-edit", "origin", "main"], check=True)
                subprocess.run(["git", "-C", BASE, "push", "origin", "main"], check=True)
                print("git push 완료")
                return
            except subprocess.CalledProcessError:
                continue
    except subprocess.CalledProcessError as e:
        print("git push 실패(수동 푸시 필요):", e)

def main():
    ledger = {"products": {}}
    if os.path.exists(LEDGER):
        try:
            ledger = json.load(open(LEDGER, encoding="utf-8"))
            ledger.setdefault("products", {})
        except Exception:
            ledger = {"products": {}}
    collect_cardgorilla(ledger)
    collect_banksalad(ledger)
    write_outputs(ledger)
    if "--push" in sys.argv:
        git_push()
    print("완료. (참고: 네이버/아정당은 collect_naver_local.py / collect_ajd_local.py 와 함께 돌리세요.)")

if __name__ == "__main__":
    main()
