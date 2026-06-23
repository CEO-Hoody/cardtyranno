# 통합 원장 수집기 설치·실행 안내 (collect_ledger.py)

이 스크립트는 **회원님 맥(거주지 인터넷)** 에서 돌려야 합니다.
GitHub의 자동수집 서버는 데이터센터라 네이버·뱅샐 같은 사이트가 막히거나, 광고용 뻥튀기 금액이 섞입니다.
회원님 맥에서 '실제 화면에 보이는 텍스트'를 그대로 읽어 정확한 원장을 만듭니다.

---

## 1. 최초 1회 설치 (터미널에 아래 3줄을 한 줄씩 붙여넣고 Enter)

터미널 여는 법: `Command(⌘) + Space` → "터미널" 입력 → Enter

```
pip3 install playwright requests
python3 -m playwright install chromium
cd ~/Documents/Claude/Projects/제휴마케팅\ 콜렉터/collector/local_ledger
```

(맨 아랫줄 경로는 실제 프로젝트 폴더 위치에 맞춰 주세요. 폴더를 터미널로 끌어다 놓으면 경로가 자동 입력됩니다.)

## 2. 실행 (수집만)

```
python3 collect_ledger.py
```

→ `collector/ledger.json`(통합 원장)과 `collector/banksalad_seed.json`(보정값)이 갱신됩니다.

## 3. 실행 (수집 + 사이트 반영까지)

```
python3 collect_ledger.py --push
```

→ 수집 후 자동으로 GitHub에 올라가고, 잠시 뒤 cardtyranno.com에 반영됩니다.

---

## 4. 매일 자동 실행 (선택)

매일 아침 7시에 자동으로 돌게 하려면, 아래 내용을 파일로 저장하세요.
파일 경로: `~/Library/LaunchAgents/com.cardtyranno.ledger.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.cardtyranno.ledger</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/사용자명/Documents/Claude/Projects/제휴마케팅 콜렉터/collector/local_ledger/collect_ledger.py</string>
    <string>--push</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/cardtyranno_ledger.log</string>
  <key>StandardErrorPath</key><string>/tmp/cardtyranno_ledger.err</string>
</dict>
</plist>
```

(`/Users/사용자명/...` 부분을 실제 경로로 바꾸세요.) 저장 후 터미널에서:

```
launchctl load ~/Library/LaunchAgents/com.cardtyranno.ledger.plist
```

---

## 무엇을 수집하나

- **카드고릴라**: API로 카드명·발급사·플레이트 이미지·캐시백 이벤트(`/event/detail/{id}` 링크)
- **뱅크샐러드**: 헤드리스 브라우저로 상품 페이지의 **렌더링된 텍스트**에서 실제 이벤트 금액
  (예: 삼성 iD SELECT ALL = 최대 23만원 — API의 잘못된 119만원을 덮어씁니다)
- **네이버페이·아정당**: 같은 폴더의 `collect_naver_local.py`, `../collect_ajd_local.py` 와 함께 돌리면 됩니다.

## 원장 구조 (ledger.json)

- 상품마다 **임의 ID**(P0001…)를 부여합니다.
- 플랫폼 간 매핑은 **상품명** 기준입니다.
- ★ "토스 미스터라이프카드"와 "미스터라이프 카드"는 **다른 상품**으로 저장됩니다(이름이 다르므로 자동 분리).

## 카드를 더 추가하려면

`collect_ledger.py` 안의 `BANKSALAD_GUIDS` 목록에 `"카드명": "CARD번호"` 를 추가하면 됩니다.
(CARD번호는 banksalad.com에서 카드 상세 페이지 주소 끝의 `CARD0000xx` 부분입니다.)
뱅샐 이벤트 차트는 매 실행 시 자동으로 추가 상품을 찾아보긴 하지만, 직접 넣어주면 가장 확실합니다.
