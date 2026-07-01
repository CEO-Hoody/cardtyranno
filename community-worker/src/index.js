/**
 * 카드티라노 커뮤니티 Worker (Cloudflare Workers + D1)
 * - 회원가입 없이 닉네임 + 4자리 비밀번호(해시) 인증
 * - 좋아요는 IP 해시로 중복 방지(토글)
 * - D1 바인딩 이름: DB  (wrangler.toml의 [[d1_databases]] binding="DB")
 * - 환경변수(선택): SALT (비번/IP 해시 솔트), ALLOW_ORIGIN (CORS 허용 오리진; 기본 *)
 */

const CATEGORIES = ["자유", "카드추천", "이벤트공유", "질문"];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { pathname } = url;
    const method = request.method;
    const origin = resolveOrigin(request, env);

    // CORS preflight
    if (method === "OPTIONS") return cors(new Response(null, { status: 204 }), origin);

    try {
      const r = await route(request, env, url, pathname, method);
      return cors(r, origin);
    } catch (e) {
      return cors(json({ error: String(e && e.message || e) }, 500), origin);
    }
  },
};

async function route(request, env, url, pathname, method) {
  const db = env.DB;
  if (!db) return json({ error: "D1 바인딩(DB) 없음 — wrangler.toml 확인" }, 500);

  // GET /api/posts  목록(페이지네이션·카테고리·정렬)
  if (pathname === "/api/posts" && method === "GET") {
    const page = Math.max(1, parseInt(url.searchParams.get("page") || "1", 10));
    const size = Math.min(50, Math.max(1, parseInt(url.searchParams.get("size") || "20", 10)));
    const cat = url.searchParams.get("category") || "";
    const sort = url.searchParams.get("sort") || "new"; // new | popular
    const order = sort === "popular" ? "likes DESC, views DESC, id DESC" : "id DESC";
    const where = (cat && CATEGORIES.includes(cat)) ? "WHERE category = ?" : "";
    const binds = where ? [cat] : [];
    const total = (await db.prepare(`SELECT COUNT(*) AS n FROM posts ${where}`).bind(...binds).first()).n;
    const rows = (await db.prepare(
      `SELECT id, author_nickname, title, category, card_event_id, likes, views, created_at,
              (SELECT COUNT(*) FROM comments c WHERE c.post_id = posts.id) AS comment_count
       FROM posts ${where} ORDER BY ${order} LIMIT ? OFFSET ?`
    ).bind(...binds, size, (page - 1) * size).all()).results;
    return json({ page, size, total, posts: rows });
  }

  // GET /api/posts/:id  상세 + 댓글
  let m = pathname.match(/^\/api\/posts\/(\d+)$/);
  if (m && method === "GET") {
    const id = +m[1];
    await db.prepare("UPDATE posts SET views = views + 1 WHERE id = ?").bind(id).run();
    const post = await db.prepare(
      `SELECT id, author_nickname, title, content, category, card_event_id, likes, views, created_at, updated_at
       FROM posts WHERE id = ?`
    ).bind(id).first();
    if (!post) return json({ error: "글을 찾을 수 없어요." }, 404);
    const comments = (await db.prepare(
      `SELECT id, author_nickname, content, likes, created_at FROM comments WHERE post_id = ? ORDER BY id ASC`
    ).bind(id).all()).results;
    return json({ post, comments });
  }

  // POST /api/posts  작성
  if (pathname === "/api/posts" && method === "POST") {
    const b = await request.json();
    const nick = clean(b.nickname, 20);
    const title = clean(b.title, 120);
    const content = clean(b.content, 8000);
    const pw = String(b.password || "");
    let category = CATEGORIES.includes(b.category) ? b.category : "자유";
    if (!nick || !title || !content) return json({ error: "닉네임·제목·내용을 모두 입력해주세요." }, 400);
    if (!/^\d{4}$/.test(pw)) return json({ error: "비밀번호는 4자리 숫자예요." }, 400);
    const pwHash = await sha256(pw + ":" + nick, env);
    const ipHash = await ipHashOf(request, env);
    const res = await db.prepare(
      `INSERT INTO posts (author_nickname, author_ip_hash, pw_hash, title, content, category, card_event_id)
       VALUES (?, ?, ?, ?, ?, ?, ?)`
    ).bind(nick, ipHash, pwHash, title, content, category, clean(b.card_event_id, 200) || null).run();
    return json({ id: res.meta.last_row_id }, 201);
  }

  // PUT /api/posts/:id  수정(비번 확인)
  if (m && method === "PUT") {
    const id = +m[1];
    const b = await request.json();
    const post = await db.prepare("SELECT pw_hash, author_nickname FROM posts WHERE id = ?").bind(id).first();
    if (!post) return json({ error: "글을 찾을 수 없어요." }, 404);
    if (!(await checkPw(b.password, post, env))) return json({ error: "비밀번호가 일치하지 않아요." }, 403);
    const title = clean(b.title, 120), content = clean(b.content, 8000);
    if (!title || !content) return json({ error: "제목·내용을 입력해주세요." }, 400);
    const category = CATEGORIES.includes(b.category) ? b.category : null;
    await db.prepare(
      `UPDATE posts SET title=?, content=?, category=COALESCE(?,category),
        card_event_id=?, updated_at=datetime('now') WHERE id=?`
    ).bind(title, content, category, clean(b.card_event_id, 200) || null, id).run();
    return json({ ok: true });
  }

  // DELETE /api/posts/:id  삭제(비번 확인)
  if (m && method === "DELETE") {
    const id = +m[1];
    const b = await safeJson(request);
    const post = await db.prepare("SELECT pw_hash, author_nickname FROM posts WHERE id = ?").bind(id).first();
    if (!post) return json({ error: "글을 찾을 수 없어요." }, 404);
    if (!(await checkPw(b.password, post, env))) return json({ error: "비밀번호가 일치하지 않아요." }, 403);
    await db.prepare("DELETE FROM comments WHERE post_id = ?").bind(id).run();
    await db.prepare("DELETE FROM posts WHERE id = ?").bind(id).run();
    return json({ ok: true });
  }

  // POST /api/posts/:id/comments  댓글 작성
  m = pathname.match(/^\/api\/posts\/(\d+)\/comments$/);
  if (m && method === "POST") {
    const pid = +m[1];
    const b = await request.json();
    const nick = clean(b.nickname, 20), content = clean(b.content, 2000), pw = String(b.password || "");
    if (!nick || !content) return json({ error: "닉네임·내용을 입력해주세요." }, 400);
    if (!/^\d{4}$/.test(pw)) return json({ error: "비밀번호는 4자리 숫자예요." }, 400);
    const exists = await db.prepare("SELECT id FROM posts WHERE id = ?").bind(pid).first();
    if (!exists) return json({ error: "글을 찾을 수 없어요." }, 404);
    const pwHash = await sha256(pw + ":" + nick, env), ipHash = await ipHashOf(request, env);
    const res = await db.prepare(
      `INSERT INTO comments (post_id, author_nickname, author_ip_hash, pw_hash, content) VALUES (?, ?, ?, ?, ?)`
    ).bind(pid, nick, ipHash, pwHash, content).run();
    return json({ id: res.meta.last_row_id }, 201);
  }

  // DELETE /api/comments/:id  댓글 삭제(비번 확인)
  m = pathname.match(/^\/api\/comments\/(\d+)$/);
  if (m && method === "DELETE") {
    const id = +m[1];
    const b = await safeJson(request);
    const c = await db.prepare("SELECT pw_hash, author_nickname FROM comments WHERE id = ?").bind(id).first();
    if (!c) return json({ error: "댓글을 찾을 수 없어요." }, 404);
    if (!(await checkPw(b.password, c, env))) return json({ error: "비밀번호가 일치하지 않아요." }, 403);
    await db.prepare("DELETE FROM comments WHERE id = ?").bind(id).run();
    return json({ ok: true });
  }

  // POST /api/posts/:id/like  좋아요 토글
  m = pathname.match(/^\/api\/posts\/(\d+)\/like$/);
  if (m && method === "POST") return like(db, "post", +m[1], "posts", request, env);

  // POST /api/comments/:id/like  댓글 좋아요 토글
  m = pathname.match(/^\/api\/comments\/(\d+)\/like$/);
  if (m && method === "POST") return like(db, "comment", +m[1], "comments", request, env);

  // ── 진단 결과 통계 (유형별 참여 비중) ─────────────────────
  // 테이블은 최초 요청 시 자동 생성(별도 마이그레이션 불필요).
  // POST /api/diag  결과 기록  body:{kind, type}
  if (pathname === "/api/diag" && method === "POST") {
    const b = await request.json().catch(() => ({}));
    const kind = String(b.kind || "").trim().slice(0, 32);
    const type = String(b.type || "").trim().slice(0, 48);
    if (!kind || !type) return json({ error: "kind/type 필요" }, 400);
    await db.prepare("CREATE TABLE IF NOT EXISTS diag_stats (kind TEXT NOT NULL, type TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (kind, type))").run();
    await db.prepare("INSERT INTO diag_stats (kind, type, n) VALUES (?, ?, 1) ON CONFLICT(kind, type) DO UPDATE SET n = n + 1").bind(kind, type).run();
    return json({ ok: true });
  }
  // GET /api/diag/stats?kind=  유형별 집계
  if (pathname === "/api/diag/stats" && method === "GET") {
    const kind = String(url.searchParams.get("kind") || "").trim().slice(0, 32);
    if (!kind) return json({ error: "kind 필요" }, 400);
    await db.prepare("CREATE TABLE IF NOT EXISTS diag_stats (kind TEXT NOT NULL, type TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (kind, type))").run();
    const rows = (await db.prepare("SELECT type, n FROM diag_stats WHERE kind = ? ORDER BY n DESC, type ASC").bind(kind).all()).results;
    const total = rows.reduce((s, r) => s + (r.n || 0), 0);
    return json({ kind, total, stats: rows });
  }

  // 헬스체크
  if (pathname === "/" || pathname === "/api" || pathname === "/api/health")
    return json({ ok: true, service: "cardtyranno-community", categories: CATEGORIES });

  return json({ error: "Not found" }, 404);
}

