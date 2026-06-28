# 카드티라노 커뮤니티 — 배포 가이드 (Cloudflare Workers + D1)

방문자 글/댓글/좋아요 커뮤니티 백엔드입니다. 회원가입 없이 **닉네임 + 4자리 비밀번호(해시)** 로 인증하고, 좋아요는 **IP 해시**로 중복을 막습니다.

```
community-worker/
├─ src/index.js     # Worker API (전 엔드포인트)
├─ schema.sql       # D1 스키마 (posts/comments/likes)
├─ wrangler.toml    # Worker 설정 (D1 바인딩·환경변수)
└─ package.json     # npm 스크립트
```

## 0. 사전 준비
- Node 18+ 설치
- 터미널에서: `cd community-worker && npm install`
- Cloudflare 로그인: `npx wrangler login` (브라우저에서 계정 인증)

## 1. D1 데이터베이스 생성
```bash
npx wrangler d1 create cardtyranno_community
```
출력 예시:
```
[[d1_databases]]
binding = "DB"
database_name = "cardtyranno_community"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"   ← 이 값을 복사
```
→ `wrangler.toml` 의 `database_id = "PUT-YOUR-D1-DATABASE-ID-HERE"` 를 위 값으로 교체.

> 대시보드로 만들려면: Cloudflare 대시보드 → **Workers & Pages → D1 SQL Database → Create** → 이름 `cardtyranno_community` → 생성 후 Database ID 복사.

## 2. 스키마 적용 (테이블 생성)
```bash
npm run db:init          # 운영(remote) D1에 적용
# 로컬 테스트용: npm run db:init:local
```

## 3. 환경변수 설정 (권장)
`wrangler.toml` `[vars]`:
- `SALT` — 임의의 비밀 문자열로 교체(비번/IP 해시 솔트). 운영 후 바꾸면 기존 해시와 불일치하니 처음에 정하세요.
- `ALLOW_ORIGIN` — 운영 시 `"https://cardtyranno.com"` 으로 제한 권장(기본 `*`).

민감값은 Secret으로 두는 것도 가능:
```bash
npx wrangler secret put SALT
```

## 4. 배포
```bash
npm run deploy           # = npx wrangler deploy
```
배포되면 URL이 출력됩니다: `https://cardtyranno-community.<your-subdomain>.workers.dev`

## 5. 프론트(community.html)와 연결
`site/community.html` 상단 스크립트의 API 주소를 배포 URL로 바꿉니다. 두 방법 중 하나:

- (간단) `community.html` 의 `var CAPI = '...'` 기본값을 배포 URL로 교체 후 재배포, 또는
- (권장·무수정) Cloudflare 대시보드에서 Worker에 **커스텀 라우트** `cardtyranno.com/api/community/*` 를 연결.
  - `wrangler.toml` 의 `routes` 주석을 해제하고 재배포하면, 프론트는 같은 도메인 `/api/community/*` 로 호출 → CORS·URL 교체 불필요.
  - 이 경우 `community.html` 은 `location.origin + '/api/community'` 를 자동 사용하도록 되어 있습니다(아래 참고).

> community.html 의 API 결정 로직: `window.COMMUNITY_API` → `<meta name="community-api">` → 기본값(workers.dev) 순. 운영 라우트(`/api/community`)를 쓰면 meta로 지정하세요.

## 6. 동작 확인
```bash
curl https://cardtyranno-community.<subdomain>.workers.dev/api/health
# {"ok":true,"service":"cardtyranno-community","categories":["자유","카드추천","이벤트공유","질문"]}
```

## API 요약
| 메서드 | 경로 | 설명 |
|---|---|---|
| GET | /api/posts?page=&size=&category=&sort=new\|popular | 글 목록 |
| GET | /api/posts/:id | 글 상세 + 댓글 |
| POST | /api/posts | 글 작성 {nickname,password(4자리),title,content,category,card_event_id} |
| PUT | /api/posts/:id | 글 수정 {password,title,content,category} |
| DELETE | /api/posts/:id | 글 삭제 {password} |
| POST | /api/posts/:id/comments | 댓글 작성 {nickname,password,content} |
| DELETE | /api/comments/:id | 댓글 삭제 {password} |
| POST | /api/posts/:id/like | 글 좋아요 토글 |
| POST | /api/comments/:id/like | 댓글 좋아요 토글 |

## 보안 메모
- 비밀번호 평문 미저장(SHA-256 + SALT). 단 4자리라 강한 보안은 아님 — 글 소유 확인용 수준.
- IP 원본 미저장, `ip_hash`(SHA-256 앞 32자)만 저장.
- 운영 시 `ALLOW_ORIGIN` 을 cardtyranno.com 으로 제한하고, 필요 시 rate-limit(Cloudflare WAF/Turnstile) 추가 권장.
- 욕설/스팸 필터, 신고 기능은 후속 과제.
