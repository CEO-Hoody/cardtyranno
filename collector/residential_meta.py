# -*- coding: utf-8 -*-
"""residential_meta — 네이버페이·아정당 카드 메타(연회비·주요/부가 혜택) 거주지 캡처 스크립트.

배경: 네이버페이(card.pay.naver.com)·아정당(ajd.co.kr) 카드 상세는 GitHub Actions(데이터센터 IP)에서
404/차단되어 일일 콜렉터로는 수집이 안 됩니다. 이 스크립트는 **거주지 IP의 PC에서 직접 실행**해
playwright로 각 상세 페이지를 렌더 → 연회비·주요혜택·부가혜택을 파싱 → scrape/residential_meta.json 으로
저장합니다. 이 파일을 git에 커밋하면, 다음 데일리 빌드(build_data.py)가 자동 병합합니다.

사용법(거주지 PC, 프로젝트 루트에서):
    pip install playwright && python -m playwright install chromium
    python collector/residential_meta.py
    # → scrape/residential_meta.json 생성 → git add scrape/residential_meta.json && commit & push

원칙: 연회비·금액은 사실(숫자) 그대로 저장. 혜택 문구는 collector._reword_*로 자체 표현으로 변환(저작권 햇징).
주요혜택 = "얼마 이상 쓰면 얼마" 결제 캐시백(첫 혜택). 부가혜택 = 해외/생활요금/마케팅 등 그 이후.
"""
import os, re, json, datetime, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from cardutil import _nk
import collector as C          # _cg_fee / _reword_main / _reword_sub / _reword_benefit 재사용
import html as _html

OUT  = os.path.dirname(BASE)
SCR  = os.path.join(OUT, "scrape"); os.makedirs(SCR, exist_ok=True)

def _render(url):
    """거주지 IP에서 playwright로 렌더한 페이지의 보이는 텍스트(+HTML) 반환."""
    try:
        import headless
        html = headless.render_html(url, wait_selector="body", timeout=40000)
        return html or ""
    except Exception as e:
        print("  render err", url, e); return ""

def _fee_from_text(txt):
    """'연회비 국내전용 4만7천원, AMEX 4만9천원' 류 → 대표 연회비(국내/기본) 사실 추출."""
    t = _html.unescape(txt or "")
    # '4만7천원' / '47,000원' / '47000원' 모두 처리해 최소(국내전용) 금액 채택
    cands = []
    for m in re.finditer(r"(\d{1,3}(?:,\d{3})+|\d+)\s*원", t):
        cands.append(int(m.group(1).replace(",", "")))
    for m in re.finditer(r"(\d+)\s*만\s*(\d+)?\s*천?\s*원", t):
        man = int(m.group(1)); cheon = int(m.group(2)) if m.group(2) else 0
        cands.append(man*10000 + cheon*1000)
    cands = [c for c in cands if 1000 <= c <= 1000000]
    if not cands:
        if re.search(r"연회비\s*(없음|면제|무료)", t): return "없음"
        return ""
    v = min(cands)
    return f"{v:,}원"

def _benefits_from_text(txt):
    """혜택 블록 → (주요, [부가...]). 'N만원 이상 … 받기/캐시백' 패턴을 순서대로 추출."""
    t = _html.unescape(txt or ""); t = re.sub(r"\s+", " ", t)
    # '혜택1/혜택 2' 또는 '24만원 이상 … 20만원' 류 라인을 후보로 수집
    lines = re.findall(r"[^.!?\n]*?\d[\d.,]*\s*만?원[^.!?\n]{0,40}?(?:받기|캐시백|적립|할인|증정|페이백)[^.!?\n]*", t)
    lines = [l.strip() for l in lines if 4 <= len(l.strip()) <= 90]
    # 중복 제거(순서 유지)
    seen=set(); uniq=[]
    for l in lines:
        if l not in seen: seen.add(l); uniq.append(l)
    if not uniq: return "", []
    main = C._reword_main(uniq[0])
    subs=[]
    for l in uniq[1:6]:
        rb = C._reword_sub(l)
        if rb and rb not in subs: subs.append(rb)
    return main, subs

# ── 아정당 이벤트 혜택 파서 ───────────────────────────────────────────────
# 아정당 카드 상세는 /card/event/detail/{N} (발급사 이벤트 1개 = 그 발급사 카드 다수 공유).
# 페이지엔 전역 배너("최대 지원금 128만원/월 700원")가 있어 단순 텍스트 정규식은 카드마다
# 같은 값을 긁는다(버그). 실제 이벤트 데이터는 Next.js RSC 직렬화 페이로드 안에 있으므로
# 구조에서 헤드라인(최대 N만원 캐시백)과 캐시백 구간들을 직접 파싱한다.
# 이벤트 캐시백 '구간 타이틀'을 종결어(캐시백/페이백/받기)로 앵커링해 추출. 카드 자체혜택(적립/할인
# 종결)은 자동 제외, 상세설명·헤드라인 총액·적립률(%)은 명시 배제. (카드고릴라 _cg_benefits와 동일 철학.)
_AJD_TIER   = re.compile(r'"([^"]{4,46}?(?:캐시백|페이백|받기))"')
_AJD_BANNED = ("전월실적", "지원금", "128만원", "700원", "경유", "적립 사이트",
               "쇼핑적립", "비교 추천", "인기 신용카드", "쿠폰 공유", "링크")
_AJD_DETAIL = re.compile(r"기간|대상|필수|응모|동의|바로가기|버튼|초과|매월|유의|확인")
_AJD_THRESH = re.compile(r"\d[\d,]*\s*만\s*원?\s*이상\s*(?:결제|이용|사용)")   # 주요 = 결제 임계 캐시백