// 좋아요 토글: 있으면 취소(-1), 없으면 추가(+1)
async function like(db, type, id, table, request, env) {
  const ipHash = await ipHashOf(request, env);
  const existing = await db.prepare(
    "SELECT id FROM likes WHERE target_type=? AND target_id=? AND ip_hash=?"
  ).bind(type, id, ipHash).first();
  if (existing) {
    await db.prepare("DELETE FROM likes WHERE id=?").bind(existing.id).run();
    await db.prepare(`UPDATE ${table} SET likes = MAX(0, likes - 1) WHERE id=?`).bind(id).run();
    const row = await db.prepare(`SELECT likes FROM ${table} WHERE id=?`).bind(id).first();
    return json({ liked: false, likes: row ? row.likes : 0 });
  } else {
    await db.prepare("INSERT INTO likes (target_type, target_id, ip_hash) VALUES (?,?,?)").bind(type, id, ipHash).run();
    await db.prepare(`UPDATE ${table} SET likes = likes + 1 WHERE id=?`).bind(id).run();
    const row = await db.prepare(`SELECT likes FROM ${table} WHERE id=?`).bind(id).first();
    return json({ liked: true, likes: row ? row.likes : 0 });
  }
}

// ---------- helpers ----------
async function checkPw(password, row, env) {
  if (!/^\d{4}$/.test(String(password || ""))) return false;
  const h = await sha256(String(password) + ":" + row.author_nickname, env);
  return h === row.pw_hash;
}
async function sha256(str, env) {
  const data = new TextEncoder().encode((env.SALT || "cardtyranno") + "|" + str);
  const buf = await crypto.subtle.digest("SHA-256", data);
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
async function ipHashOf(request, env) {
  const ip = request.headers.get("CF-Connecting-IP") || request.headers.get("x-forwarded-for") || "0.0.0.0";
  return (await sha256("ip:" + ip, env)).slice(0, 32);
}
function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 1000);
}
function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status: status || 200,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}
// ALLOW_ORIGIN 은 콤마구분 허용목록("*" 가능). 요청 Origin 이 목록에 있으면 그 값을 그대로 반환
// (ACAO 헤더는 단일 오리진만 echo 가능 → apex/www 동시 허용하려면 요청별 매칭 필요).
function resolveOrigin(request, env) {
  const conf = (env.ALLOW_ORIGIN || "*").trim();
  if (conf === "*") return "*";
  const allow = conf.split(",").map((s) => s.trim()).filter(Boolean);
  const reqOrigin = request.headers.get("Origin");
  if (reqOrigin && allow.includes(reqOrigin)) return reqOrigin;
  return allow[0] || "*";
}
function cors(res, origin) {
  const h = new Headers(res.headers);
  h.set("Access-Control-Allow-Origin", origin || "*");
  h.set("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
  h.set("Access-Control-Allow-Headers", "content-type");
  h.set("Access-Control-Max-Age", "86400");
  h.set("Vary", "Origin");
  return new Response(res.body, { status: res.status, headers: h });
}
async function safeJson(request) {
  try { return await request.json(); } catch { return {}; }
}
