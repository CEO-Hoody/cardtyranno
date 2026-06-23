# -*- coding: utf-8 -*-
"""bronto(브론토) — 아정당(ajd.co.kr) 파서.
RSC(self.__next_f)/렌더 텍스트 → 리워드/기간 generic 추출."""
import re
from cardutil import parse_won

def parse_ajd_rsc(text, evt_id):
    mt = re.search(r"(최대\s*[\d.,]+\s*(?:억|만원|원))", text)
    won = parse_won(mt.group(1)) if mt else parse_won(text)
    if not won:
        return None
    period = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", text)
    return {"reward_text": (mt.group(1) if mt else f"최대 {won//10000}만원"), "reward_won": won,
            "period_start": period.group(1).replace("-", ".") if period else None,
            "period_end": period.group(2).replace("-", ".") if period else None,
            "url": f"https://www.ajd.co.kr/card/event/detail/{evt_id}"}
