# 카드티라노 작업 규칙 (분업 · 회귀방지)

## 분업
- **디자인 = 코워크(Claude Cowork)**: 시안·비주얼·정적 컴포넌트 authoring(`*.dc.html`/목업).
- **라이브 통합·검증 = 맥(Claude Code)**: 디자인을 실제 `site/*` 파일에 옮기고 `cards.json` 등 데이터에 와이어링 + 라이브 검증/배포.
  - 데이터 바인딩 페이지(carddetail·비교표·티라노순위·카드목록)는 맥에서 통합. 순수 정적 페이지만 코워크 end-to-end 가능.

## 파일 소유권 (덮어쓰기 충돌 방지)
- **디자인 시안 파일** → 코워크.
- **라이브 사이트 파일 `site/*`, `build_data.py` 끝단, `tier_enrich.py`** → 맥에서 검증 후 확정. 코워크가 같은 파일을 export하면 맥 검증을 거쳐 머지.

## ⚠️ 회귀방지 — 주요/부가 구조화 (`tier_enrich.py`)
이벤트 주요(임계·보상·효율%)/부가(조건카테고리·보상) 구조화 로직은 **`tier_enrich.py`(맥 소유)** 에 있다.
`build_data.py`에는 `# >>> MAC-OWNED` 마커로 표시된 **import + `_te.enrich_card()` 호출 2곳**만 둔다.

**코워크가 `build_data.py`를 다시 export할 때 반드시:**
1. `# >>> MAC-OWNED … <<<` 블록(소스맵 빌드 + export 루프의 `_te.enrich_card` 호출)을 **보존**한다.
2. export 후 검증·복구:
   ```
   python tier_guard.py          # 검증(회귀면 exit 1)
   python tier_guard.py --fix    # cards.json에 main_tier/sub_tiers 재적용 복구
   ```
정상 커버리지: `main_benefit ~100장 · main_tier ~92~99장`. `main_tier < 70`이면 회귀 → `--fix`.

## 배포
`collector/*_seed.json` 등 시드를 push → GitHub Actions(06:05 KST)가 `collector.py`+`build_data.py` 실행 → `site/` 재생성 커밋 → Cloudflare. **로컬에서 `site/`를 직접 빌드·커밋하지 말 것**(카드고릴라 라이브 fetch 누락으로 퇴화). 거주지 수집물(naver/ajd/residential_meta)만 맥에서 돌려 커밋.
