# -*- coding: utf-8 -*-
"""diplo(디플로) — 토스 카드라운지(card-lounge.toss.im) 파서.
이벤트 헤드라인 총액 추출. 토스 카드라운지 웹은 상세 티어(주요/부가)를 노출하지 않고
('토스 앱 내 이벤트 페이지에서' 확인 안내) 카드별 'N만원 이벤트' 배지만 보여준다.
→ 웹에서는 헤드라인 총액만, 상세 티어는 토스 앱 캡처(toss_seismo_seed.json)가 보강.
포맷: 현재 'N만원 이벤트'·'N만 M천원 이벤트'(최대 없음), 구포맷 '최대 N만원 받는 이벤트' 모두 처리.
카드 상세 페이지엔 비교 카드도 섞여 있어 페이지 내 최대 금액을 해당 카드 헤드라인으로 채택."""
import re
from cardutil import parse_won, _fmt_man

_TOSS_AMT = r"\d[\d,]*\s*만(?:\s*\d+\s*천)?\s*원?"

def parse_toss(html, card_id):
    h = html or ""
    best = 0
    m = re.search(r"최대\s*(" + _TOSS_AMT + r")\s*받는\s*이벤트", h)
    if m:
        best = parse_won(m.group(1))
    for mm in re.finditer(r"(" + _TOSS_AMT + r")\s*이벤트", h):   # 현재 포맷 'N만원 이벤트' 최대값
        w = parse_won(mm.group(1))
        if w > best:
            best = w
    if not best:
        return None
    pr = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", h)  # 이벤트 기간(있으면)
    return {"reward_text": "최대 " + _fmt_man(best) + " 이벤트", "reward_won": best,
            "period_start": pr.group(1).replace("-", ".") if pr else None,
            "period_end": pr.group(2).replace("-", ".") if pr else None,
            "url": f"https://card-lounge.toss.im/card/{card_id}"}
