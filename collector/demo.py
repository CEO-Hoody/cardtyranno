# -*- coding: utf-8 -*-
"""변경감지 시연 (네트워크 없이 실제 수집값 주입). 3일치 시뮬레이션."""
import os, json, sqlite3
import collector as C

C.DB = "/tmp/meta_demo.db"
if os.path.exists(C.DB): os.remove(C.DB)

prods = json.load(open(os.path.join(C.BASE,"products.json"),encoding="utf-8"))
mr = [p for p in prods if p["name"]=="신한카드 Mr.Life"]

def ev(t,w,ps,pe,u): return {"reward_text":t,"reward_won":w,"period_start":ps,"period_end":pe,"url":u}
CG="https://www.card-gorilla.com/card/13"; BS="https://www.banksalad.com/product/cards/CARD000004"

days = {
 "2026-06-21": {  # Day1 — 최초 수집
   ("신한카드 Mr.Life","cardgorilla"): ev("최대 57.9만원 혜택",579000,"2026.6.1","2026.6.30",CG),
   ("신한카드 Mr.Life","banksalad"):   ev("최대 84만원 캐시백",840000,None,None,BS),
   ("신한카드 Mr.Life","toss"): None, ("신한카드 Mr.Life","ajungdang"): None },
 "2026-06-22": {  # Day2 — 카드고릴라 금액 상향(57.9→60만), 뱅샐 동일
   ("신한카드 Mr.Life","cardgorilla"): ev("최대 60만원 혜택",600000,"2026.6.1","2026.6.30",CG),
   ("신한카드 Mr.Life","banksalad"):   ev("최대 84만원 캐시백",840000,None,None,BS),
   ("신한카드 Mr.Life","toss"): None, ("신한카드 Mr.Life","ajungdang"): None },
 "2026-06-23": {  # Day3 — 카드고릴라 이벤트 종료(없음), 뱅샐 동일
   ("신한카드 Mr.Life","cardgorilla"): None,
   ("신한카드 Mr.Life","banksalad"):   ev("최대 84만원 캐시백",840000,None,None,BS),
   ("신한카드 Mr.Life","toss"): None, ("신한카드 Mr.Life","ajungdang"): None },
}

for day, inj in days.items():
    print(f"\n=== 수집일 {day} ===")
    C.run(mr, day, injected=inj)

con=sqlite3.connect(C.DB); cur=con.cursor()
print("\n────────── 상품 ↔ 플랫폼 매핑 ──────────")
for r in cur.execute("SELECT cp.name, pp.platform, pp.platform_product_id, pp.url FROM product_platform pp JOIN card_product cp ON cp.id=pp.card_product_id ORDER BY pp.platform"):
    print(f"  {r[0]} | {r[1]:<11} | id={r[2]:<12} | {r[3]}")

print("\n────────── 현재 활성 이벤트(상품×플랫폼) ──────────")
for r in cur.execute("SELECT platform,reward_text,reward_won,period_end,status FROM event WHERE status='active' ORDER BY platform"):
    print(f"  {r[0]:<11} | {r[1]:<16} | {r[2]}원 | ~{r[3]} | {r[4]}")

print("\n────────── 변경 이력(일자별 스냅샷) ──────────")
for r in cur.execute("SELECT captured_date,platform,change_type,reward_text,reward_won FROM event_snapshot ORDER BY captured_date,platform"):
    print(f"  {r[0]} | {r[1]:<11} | {r[2]:<7} | {r[3]} ({r[4]})")
con.close()
