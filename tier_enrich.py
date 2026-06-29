# -*- coding: utf-8 -*-
"""tier_enrich.py — [맥 소유 / MAC-OWNED] 이벤트 주요·부가 혜택 구조화 모듈.

코워크가 build_data.py를 다시 export해도 이 파일은 건드리지 않으므로 로직이 보존된다.
build_data.py 쪽에는 import + 호출 2곳만 두고(`# >>> MAC-OWNED` 마커로 표시),
실제 로직(통합 소스맵 느슨매칭 + 임계/보상/효율 + 부가 조건분류)은 전부 여기에 있다.

회귀 시 복구:  python tier_guard.py --fix   (site/cards.json에 main_tier/sub_tiers 재적용)
"""
import os, re, json

def _nk(s): return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())

def build_src_maps(base):
    """카드고릴라·거주지(naver/ajd)·뱅샐 seed의 main/sub를 _nk 키로 통합."""
    main = {}; sub = {}
    def absorb(mm, ms):
        for k, v in (mm or {}).items():
            if v: main.setdefault(_nk(k), v)
        for k, v in (ms or {}).items():
            if v: sub.setdefault(_nk(k), v)
    for f in ["scrape/cg_meta.json", "scrape/residential_meta.json"]:
        p = os.path.join(base, f)
        if os.path.exists(p):
            try:
                d = json.load(open(p, encoding="utf-8"))
                absorb(d.get("mainByName"), d.get("subByName"))
            except Exception as e:
                print("tier_enrich src skip:", f, e)
    bp = os.path.join(base, "collector/banksalad_seed.json")
    if os.path.exists(bp):
        try:
            cs = json.load(open(bp, encoding="utf-8")).get("cards", {})
            absorb({k: v.get("main") for k, v in cs.items()},
                   {k: v.get("subs") for k, v in cs.items()})
        except Exception as e:
            print("tier_enrich banksalad skip:", e)
    return main, sub

def srcget(mp, n):
    """느슨 매칭: 정확 → 토스접두 제거 → 7자 이상 부분문자열."""
    k = _nk(n)
    if k in mp: return mp[k]
    k2 = _nk(re.sub(r"^토스\s+", "", n))
    if k2 in mp: return mp[k2]
    for sk, sv in mp.items():
        if len(sk) >= 7 and (sk in k or k in sk): return sv
    return None

def mtier(t):
    """주요 텍스트 → {spend, reward, eff, text}. 'N만원 이상/사용/쓰고 … M(+K)만원'."""
    if not t: return None
    th = re.search(r"(\d[\d,]*)\s*만\s*원?\s*(?:이상|사용|쓰고|쓰면)", t)
    rw = re.search(r"(?:이상|사용|쓰고|쓰면|시|최대)[^0-9]*?(\d+)(?:\s*\+\s*(\d+))?\s*만\s*원", t)
    sp = int(th.group(1).replace(",", "")) * 10000 if th else None
    rwon = (int(rw.group(1)) + (int(rw.group(2)) if rw.group(2) else 0)) * 10000 if rw else None
    if not rwon: return None
    return {"spend": sp, "reward": rwon, "eff": (round(rwon / sp * 100) if sp else None), "text": t}

_SUBCAT = [
    (r"해외", ("해외", "🌍")), (r"리볼빙|이월약정", ("리볼빙", "🔄")),
    (r"멤버십|구독|스트리밍", ("멤버십", "📺")),
    (r"자동납부|정기결제|생활요금|공과금|관리비", ("자동납부", "📅")),
    (r"마케팅|수신\s*동의|정보\s*동의", ("마케팅동의", "✅")),
    (r"쿠폰|상품권|백화점|마이샵", ("쿠폰", "🎁")),
    (r"라운지|마일리지|항공|여행", ("여행", "✈️")),
    (r"오프라인", ("오프라인", "🏪")),
    (r"연회비", ("연회비", "💳")),
    (r"신규\s*회원|신규가입|첫\s*결제|첫\s*이용", ("신규", "🆕")),
    (r"pay\s*로|페이\s*로|간편결제|네이버페이|카카오페이|토스페이|애플페이|삼성페이", ("간편결제", "📲")),
    # 추가이용은 가장 포괄적이라 마지막(특정 유형 우선 매칭 후 남는 '더 쓰고/쓰고' 임계형 흡수)
    (r"추가\s*이용|추가이용|더\s*받|더\s*쓰|추가로|쓰고", ("추가이용", "➕")),
]
def stier(t):
    """부가 텍스트 → {cat, icon, reward, text} (조건 카테고리 분류)."""
    rw = re.search(r"(\d[\d,]*)\s*만\s*원", t or "")
    cat, icon = "기타", "•"
    for pat, (c, ic) in _SUBCAT:
        if re.search(pat, t or "", re.I): cat, icon = c, ic; break  # NH PAY 등 대소문자 무시
    return {"cat": cat, "icon": icon,
            "reward": (int(rw.group(1).replace(",", "")) * 10000 if rw else None), "text": t}

def enrich_card(card, name, src_main, src_sub, existing_main=None, existing_sub=None):
    """카드 dict에 main_benefit/main_tier/sub_benefits/sub_tiers를 부착(in-place)."""
    mtext = existing_main or srcget(src_main, name)
    stext = existing_sub or srcget(src_sub, name)
    if mtext:
        card["main_benefit"] = mtext
        mt = mtier(mtext)
        if mt: card["main_tier"] = mt
    if stext:
        slist = stext if isinstance(stext, list) else [stext]
        card["sub_benefits"] = slist
        card["sub_tiers"] = [stier(s) for s in slist]
    return card

def coverage(cards_dict):
    """(전체, main_benefit, main_tier) 카운트 — 회귀 감지용."""
    n = mb = mt = 0
    for arr in cards_dict.values():
        for c in arr:
            n += 1
            if c.get("main_benefit"): mb += 1
            if c.get("main_tier"): mt += 1
    return n, mb, mt
