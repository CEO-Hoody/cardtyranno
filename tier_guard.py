# -*- coding: utf-8 -*-
"""tier_guard.py — [맥 소유] 주요/부가 구조화 회귀 가드.

site/cards.json에 main_tier/sub_tiers가 정상 적용됐는지 검증한다.
코워크가 build_data.py를 다시 export하면서 tier_enrich 연결을 빠뜨리면 커버리지가 급락하는데,
이 스크립트로 즉시 감지하고 복구한다.

  python tier_guard.py          # 검증만. 회귀면 exit 1 (CI/배치에서 차단용)
  python tier_guard.py --fix    # cards.json에 main_tier/sub_tiers 직접 재적용(복구)
"""
import sys, os, json
import tier_enrich as te

BASE = os.path.dirname(os.path.abspath(__file__))
CJ = os.path.join(BASE, "site", "cards.json")
FLOOR = 70  # main_tier 최소 기대치(정상 ~92장)

def main():
    fix = "--fix" in sys.argv
    d = json.load(open(CJ, encoding="utf-8"))
    cards = d["cards"]
    n, mb, mt = te.coverage(cards)
    print(f"cards {n} · main_benefit {mb} · main_tier {mt} (기대 ≥{FLOOR})")
    if mt >= FLOOR:
        print("✅ 정상 — 회귀 없음.")
        return 0
    print(f"⚠️ 회귀 감지: main_tier {mt} < {FLOOR}.")
    if not fix:
        print("→ 복구하려면: python tier_guard.py --fix")
        return 1
    sm, ss = te.build_src_maps(BASE)
    for arr in cards.values():
        for c in arr:
            te.enrich_card(c, c["name"], sm, ss, c.get("main_benefit"), c.get("sub_benefits"))
    json.dump(d, open(CJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n2, mb2, mt2 = te.coverage(cards)
    print(f"[복구 완료] main_benefit {mb2} · main_tier {mt2} / {n2}장")
    return 0 if mt2 >= FLOOR else 1

if __name__ == "__main__":
    sys.exit(main())
