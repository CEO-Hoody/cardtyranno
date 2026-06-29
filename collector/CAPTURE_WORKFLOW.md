# 토스 앱 · 카카오페이 캡처 처리 워크플로 (매월 수동)

토스 앱·카카오페이는 **공개 웹 스크래핑 소스가 없어** 앱 캡처를 비전 분석해서 적재한다.
따라서 매월 1일 자동수집은 이 둘을 **자동으로 채울 수 없다.** 아래 절차로 매달 1회 갱신한다.

## 동작 원리 (stale 가드)
`toss_seismo_seed.json` · `kakaopay_seed.json` 상단의 `"month"`(예: `"2026-07"`)을
`collector.py`가 현재월(KST)과 비교 → **다르면 주입 SKIP**(전월 캡처가 신월 데이터에 섞이는 것 방지).
즉 7월 1일 자동수집은 6월 캡처 시드를 건너뛰고 토스앱·카카오를 **비운 채** 빌드한다.
로그: `⚠️ … 앱캡처 시드 stale(시드=2026-06, 현재=2026-07) — 주입 SKIP …`

## 매월 절차
1. **(사용자)** 토스 앱·카카오페이 앱에서 그 달 카드 이벤트 화면 캡처 → 폴더로 업로드
   (예: `~/Downloads/토스 7월/`, `~/Downloads/카카오페이 7월 이벤트/`). 어시스턴트에게 알림.
2. **(어시스턴트)** 각 캡처 이미지를 Read(비전)로 읽어 이벤트 추출 →
   `toss_seismo_seed.json` · `kakaopay_seed.json`을 **그 달 month로** 재작성(아래 스키마).
   카드명은 반드시 우리 카드 유니버스(cards.json) 표기와 일치시킬 것(불일치 시 주입 누락).
3. **(어시스턴트)** 시드를 git 클론에 반영 → `bash fullbuild_deploy.sh`(또는 collector.py+build_data) →
   guard 통과(month 일치)로 토스앱·카카오 주입됨 → push·배포.

## 시드 스키마
```json
{
  "_source": "토스 앱 7월 이벤트 캡처(비전 분석)",
  "_captured": "2026-07-01",
  "month": "2026-07",                       // ← 현재월. 가드 통과 핵심.
  "platform": "toss",                       // 또는 "kakaopay"
  "events": [
    {
      "issuer": "롯데카드",
      "cards": ["롯데카드 LOCA LIKIT 1.5", "롯데카드 LOCA LIKIT 2.0"],  // 우리 표기와 일치
      "reward_won": 150000,                 // 국내 이용 메인 캐시백(타 플랫폼 비교용)
      "headline_won": 620000,               // 앱 헤드라인 '최대 N만원'(국내+해외+쿠폰 합산)
      "reward_text": "25만원 이상 이용 시 최대 15만 토스포인트 + 해외 30만 + 쿠폰 10만",
      "period_start": "2026-07-01",
      "period_end": "2026-07-31",
      "url": "https://toss.im/_m/..."        // 있으면. 카카오는 fest.kakaopay.com 그룹 링크
    }
  ]
}
```
- 토스: `reward_won` = 헤드라인과 동일(토스포인트=원 1:1)인 경우 많음. 카카오: `reward_won`(국내 메인) < `headline_won`(마케팅 합산).
- `reward_text`에 `+` 티어(해외/리볼빙/쿠폰)를 적으면 build_data가 부가혜택으로 분해·유형분류(tier_enrich).
