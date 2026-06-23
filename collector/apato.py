# -*- coding: utf-8 -*-
"""apato(아파토) — 뱅크샐러드(banksalad) 파서.
상세 __NEXT_DATA__의 cashbackPromotion.cashbackAmountKrw0f(정확 금액·원) 우선."""
import re
from cardutil import parse_won, _fmt_man

def parse_banksalad(html, prod_id):
    """상세 페이지엔 해당 카드 1건만 있어 모호성 없음. 없으면 렌더 텍스트 폴백."""
    html = html or ""
    m = re.search(r'cashbackAmountKrw0f"?\s*:\s*"?(\d+)', html)   # 1) 정확 금액(JSON)
    won = int(m.group(1)) if m else 0
    if not won:                                                   # 2) 폴백: "최대 N만원 캐시백"
        m2 = re.search(r"최대\s*([\d.,]+\s*(?:억|만원|원))\s*캐시백", html)
        if m2:
            won = parse_won("최대 " + m2.group(1).replace(" ", "") + " 캐시백")
    if not won:
        return None
    pr = re.search(r"(20\d\d[.\-]\d\d?[.\-]\d\d?)\D{1,4}(20\d\d[.\-]\d\d?[.\-]\d\d?)", html)  # 이벤트 기간(있으면)
    return {"reward_text": "최대 " + _fmt_man(won) + " 캐시백", "reward_won": won,
            "period_start": pr.group(1).replace("-", ".") if pr else None,
            "period_end": pr.group(2).replace("-", ".") if pr else None,
            "url": f"https://www.banksalad.com/product/cards/{prod_id}"}
