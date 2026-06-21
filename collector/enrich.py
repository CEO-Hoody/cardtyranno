# -*- coding: utf-8 -*-
"""혜택 통합(플랫폼 공통 안내만 추출) + 카드 플레이트 이미지 셀프호스팅/리사이징.
- 혜택: 여러 플랫폼이 공통(과반)으로 안내하는 사실 혜택만 남김 → 문구는 우리가 자체 작성(저작권 안전).
- 이미지: 외부 URL을 받아 우리 영역 규격으로 cover-crop 저장(플레이트가 영역에 딱 맞게).
운영(GitHub Actions)에서 requests/Pillow로 실행.
"""
import os, re, io
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(BASE), "site")
CARD_IMG_DIR = os.path.join(SITE, "img", "cards")
# 카드 플레이트 가로형 비율(~1.585). 우리 페이지 영역별 규격.
SIZES = {"tile": (320, 202), "chart": (148, 94), "hero": (480, 303)}

def _nk_area(a): return re.sub(r"[\s()·/,]+", "", a or "")

def consolidate_benefits(per_platform):
    """per_platform = {platform: [{"area","value","type"}, ...]}.
    과반 플랫폼이 공통 안내하는 혜택(area)만 사실로 채택. 문구는 미저장(우리 스키마로 재가공)."""
    bucket = defaultdict(list)
    for plat, items in (per_platform or {}).items():
        for it in items or []:
            if it.get("area"): bucket[_nk_area(it["area"])].append((plat, it))
    n = max(1, len(per_platform or {}))
    need = max(2, (n + 1) // 2)         # 과반 이상 공통
    out = []
    for _, lst in bucket.items():
        plats = sorted({p for p, _ in lst})
        if len(plats) >= need:
            it = lst[0][1]
            out.append({"area": it["area"], "value": it.get("value"),
                        "type": it.get("type"), "sources": plats})
    return out

def fetch_and_resize(url, key):
    """외부 플레이트 이미지를 받아 영역별 규격으로 cover-crop 저장. 반환: {size:relpath} 또는 None."""
    if not url: return None
    try:
        import requests
        from PIL import Image, ImageOps
        b = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}).content
        im = Image.open(io.BytesIO(b)).convert("RGB")
        os.makedirs(CARD_IMG_DIR, exist_ok=True)
        out = {}
        for name, (w, h) in SIZES.items():
            cropped = ImageOps.fit(im, (w, h), method=Image.LANCZOS)  # 영역에 딱 맞게 cover-crop
            rel = f"img/cards/{key}_{name}.png"
            cropped.save(os.path.join(SITE, rel), "PNG", optimize=True)
            out[name] = "/" + rel
        return out
    except Exception as e:
        print("  ! img err", url, e); return None
