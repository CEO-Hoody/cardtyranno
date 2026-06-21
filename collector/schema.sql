-- 카드 중개 메타 수집 DB (크로스플랫폼 상품/이벤트 매핑 + 일일 변경감지)
-- 원칙: 사실 데이터(상품ID·리워드 금액·기간)만 저장. 소개 문구는 미저장.

-- 플랫폼 마스터
CREATE TABLE IF NOT EXISTS platform(
  code TEXT PRIMARY KEY,            -- toss | cardgorilla | banksalad | ajungdang
  name TEXT NOT NULL
);

-- 카드티라노 표준 상품 (우리 기준 단일 상품)
CREATE TABLE IF NOT EXISTS card_product(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,               -- 표준 카드명 (예: 신한카드 Mr.Life)
  name_norm TEXT NOT NULL UNIQUE,   -- 정규화 키(_nk)
  issuer TEXT                       -- 카드사
);

-- 상품 ↔ 플랫폼 상품ID 매핑 (플랫폼별 product_id)
CREATE TABLE IF NOT EXISTS product_platform(
  card_product_id INTEGER NOT NULL REFERENCES card_product(id),
  platform TEXT NOT NULL REFERENCES platform(code),
  platform_product_id TEXT NOT NULL,   -- 토스3480 / 고릴라13 / CARD000004 / 75
  url TEXT,
  active INTEGER DEFAULT 1,             -- 해당 플랫폼에 현재 중개 노출 여부
  first_seen TEXT, last_seen TEXT,
  PRIMARY KEY(card_product_id, platform)
);

-- 이벤트(리워드) — 상품 × 플랫폼 = 1개 활성 이벤트 원칙
CREATE TABLE IF NOT EXISTS event(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  card_product_id INTEGER NOT NULL REFERENCES card_product(id),
  platform TEXT NOT NULL REFERENCES platform(code),
  reward_text TEXT,                 -- 원문 리워드 표기 (예: 최대 57.9만원 혜택)
  reward_won INTEGER,               -- 파싱한 원 단위 금액 (정렬·비교용)
  period_start TEXT, period_end TEXT,
  source_url TEXT,
  status TEXT DEFAULT 'active',     -- active | closed
  first_seen TEXT, last_seen TEXT
);
CREATE INDEX IF NOT EXISTS idx_event_active ON event(card_product_id, platform, status);

-- 일일 스냅샷 — 변경감지/이력
CREATE TABLE IF NOT EXISTS event_snapshot(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER REFERENCES event(id),
  card_product_id INTEGER, platform TEXT,
  captured_date TEXT NOT NULL,
  reward_text TEXT, reward_won INTEGER,
  change_type TEXT                  -- NEW | UPDATE | CLOSED | SAME
);

-- 수집 실행 로그
CREATE TABLE IF NOT EXISTS scrape_run(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_date TEXT, platform TEXT, items INTEGER, ok INTEGER, note TEXT
);
