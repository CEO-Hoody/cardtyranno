# -*- coding: utf-8 -*-
"""공용 유틸 (용각류 콜렉터 공통). 이름정규화·금액파싱·표기·월필터.
순수 함수만 — 네트워크/DB 의존성 없음(단위테스트 용이)."""
import re

def _nk(n):
    """카드명 정규화 키: 공백/괄호/구분기호 제거 + 소문자."""
    return re.sub(r"[\s()（）·\-_/+.]+", "", (n or "")).lower()

def parse_won(text):
    """'최대 57.9만원 혜택' -> 579000, '84만원' -> 840000. 여러 개면 최대값."""
    if not text:
        return None
    t = text.replace(",", "")
    best = 0
    for m in re.finditer(r"([\d]+(?:\.\d+)?)\s*(억|만원|만|원)", t):
        v = float(m.group(1)); u = m.group(2)
        won = v*100000000 if u == "억" else v*10000 if u in ("만원", "만") else v
        best = max(best, int(won))
    return best or None

def _fmt_man(won):
    """원 -> '78만원' / '63.4만원'."""
    m = won/10000
    return (str(int(m)) if m == int(m) else ("%.1f" % m)) + "만원"

# 부가(조건부) 이벤트로 보는 키워드 — 이 키워드가 세그먼트에 있으면 bonus 후보
_COND_KW = ("이상", "이용 시", "이용시", "결제 시", "결제시", "국내", "해외", "추가", "응모",
            "전월", "실적", "신규 가입", "첫 결제", "첫결제", "이용금액", "사용 시", "사용시")
# 메인(무조건/대표)으로 보는 키워드
_MAIN_KW = ("연회비", "기본", "발급", "100%")

def parse_breakdown(text, total_won):
    """이벤트 상세 텍스트 → (main_won, bonus_won, components[]).
    세그먼트별 'N만원'을 뽑아 조건 키워드 유무로 메인/부가 분리.
    - main_won: 무조건성(연회비/기본/발급) 또는 최대 무조건 금액
    - bonus_won: 조건부 금액 합
    분해 실패 시 (total_won, 0, []) 로 안전 degrade."""
    total = int(total_won or 0)
    if not text:
        return (total, 0, [])
    segs = re.split(r"[\n\r。!?]+|\s*[·•/]\s*|(?<=원)\s*[,，]\s*", text)
    comps = []
    for s in segs:
        s = (s or "").strip()
        if not s:
            continue
        # 조건 임계금액("30만원 이상")은 리워드가 아니므로 제거 후 리워드 금액 추출
        sclean = re.sub(r"[\d.]+\s*만\s*원?\s*이상", " ", s.replace(",", ""))
        ms = re.findall(r"([\d]+(?:\.\d+)?)\s*만\s*원?", sclean)
        if not ms:
            continue
        won = int(float(ms[-1]) * 10000)   # 리워드는 보통 세그먼트 뒤쪽(캐시백/혜택 앞)
        if won <= 0:
            continue
        is_main_kw = any(k in s for k in _MAIN_KW)
        is_cond = (not is_main_kw) and any(k in s for k in _COND_KW)
        comps.append({"text": s[:70], "won": won, "cond": is_cond})
    if not comps:
        return (total, 0, [])
    if len(comps) == 1:           # 단일 컴포넌트(헤드라인)는 메인으로 간주
        comps[0]["cond"] = False
    mains = [c["won"] for c in comps if not c["cond"]]
    bonus = sum(c["won"] for c in comps if c["cond"])
    main = max(mains) if mains else 0
    # 정합 보정: 메인 미검출이면 total에서 부가를 뺀 값을 메인으로
    if not main:
        main = max(0, total - bonus)
    # 메인이 total보다 크면(과검출) total로 클램프
    if total and main > total:
        main = total
    return (main, bonus, comps[:8])

def is_june2026(ev):
    """6월(2026.06) 이벤트만 우선 필터. 기간 미표기는 현행으로 간주."""
    if not ev:
        return False
    s = (ev.get("period_start") or "") + (ev.get("period_end") or "") + (ev.get("reward_text") or "")
    return ("2026.6" in s) or ("2026.06" in s) or ("2026-06" in s) or (not ev.get("period_start"))