def _ajd_is_headline(s):
    """이벤트 전체 총액 헤드라인(주요/부가 아님)인지: '최대 N만원…'·'발급사 쓰고 최대 N만원 받기'."""
    if re.match(r"^최대\s*[\d.,]+\s*만", s) and not re.search(r"이상|추가|해외|자동납부|생활|리볼빙|마케팅", s):
        return True
    return bool(re.search(r"쓰고\s*최대.*만.*받기", s))

def _ajd_event_benefits(html):
    """아정당 이벤트 상세(RSC) → (주요=결제 임계 캐시백, [부가=추가/해외/자동납부 …]).
    종결어로 구간 타이틀만 추출하고 상품혜택(적립률%)·상세설명·헤드라인 총액은 배제.
    주요 = 'N만원 이상 결제/이용/사용 …' 첫 구간, 부가 = 나머지. (텍스트 구간이 없는
    이미지형 이벤트는 주요가 빌 수 있음 → 카드고릴라 main_benefit이 우선 채움.)"""
    kept = []; seen = set()
    for raw in _AJD_TIER.findall(html):
        s = re.sub(r"\s+", " ", _html.unescape(raw).replace("\\n", " ")).strip()
        if s in seen or not re.search(r"\d", s): continue
        if "%" in s: continue                                       # 적립/할인율(상품혜택)
        if any(b in s for b in _AJD_BANNED) or _AJD_DETAIL.search(s): continue
        if _ajd_is_headline(s): continue                            # 전체 총액 헤드라인
        seen.add(s); kept.append(s)
    mains = [b for b in kept if _AJD_THRESH.search(b)]
    main, subs = (mains[0], [b for b in kept if b != mains[0]]) if mains else ("", kept)
    return main, subs[:5]

# 네이버페이 프로모션 페이지 파서. 주요 = EventBenefitList 타임라인 중 임계 보상 타이틀
# ('N만원 쓰고/이상 … M만원 받기'). 부가 = 강조된 '최대 N만원 캐시백' 문구(해외/추가/생활요금).
# 상품 자체혜택(rewardSummary=전월실적 M포인트 적립)은 이벤트가 아니므로 제외. (카드고릴라/뱅샐과 동일 철학.)
def _naver_event_benefits(html):
    def _c(s):
        s = re.sub(r"<!--.*?-->", "", s)
        return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
    main = ""
    for t in re.findall(r'<div class="EventBenefitList_title__[^"]*">(.*?)</div>', html, re.S):
        s = _c(t)
        if re.search(r"\d[\d,]*\s*만\s*원.*?(?:쓰고|이상).*?\d[\d,]*\s*만\s*원?.*?(?:받기|캐시백|포인트)", s):
            main = s; break
    subs = []
    for m in re.finditer(r'([가-힣A-Za-z0-9·,\s]{4,34}?)<[^>]*>\s*(최대\s*[\d./]+\s*만\s*원?\s*캐시백)', html):
        s = re.sub(r"^[·,\s]+", "", re.sub(r"\s+", " ", _c(m.group(1)) + " " + m.group(2)).strip())
        if s and s not in subs and "쓰고" not in s:
            subs.append(s)
    return main, subs[:5]

_RENDER_CACHE = {}
def _render_cached(url):
    """같은 이벤트 URL을 여러 카드가 공유하므로 렌더 결과를 URL 단위로 캐시(중복 렌더 방지)."""
    if url not in _RENDER_CACHE:
        _RENDER_CACHE[url] = _render(url)
    return _RENDER_CACHE[url]

def _collect(seed_file, label):
    mainN={}; subN={}; n=0
    try:
        cards = json.load(open(os.path.join(BASE, seed_file), encoding="utf-8")).get("cards", {})
    except Exception as e:
        print(f"{label}: seed 로드 실패 {e}"); return mainN, subN
    for name, info in cards.items():
        url = info.get("url")
        if not url: continue
        html = _render_cached(url)
        if not html: continue
        nk = _nk(name); n += 1
        if label == "ajungdang":
            m, s = _ajd_event_benefits(html)                       # 아정당: RSC 구조
        elif label == "naver":
            m, s = _naver_event_benefits(html)                     # 네이버: EventBenefitList DOM
        else:
            text = re.sub(r"<[^>]+>", " ", html)
            m, s = _benefits_from_text(text)                       # 폴백: 렌더 텍스트
        if m: mainN.setdefault(nk, m)
        if s: subN.setdefault(nk, s)
        print(f"  [{label}] {name}: main={m or '-'} subs={len(s)}")
    print(f"{label}: {n}건 처리 (main {len(mainN)}, sub {len(subN)})")
    return mainN, subN

def main():
    mainAll={}; subAll={}
    for seed, label in [("naver_seed.json", "naver"), ("ajd_seed.json", "ajungdang")]:
        m, s = _collect(seed, label)
        mainAll.update(m); subAll.update(s)
    # 연회비·상품혜택은 타 사이트(카드고릴라/토스) 기준으로 적재 → 거주지 수집에서 제외(feeByName 비움).
    out = {"_updated": datetime.date.today().isoformat(), "source": "residential",
           "feeByName": {}, "mainByName": mainAll, "subByName": subAll}
    json.dump(out, open(os.path.join(SCR, "residential_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"residential_meta.json → main {len(mainAll)}, sub {len(subAll)} (연회비 제외: 타 사이트 기준)")

if __name__ == "__main__":
    main()
