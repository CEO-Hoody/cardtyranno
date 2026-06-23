# -*- coding: utf-8 -*-
"""brachio(브라키오) — 카드고릴라(card-gorilla) 파서.
상세 응답의 event.card_detail_text/subject + 기간 추출."""
import re
from cardutil import parse_won

def parse_cardgorilla(card_json, card_id):
    ev = (card_json or {}).get("event") or {}
    txt = ev.get("card_detail_text") or ev.get("subject")
    period = re.search(r"(20\d\d\.\d\d?\.\d\d?)\s*~\s*(20\d\d\.\d\d?\.\d\d?)", ev.get("detail", "") or "")
    return {"reward_text": txt, "reward_won": parse_won(txt),
            "period_start": period.group(1) if period else None,
            "period_end": period.group(2) if period else None,
            "url": f"https://www.card-gorilla.com/card/{card_id}"} if txt else None
