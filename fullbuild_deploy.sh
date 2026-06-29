#!/bin/bash
# 카드티라노 맥 풀빌드+배포 (launchd). 거주지 수집 → 전체 site/ 빌드 → push.
# 기존 daily_residential.sh(시드만)와 달리, 이 스크립트는 맥에서 collector.py+build_data까지
# 돌려 site/를 직접 생성·배포한다(클라우드 06:05 cron을 안 기다림). 7월 1일 3회(00/06/14시)용.
#  - collector.py가 카드고릴라(443)·뱅샐(API 63장)·토스를 라이브 재생성 → ledger 클로버 자가치유.
#  - 월 라벨/필터/스냅샷은 KST 동적(2026-07.json 자동 생성). build_data 끝단은 tier_enrich 보존.
set -u
export HOME=/Users/hoody
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export LANG=ko_KR.UTF-8
PY=/usr/bin/python3
REPO=/Users/hoody/cardtyranno-auto
LOG=/tmp/cardtyranno_fullbuild.log
cd "$REPO" || exit 1

echo "===== $(date '+%F %T') 풀빌드+배포 시작 =====" >> "$LOG"

# 0) 깨끗한 최신 상태 (stale/미커밋 충돌 방지 — origin이 진실)
git fetch origin main >> "$LOG" 2>&1
git reset --hard origin/main >> "$LOG" 2>&1

# 1) 거주지 수집 (7월 신규 이벤트 — 거주지 IP 전용 소스)
"$PY" collector/local_ajd/collect_naver_local.py >> "$LOG" 2>&1 || echo "[err] naver" >> "$LOG"
"$PY" collector/local_ajd/collect_ajd_local.py    >> "$LOG" 2>&1 || echo "[err] ajd"   >> "$LOG"
"$PY" collector/residential_meta.py               >> "$LOG" 2>&1 || echo "[err] resid" >> "$LOG"
"$PY" collector/local_ledger/collect_ledger.py    >> "$LOG" 2>&1 || echo "[err] ledger">> "$LOG"

# 2) 풀빌드 — collector.py가 카드고릴라/뱅샐/토스 라이브 재생성(ledger 클로버 자가치유) + 거주지 시드 주입
"$PY" collector/collector.py >> "$LOG" 2>&1 || echo "[err] collector.py" >> "$LOG"
"$PY" build_data.py          >> "$LOG" 2>&1 || echo "[err] build_data"   >> "$LOG"

# 3) 구조화 회귀 검증(실패해도 배포 계속 — 로그로 경고)
"$PY" tier_guard.py >> "$LOG" 2>&1 || echo "[warn] tier_guard 회귀 — 확인 필요" >> "$LOG"

# 4) 커밋·push (site + seeds + meta). origin 변동 대비 pull(-X ours)→push 재시도.
git add -A site collector scrape 2>/dev/null
git add -f collector/meta.db 2>/dev/null || true
if git diff --cached --quiet; then
  echo "변경 없음 — push 생략" >> "$LOG"
else
  git commit -m "fullbuild deploy $(date '+%F %H:%M')" >> "$LOG" 2>&1
  ok=0
  for i in 1 2 3; do
    if git pull --no-rebase -X ours --no-edit >> "$LOG" 2>&1 && git push >> "$LOG" 2>&1; then ok=1; echo "push 성공" >> "$LOG"; break; fi
    echo "[retry] push $i" >> "$LOG"; sleep 5
  done
  [ "$ok" = 1 ] || echo "[err] push 최종 실패" >> "$LOG"
fi
echo "===== $(date '+%F %T') 풀빌드+배포 종료 =====" >> "$LOG"
