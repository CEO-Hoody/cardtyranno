# 아정당 로컬 수집 셋업 (거주지 IP)

아정당은 GitHub Actions(데이터센터 IP)를 차단합니다. 회원님 맥(가정/사무실 IP)에서
하루 한 번 수집해 결과(`ajd_seed.json`)를 깃에 올리면, 클라우드 콜렉터가 그걸 읽어
`platform_events.json`에 합칩니다.

## 1. 최초 1회 준비
```bash
# 레포 클론(이미 있으면 생략)
git clone https://github.com/CEO-Hoody/cardtyranno.git
cd cardtyranno/collector/local_ajd

pip3 install requests   # (requests만 있으면 됩니다. 표준 라이브러리로도 동작)
```

## 2. (자동) 수집 대상 — 설정 불필요
스크립트가 아정당 `/card` 랜딩에서 **이번 달 발급사 이벤트를 자동 발견**하고,
각 이벤트의 발급사·최대 캐시백·대상 카드를 뽑아 우리 카드명과 매칭합니다.
월이 바뀌어 이벤트가 교체돼도 자동으로 따라갑니다. 손댈 것 없습니다.

## 3. 수동 실행 테스트
```bash
python3 collect_ajd_local.py          # 수집만(파일 생성 확인)
python3 collect_ajd_local.py --push   # 수집 + git 커밋/푸시
```
`--push` 가 인증을 물으면, 깃 인증을 먼저 설정하세요:
```bash
gh auth login        # GitHub CLI 사용 시 (brew install gh)
# 또는 https 토큰/SSH 키 설정
```

## 4. 매일 자동 실행 (macOS launchd)
아래를 `~/Library/LaunchAgents/com.cardtyranno.ajd.plist` 로 저장
(경로 `/ABSOLUTE/PATH/...` 는 본인 클론 경로로 교체):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.cardtyranno.ajd</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/ABSOLUTE/PATH/cardtyranno/collector/local_ajd/collect_ajd_local.py</string>
    <string>--push</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/ajd.log</string>
  <key>StandardErrorPath</key><string>/tmp/ajd.err</string>
</dict></plist>
```

등록:
```bash
launchctl load ~/Library/LaunchAgents/com.cardtyranno.ajd.plist
launchctl start com.cardtyranno.ajd     # 즉시 1회 실행 테스트
tail -f /tmp/ajd.log                     # 로그 확인
```
매일 오전 7시(맥이 켜져 있을 때) 자동 수집·푸시됩니다.

## 5. 클라우드 병합 (이미 콜렉터에 연동됨)
콜렉터(`collector.py`)가 `ajd_seed.json` 을 읽어 각 카드의 ajd 이벤트로 병합합니다.
즉 회원님 맥이 푸시 → 다음 일일 스크래핑에서 `cardtyranno.com/cashback` 에
아정당 캐시백이 교차비교로 함께 표시됩니다.

> 대안: GitHub **self-hosted runner** 를 맥에 등록하면 별도 푸시 없이 Actions가
> 맥(거주지 IP)에서 직접 아정당을 돌립니다. 더 자동화되지만 설정·보안 부담이 큽니다.
> 우선은 위 launchd 방식(가장 간단)을 권장합니다.
