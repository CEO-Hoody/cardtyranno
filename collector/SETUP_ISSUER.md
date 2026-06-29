# 카드사 자체 이벤트 거주지 수집 — 설치/운영 가이드

각 카드사(삼성·현대·KB국민·신한·롯데·우리·하나·NH농협·IBK) **자체 사이트의 발급 캐시백/프로모션**을
거주지 IP(회원님 맥)에서 Playwright로 직접 수집합니다. 카드고릴라·토스 등 중개 플랫폼과 **별개 소스**이며,
데이터센터(GitHub Actions)에서 차단/빈 렌더되는 카드사 사이트를 거주지 IP로 우회합니다.

- 소속: 카카오페이 플랫폼프로덕트유닛 · 이름: hoody.s

## 0. 구성요소
| 파일 | 역할 |
|---|---|
| `collector/collect_issuer_local.py` | 로컬 수집기 (Playwright 렌더 + 금액·주요/부가 파싱 + 카드 유니버스 역매칭) |
| `collector/issuer_event_urls.json` | **카드사별 이벤트 리스트 URL (직접 확인·편집)** |
| `collector/issuer_seed.json` | 수집 결과 (collector.py가 자동 주입) |
| `collector/run_issuer.sh` | launchd 러너 (수집→git push) |
| `collector/com.cardtyranno.issuer.plist` | 매일 자동 실행(7:50) |

## 1. 사전 설치 (최초 1회)
```bash
pip3 install playwright
python3 -m playwright install chromium
```

## 2. 이벤트 URL 확인·편집  ⚠ 중요
카드사 이벤트 페이지 URL은 개편으로 자주 바뀝니다. `issuer_event_urls.json` 에 카드사별 **'이벤트(진행중) 리스트' URL** 을 넣습니다(여러 개면 배열로).
- 확인법: 브라우저에서 카드사 홈 → **이벤트** 메뉴 클릭 → 주소창 URL 복사 → JSON에 붙여넣기.
- **2026-06 브라우저 확인(6개):** 삼성 `personal/event/ing/UHPPBE1401M0.jsp` · 현대 `cpb/ev/CPBEV0101_01.hc` · KB국민 `card.kbcard.com/BON/DVIEW/HBBMCXCRVNEC0001` · 신한 `mob/MOBFM829N/MOBFM829R01.shc`(상세=`/pconts/html/benefit/event/{id}.html`) · 롯데 `app/LPBNFDA_V100.lc` · 우리 `dcpc/yh1/bnf/bnf02/prgevnt/H1BNF202S00.do`.
- **best-effort(3개, 맥에서 0건이면 교체):** 하나(iframe 사이트)·NH농협(무거운 SPA)·IBK(은행 도메인, 원격 확인 불가). 맥에서 해당 카드사 이벤트 메뉴 URL을 직접 복사해 넣으세요.

## 3. 수집 실행
```bash
cd "/Users/hoody/Documents/Claude/Projects/제휴마케팅 콜렉터"
python3 collector/collect_issuer_local.py            # 수집만 (issuer_seed.json 생성)
python3 collector/collect_issuer_local.py --push     # 수집 + git commit/push (라이브 반영)
python3 collector/collect_issuer_local.py --only 삼성카드   # 특정 카드사만(URL 디버그)
```
실행 끝에 카드사별 매칭 건수가 출력됩니다. **`⚠ 0건`** 인 카드사는 §2에서 URL을 고친 뒤 다시 실행하세요.

## 4. 매일 자동 실행 (launchd)
```bash
cp "collector/com.cardtyranno.issuer.plist" ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.cardtyranno.issuer.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.cardtyranno.issuer.plist
launchctl start  com.cardtyranno.issuer      # 즉시 1회 테스트
tail -f collector/issuer.log                 # 로그 확인
```
해제: `launchctl unload ~/Library/LaunchAgents/com.cardtyranno.issuer.plist`

## 5. 라이브 반영 흐름
`issuer_seed.json` push → 다음 **daily-scrape Action** 빌드에서 `collector.py`가 주입
→ `platform_events.json` 에 **platform="issuer"(카드사 공식)** 이벤트로 합류 → cashback 비교/이번달 캐시백에 노출.
(주요/부가 분해 `main_won`/`bonus_won` 포함. 카드 매칭은 우리 카드 유니버스 역매칭 — 신규 상품 생성 안 함.)

## 6. 동작 원리(요약)
1. 카드사별 이벤트 리스트 렌더 → 이벤트 상세 링크 발견(없으면 리스트 자체 파싱)
2. 각 페이지 텍스트에서 `최대 N만원`(전체) + `N만원 이상/쓰면/결제 시 M만원`(주요) 추출, 부가=전체-주요
3. 우리 카드 유니버스(해당 발급사)를 텍스트에 역매칭 → 카드명 확정
4. `issuer_seed.json` 저장

## 7. 트러블슈팅
- **전부 0건**: playwright/chromium 미설치 또는 URL 오류. `--only`로 카드사별 점검.
- **특정 카드사 0건**: §2에서 URL 교체. 일부 카드사는 로그인/앱 전용이라 공개 페이지에 발급 캐시백이 없을 수 있음(정상).
- **금액 오검출**: 카드사 페이지에 '최대 N만원'이 광고문구로 과다 표기될 수 있음 → 필요 시 `collect_issuer_local.py`의 `AMT_HEAD`/`TIER_MAIN` 정규식 조정.
