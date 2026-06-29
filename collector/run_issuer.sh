#!/bin/bash
# 카드티라노 카드사 자체 이벤트 일일 수집 러너 — 사용자 Mac에서 launchd로 매일 실행.
# collect_issuer_local.py(각 카드사 사이트 거주지 IP 렌더 수집) 실행 → collector/issuer_seed.json 생성
# → git 저장소면 커밋·푸시(다음 daily-scrape Action 빌드에서 라이브 반영), 아니면 파일만 만들고 안내.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
PROJ="/Users/hoody/Documents/Claude/Projects/제휴마케팅 콜렉터"
LOG="$PROJ/collector/issuer.log"
cd "$PROJ" || { echo "$(date) 프로젝트 폴더 없음" >> "$LOG"; exit 1; }

echo "===== $(date '+%Y-%m-%d %H:%M:%S') 카드사 이벤트 수집 시작 =====" >> "$LOG"

# 1) 수집 실행 (playwright 필요: pip3 install playwright && python3 -m playwright install chromium)
python3 collector/collect_issuer_local.py >> "$LOG" 2>&1
if [ $? -ne 0 ]; then
  echo "[!] collect_issuer_local.py 실행 실패 — playwright 설치/네트워크 확인" >> "$LOG"
  exit 1
fi

# 2) git 저장소면 변경분 커밋·푸시
if [ -d "$PROJ/.git" ]; then
  git add collector/issuer_seed.json >> "$LOG" 2>&1 || true
  if git diff --cached --quiet; then
    echo "[=] 변경 없음" >> "$LOG"
  else
    git commit -m "issuer events refresh $(date +%F)" >> "$LOG" 2>&1
    if git push >> "$LOG" 2>&1; then
      echo "[✓] 푸시 완료 → 다음 daily-scrape 빌드에서 반영" >> "$LOG"
    else
      echo "[!] git push 실패 — 원격/인증(토큰·키체인) 설정 확인" >> "$LOG"
    fi
  fi
else
  echo "[i] git 저장소 아님 — collector/issuer_seed.json 을 수동 업로드(GitHub) 하세요." >> "$LOG"
fi
echo "===== $(date '+%H:%M:%S') 종료 =====" >> "$LOG"
