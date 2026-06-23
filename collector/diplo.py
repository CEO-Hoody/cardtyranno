# -*- coding: utf-8 -*-
"""diplo(디플로) — 토스 카드라운지(card-lounge.toss.im) 파서.
'카드 쓰고 최대 N만원 받는 이벤트' 배너 추출."""
import re
from cardutil import parse_won

def parse_toss(html, card_id):
    m = re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*받는\s*이벤트", html or "") \
        or re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*이벤트", html or "")
    if not m:
        return None
    txt = "최대 " + m.group(1).replace(" ", "") + " 이벤트"
    pr = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", html or "")  # 이벤트 기간(있으면)
    return {"reward_text": txt, "reward_won": parse_won(txt),
            "period_start": pr.group(1).replace("-", ".") if pr else None,
            "period_end": pr.group(2).replace("-", ".") if pr else None,
            "url": f"https://card-lounge.toss.im/card/{card_id}"}
