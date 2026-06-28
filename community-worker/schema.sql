-- 카드티라노 커뮤니티 D1 스키마 (Cloudflare D1 / SQLite)
-- 적용: wrangler d1 execute cardtyranno_community --file=./schema.sql  (로컬은 --local)
-- 비고: 비밀번호는 평문 저장 금지 → pw_hash(SHA-256)만 저장. IP는 ip_hash로만.

PRAGMA foreign_keys = ON;

-- 글
CREATE TABLE IF NOT EXISTS posts (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  author_nickname TEXT    NOT NULL,
  author_ip_hash  TEXT,                         -- 작성자 IP 해시(작성자 식별/남용 방지용, 원본 IP 미저장)
  pw_hash         TEXT    NOT NULL,             -- 수정/삭제 인증용 비밀번호 해시
  title           TEXT    NOT NULL,
  content         TEXT    NOT NULL,
  category        TEXT    NOT NULL DEFAULT '자유',   -- 자유 | 카드추천 | 이벤트공유 | 질문
  card_event_id   TEXT,                         -- 카드/이벤트 연결(카드명 또는 events.html?n=... 식별자)
  likes           INTEGER NOT NULL DEFAULT 0,
  views           INTEGER NOT NULL DEFAULT 0,
  created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 댓글
CREATE TABLE IF NOT EXISTS comments (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id         INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  author_nickname TEXT    NOT NULL,
  author_ip_hash  TEXT,
  pw_hash         TEXT    NOT NULL,             -- 댓글 삭제 인증용
  content         TEXT    NOT NULL,
  likes           INTEGER NOT NULL DEFAULT 0,
  created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 좋아요(중복 방지: 같은 IP해시가 같은 대상에 1회만)
CREATE TABLE IF NOT EXISTS likes (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  target_type TEXT    NOT NULL,                 -- 'post' | 'comment'
  target_id   INTEGER NOT NULL,
  ip_hash     TEXT    NOT NULL,
  created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
  UNIQUE(target_type, target_id, ip_hash)
);

CREATE INDEX IF NOT EXISTS idx_posts_cat     ON posts(category, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_likes   ON posts(likes DESC);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id, created_at);
CREATE INDEX IF NOT EXISTS idx_likes_target  ON likes(target_type, target_id);
