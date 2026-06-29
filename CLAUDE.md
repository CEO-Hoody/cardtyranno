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

---

# 프론트 구현 규칙 (데이터 ↔ 시안 정합 — 재발방지)

## 0. 프론트 생성 파이프라인
- **모든 `site/*.html`은 `webdark.py`(루트) 생성물.** 페이지 본문은 webdark.py 안의 문자열 템플릿(`INDEX_BODY/JS`, `CARDDETAIL_*`, `EVENTDETAIL_*`(=이번달 캐시백 리워드그룹), `ISSUE_*`(=이번달 캐시백+`?v=cmp` 플랫폼비교) 등). **HTML 직접 수정 금지 → webdark.py 편집 후 `python webdark.py` 재생성.**
- `python webdark.py`는 로컬 JSON만 읽어 HTML 생성(네트워크 fetch 없음) → **로컬 실행·검증 안전.** (단 `scrape/installment.json` 등 콜렉터 산출물이 없으면 그 페이지에서 멈춤 → 빈 stub 후 `git checkout`으로 되돌리거나 해당 페이지만 무시.)
- 페이지는 런타임에 `fetch('cards.json'…)`으로 데이터 바인딩 → 데이터 갱신돼도 HTML 재생성 불필요.

## 1. 데이터 스키마 위치 — **추측 금지, 여기서 확인**
"데이터에 없다 / 한계다"라고 결론짓기 전에 반드시 아래와 `tier_enrich.py`를 먼저 확인할 것. (과거 `platform_events.breakdown`만 보고 "부가 카테고리 없음"이라 오판 → 실은 `cards.json.sub_tiers`에 있었음.)
- **`site/cards.json`** `{month,source,order,apply,cards:{발급사:[card…]}}`. card 키: `id,name,issuer,img,fee,benefit,detail,events,plat,rank,source,main_benefit,sub_benefits,` **`main_tier`{spend,reward,eff,text}** · **`sub_tiers`[{cat,icon,reward,text}]**(tier_enrich 산출). → **카드별 주요/부가 구조화 캐시백·유형은 전부 여기.** sub_tiers 유형: 해외·자동납부·리볼빙·쿠폰·추가이용·마케팅동의·멤버십·여행·오프라인·연회비·간편결제.
- **`site/platform_events.json`** `{updated,month,reward_groups,products:[{id,name,issuer,img,platforms,events:[{platform,reward_won,main_won,bonus_won,reward_text,period_end,url,breakdown,reward_group}]}]}`. `breakdown`=헤드라인 텍스트(카테고리 아님). **유형별 부가가 필요하면 product를 cards.json과 매칭해 `sub_tiers`를 써라.**
- **`reward_groups`**(platform_events 최상위): `{gid:{month,platform,issuer,reward_won,reward_text,count,cards}}`. `reward_group` id = `"월|플랫폼|카드사|reward_won"`. **리워드그룹 = (월·플랫폼·카드사·조건[reward_won]) 동일 상품**(URL/플랫폼 전체로 묶지 말 것). collector.py가 영속, 프론트는 `e.reward_group` 우선·없으면 동일 키 파생.
- 기타: `rank.json`(items[{name,issuer,rank,avg…}]), `reco.json`, `hero.json`, `history/{YYYY-MM}.json`{cards:[{name,issuer,platforms,max}],issuers}, `events.json`, `data.json`, `issue.json`.

## 2. 시안(.dc.html) 구현 규칙
- 가이드 .dc.html은 섹션마다 **좌=PC 시안 · 우=모바일 시안이 따로** 있다. **둘 다 읽고 각각 반응형으로 맞춰라**(모바일 전용 축소·재배치·삭제·세로스택·칩 줄바꿈·큰 플레이트 금지 등 노란 메모 반드시 반영). PC만 보고 모바일에 그대로 줄여쓰기 금지.
- **흰색 프레임 안만 실제 사이트.** 회색 섹션 제목·프레임 라벨·노란/분홍 메모는 가이드 주석 → 사이트에 텍스트로 넣지 말 것. 메모가 시안과 충돌하면 **메모 우선.**
- **시안의 더미는 실데이터로 교체**: 공룡 파스텔 플레이트 → **실제 카드 이미지**(`imgTag(p.img)`). **단** 알 둥지(`__eggs`)·티라노 글리프·커플 엠블럼 등 **브랜드 일러스트는 더미가 아니므로 SVG로 포팅**.
- **이모지 금지 → 아웃라인 글리프.** (데이터의 `sub_tiers[].icon`이 이모지여도 UI는 outline SVG로 매핑해서 표시.) 회색 본문 금지(weight로 위계), 마젠타 페이지당 1회, CTA pill 50px, 카드=흰배경+1px 헤어라인(그림자 금지).
- 외부 광고/제휴 링크 = `rel="sponsored nofollow"` + "광고(AD)" 라벨.

## 3. 구현/CSS 주의
- **CSS 클래스명 페이지 내 재사용 충돌 주의**(`.rg-sub`가 헤더부제·부가카드에 중복돼 테두리/flex 상속 사고 → `.rg-hsub`로 분리). 새 컴포넌트는 고유 prefix.
- 한글 줄바꿈 깨짐 방지: `word-break:keep-all`.

## 4. 검증 (push 전 필수)
- 로컬 정적서버(`python -m http.server`) + 프리뷰로 **PC·모바일 둘 다** 렌더 확인, **콘솔 에러 0**, 실데이터로 의도대로 표시되는지 확인 후에만 push.
- 작업 흐름: webdark.py 편집 → `python webdark.py` → site/*.html 검증 → 커밋·push → (데이터 파이프라인 변경분은 다음 CI 빌드에 반영).
