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

def is_june2026(ev):
    """6월(2026.06) 이벤트만 우선 필터. 기간 미표기는 현행으로 간주."""
    if not ev:
        return False
    s = (ev.get("period_start") or "") + (ev.get("period_end") or "") + (ev.get("reward_text") or "")
    return ("2026.6" in s) or ("2026.06" in s) or ("2026-06" in s) or (not ev.get("period_start"))
