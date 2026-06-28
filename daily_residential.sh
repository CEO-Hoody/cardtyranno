#!/bin/bash
# 카드티라노 거주지 일일 배치 (launchd, 홈 루트=TCC 비보호).
# 거주지 IP에서만 되는 수집(네이버·아정당·원장)을 매일 갱신 → git push.
# 카드고릴라/뱅샐/토스 메타는 클라우드 GitHub Actions가 담당(시드 충돌 방지).
# 빌드(build_data→site/)는 클라우드/Cowork 환경. 이 잡은 '데이터 수집+push'만.
set -u
export HOME=/Users/hoody
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
PY=/usr/bin/python3
REPO=/Users/hoody/cardtyranno-auto
cd "$REPO" || exit 1

echo "===== $(date '+%F %T') 거주지 배치 시작 ====="

# 0) 최신 동기화 (코드+타 플랫폼 시드)
git pull --no-edit 2>&1 || echo "[warn] pull 경고 — 계속"

# 1) 거주지 수집 (각 단계 독립; 실패해도 다음 진행)
#    naver_seed → ajd_seed → residential_meta(두 시드의 URL 렌더해 주요/부가) → 원장 순서.
#    ajd는 v2(headless 렌더+유니버스 역매칭)로 8이벤트≈22장 정상 수집.
"$PY" collector/local_ajd/collect_naver_local.py 2>&1 || echo "[err] naver 수집 실패"
"$PY" collector/local_ajd/collect_ajd_local.py    2>&1 || echo "[err] ajd 수집 실패"
"$PY" collector/residential_meta.py               2>&1 || echo "[err] residential_meta 실패"
"$PY" collector/local_ledger/collect_ledger.py    2>&1 || echo "[err] ledger 실패"

# banksalad_seed.json은 클라우드 scrape_banksalad_meta(API 63장·서술티어)가 소유.
# collect_ledger.py가 렌더텍스트 13장으로 덮어쓰므로 커밋 전 origin 버전으로 되돌림.
git checkout -- collector/banksalad_seed.json 2>/dev/null || true

# 2) 통합 커밋·push (거주지 산출물만; origin 변동 대비 pull→push 재시도)
git add -A collector scrape 2>/dev/null
if git diff --cached --quiet; then
  echo "변경 없음 — push 생략"
else
  git commit -m "daily residential collect $(date +%F)" 2>&1
  ok=0
  for i in 1 2 3; do
    if git pull --no-edit 2>&1 && git push 2>&1; then ok=1; echo "push 성공"; break; fi
    echo "[retry] push 재시도 $i"; sleep 5
  done
  [ "$ok" = 1 ] || echo "[err] push 최종 실패"
fi
echo "===== $(date '+%F %T') 배치 종료 ====="
