# 프론트 작업 스펙: 고정 영역 빈칸 → "업데이트 예정"

> 이 작업은 **프론트 정본 `~/Downloads/cardtyranno-site/webdark.py`** 에서 진행한다(데이터 신호는 이미 배포됨).
> 다른 클론(`~/Documents/GitHub/cardtyranno`)의 webdark.py는 구버전이므로 **건드리지 말 것**(병행세션 클로버 방지).

## 배경
매월 1일 00시 전 플랫폼 컨텐츠가 바뀌지만 우리 수집엔 시차가 있고, 토스앱·카카오페이는 앱캡처라
사용자가 캡처를 올리기 전까지 비어 있다. 이때 **고정 레이아웃(영역 잡힌 곳)이 빈 채로 보이면 안 됨** → "업데이트 예정".
(단순 미노출 케이스 — 데이터 없으면 그냥 숨기는 곳 — 은 그대로 둔다.)

## 데이터 계약 (이미 배포됨: `site/status.json`)
```json
{ "month": "2026-07", "updated": "2026-07-01",
  "pending_platforms": ["kakaopay", "toss"],   // 이번 달 미수집(대기) 플랫폼. 비면 []
  "pending_label": "업데이트 예정" }
```
- collector.py가 매 빌드 생성. 앱캡처 stale로 SKIP된 플랫폼이 `pending_platforms`에 들어감.
- 캡처 업로드 후 재빌드되면 해당 플랫폼이 목록에서 빠짐(자동 해제).

## 구현 규칙
1. 페이지 로드시 `fetch('status.json')` 1회 → `PENDING=new Set(status.pending_platforms)`, `PLABEL=status.pending_label`.
2. **고정 플랫폼 영역**(플랫폼 비교 셀 = EVENTDETAIL 리워드그룹 / ISSUE `?v=cmp` 교차비교, carddetail 플랫폼 행, 홈 플랫폼 섹션 등 *자리가 예약된* 영역)에서 해당 플랫폼 데이터가 없을 때:
   - `PENDING.has(platform)` 이면 → 그 셀에 **`PLABEL`("업데이트 예정")** 표시(흐린 톤, 금액 자리 대체).
   - 아니면 → 기존대로 **미노출**(숨김).
3. **플랫폼 무관 고정 영역**(자리는 잡혔는데 이번 수집분이 아직 빈 섹션)도 빈 상태일 때 기존 "데이터 준비 중/없어요" 대신 일관되게 **"업데이트 예정"** 노출(영역이 *고정*인 경우만 — hide-when-empty 영역은 제외).
4. 플랫폼 키: `cardgorilla|banksalad|naver|ajungdang|toss|kakaopay`. 표기 매핑은 기존 PN 사용.
5. CLAUDE.md 프론트 규칙 준수: 이모지 금지(아웃라인/흐린 텍스트), `word-break:keep-all`, PC·모바일 둘 다 확인, 콘솔 에러 0, webdark.py 편집→`python webdark.py`→검증→커밋.

## 검증 시나리오
- `status.json`의 `pending_platforms`에 toss/kakaopay 있을 때: 비교 셀에 "업데이트 예정" 노출 확인.
- `pending_platforms: []`(평월)일 때: 라벨 안 뜨고 정상 데이터/미노출 동작 확인.
