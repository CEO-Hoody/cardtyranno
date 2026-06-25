# 프테라노돈(pteranodon) — 결제처 카드할인 수집기 안내

용각류 모듈들이 '카드 발급 캐시백'을 모은다면, **프테라노돈은 '무신사·하이마트 등 결제처에서 특정
카드로 결제 시 받는 할인'**을 모읍니다. 회원님 맥(거주지 IP)에서 헤드리스 브라우저로 결제처/카드사
이벤트 페이지의 **렌더링된 화면 텍스트**를 읽어, (카드사 + 금액 + 할인유형)을 추출합니다.
(카드 캐시백에서 검증된 방식과 동일)

## 설치 (최초 1회)

```
pip3 install playwright
python3 -m playwright install chromium
```

## 실행

```
python3 collector/pteranodon.py            # 수집 → discount_seed.json + site/data.json 병합
python3 collector/pteranodon.py --push      # 수집 + git push (사이트 자동 반영)
python3 collector/pteranodon.py --dry       # 브라우저 없이 파서만 점검(샘플 텍스트)
```

## 동작

1. `collector/pteranodon.py` 안의 `MERCHANTS` 레지스트리(결제처명·도메인·온오프라인·소스 URL)를 순회.
2. 각 페이지를 헤드리스 크롬으로 열고 **본문 텍스트**를 읽음.
3. 한 줄에 `카드사 + 금액(원/%) + 할인유형(즉시할인·청구할인·캐시백·적립…)`이 있으면 한 항목으로 추출.
   - "N원 이상" 같은 **임계금액은 할인액에서 제외**(min 으로 따로 저장).
4. `collector/discount_seed.json` 저장 + `site/data.json` 에 병합(수기 항목은 보존, 신규만 추가).
5. `--push` 면 커밋·푸시 → Cloudflare 자동 배포.

## 출력 스키마 (site/data.json 항목과 동일)

`plat`(결제처) · `domain` · `gubun`(온/오프라인) · `card`/`tab`(카드·카드사) · `type`(할인유형) ·
`min`(최소결제) · `disc`(할인액) · `cond` · `period` · `conf`(자동수집=중, 수기검증=상) · `url`

## 결제처 추가 / 정확도 높이기

- `MERCHANTS` 리스트에 `{"plat","domain","gubun","src","url"}` 한 줄 추가하면 그만큼 더 수집됩니다.
- 결제처마다 페이지 구조가 달라, 첫 실행 결과를 보고 키워드(`ISSUERS`/`TYPE_KW`)나 소스 URL을 보강하면
  정확도가 올라갑니다. (카드 캐시백 수집기도 동일하게 점진적으로 다듬었습니다.)
- 자동수집 항목은 `conf:"중"`으로 들어갑니다. 사람이 확인한 항목은 `"상"`으로 올리면 됩니다.

## 매일 자동 실행

`collector/local_ledger/SETUP.md` 의 launchd 예시와 동일한 방식으로,
`ProgramArguments` 의 스크립트 경로만 `collector/pteranodon.py` 로 바꾼 plist를 추가하면
매일 자동으로 결제처 할인까지 갱신됩니다.
