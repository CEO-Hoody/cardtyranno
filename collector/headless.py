# -*- coding: utf-8 -*-
"""Playwright 헤드리스 폴백 — API/SSR로 안 잡히는 플랫폼(네이버페이·아정당) 렌더링 수집.
GitHub Actions에서 chromium으로 페이지를 띄워 렌더 후 HTML 반환.
idle 대기(networkidle)는 광고 스크립트로 영원히 안 끝나므로 domcontentloaded + 셀렉터/timeout 사용.
"""
def render_html(url, wait_selector=None, timeout=25000):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print("  ! playwright 미설치:", e); return None
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
            pg = b.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                            locale="ko-KR", extra_http_headers={"Accept-Language": "ko-KR,ko;q=0.9"})
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=timeout)
                if wait_selector:
                    try: pg.wait_for_selector(wait_selector, timeout=8000)
                    except Exception: pass
                pg.wait_for_timeout(2500)        # 렌더/하이드레이션 여유
                return pg.content()
            finally:
                b.close()
    except Exception as e:
        print("  ! headless err:", url, e); return None
