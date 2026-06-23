# -*- coding: utf-8 -*-
"""mamenchi(마멘치) — 네이버페이(card.pay.naver.com) 파서.
detail.json/promotion.json/page-data → 리워드/기간 generic 추출.
(네이버는 데이터센터 IP 404 → 운영은 주로 naver_seed.json 주입.)"""
import re
from cardutil import parse_won

def parse_naver(text, url):
    mt = re.search(r"(최대\s*[\d.,]+\s*(?:억|만원|원))", text)
    won = parse_won(mt.group(1)) if mt else parse_won(text)
    if not won:
        return None
    period = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", text)
    return {"reward_text": (mt.group(1) if mt else f"최대 {won//10000}만원"), "reward_won": won,
            "period_start": period.group(1).replace("-", ".") if period else None,
            "period_end": period.group(2).replace("-", ".") if period else None, "url": url}
