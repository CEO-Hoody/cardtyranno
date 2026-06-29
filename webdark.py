# -*- coding: utf-8 -*-
"""카드티라노 프론트엔드 v2 — 다크테마(무신사 감성·카드고릴라 구조) + SEO/AEO 최적화.
데이터는 site/*.json(DB export) 런타임 fetch. AEO: JSON-LD, llms.txt, FAQ, AI 크롤러 허용.
"""
import os, json, datetime
OUT=os.path.dirname(os.path.abspath(__file__)); SITE=os.path.join(OUT,"site")
BASE="https://cardtyranno.com"; BRAND="카드티라노"; BRAND_EN="CardTyranno"
# Cloudflare Web Analytics 토큰(대시보드 Web Analytics에서 발급). 값 채우면 전 페이지에 beacon 자동 삽입.
CF_BEACON_TOKEN=""
# 검색엔진 사이트 소유확인 코드(등록 후 발급값 입력하면 전 페이지 <head>에 자동 삽입)
#  네이버 서치어드바이저(searchadvisor.naver.com) → 사이트 등록 → HTML 태그 방식의 content 값만 붙여넣기
NAVER_SITE_VERIFICATION=""
#  구글 서치콘솔(search.google.com/search-console) → HTML 태그 방식의 content 값만 붙여넣기
GOOGLE_SITE_VERIFICATION=""
DESC_SITE="여러 카드 중개 플랫폼(토스 카드라운지·카드고릴라·아정당·뱅크샐러드)의 카드 발급 혜택과 결제 할인 이벤트를 한곳에서 비교·분석하는 카드 비교 플랫폼."

CSS = r"""
:root{--bg:#ffffff;--surface:#ffffff;--surface2:#f7f7f5;--line:#e6e6e6;--text:#000000;--sub:#54545f;--dim:#8a8780;--accent:#000000;--accent-d:#000000;--blue:#2f6bff;--plate:#eceef2;--radius:18px;
/* Canvas Design System 토큰(핸드오프 §2) */
--ink:#000;--white:#fff;--surface-soft:#f7f7f5;--hairline:#e6e6e6;--hairline-soft:#f1f1f1;--block-lime:#dceeb1;--block-lilac:#c5b0f4;--block-cream:#f4ecd6;--block-pink:#efd4d4;--block-mint:#c8e6cd;--block-coral:#f3c9b6;--block-navy:#1f1d3d;--accent-magenta:#ff3d8b;--success:#1ea64a}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--text);font-family:'Pretendard','Pretendard Variable',-apple-system,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;line-height:1.45;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none} img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.muted{color:var(--sub)} .accent{color:var(--accent)} .empty{color:var(--sub);text-align:center;padding:46px 20px;font-size:14px}
.util{border-bottom:1px solid var(--line);font-size:12px;color:var(--sub)}
.util .wrap{display:flex;justify-content:flex-end;gap:18px;height:34px;align-items:center}
.util a:hover{color:var(--text)}
.hd{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hd .row{display:flex;align-items:center;gap:24px;height:64px}
.logo{font-size:21px;font-weight:900;letter-spacing:-1px;display:flex;align-items:center;gap:7px}
.logo .rx{width:23px;height:23px;color:var(--text);display:block;flex:0 0 auto}.logo b{color:var(--text);font-weight:400}
.gnb{display:flex;gap:22px;font-size:15px;font-weight:700}
.gnb a{color:#55555e;padding:6px 0;position:relative}.gnb a:hover,.gnb a.on{color:var(--accent)}
.gnb a.on::after{content:"";position:absolute;left:0;right:0;bottom:-21px;height:3px;background:var(--accent)}
.hd .right{margin-left:auto;display:flex;align-items:center;gap:14px}
.icbtn{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#55555e;border:1px solid var(--line);cursor:pointer}
.ic{width:20px;height:20px;display:block;flex:0 0 auto}
.cat .ico .ic{width:22px;height:22px}.curc .em .ic{width:26px;height:26px}.favbtn .ic{width:20px;height:20px}
.dday{display:inline-block;font-size:10.5px;font-weight:800;padding:1px 7px;border-radius:999px;background:var(--surface2);color:var(--sub);margin-left:6px;vertical-align:middle}.dday.soon{background:#ff3d8b;color:#fff}
/* ===== INTERACTION.md 전역 모션 레이어 ===== */
:root{--dur-fast:140ms;--dur-base:240ms;--dur-slow:320ms;--ease:cubic-bezier(.2,0,0,1)}
a,button{transition:opacity var(--dur-fast) var(--ease),transform var(--dur-fast) var(--ease),background-color var(--dur-fast) var(--ease),color var(--dur-fast) var(--ease),border-color var(--dur-fast) var(--ease)}
.nhe-cta:hover,.cf-go:hover,.adb:hover,.evh-cta:hover,.obb1:hover,.obb2:hover{opacity:.92}
.nhe-cta:active,.cf-go:active,.adb:active,.obb1:active,.obb2:active,.cf-sortbtn:active,.nmore:active{transform:scale(.97)}
.icbtn:active,.cf-fav:active,.favbtn:active{transform:scale(.94)}
.cf-card,.nrow,.npc,.ctile,.gcard,.ev{transition:border-color var(--dur-fast) var(--ease),background-color var(--dur-fast) var(--ease),transform var(--dur-fast) var(--ease)}
.nrow:hover,.ev:hover{background:var(--surface-soft)}
@keyframes heartpop{0%{transform:scale(1)}45%{transform:scale(1.22)}100%{transform:scale(1)}}
.favbtn.pop svg,.cf-fav.pop svg{animation:heartpop 180ms var(--ease)}
.subnav2 button,.cf-sort button,.pchips button{transition:background-color var(--dur-base) var(--ease),color var(--dur-base) var(--ease)}
a:focus-visible,button:focus-visible,input:focus-visible,[tabindex]:focus-visible{outline:2px solid #000;outline-offset:2px;border-radius:4px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}.nlive-tk,.mlive .lvt span{animation:none!important}}
.icbtn:hover{color:var(--accent);border-color:#d6d6dd}
.menu{display:none}
.searchbar{border-bottom:1px solid var(--line)}
.searchbar .wrap{padding:15px 20px}
.sb{display:flex;align-items:center;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:13px 17px}
.sb:focus-within{border-color:#d6d6dd}
.sb input{flex:1;background:transparent;border:0;color:var(--text);font-size:15px;outline:none}
.sb .go{background:var(--accent);color:#fff;font-weight:800;font-size:13px;border:0;border-radius:8px;padding:9px 16px;cursor:pointer}
.sfilters{display:flex;gap:8px;margin-top:11px;flex-wrap:wrap}
.chip{font-size:12.5px;font-weight:700;color:#55555e;background:var(--surface2);border:1px solid var(--line);border-radius:999px;padding:7px 13px;cursor:pointer}
.chip:hover,.chip.on{border-color:var(--accent);color:var(--accent);background:#fff4f0}
.catstrip{border-bottom:1px solid var(--line);overflow-x:auto}.catstrip::-webkit-scrollbar{display:none}
.catstrip .wrap{display:flex;gap:6px;padding:13px 20px}
.cat{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;gap:7px;width:72px;padding:7px 3px;border-radius:12px;font-size:12px;font-weight:700;color:#55555e}
.cat:hover{background:var(--surface)}
.cat .ico{width:44px;height:44px;border-radius:13px;background:var(--surface2);display:flex;align-items:center;justify-content:center;font-size:21px}
.ad{position:relative;border:1px dashed #d6d6dd;border-radius:var(--radius);background:repeating-linear-gradient(135deg,#ffffff,#ffffff 12px,#f7f7f9 12px,#f7f7f9 24px);display:flex;align-items:center;justify-content:center;color:var(--dim);font-size:13px;font-weight:700}
.ad::before{content:"AD";position:absolute;top:10px;left:12px;font-size:10px;font-weight:900;color:#fff;background:#33333b;padding:2px 7px;border-radius:5px;letter-spacing:1px}
.ad.hero{height:280px;margin:22px 0}.ad.inline{height:104px;margin:14px 0}
.adbanner{position:relative;display:block;border-radius:var(--radius);overflow:hidden;margin:22px 0;border:1px solid var(--line)}
.adbanner img{width:100%;height:auto;display:block}
.adbanner .adtag{position:absolute;top:10px;left:12px;font-size:10px;font-weight:900;color:#fff;background:rgba(0,0,0,.45);padding:2px 7px;border-radius:5px;letter-spacing:1px}
.cardad{position:relative;display:block;margin:18px 0;border:1px solid var(--line);border-radius:var(--radius);background:radial-gradient(120% 140% at 0% 0%,#f7f8fa 0%,#f4f5f7 60%,#f4f5f7 100%);overflow:hidden}
.cardad:hover{border-color:#d6d6dd}
.cardad .adtag{position:absolute;top:10px;right:12px;font-size:10px;font-weight:900;color:#fff;background:rgba(0,0,0,.14);padding:2px 7px;border-radius:5px;letter-spacing:1px;z-index:2}
.cadbody{display:flex;align-items:center;gap:20px;padding:20px 22px}
.cadplate{width:178px;height:112px;flex:0 0 auto;border-radius:13px;overflow:hidden;background:#eef0f3;box-shadow:0 12px 28px rgba(0,0,0,.16);transform:rotate(-3deg);transition:.2s}
.cardad:hover .cadplate{transform:rotate(-3deg) scale(1.03)}
.cadplate img{width:100%;height:100%;object-fit:cover}
.cadinfo{flex:1;min-width:0}
.cadev{font-size:11.5px;font-weight:900;color:var(--accent);letter-spacing:.3px}
.cadname{font-size:20px;font-weight:900;margin-top:6px;letter-spacing:-.5px;line-height:1.28}
.cadiss{font-size:12px;color:var(--sub);margin-top:3px}
.cadamt{font-size:14.5px;font-weight:800;margin-top:9px;color:var(--text)}
.cadamt b{color:var(--accent);font-size:21px}
.cadplats{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.cadplats .pb2{font-size:10.5px;font-weight:800;color:#fff;padding:3px 9px;border-radius:6px;white-space:nowrap}
.cadcta{font-size:12px;color:var(--sub);margin-top:11px;font-weight:700}
.cadcta b{color:var(--text)}
@media(max-width:560px){.cadbody{gap:14px;padding:16px}.cadplate{width:122px;height:78px}.cadname{font-size:16px}.cadamt b{font-size:18px}}
.ghero{margin:-2px -2px 20px;border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.ghero img{width:100%;height:auto;display:block}
.asum{font-size:14.5px;color:var(--sub);font-weight:600;margin:2px 0 16px;padding-bottom:14px;border-bottom:1px solid var(--line)}
.herowrap{display:grid;grid-template-columns:1fr;gap:12px;margin:20px 0 6px}
.vhero{position:relative;min-height:210px;border-radius:18px;padding:20px 18px;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;color:#fff}
.vhero::after{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 80% 0%,rgba(255,255,255,.18),transparent 60%)}
.vhero>*{position:relative;z-index:1}
.vh1{background:#c5b0f4}.vh1,.vh1 .vh-iss,.vh1 .vh-name,.vh1 .vh-amt,.vh1 .vh-go{color:#15131f}.vh1 .vh-tag{background:rgba(255,255,255,.55);color:#15131f}.vh1::after{background:radial-gradient(120% 90% at 80% 0%,rgba(255,255,255,.4),transparent 60%)}
.vh2{background:linear-gradient(160deg,#1f8f5b 0%,#0f7a45 100%)}
.vhero .vh-tag{font-size:12px;font-weight:800;opacity:.92;margin-bottom:auto;letter-spacing:-.01em;background:rgba(0,0,0,.18);align-self:flex-start;padding:5px 10px;border-radius:999px}
.vhero .vh-iss{font-size:12px;opacity:.9;font-weight:700;margin-top:14px}
.vhero .vh-name{font-size:18px;font-weight:900;line-height:1.25;letter-spacing:-.02em;margin-top:3px}
.vhero .vh-amt{font-size:24px;font-weight:900;letter-spacing:-.02em;margin-top:8px}
.vhero .vh-amt small{font-size:13px;font-weight:700;opacity:.85;margin-left:3px}
.vhero .vh-go{font-size:12.5px;font-weight:800;margin-top:12px;opacity:.95}
@media(max-width:560px){.herowrap{grid-template-columns:1fr;gap:9px}.vhero{min-height:178px;padding:15px 13px}.vhero .vh-name{font-size:15px}.vhero .vh-amt{font-size:20px}}
section{padding:30px 0}
.sec-h{display:flex;align-items:baseline;gap:12px;margin-bottom:16px}
.sec-h h2{font-size:22px;font-weight:900;letter-spacing:-.6px}
.sec-h .more{margin-left:auto;font-size:13px;color:var(--sub);font-weight:700}.sec-h .more:hover{color:var(--accent)}
.tabs{display:flex;gap:18px;margin-bottom:16px;border-bottom:1px solid var(--line);overflow-x:auto}.tabs::-webkit-scrollbar{display:none}
.tabs span,.tabs .tab{flex:0 0 auto;font-size:14.5px;font-weight:800;color:var(--sub);padding:0 0 12px;cursor:pointer;position:relative;white-space:nowrap}
.tabs .tab.active,.tabs span.on{color:var(--text)}
.tabs .tab.active::after,.tabs span.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--accent)}
.tabs .cnt{font-size:11px;color:var(--accent);margin-left:3px}
.seg{display:inline-flex;background:var(--surface2);border:1px solid var(--line);border-radius:10px;padding:3px}
.seg button{border:0;background:transparent;font-size:13px;font-weight:700;color:var(--sub);padding:7px 13px;border-radius:8px;cursor:pointer}
.seg button.on{background:var(--accent);color:#fff}
.filterbar{display:flex;align-items:center;gap:10px;padding:8px 0;flex-wrap:wrap}
.filterbar select{font-size:13px;padding:8px 11px;border:1px solid var(--line);border-radius:9px;background:var(--surface);color:var(--text);min-width:150px}
.rank{display:grid;grid-template-columns:1fr 1fr;gap:0 30px}
.rk{display:flex;align-items:center;gap:15px;padding:14px 6px;border-bottom:1px solid var(--line)}
.rk .no{width:24px;font-size:18px;font-weight:900;text-align:center;font-style:italic}.rk .no.top{color:var(--accent)}
.rk .pl{width:80px;height:50px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;overflow:hidden;border-radius:6px}
.rk .pl img{width:100%;height:100%;object-fit:cover;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.14)} .rk .pl .ph{font-size:24px}
.rk .ri{flex:1;min-width:0}.rk .rn{font-size:14.5px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rk .rs{font-size:12px;color:var(--sub);margin-top:3px}.rk .rw{font-size:14px;font-weight:900;color:var(--accent);white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.gcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:17px;transition:.15s}
.gcard:hover{border-color:#d6d6dd;transform:translateY(-3px)}
.gcard .badge{display:inline-block;font-size:10.5px;font-weight:800;color:#fff;background:var(--accent);padding:3px 8px;border-radius:6px}
.gcard .badge.gray{background:#33333b;color:#55555e}
.gcard .ct{font-size:14.5px;font-weight:800;margin-top:10px;line-height:1.35}
.gcard .cw{font-size:18px;font-weight:900;margin-top:7px;letter-spacing:-.5px}
.gcard .cs{font-size:12px;color:var(--sub);margin-top:6px;line-height:1.5;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.cur{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.curc{position:relative;height:170px;border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;padding:20px;background:linear-gradient(180deg,#f4f5f7,#0e0e10);border:1px solid var(--line)}
.curc .th{font-size:11px;font-weight:800;color:var(--accent)}.curc .ti{font-size:18px;font-weight:900;margin-top:6px}.curc .ds{font-size:12px;color:var(--sub);margin-top:6px}.curc .em{position:absolute;top:14px;right:16px;font-size:38px;opacity:.5}
.posts{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.post{border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--surface)}
.post .thumb{height:92px;background:linear-gradient(135deg,#eef0f3,#ffffff);display:flex;align-items:center;justify-content:center;font-size:32px}
.post .pb{padding:13px}.post .pc{font-size:11px;font-weight:800;color:var(--accent)}.post .pt{font-size:14px;font-weight:800;margin-top:5px;line-height:1.35}
.faq{border-top:1px solid var(--line)}
.faq .q{border-bottom:1px solid var(--line);padding:18px 2px}
.faq .q h3{font-size:15.5px;font-weight:800}.faq .q p{font-size:14px;color:var(--sub);margin-top:9px;line-height:1.7}
.list{display:grid;grid-template-columns:1fr}
.item{display:flex;align-items:center;gap:13px;padding:15px 4px;border-bottom:1px solid var(--line)}
.item .th{flex:0 0 auto;width:48px;height:48px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;overflow:hidden}
.item .th img{width:74%;height:74%;object-fit:contain;border-radius:5px}
.thic{width:50%;height:50%;color:#000}.item .th .thic{width:46%;height:46%}
.item .body{flex:1;min-width:0}.item .l1{display:flex;align-items:center;gap:6px;margin-bottom:3px}
.item .store{font-size:13px;color:#6a6a72;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:60%}
.item .tag{font-size:10px;font-weight:800;background:#fbf0df;color:#e8a33c;padding:2px 7px;border-radius:6px}.item .tag.off{background:#ececf0;color:#9a9aa2}
.item .l2{font-size:16px;font-weight:800;letter-spacing:-.3px}.item .l2 .hl{color:var(--accent)}
.item .l3{font-size:12.5px;color:var(--sub);margin-top:4px;line-height:1.5;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.item .chev{color:#46464d;font-size:20px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:18px 14px;padding:16px 0}
.ctile{position:relative;border-radius:16px;padding:6px 8px 12px;background:var(--surface);border:1px solid var(--line);display:flex;flex-direction:column;transition:.15s}
.favbtn{position:absolute;top:9px;right:11px;cursor:pointer;z-index:3;line-height:0;color:var(--dim)}.favbtn.on{color:var(--accent)}.favbtn .ic{width:21px;height:21px}
.cev{font-size:10.5px;font-weight:800;color:var(--accent);text-align:center;margin-top:5px}
.ctile:hover{transform:translateY(-3px);border-color:#d6d6dd}
.ctile .plate{width:100%;height:104px;display:flex;align-items:center;justify-content:center;margin:6px 0 12px;font-size:32px;overflow:hidden;border-radius:9px;background:#eef0f3}
.ctile .plate img{width:100%;height:100%;object-fit:cover;border-radius:9px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.45))}
.ctile .cn{font-size:13.5px;font-weight:800;text-align:center;line-height:1.32}
.ctile .cfee{font-size:11px;color:var(--dim);font-weight:700;margin-top:4px;text-align:center}
.ctile .cd{font-size:11.5px;color:var(--sub);margin-top:6px;text-align:center;flex:1;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.ctile .apply{margin-top:11px;font-size:11.5px;font-weight:800;color:#fff;background:var(--accent);border-radius:8px;text-align:center;padding:8px}
.tablewrap{overflow-x:auto;margin:14px 0;border:1px solid var(--line);border-radius:14px}
table.cmp{border-collapse:collapse;width:100%;min-width:620px;font-size:13.5px}
table.cmp th,table.cmp td{padding:13px 12px;text-align:center;border-bottom:1px solid var(--line);white-space:nowrap}
table.cmp thead th{background:var(--surface2);font-weight:800;font-size:13px}
table.cmp .iss{position:sticky;left:0;background:var(--surface);text-align:left;font-weight:800;z-index:1}
table.cmp thead .iss{background:var(--surface2)}
table.cmp td.none{color:var(--dim)} table.cmp td.mx{background:#fbf0df;color:var(--accent);font-weight:900}
table.cmp td .st{font-size:10px;display:block} .doth{display:inline-flex;align-items:center;gap:5px;justify-content:center}.dot{width:8px;height:8px;border-radius:50%}
.subnav{display:flex;gap:8px;padding:14px 0 4px}
.subnav button{border:1px solid var(--line);background:var(--surface);font-size:14px;font-weight:800;color:var(--sub);padding:9px 16px;border-radius:999px;cursor:pointer}
.subnav button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.ev{display:flex;align-items:center;gap:12px;padding:15px 4px;border-bottom:1px solid var(--line)}
.ev .pf{width:64px;text-align:center;font-size:10.5px;font-weight:800;color:#fff;padding:5px 0;border-radius:8px;flex:0 0 auto}
.ev .ev-th{width:78px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:9px;overflow:hidden;background:var(--surface-soft);border:1px solid var(--hairline-soft)}
.ev .ev-th img{width:100%;height:100%;object-fit:cover;display:block}
.ev .ei i{vertical-align:middle}
.ev .eb{flex:1;min-width:0}.ev .ec{font-size:14px;font-weight:800}.ev .ei{font-size:11.5px;color:var(--sub);margin-top:3px}
.ev .ebn{font-size:14.5px;font-weight:900;color:var(--accent);text-align:right;max-width:42%}.ev .chev{color:#46464d;font-size:19px}.ev .ev-go{flex:0 0 auto;font-size:12.5px;font-weight:700;color:#000;white-space:nowrap}
.hero-detail{padding:26px 16px 20px;text-align:center;border-bottom:1px solid var(--line)}
.hero-detail .th{width:70px;height:70px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;margin:0 auto 12px;overflow:hidden}
.hero-detail .th img{width:74%;height:74%;object-fit:contain}
.hero-detail .store{font-size:14px;color:#6a6a72;font-weight:700;margin-bottom:8px}
.hero-detail .disc{font-size:28px;font-weight:900;letter-spacing:-.6px}.hero-detail .disc .hl{color:var(--accent)}
.hero-detail .type{font-size:14px;color:var(--sub);margin-top:6px}
.rows{max-width:600px;margin:0 auto;padding:6px 16px}
.r{display:flex;padding:14px 0;border-bottom:1px solid var(--line);font-size:14.5px}.r .k{width:96px;color:var(--sub);font-weight:700}.r .v{flex:1;font-weight:700}
.cta{max-width:600px;margin:0 auto;padding:18px 16px 36px}
.cta a{display:block;text-align:center;background:var(--accent);color:#fff;font-size:16px;font-weight:900;padding:16px;border-radius:14px}
.bk{font-size:24px;color:#55555e} .adt{max-width:720px;margin:0 auto;padding:6px 2px 50px}
.adt .acat{font-size:12px;font-weight:800;color:var(--accent);padding-top:16px}.adt .ah{font-size:24px;font-weight:900;letter-spacing:-.5px;line-height:1.35;padding:7px 0 6px}
.adt p{font-size:15.5px;line-height:1.8;color:#44444c;margin:15px 0}.adt .bk2{display:inline-block;margin-top:24px;font-weight:800;color:var(--blue)}
.adt .hl{font-weight:900;font-size:1.16em;color:var(--accent-magenta,#ff3d8b);letter-spacing:-.3px;white-space:nowrap}
.adt .kw{font-weight:800;color:#000000;background:linear-gradient(transparent 62%,rgba(197,176,244,.55) 0)}
.adt .tip{display:block;position:relative;background:var(--block-cream,#f7f3e9);border-left:3px solid var(--accent-magenta,#ff3d8b);border-radius:10px;padding:13px 16px 13px 44px;margin:18px 0;font-size:14.5px;line-height:1.65;color:#3a3a42}
.adt .tip::before{content:"💡";position:absolute;left:15px;top:12px;font-size:16px}
.adt .tip.warn{border-left-color:#e8843c}.adt .tip.warn::before{content:"⚠️"}
footer{border-top:1px solid var(--line);margin-top:40px;background:#f5f5f7}
.foot{display:flex;gap:50px;padding:42px 0 10px;flex-wrap:wrap}
.foot .col h4{font-size:12px;color:var(--dim);font-weight:800;margin-bottom:13px}.foot .col a{display:block;font-size:13.5px;color:#55555e;margin-bottom:9px}.foot .col a:hover{color:var(--accent)}
.foot .brand{flex:1;min-width:220px}.foot .brand .lg{font-size:20px;font-weight:900;letter-spacing:-1px}.foot .brand .lg b{color:var(--text);font-weight:400}.foot .brand p{font-size:12px;color:var(--sub);margin-top:12px;line-height:1.7;max-width:400px}
.legal{border-top:1px solid var(--line);padding:18px 0 40px;font-size:11.5px;color:var(--dim);line-height:1.8}.legal .biz{margin-top:8px}
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.16);opacity:0;visibility:hidden;transition:.2s;z-index:60}.scrim.on{opacity:1;visibility:visible}
.drawer{position:fixed;top:0;left:0;bottom:0;width:270px;max-width:82%;background:#ffffff;border-right:1px solid var(--line);transform:translateX(-100%);transition:.24s;z-index:61;padding:20px}.drawer.on{transform:translateX(0)}
.drawer a{display:block;padding:13px 6px;font-size:16px;font-weight:800;border-bottom:1px solid var(--line)}
/* 인터랙션: 카드 플레이트·광고배너 호버 */
.ctile .plate img{transition:transform .18s ease}.ctile:hover .plate img{transform:scale(1.07)}
.adbanner img{transition:transform .25s ease}.adbanner{transition:box-shadow .18s,transform .18s}.adbanner:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgba(0,0,0,.12)}.adbanner:hover img{transform:scale(1.02)}
.cardad{transition:box-shadow .18s,transform .18s}.cardad:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,0,0,.10)}
.rk .pl img{transition:transform .16s ease}.rk:hover .pl img{transform:scale(1.06)}
.ctile .plate{overflow:hidden}
/* 온보딩/랜딩 히어로(인덱스 첫 화면 정체성) */
.obhero{background:#c5b0f4;border-radius:20px;padding:30px 26px;margin:14px 0 8px;position:relative;overflow:hidden}
.obhero::after{content:"";position:absolute;right:-50px;top:-50px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.35),transparent 70%)}
.obhero .obeb{font-size:12px;font-weight:900;letter-spacing:.4px;color:#5b3fb0;position:relative;z-index:1}
.obhero .obh{font-size:26px;font-weight:900;letter-spacing:-.03em;line-height:1.22;margin-top:9px;color:#000000;position:relative;z-index:1}
.obhero .obs{font-size:14px;color:#3a2d5e;margin-top:10px;line-height:1.6;max-width:560px;position:relative;z-index:1}
.obhero .obcta{display:flex;gap:10px;margin-top:18px;flex-wrap:wrap;position:relative;z-index:1}
.obhero .obb1{background:#000000;color:#fff;font-weight:800;font-size:14px;padding:12px 18px;border-radius:999px;transition:transform .15s}
.obhero .obb2{background:rgba(255,255,255,.72);color:#000000;font-weight:800;font-size:14px;padding:12px 18px;border-radius:999px;transition:transform .15s}
.obhero .obb1:hover,.obhero .obb2:hover{transform:translateY(-1px)}
@media(max-width:560px){.obhero{padding:22px 18px}.obhero .obh{font-size:21px}.obhero .obcta a{flex:1;text-align:center}}
/* ===== 홈 PC 시안(핸드오프 §4.1) ===== */
.nhero{background:var(--block-lilac);border-radius:24px;padding:56px 48px;margin:28px 0 0;position:relative;overflow:hidden;min-height:300px}
.nhe-eb{font-size:12px;letter-spacing:.6px;text-transform:uppercase;color:rgba(0,0,0,.6);font-weight:700}
.nhe-eb.dim{color:rgba(0,0,0,.55)}
.nhe-h{font-weight:400;font-size:64px;line-height:.99;letter-spacing:-2px;margin:16px 0 0;max-width:640px;color:#000}
.nhe-p{font-weight:400;font-size:19px;line-height:1.5;margin:20px 0 0;max-width:480px;color:rgba(0,0,0,.72)}
.nhe-cta{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;background:#000;color:#fff;font-weight:600;font-size:16px;margin-top:30px;transition:transform .12s}
.nhe-cta:active{transform:scale(.97)}
.nhe-plate{position:absolute;right:40px;top:50%;transform:translateY(-50%) rotate(7deg);width:300px}
.nhe-plate .hpcard{border-radius:14px;overflow:hidden;box-shadow:0 18px 44px rgba(0,0,0,.22)}
.nhe-plate img,.npc-plate img,.nrow .mp img{width:100%;display:block}
@media(max-width:820px){.nhe-plate{display:none}}
@media(max-width:560px){.nhero{padding:32px 22px;min-height:0}.nhe-h{font-size:33px;letter-spacing:-1px}.nhe-p{font-size:15px}}
.nlive{background:#000;color:#fff;margin-top:28px;overflow:hidden;white-space:nowrap;display:flex;align-items:center}
.nlive-tag{flex:0 0 auto;display:inline-flex;align-items:center;gap:8px;background:var(--accent-magenta);color:#fff;padding:14px 22px;font-size:13px;letter-spacing:.5px;text-transform:uppercase;font-weight:700}
.nlive-tag i{width:8px;height:8px;border-radius:50%;background:#fff;display:inline-block;animation:lvpulse 1.2s infinite}
.nlive-vp{overflow:hidden;flex:1}
.nlive-tk{display:inline-block;padding-left:100%;animation:lvmarq 30s linear infinite;font-size:13px;letter-spacing:.4px;text-transform:uppercase;font-weight:600}
.npod{background:var(--block-lime);border-radius:24px;padding:44px 40px;margin-top:28px}
.npod-h{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:28px;gap:16px}
.npod-t{font-weight:400;font-size:34px;letter-spacing:-.9px;margin:6px 0 0}
.npod-s{font-weight:400;font-size:15px;color:rgba(0,0,0,.62);margin:8px 0 0}
.nmore{font-weight:500;font-size:14px;white-space:nowrap;color:#000}
.npod-g{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:start}
.npc{display:flex;flex-direction:column;gap:14px;text-decoration:none;color:#000}
.npc-rk{display:flex;align-items:center;gap:8px}
.npc-rk b{width:30px;height:30px;border-radius:50px;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.npc-rk span{font-size:11px;opacity:.6;text-transform:uppercase}
.npc-plate{width:100%;aspect-ratio:1.586/1;border-radius:14px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.16);background:#eceef2}
.npc-plate img{width:100%;height:100%;object-fit:cover;display:block}
.npc-nm{font-weight:700;font-size:17px}
.npc-bn{font-weight:400;font-size:14px;color:rgba(0,0,0,.62);margin-top:3px}
.npc-ev{background:#fff;border-radius:14px;padding:14px 16px;border:1px solid rgba(0,0,0,.06)}
.npc-ev .lab{font-size:10px;opacity:.5;margin-bottom:8px;text-transform:uppercase;font-weight:700;letter-spacing:.4px}
.npc-ev .row{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-top:1px solid var(--hairline-soft)}
.npc-ev .row .p{font-weight:500;font-size:13.5px;display:inline-flex;align-items:center;gap:6px}
.npc-ev .row .p i{width:7px;height:7px;border-radius:50%;display:inline-block;flex:0 0 auto}
.npc-ev .row .v{font-weight:700;font-size:14px}
@media(max-width:820px){.npod-g{grid-template-columns:1fr 1fr}.npc{transform:none!important}.npod{padding:28px 20px}}
@media(max-width:640px){.npod{background:none;padding:6px 0 0}.npod-h{padding:0 4px}.npod-g{display:flex;flex-direction:row;flex-wrap:nowrap;overflow-x:auto;scroll-snap-type:x mandatory;gap:13px;-webkit-overflow-scrolling:touch;padding:0 4px 6px;scroll-padding-left:4px}.npod-g::-webkit-scrollbar{display:none}.npc{flex:0 0 62%;scroll-snap-align:start;transform:none!important}.npc-plate{max-width:none}.nrow{grid-template-columns:30px 60px 1fr auto}}
.nspon-sec{margin-top:80px}.sponlbl{margin-bottom:16px}
.nspon{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:130px;gap:16px}
.nspt{border-radius:22px;padding:24px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden}
.nspt .adm{font-size:11px;opacity:.62;text-transform:uppercase;letter-spacing:.4px}
.nspt .adh{font-weight:700;letter-spacing:-.3px;line-height:1.12;margin-top:8px}
.nspt .adb{align-self:flex-start;display:inline-flex;align-items:center;gap:7px;padding:11px 20px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:14px;text-decoration:none}
@media(max-width:760px){.nspon{grid-template-columns:repeat(2,1fr);grid-auto-rows:auto}.nspt{grid-column:span 1!important;grid-row:auto!important;min-height:128px}.nspt[style*="span 3"]{grid-column:span 2!important}.nspon .adh{font-size:18px!important}.nspt .adb{margin-top:12px}}
.nrank-sec{margin-top:80px}
.nrank-h{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:8px}
.nrank-t{font-weight:400;font-size:38px;letter-spacing:-1px;margin:6px 0 0}
.nrow{display:grid;grid-template-columns:50px 96px 1fr auto;gap:24px;align-items:center;padding:18px 4px;border-top:1px solid var(--hairline);text-decoration:none;color:#000}
.nrow .no{font-weight:700;font-size:30px;letter-spacing:-1px}
.nrow .mp{width:96px;border-radius:8px;overflow:hidden;border:1px solid rgba(0,0,0,.05)}
.nrow .nm{font-weight:700;font-size:19px;letter-spacing:-.3px}
.nrow .mt{font-size:12px;opacity:.55;margin-top:5px}
.nrow .amt{font-weight:700;font-size:19px;text-align:right}
.nrow .pt{font-size:11px;opacity:.5;margin-top:5px;text-align:right}
@media(max-width:560px){.nrow{grid-template-columns:30px 60px 1fr auto;gap:12px}.nrow .no{font-size:20px}.nrow .mp{width:60px}.nrow .nm{font-size:15px}.nrank-t{font-size:25px}.npod-t{font-size:26px}}
/* 티라노 브랜드 플레이트 배너(특정 카드 아님·서비스 대표 장식) */
.tybnr{display:flex;align-items:center;gap:20px;background:#c5b0f4;border-radius:20px;padding:24px 26px;margin:18px 0 22px;overflow:hidden;position:relative;color:#000000;text-decoration:none;transition:box-shadow .18s,transform .18s}
.tybnr:hover{transform:translateY(-2px);box-shadow:0 16px 36px rgba(123,90,210,.28)}
.tybnr .tyb-txt{flex:1;min-width:0;position:relative;z-index:1}
.tybnr .tyb-eb{font-size:11.5px;font-weight:900;letter-spacing:.6px;color:#5b3fb0;text-transform:uppercase}
.tybnr .tyb-h{font-size:21px;font-weight:900;letter-spacing:-.03em;line-height:1.25;margin-top:8px}
.tybnr .tyb-sub{font-size:13px;color:#3a2d5e;margin-top:7px;line-height:1.55}
.tybnr .tyb-plate{position:relative;width:172px;aspect-ratio:1.586/1;border-radius:13px;background:linear-gradient(135deg,#ffffff 0%,#efe7ff 100%);box-shadow:0 16px 34px rgba(70,40,120,.30);transform:rotate(-6deg);flex:0 0 auto;overflow:hidden}
.tybnr .tyb-plate .tyb-mk{position:absolute;top:13px;left:15px;font-size:12px;font-weight:900;letter-spacing:-.3px;color:#000000}.tybnr .tyb-plate .tyb-mk b{color:#ef5226}
.tybnr .tyb-plate .tyb-dino{position:absolute;right:-7%;bottom:-12%;width:62%;height:62%;color:#ef5226;opacity:.92}
.tybnr .tyb-plate .tyb-dino.bg{right:auto;left:-14%;bottom:auto;top:36%;width:44%;height:44%;color:#c9b6f0;opacity:.5}
.tybnr::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.35),transparent 70%)}
@media(max-width:560px){.tybnr{padding:18px;gap:14px}.tybnr .tyb-h{font-size:17px}.tybnr .tyb-plate{width:120px}}
@media(max-width:900px){.grid,.posts{grid-template-columns:1fr 1fr}.cur{grid-template-columns:1fr}.rank{grid-template-columns:1fr}.gnb,.util{display:none}.menu{display:flex}.wrap{padding:0 16px}.icbtn{width:42px;height:42px}}
@media(max-width:480px){.wrap{padding:0 13px}.grid,.posts{grid-template-columns:1fr}.sec-h h2{font-size:19px}.chip,.ctlb,.ctlf{padding:9px 13px}.cat{width:62px}.cat .ico{width:40px;height:40px}.hd .row{height:56px}.logo{font-size:18px}.searchbar .wrap{padding:11px 13px}.sb{padding:11px 13px}.sb .go{padding:10px 14px}.sec-h{margin-bottom:12px}section{padding:22px 0}}
/* 티라노차트 TOP 추천 가로 캐러셀(시안 홈) */
.t3caro{display:flex;gap:12px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:2px 0 10px;margin-bottom:6px}
.t3caro::-webkit-scrollbar{display:none}
.t3c{flex:0 0 152px;text-decoration:none;color:inherit}
.t3c .t3p{position:relative;width:100%;aspect-ratio:1.586/1;border-radius:12px;overflow:hidden;background:#eceef2;box-shadow:0 6px 16px rgba(0,0,0,.12)}
.t3c .t3p img{width:100%;height:100%;object-fit:cover;transition:transform .18s ease}
.t3c:hover .t3p img{transform:scale(1.06)}
.t3c .t3rk{position:absolute;top:8px;left:8px;width:24px;height:24px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:12px;box-shadow:0 2px 6px rgba(0,0,0,.18);z-index:2}
.t3c .t3n{font-weight:800;font-size:13.5px;margin-top:8px;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.t3c .t3a{font-weight:800;font-size:13px;color:var(--accent);margin-top:2px}
.t3c .t3i{font-size:10.5px;color:var(--dim);margin-top:1px}
/* ===== 모바일 재구성(시안: 카드티라노 모바일 최적화) ===== */
/* 하단 탭바 — 데스크톱 숨김, 모바일 고정 */
.mtab{display:none}
/* LIVE 티커(홈) */
.mlive{display:none}
.mlive .lvb{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;background:#ff3d8b;color:#fff;padding:9px 13px;font-family:var(--font-mono,monospace);font-size:11px;font-weight:800;letter-spacing:.5px;text-transform:uppercase}
.mlive .lvb i{width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block;animation:lvpulse 1.2s infinite}
@keyframes lvpulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes tyrannoPulse{0%,100%{opacity:.35;transform:scale(.96)}50%{opacity:1;transform:scale(1)}}
.tload{display:inline-flex;flex-direction:column;align-items:center;gap:9px;color:rgba(0,0,0,.5);font-size:11px;letter-spacing:.4px;font-family:ui-monospace,monospace;padding:24px 0}
.tload .tmk{width:36px;height:36px;color:#000;animation:tyrannoPulse 1.2s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.tload .tmk{animation:none}}
.lgl{padding:40px 0 64px}
.lgl-eb{font-family:ui-monospace,monospace;font-size:11px;letter-spacing:1px;color:#8b6fd6;font-weight:700}
.lgl-h{font-size:32px;font-weight:800;margin:8px 0 6px;letter-spacing:-.5px}
.lgl-date{font-family:ui-monospace,monospace;font-size:11.5px;color:rgba(0,0,0,.45);margin-bottom:14px}
.lgl-sec{border-top:1px solid var(--hairline,#e6e6e6);padding:20px 0 4px}
.lgl-sec h2{font-size:16.5px;font-weight:800;margin:0 0 9px}
.lgl-sec p{font-size:14px;line-height:1.75;color:rgba(0,0,0,.74);margin:0}
.lgl-sec a{color:#5b46b3;text-decoration:none;border-bottom:1px solid rgba(91,70,179,.3)}
.lgl-tbl{width:100%;border-collapse:collapse;font-size:14px}
.lgl-tbl th{text-align:left;width:170px;padding:11px 12px;background:#f6f5f1;border:1px solid var(--hairline,#e6e6e6);font-weight:700;color:rgba(0,0,0,.7);vertical-align:top}
.lgl-tbl td{padding:11px 14px;border:1px solid var(--hairline,#e6e6e6);color:rgba(0,0,0,.78)}
.lgl-note{font-size:12.5px;color:rgba(0,0,0,.5);margin-top:14px;line-height:1.6}
.lgl-back{margin-top:30px}.lgl-back a{font-family:ui-monospace,monospace;font-size:12.5px;color:rgba(0,0,0,.55);text-decoration:none}
@media(max-width:640px){.lgl-h{font-size:25px}.lgl-tbl th{width:108px;padding:9px}.lgl-tbl td{padding:9px}}
.lgl-grid{display:grid;grid-template-columns:180px 1fr;gap:40px;align-items:start}
.lgl-nav{position:sticky;top:84px;display:flex;flex-direction:column;gap:2px}
.lgl-nav .lnh{font-family:ui-monospace,monospace;font-size:10.5px;letter-spacing:1px;color:rgba(0,0,0,.4);font-weight:700;padding:0 12px 8px}
.lgl-nav a{font-size:13.5px;font-weight:600;color:rgba(0,0,0,.6);text-decoration:none;padding:10px 12px;border-radius:9px;border-left:2px solid transparent}
.lgl-nav a:hover{background:#f6f5f1;color:#000}
.lgl-nav a.on{background:#f3f0fb;color:#5b46b3;border-left-color:#5b46b3;font-weight:800}
@media(max-width:760px){.lgl-grid{grid-template-columns:1fr;gap:18px}.lgl-nav{position:static;flex-direction:row;flex-wrap:wrap;gap:6px}.lgl-nav .lnh{display:none}.lgl-nav a{border:1px solid var(--hairline,#e6e6e6)}.lgl-nav a.on{border-color:#5b46b3}}
.mlive .lvt{overflow:hidden;white-space:nowrap;flex:1}
.mlive .lvt span{display:inline-block;padding-left:100%;animation:lvmarq 16s linear infinite;font-size:12px;font-weight:700;letter-spacing:-.01em}
@keyframes lvmarq{0%{transform:translateX(0)}100%{transform:translateX(-100%)}}
/* 발급이벤트 네이비 피처 히어로(시안 screen4) */
.evhero{display:block;background:var(--block-navy);color:#fff;border-radius:24px;padding:30px 28px;margin:4px 0 16px;text-decoration:none;position:relative;overflow:hidden}
.evhero .eb{font-family:var(--font-mono,monospace);font-size:11px;letter-spacing:.5px;text-transform:uppercase;opacity:.72}
.evhero .evh-t{font-size:34px;font-weight:700;line-height:1.18;margin-top:8px;letter-spacing:-.02em}
.evhero .evh-t b{color:#fff}
.evhero .evh-cta{display:inline-block;margin-top:16px;background:#fff;color:#000;font-weight:800;font-size:15px;padding:13px 22px;border-radius:50px}
.evhero::after{content:"";position:absolute;right:-40px;top:-40px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.12),transparent 70%)}
.evhero .evh-wm{position:absolute;right:-3%;bottom:-14%;width:42%;max-width:230px;color:#fff;opacity:.14;pointer-events:none}
.evhero .evh-body{position:relative;z-index:1}
@media(max-width:760px){
 .mtab{display:flex;position:fixed;left:0;right:0;bottom:0;height:60px;background:#fff;border-top:1px solid var(--line);z-index:60;box-shadow:0 -2px 14px rgba(0,0,0,.06)}
 .mtab a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;color:var(--dim);font-size:10.5px;font-weight:700;text-decoration:none;min-height:44px}
 .mtab a svg{width:23px;height:23px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
 .mtab a.on{color:var(--accent)}
 body{padding-bottom:60px}
 .mlive{display:flex;align-items:center;background:#111;color:#fff;margin:14px 0 4px;overflow:hidden;border-radius:10px}
 /* 카드찾기(.cgrid): 그리드 → 리스트 행(플레이트 좌측) */
 .cgrid{grid-template-columns:1fr!important;gap:12px}
 .cgrid .ctile{flex-direction:row;align-items:center;gap:13px;padding:12px;text-align:left}
 .cgrid .ctile .plate{width:108px;height:68px;flex:0 0 auto;margin:0}
 .cgrid .ctile .cbody{flex:1;min-width:0;display:flex;flex-direction:column}
 .cgrid .ctile .cn{text-align:left;font-size:14.5px}
 .cgrid .ctile .cfee,.cgrid .ctile .cd{text-align:left;margin-top:4px}
 .cgrid .ctile .tag,.cgrid .ctile .evtag{align-self:flex-start}
 /* 칩 가로 스크롤 */
 .sfilters,.chips,.tabs,.subnav,.subnav2,.cmpctl .ctlrow{flex-wrap:wrap!important}
 .sfilters::-webkit-scrollbar,.chips::-webkit-scrollbar,.tabs::-webkit-scrollbar,.cmpctl .ctlrow::-webkit-scrollbar{display:none}
 .sfilters>*,.tabs>*,.subnav>*,.subnav2>*{flex:0 0 auto}
 /* 발급이벤트: 행 → 카드형 */
 .evlist .evrow,#list .ev{border:1px solid var(--line);border-radius:16px;padding:13px 14px;margin-bottom:11px}
 /* 터치타깃 */
 .pl,.chip,.tab,.ctlb,.ctlf,.subnav2 button{min-height:38px}
}
"""

HELPERS = r"""
// 모바일 하단 탭바 활성 표시(현재 페이지 기준)
(function(){var mt=document.getElementById('mtab');if(!mt)return;var pn=(location.pathname.split('/').pop()||'index').replace(/\.html$/,'');var qs=location.search||'';var cur='';
 if(pn==='cards'||pn==='carddetail')cur='cards';else if(pn==='issue')cur=/v=cmp/.test(qs)?'compare':'issue';else if(pn===''||pn==='index')cur='home';
 mt.querySelectorAll('a').forEach(function(a){if(a.dataset.tab===cur)a.classList.add('on');});})();
function _purl(plat,id){id=String(id||'').trim();if(!id)return '';return ({cardgorilla:'https://www.card-gorilla.com/card/detail/'+id,banksalad:'https://www.banksalad.com/product/cards/'+id,toss:'https://card-lounge.toss.im/card/'+id,ajungdang:'https://www.ajd.co.kr/card/event/detail/'+id}[plat])||'';}
function favSvg(f){return '<svg class="ic"><use href="#ic-heart'+(f?'-f':'')+'"/></svg>';}
function favClick(el,id){var f=toggleFav(id);el.innerHTML=favSvg(f);el.classList.toggle('on',f);if(f){el.classList.remove('pop');void el.offsetWidth;el.classList.add('pop');}if(window._fr)try{window._fr();}catch(e){}}
function _isList(u){if(!u)return true;return /banksalad\.com\/cards\/event/.test(u)||/pay\.naver\.com\/home\/promotion\/event/.test(u)||/card-gorilla\.com\/event\/?($|\?)/.test(u);}
// 카드고릴라 카드사 이벤트 그룹 페이지(웹사이트 /event/detail/{작은ID}). API idx(1288류)와 다른 id공간이라 발급사→그룹ID로 생성.
var _CGG={'삼성카드':'1','신한카드':'2','KB국민카드':'3','롯데카드':'4','우리카드':'5','현대카드':'7','하나카드':'8','NH농협카드':'9','IBK기업은행':'10'};
function _cgUrl(issuer,id){var g=_CGG[(issuer||'').trim()];return g?('https://www.card-gorilla.com/event/detail/'+g):(id?('https://www.card-gorilla.com/card/detail/'+id):'');}
// 카카오페이 fest 링크: 공유채널 추적 파라미터(t_src/t_ch=...share_link/t_obj)는 앱 컨텍스트를 요구해
// 데스크톱 웹에서 홈으로 리다이렉트시킨다. 이를 제거한다. 외부 추천인 코드(f_recommenderCode)도 제거(미보유 코드 적립 방지).
function _kpClean(u){try{if(!/fest\.kakaopay\.com/.test(u))return u;var x=new URL(u);['t_src','t_ch','t_obj','t_act','t_page','f_recommenderCode'].forEach(function(k){x.searchParams.delete(k);});return x.toString();}catch(e){return u;}}
function _best(plat,raw,id){if(raw&&!_isList(raw))return (plat==='kakaopay')?_kpClean(raw):raw;var d=_purl(plat,id);return (d&&!_isList(d))?d:'';}  // 그룹/상세 우선, 전체리스트는 배제·카카오페이 공유파라미터 정리
function thumbOf(p){var m=[["마트|이마트24","ic-cart"],["하이마트|가전|전자","ic-grid"],["편의|GS25|CU|세븐","ic-cart"],["백화점","ic-bag"],["면세","ic-bag"],["주유|칼텍스|에너지|OIL|오일","ic-fuel"],["CGV|시네마|메가박스|영화","ic-film"],["스타벅스|카페|커피","ic-cup"],["무신사|W컨셉|한섬|패션|의류","ic-bag"],["알라딘|교보|도서|서점","ic-grid"],["홈쇼핑|CJ|GS샵|NS","ic-bag"],["야놀자|여행|항공|패키지","ic-plane"],["통신|SKT|KT|LG U|U\\+","ic-phone"],["쿠팡|11번가|G마켓|옥션|SSG|롯데온|올리브영|온라인","ic-bag"]];for(var i=0;i<m.length;i++){if(new RegExp(m[i][0]).test(p))return{e:m[i][1],bg:"#f7f7f5"};}return{e:"ic-grid",bg:"#f7f7f5"};}
function favico(dom,e,bg){return '<svg class="thic" aria-hidden="true"><use href="#'+(e||'ic-grid')+'"/></svg>';}
var DEFCARD="data:image/svg+xml,"+encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 202'><rect width='320' height='202' rx='14' fill='#f1eef8'/><rect x='24' y='34' width='46' height='34' rx='6' fill='#dcd5ef'/><g opacity='0.14' transform='translate(150 64) scale(7)' fill='#2a2440'><path d='M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z'/><path fill-rule='evenodd' d='M15.4 4.6 H19 A2 2 0 0 1 21 6.6 V9.2 A2 2 0 0 1 19 11.2 H15.4 A2 2 0 0 1 13.4 9.2 V6.6 A2 2 0 0 1 15.4 4.6 Z M17.6 6.5 a0.8 0.8 0 1 1 -1.6 0 a0.8 0.8 0 1 1 1.6 0 Z M18.2 7.8 H19.9 A0.5 0.5 0 0 1 20.4 8.3 V9.6 A0.5 0.5 0 0 1 19.9 10.1 H18.2 A0.5 0.5 0 0 1 17.7 9.6 V8.3 A0.5 0.5 0 0 1 18.2 7.8 Z'/></g><text x='24' y='176' font-family='ui-monospace,monospace' font-size='15' font-weight='700' fill='#2a2440'>CARD<tspan font-weight='400'>TYRANNO</tspan></text></svg>");
function imgTag(src,cls){var c=cls?(' class="'+cls+'"'):'';if(!src)return '<img'+c+' src="'+DEFCARD+'" alt="">';return '<img'+c+' src="'+encodeURI(src)+'" loading="lazy" alt="" onerror="this.onerror=null;this.src=DEFCARD;this.classList.add(\'isdef\')">';}
// 카드 플레이트 이미지 메타 맵: 카드고릴라 카탈로그(card_img)에서 정규화 카드명→이미지. 거주지 IP면 :8080이 card_img 제공. localStorage 24h 캐시.
function _nkimg(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function cgImageMap(){
 if(window.__CGIMG)return Promise.resolve(window.__CGIMG);
 try{var c=JSON.parse(localStorage.getItem('ct_cgimg')||'null');if(c&&c.t&&(Date.now()-c.t)<86400000&&c.m){window.__CGIMG=c.m;return Promise.resolve(c.m);}}catch(e){}
 return fetch('https://api.card-gorilla.com:8080/v1/cards?type=CBK&is_live=true',{headers:{'Accept':'application/json'}}).then(function(r){return r.json();}).then(function(j){
  var arr=Array.isArray(j)?j:(j.data||j.list||[]);var m={};arr.forEach(function(c){var u=(c&&c.card_img||{}).url;if(c&&c.name&&u)m[_nkimg(c.name)]=u;});
  window.__CGIMG=m;try{localStorage.setItem('ct_cgimg',JSON.stringify({t:Date.now(),m:m}));}catch(e){}return m;
 }).catch(function(){return {};});
}
function repairImages(){cgImageMap().then(function(M){if(!M||!Object.keys(M).length)return;
 document.querySelectorAll('img[src^="data:image/svg+xml"]').forEach(function(im){
  var card=im.closest('.ctile,.cmpcard,.gcard,.rk,.crow,#cardad');if(!card)return;
  var n=card.querySelector('.cn,.ch,.ct,.rn,#cadname');if(!n)return;
  var u=M[_nkimg(n.textContent)];if(u){im.onerror=null;im.src=encodeURI(u);im.classList.remove('isdef');}
 });});}
if(typeof window!=='undefined'){window.addEventListener('load',function(){setTimeout(repairImages,600);setTimeout(repairImages,2200);});}
function getFav(){try{return JSON.parse(localStorage.getItem('ct_fav')||'[]');}catch(e){return [];}}
function setFav(a){try{localStorage.setItem('ct_fav',JSON.stringify(a));}catch(e){}}
function isFav(id){return getFav().indexOf(id)>=0;}
function toggleFav(id){var a=getFav();var i=a.indexOf(id);if(i>=0)a.splice(i,1);else a.push(id);setFav(a);updateFavCount();if(window.ctPushSync)try{ctPushSync();}catch(e){}return i<0;}
function updateFavCount(){var el=document.getElementById('favCount');if(el){var n=getFav().length;el.textContent=n;el.style.display=n?'inline-block':'none';}}
function _pg(){return location.pathname.split('/').pop()||'index.html';}
function track(type,label){try{
 var a=JSON.parse(localStorage.getItem('ct_evt')||'[]');
 a.push({t:type,l:(label||'').toString().trim().slice(0,80),p:_pg(),ts:Date.now()});
 if(a.length>3000)a=a.slice(-3000);localStorage.setItem('ct_evt',JSON.stringify(a));
 var sid=localStorage.getItem('ct_sid');if(!sid){sid=Date.now()+'-'+Math.random().toString(36).slice(2,8);localStorage.setItem('ct_sid',sid);localStorage.setItem('ct_first',Date.now());}
}catch(_){}}
function trackPV(){track('pageview',_pg());}
function bindTrack(){document.addEventListener('click',function(ev){
 var t=ev.target;if(!t||!t.closest)return;
 var el=t.closest('[data-track]');
 if(el){track(el.getAttribute('data-track'),el.getAttribute('data-label')||el.textContent);return;}
 el=t.closest('.gnb a,.drawer a,.util a,.foot a');if(el){track('menu',el.textContent);return;}
 el=t.closest('.ctile');if(el){track('card',(el.querySelector('.cn')||{}).textContent||'');return;}
 el=t.closest('.cat');if(el){track('category',el.textContent);return;}
 el=t.closest('.tab,.chip');if(el){track('filter',el.textContent);return;}
 el=t.closest('.item');if(el){track('item',(el.querySelector('.l2')||{}).textContent||el.textContent);return;}
 el=t.closest('.rk,.crow');if(el){track('rank',(el.querySelector('.rn,.cn')||{}).textContent||'');return;}
},true);}
function bindUI(){var d=document.getElementById('drawer'),s=document.getElementById('scrim'),m=document.getElementById('menuBtn');if(m)m.onclick=function(){d.classList.add('on');s.classList.add('on');};if(s)s.onclick=function(){d.classList.remove('on');s.classList.remove('on');};
 function go(){var q=(document.getElementById('siteSearch')||{}).value||'';location.href='search.html?q='+encodeURIComponent(q);}
 var f=document.getElementById('siteSearch');if(f)f.addEventListener('keydown',function(e){if(e.key==='Enter')go();});
 ['searchGo','searchGo2'].forEach(function(id){var b=document.getElementById(id);if(b)b.onclick=go;});
 updateFavCount();trackPV();bindTrack();}
function renderBenefit(d){
 if(!d||!d.items) return '<div class="bnone">상세 혜택 정보 준비 중이에요. 카드사·플랫폼에서 최종 확인하세요.</div>';
 var lg={};(d.limit_groups||[]).forEach(function(g){lg[g.id]=g;});
 var groups={},order=[];
 d.items.forEach(function(it){var g=it.limit||'_';if(!groups[g]){groups[g]=[];order.push(g);}groups[g].push(it);});
 var html=order.map(function(gid){var g=lg[gid]||{};var cap='';
  if(g.scope==='통합') cap='<div class="lcap">통합한도'+(g.amount?(' · '+g.unit+' '+g.amount.toLocaleString()+'원'):'')+'</div>';
  else if(g.amount) cap='<div class="lcap">개별한도 · '+g.unit+' '+g.amount.toLocaleString()+'원</div>';
  return '<div class="bgrp">'+cap+groups[gid].map(function(it){
   return '<div class="bitem"><div class="bareas">'+it.areas.map(function(a){return '<span class="ba">'+a+'</span>';}).join('')+'</div><div class="bval"><span class="bv">'+it.value+'</span> <span class="bm">'+(it.method||'')+(it.type||'')+'</span>'+(it.tier&&it.tier!=='기본'?'<span class="btier">'+it.tier+'</span>':'')+'</div></div>';
  }).join('')+'</div>';
 }).join('');
 var head='<div class="bhead">'+(d.prev_spend?('전월실적 '+d.prev_spend):'전월실적 없음')+(d.max_benefit?(' · '+d.max_benefit):'')+'</div>';
 return head+html;
}
/* ===== 관심카드 푸시 알림 (옵션 A: SW 로컬 체크, 백엔드 불필요) ===== */
function ctPushSupported(){return ('Notification' in window)&&('serviceWorker' in navigator);}
function ctPushOn(){try{return localStorage.getItem('ct_push')==='1';}catch(e){return false;}}
function _ctMsg(m){if(!('serviceWorker' in navigator))return;navigator.serviceWorker.ready.then(function(r){var t=r.active||navigator.serviceWorker.controller;if(t)t.postMessage(m);});}
function ctFavList(cb){fetch('cards.json').then(function(r){return r.json();}).then(function(j){var fav=getFav(),out=[],seen={};for(var k in j.cards){(j.cards[k]||[]).forEach(function(c){if(fav.indexOf(c.id)>=0){var nk=_nk2(c.name);if(!seen[nk]){seen[nk]=1;out.push({nk:nk,name:c.name});}}});}cb(out);}).catch(function(){cb([]);});}
function ctRegSW(){return navigator.serviceWorker.register('/sw.js');}
function ctPushSync(){if(!ctPushOn()||!('serviceWorker' in navigator))return;ctFavList(function(list){_ctMsg({type:'sync',favList:list});});}
function ctPushEnable(cb){cb=cb||function(){};
 if(!ctPushSupported()){cb(false,'이 브라우저는 알림을 지원하지 않아요.');return;}
 Notification.requestPermission().then(function(p){
  if(p!=='granted'){cb(false,'알림 권한이 거부됐어요. 브라우저 주소창 옆 설정에서 알림을 허용해 주세요.');return;}
  try{localStorage.setItem('ct_push','1');}catch(e){}
  ctRegSW().then(function(reg){ctFavList(function(list){
    _ctMsg({type:'enable',favList:list});
    if(reg.periodicSync){try{reg.periodicSync.register('ct-events',{minInterval:12*60*60*1000});}catch(e){}}
    cb(true,'');
  });}).catch(function(){cb(false,'알림 등록에 실패했어요. 잠시 후 다시 시도해 주세요.');});
 }).catch(function(){cb(false,'알림 권한 요청에 실패했어요.');});
}
function ctPushDisable(){try{localStorage.setItem('ct_push','0');}catch(e){}_ctMsg({type:'disable'});}
function ctPushTest(cb){cb=cb||function(){};
 if(!ctPushSupported()){cb(false,'이 브라우저는 알림을 지원하지 않아요.');return;}
 Notification.requestPermission().then(function(p){
  if(p!=='granted'){cb(false,'알림 권한을 허용해야 테스트할 수 있어요.');return;}
  ctRegSW().then(function(){_ctMsg({type:'test'});cb(true,'');}).catch(function(){cb(false,'알림 등록에 실패했어요.');});
 }).catch(function(){cb(false,'알림 권한 요청에 실패했어요.');});
}
function ctPushBoot(){if(!ctPushOn()||!('serviceWorker' in navigator))return;
 ctRegSW().then(function(){ctFavList(function(list){_ctMsg({type:'sync',favList:list});_ctMsg({type:'check'});});}).catch(function(){});}
if(typeof window!=='undefined'){window.addEventListener('load',function(){setTimeout(ctPushBoot,1500);});}
"""

# 디자인 QA HIGH: 이모지 → 아웃라인 글리프(24 그리드, 1.75 stroke, currentColor). OS 의존·모노크롬 붕괴 제거.
ICONS=('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
 '<g id="o" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"></g>'
 '<symbol id="ic-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-5-5"/></symbol>'
 '<symbol id="ic-heart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20S4 15.3 4 9.8A3.9 3.9 0 0 1 12 7.6 3.9 3.9 0 0 1 20 9.8C20 15.3 12 20 12 20Z"/></symbol>'
 '<symbol id="ic-heart-f" viewBox="0 0 24 24"><path fill="currentColor" d="M12 20S4 15.3 4 9.8A3.9 3.9 0 0 1 12 7.6 3.9 3.9 0 0 1 20 9.8C20 15.3 12 20 12 20Z"/></symbol>'
 '<symbol id="ic-food" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3v8M9 3v8M6 11h3M7.5 11v10M16.5 3c-1.4 0-2.5 2-2.5 5.5S15.1 13 16.5 13 19 11 19 8.5 17.9 3 16.5 3Zm0 10v8"/></symbol>'
 '<symbol id="ic-bag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8a3 3 0 0 1 6 0"/></symbol>'
 '<symbol id="ic-fuel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 20V6a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v14M4 20h12M15 9h2.5A1.5 1.5 0 0 1 19 10.5V16a1.5 1.5 0 0 0 1.5 1.5A1.5 1.5 0 0 0 22 16V8l-3-3"/><path d="M8 8h4"/></symbol>'
 '<symbol id="ic-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/></symbol>'
 '<symbol id="ic-plane" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10 4.5a1.5 1.5 0 0 1 3 0V10l8 4.5V17l-8-2.5V19l2.5 1.5V22L11.5 21 8 22v-1.5L10.5 19v-4.5L2.5 17v-2.5L10.5 10Z"/></symbol>'
 '<symbol id="ic-cart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h2l2.5 12h10l2-8H6.5"/><circle cx="9" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/></symbol>'
 '<symbol id="ic-cup" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h12v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8Z"/><path d="M17 9h2a2 2 0 0 1 0 4h-2M8 3v2M11 3v2"/></symbol>'
 '<symbol id="ic-film" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M4 9h16M4 15h16M9 5v14M15 5v14"/></symbol>'
 '<symbol id="ic-repeat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h12l-2-2M20 16H8l2 2"/></symbol>'
 '<symbol id="ic-car" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v-3l2-5a2 2 0 0 1 2-1.3h8A2 2 0 0 1 18 8l2 5v3M4 13h16"/><circle cx="7.5" cy="16.5" r="1.3"/><circle cx="16.5" cy="16.5" r="1.3"/></symbol>'
 '<symbol id="ic-cross" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v12M6 12h12"/></symbol>'
 '<symbol id="mk" viewBox="2 3.6 20 16.4"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z"/><path fill="currentColor" fill-rule="evenodd" d="M15.4 4.6 H19 A2 2 0 0 1 21 6.6 V9.2 A2 2 0 0 1 19 11.2 H15.4 A2 2 0 0 1 13.4 9.2 V6.6 A2 2 0 0 1 15.4 4.6 Z M17.6 6.5 a0.8 0.8 0 1 1 -1.6 0 a0.8 0.8 0 1 1 1.6 0 Z M18.2 7.8 H19.9 A0.5 0.5 0 0 1 20.4 8.3 V9.6 A0.5 0.5 0 0 1 19.9 10.1 H18.2 A0.5 0.5 0 0 1 17.7 9.6 V8.3 A0.5 0.5 0 0 1 18.2 7.8 Z"/></symbol>'
 '<symbol id="ic-grid" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></symbol>'
 '</defs></svg>')

def header(active):
    L=[("cards","cards.html","카드찾기",""),("compare","issue.html?v=cmp","플랫폼 비교","캐시백 가장 많이 주는 사이트를 확인해보세요!"),("issue","issue.html","이번달 캐시백",""),
       ("charts","chart.html","티라노차트",""),("content","content.html","티라노TIP",""),("community","community.html","커뮤니티","")]
    gnb="".join('<a href="%s" class="%s"%s>%s</a>'%(u,("on" if k==active else ""),(' title="%s"'%tip if tip else ''),t) for k,u,t,tip in L)
    drawer="".join('<a href="%s"%s>%s</a>'%(u,(' title="%s"'%tip if tip else ''),t) for k,u,t,tip in L)
    return (ICONS+'<div class="scrim" id="scrim"></div><aside class="drawer" id="drawer">'
            '<div class="logo" style="margin-bottom:10px"><svg class="rx" viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.4 4.6 H19 A2 2 0 0 1 21 6.6 V9.2 A2 2 0 0 1 19 11.2 H15.4 A2 2 0 0 1 13.4 9.2 V6.6 A2 2 0 0 1 15.4 4.6 Z M17.6 6.5 a0.8 0.8 0 1 1 -1.6 0 a0.8 0.8 0 1 1 1.6 0 Z M18.2 7.8 H19.9 A0.5 0.5 0 0 1 20.4 8.3 V9.6 A0.5 0.5 0 0 1 19.9 10.1 H18.2 A0.5 0.5 0 0 1 17.7 9.6 V8.3 A0.5 0.5 0 0 1 18.2 7.8 Z M18.05 8.87 H20.05 V9.03 H18.05 Z M18.78 8.13 H18.94 V9.77 H18.78 Z"/></svg>CARD<b>TYRANNO</b></div>'+drawer+'</aside>'
            '<div class="util"><div class="wrap"><a href="content.html">가이드</a><a href="mailto:contact@cardtyranno.com">제휴·광고 문의</a></div></div>'
            '<header class="hd"><div class="wrap row">'
            '<span class="icbtn menu" id="menuBtn">☰</span>'
            '<a class="logo" href="index.html"><svg class="rx" viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.4 4.6 H19 A2 2 0 0 1 21 6.6 V9.2 A2 2 0 0 1 19 11.2 H15.4 A2 2 0 0 1 13.4 9.2 V6.6 A2 2 0 0 1 15.4 4.6 Z M17.6 6.5 a0.8 0.8 0 1 1 -1.6 0 a0.8 0.8 0 1 1 1.6 0 Z M18.2 7.8 H19.9 A0.5 0.5 0 0 1 20.4 8.3 V9.6 A0.5 0.5 0 0 1 19.9 10.1 H18.2 A0.5 0.5 0 0 1 17.7 9.6 V8.3 A0.5 0.5 0 0 1 18.2 7.8 Z M18.05 8.87 H20.05 V9.03 H18.05 Z M18.78 8.13 H18.94 V9.77 H18.78 Z"/></svg>CARD<b>TYRANNO</b></a>'
            '<nav class="gnb">'+gnb+'</nav>'
            '<div class="right"><div class="icbtn" id="searchGo"><svg class="ic"><use href="#ic-search"/></svg></div>'
            '<a class="icbtn" href="favorites.html" title="관심카드" style="position:relative"><svg class="ic"><use href="#ic-heart"/></svg><i id="favCount" style="position:absolute;top:-5px;right:-5px;background:var(--accent);color:#fff;font-size:9px;font-weight:800;border-radius:8px;padding:1px 5px;font-style:normal;display:none"></i></a></div>'
            '</div></header>')

SEARCHBAR=('<div class="searchbar"><div class="wrap">'
 '<div class="sb"><span><svg class="ic"><use href="#ic-search"/></svg></span><input id="siteSearch" placeholder="카드명 · 카드사 · 가맹점 · 혜택을 검색하세요"><button class="go" id="searchGo2">검색</button></div>'
 '<div class="sfilters"><span class="chip">즉시할인</span><span class="chip">청구할인</span><a class="chip" href="installment.html">무이자할부</a><span class="chip">캐시백</span><a class="chip" href="issue.html">발급 이벤트</a></div>'
 '</div></div>')

CATSTRIP=('<div class="catstrip"><div class="wrap">'
 +"".join('<a class="cat" href="discount.html?cat=%s"><span class="ico"><svg class="ic"><use href="#ic-%s"/></svg></span>%s</a>'%(n,g,n) for g,n in
   [("food","식음료"),("bag","쇼핑"),("fuel","주유"),("phone","통신"),("plane","여행"),("cart","마트"),("cup","카페"),("film","문화"),("repeat","구독"),("car","자동차"),("cross","병원"),("grid","전체")])
 +'</div></div>')

MTABBAR=('<nav class="mtab" id="mtab" aria-label="모바일 내비게이션">'
 '<a href="index.html" data-tab="home"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11.4 12 4l8 7.4"/><path d="M6 10v9.5h12V10"/></svg><span>홈</span></a>'
 '<a href="cards.html" data-tab="cards"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M3 10h18"/></svg><span>카드찾기</span></a>'
 '<a href="issue.html?v=cmp" data-tab="compare"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4v16M18 4v16M6 9h7M18 15h-7"/></svg><span>비교</span></a>'
 '<a href="issue.html" data-tab="issue"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 3l-7 10h5l-1 8 7-10h-5z"/></svg><span>캐시백</span></a>'
 '<a href="community.html" data-tab="community"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>커뮤니티</span></a>'
 '</nav>')

FOOTER=('<footer><div class="wrap foot">'
 '<div class="brand"><div class="lg">CARD<b>TYRANNO</b></div>'
 '<p>카드티라노는 여러 카드 중개 플랫폼의 카드·이벤트 혜택을 한곳에서 비교·분석해 드리는 정보 서비스입니다. 실제 카드 발급·심사는 각 카드사에서 진행됩니다.</p></div>'
 '<div class="col"><h4>서비스</h4><a href="cards.html">카드찾기</a><a href="issue.html">이번달 캐시백</a><a href="installment.html">무이자할부</a><a href="content.html">카드 가이드</a></div>'
 '<div class="col"><h4>회사</h4><a href="mailto:contact@cardtyranno.com">제휴·광고 문의</a><a href="business.html">사업자정보</a></div>'
 '<div class="col"><h4>약관·정책</h4><a href="terms.html">이용약관</a><a href="privacy.html">개인정보처리방침</a></div></div>'
 '<div class="wrap legal">카드티라노는 카드사·제휴 플랫폼의 광고/정보를 제공하는 <b>광고·정보제공 매체</b>이며, 카드 발급을 중개·접수하지 않습니다. 카드 신청·발급·심사는 각 카드사에서 진행됩니다. 게시된 캐시백·이벤트는 제휴 플랫폼·카드사의 <b>공개 데이터를 기준으로 자동 정렬</b>되며, 금액은 <b>최대 금액 기준</b>(전월실적·사용처·한도 등 조건 충족 시)입니다. 게시된 혜택·캐시백·연회비는 수집 시점 기준이며 실제와 다를 수 있어 신청 전 각 카드사·플랫폼에서 최종 확인이 필요합니다. <b>일부 링크는 제휴(광고) 링크</b>로, 이를 통해 수수료를 받을 수 있습니다.'
 '<div class="biz muted">카드티라노(CardTyranno) · 쥬라기랩스 · 제휴/광고 contact@cardtyranno.com</div>'
 '<div class="biz">© 2026 CARDTYRANNO. All rights reserved.</div></div></footer>')

def jsonld_base(path):
    site={"@context":"https://schema.org","@type":"WebSite","name":BRAND,"alternateName":BRAND_EN,"url":BASE,
      "description":DESC_SITE,"inLanguage":"ko",
      "potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":BASE+"/discount.html?q={query}"},"query-input":"required name=query"}}
    org={"@context":"https://schema.org","@type":"Organization","name":BRAND,"alternateName":BRAND_EN,"url":BASE,"logo":BASE+"/logo.png",
      "description":DESC_SITE,"sameAs":[]}
    return [site,org]

def head(title,desc,path,extra_jsonld=None,noindex=False):
    kw="카드티라노,카드 비교,카드 발급 혜택,카드 할인 혜택,카드 캐시백,신용카드 추천,카드 이벤트,카드 순위,2026 카드"
    blocks=[] if noindex else jsonld_base(path)+([extra_jsonld] if extra_jsonld else [])
    ld="".join('<script type="application/ld+json">%s</script>'%json.dumps(b,ensure_ascii=False) for b in blocks)
    robots="noindex,nofollow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
      '<title>'+title+'</title>'
      '<meta name="description" content="'+desc+'"><meta name="keywords" content="'+kw+'">'
      '<meta name="robots" content="'+robots+'">'
      '<meta name="theme-color" content="#ffffff"><link rel="canonical" href="'+BASE+path+'">'
      +('<meta name="naver-site-verification" content="'+NAVER_SITE_VERIFICATION+'">' if NAVER_SITE_VERIFICATION else '')
      +('<meta name="google-site-verification" content="'+GOOGLE_SITE_VERIFICATION+'">' if GOOGLE_SITE_VERIFICATION else '')
      +'<link rel="alternate" type="application/rss+xml" title="카드티라노 카드 이벤트" href="'+BASE+'/rss.xml">'
      '<meta property="og:type" content="website"><meta property="og:site_name" content="'+BRAND+'"><meta property="og:title" content="'+title+'">'
      '<meta property="og:description" content="'+desc+'"><meta property="og:url" content="'+BASE+path+'"><meta property="og:image" content="'+BASE+'/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="'+BRAND+'"><meta property="og:locale" content="ko_KR">'
      '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+title+'"><meta name="twitter:description" content="'+desc+'"><meta name="twitter:image" content="'+BASE+'/og-image.png">'
      '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22></text></svg>">'
      +('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token":"'+CF_BEACON_TOKEN+'"}\'></script>' if CF_BEACON_TOKEN else '')
      +ld)

def page(fname,title,desc,path,body,script="",extra_jsonld=None,searchbar=False,catstrip=False,active="",noindex=False):
    html=('<!DOCTYPE html><html lang="ko"><head>'+head(title,desc,path,extra_jsonld,noindex)
      +'<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">'
      +'<style>'+CSS+'</style></head><body>'
      +header(active)+(SEARCHBAR if searchbar else "")+(CATSTRIP if catstrip else "")
      +body+FOOTER+MTABBAR+'<script>'+HELPERS+script+'\nbindUI();</script></body></html>')
    open(os.path.join(SITE,fname),"w",encoding="utf-8").write(html)

# ===== 티라노 브랜드 플레이트 배너(특정 카드 아님 · 서비스 대표 장식) =====
_DINO='<path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.8 4.6 h2.6 a2.6 2.6 0 0 1 2.6 2.6 v1.7 a2.6 2.6 0 0 1 -2.6 2.6 h-2.6 a2.6 2.6 0 0 1 -2.6 -2.6 v-1.7 a2.6 2.6 0 0 1 2.6 -2.6 z M17.75 7.4 a0.85 0.85 0 1 0 1.7 0 a0.85 0.85 0 1 0 -1.7 0 z M18.4 9.5 h2.6 v1 h-2.6 z"/>'
def tybnr(href,eb,h,sub):
    dino='<svg class="tyb-dino" viewBox="0 0 24 24" aria-hidden="true">'+_DINO+'</svg>'
    plate=('<div class="tyb-plate"><span class="tyb-mk">CARD<b>TYRANNO</b></span>'+dino+'</div>')
    return ('<a class="tybnr" href="'+href+'"><div class="tyb-txt"><div class="tyb-eb">'+eb+'</div>'
      '<div class="tyb-h">'+h+'</div><div class="tyb-sub">'+sub+'</div></div>'+plate+'</a>')

# ===== FAQ (AEO) =====
FAQ=[
 ["2026년 6월 카드 발급 시 가장 많이 주는 카드는?","삼성카드가 최대 119만원, 현대카드 최대 89만원, KB국민카드 최대 86만원 수준의 신규 발급 혜택을 제공합니다. 같은 카드라도 발급 채널(토스·카드고릴라·아정당·카카오페이)에 따라 금액이 달라집니다."],
 ["카드 즉시할인과 청구할인의 차이는?","즉시할인은 결제하는 순간 금액이 차감되고, 청구할인은 카드값 청구 시점에 차감됩니다. 최종 할인액이 같다면 손익은 비슷하지만 적립·한도 조건에서 차이가 있을 수 있습니다."],
 ["발급 채널(플랫폼)에 따라 혜택이 다른가요?","네. 같은 카드라도 토스 카드라운지·카드고릴라·아정당·카카오페이 등 채널별로 캐시백·사은품이 다를 수 있어 발급 전 비교가 필요합니다."],
 ["연회비 캐시백은 어떻게 받나요?","보통 신규 발급 후 일정 기간 내 결제와 마케팅 수신 동의 등 조건을 충족하면 익월 전후에 지급됩니다. 직전 6개월 내 동일 카드사 이력이 있으면 제외될 수 있습니다."],
]
def faq_jsonld():
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
FAQ_HTML='<section class="faq"><div class="sec-h"><h2>자주 묻는 질문</h2></div>'+"".join('<div class="q"><h3>'+q+'</h3><p>'+a+'</p></div>' for q,a in FAQ)+'</section>'

CUR_HTML=('<section id="curation"><div class="sec-h"><h2>테마별 큐레이션</h2></div><div class="cur">'
 '<a class="curc"><span class="em"><svg class="ic"><use href="#ic-car"/></svg></span><div class="th">THEME</div><div class="ti">신차 구매자를 위한 카드</div><div class="ds">자동차 할부·주유·정비 혜택 모음</div></a>'
 '<a class="curc"><span class="em"><svg class="ic"><use href="#ic-plane"/></svg></span><div class="th">THEME</div><div class="ti">해외여행 필수 카드</div><div class="ds">수수료 면제·라운지·마일리지</div></a>'
 '<a class="curc"><span class="em"><svg class="ic"><use href="#ic-grid"/></svg></span><div class="th">THEME</div><div class="ti">사회초년생 첫 카드</div><div class="ds">연회비 낮고 실적 부담 적은 카드</div></a></div></section>')

# ===== INDEX (landing) =====
INDEX_BODY=('<div class="wrap">'
 # ===== A · 히어로 롤링 컴카드 (캐러셀) =====
 '<div class="nhc" id="nhc" aria-roledescription="carousel">'
 '<div class="nhc-vp"><div class="nhc-track" id="nhcTrack">'
 # 슬라이드 1 · 6개 사이트 비교
 '<div class="nhc-slide nhc-s1">'
 '<svg class="nhc-face" viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg>'
 '<div class="nhc-txt"><div class="nhe-eb">2026 JUNE</div>'
 '<h1 class="nhc-h">6개 사이트<br>캐시백, 한눈에.</h1>'
 '<p class="nhc-p">토스·카드고릴라·아정당·뱅크샐러드·카카오페이·네이버페이. <b>6개 카드 발급 사이트의 캐시백을 한 번에 비교</b>해 드려요.</p>'
 '<a class="nhe-cta" href="content.html">이번달 전문가 TIP <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></div>'
 '<div class="nhc-ill"><div class="nhc-cmp" id="heroCmp"><div class="nhc-cmp-h"><span class="mono">6개 플랫폼 캐시백</span><span class="mono nhc-cmp-top">최고값</span></div><div class="nhc-cmp-bars" id="heroCmpBars"></div></div></div>'
 '</div>'
 # 슬라이드 2 · 이번달 최고 캐시백 상품 (JS가 채움)
 '<a class="nhc-slide nhc-s2" id="heroS2" href="issue.html?v=cmp">'
 '<svg class="nhc-face nhc-face-b" viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg>'
 '<div class="nhc-txt"><div class="nhe-eb">이번달 최고 캐시백</div>'
 '<h1 class="nhc-h nhc-h2" id="heroS2Name">불러오는 중…</h1>'
 '<div class="nhc-amt" id="heroS2Amt"></div>'
 '<p class="nhc-p" id="heroS2Sub"></p>'
 '<span class="nhe-cta">이 상품 보러가기 <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></span></div>'
 '<div class="nhc-plate" id="heroS2Plate"></div>'
 '</a>'
 '</div></div>'
 '<div class="nhc-dots" id="nhcDots"><span class="on" data-i="0" role="button" aria-label="슬라이드 1"></span><span data-i="1" role="button" aria-label="슬라이드 2"></span></div>'
 '</div>'
 '</div>'
 '<div class="nlive"><span class="nlive-tag"><i></i>LIVE</span><div class="nlive-vp"><div class="nlive-tk" id="liveTk">이번 달 최대 캐시백 <span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div class="wrap">'
 '<div class="npod"><div class="npod-h"><div><div class="nhe-eb dim">이번 달 캐시백</div><h2 class="npod-t">이번 달 이벤트 TOP 3</h2><p class="npod-s">발급 이벤트 금액이 가장 큰 상품을 카드사별 1개씩 · 공개 데이터 기준 자동 정렬</p></div><a class="nmore" href="issue.html?v=cmp">플랫폼 비교 ›</a></div>'
 '<div class="npod-g" id="t3pod"></div></div>'
 '<style>'
 # --- A · 히어로 캐러셀 ---
 '.nhc{margin:28px 0 0}'
 '.nhc-vp{overflow:hidden;border-radius:24px}'
 '.nhc-track{display:flex;width:200%;transition:transform .6s cubic-bezier(.4,0,.2,1)}'
 '.nhc-slide{width:50%;flex-shrink:0;padding:48px 48px;position:relative;overflow:hidden;display:flex;align-items:center;gap:30px;min-height:300px;text-decoration:none;color:#000}'
 '.nhc-s1{background:var(--block-lilac)}.nhc-s2{background:var(--block-mint)}'
 '.nhc-face{position:absolute;left:-18px;top:-26px;width:128px;height:128px;opacity:.12;color:#000;pointer-events:none}'
 '.nhc-face-b{left:auto;right:-22px;top:auto;bottom:-30px;width:150px;height:150px}'
 '.nhc-txt{flex:1;min-width:0;position:relative;z-index:1}'
 '.nhc-h{font-weight:400;font-size:46px;line-height:1;letter-spacing:-1.6px;margin:14px 0 0;color:#000}'
 '.nhc-h2{font-size:40px;letter-spacing:-1.3px}'
 '.nhc-amt{font-weight:700;font-size:30px;letter-spacing:-.8px;margin-top:8px}'
 '.nhc-p{font-weight:400;font-size:15px;line-height:1.5;margin:14px 0 0;max-width:380px;color:rgba(0,0,0,.74)}'
 '.nhc-ill{width:248px;flex-shrink:0;position:relative;z-index:1}'
 '.nhc-cmp{background:#fff;border-radius:18px;padding:18px 18px 16px;box-shadow:0 14px 34px rgba(0,0,0,.16)}'
 '.nhc-cmp-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px}.nhc-cmp-h .mono{font-size:9.5px;letter-spacing:.5px;text-transform:uppercase;opacity:.55}.nhc-cmp-top{opacity:.85!important;font-weight:700}'
 '.nhc-cmp-bars{display:flex;flex-direction:column;gap:9px}'
 '.nhc-cmp-row{display:flex;align-items:center;gap:9px}.nhc-cmp-row i{width:8px;height:8px;border-radius:50%;flex-shrink:0}.nhc-cmp-row .nm{width:58px;font-weight:540;font-size:11px;white-space:nowrap;flex-shrink:0}'
 '.nhc-cmp-row .tr{flex:1;height:9px;border-radius:50px;background:#f1f1ef;overflow:hidden}.nhc-cmp-row .tr i{display:block;height:100%;border-radius:50px;width:0;background:#cfcfcf;border-radius:50px}'
 '.nhc-plate{width:300px;flex-shrink:0;position:relative;z-index:1;transform:rotate(-8deg);aspect-ratio:1.586/1;border-radius:14px;background:var(--surface-soft);box-shadow:0 20px 44px rgba(0,0,0,.22);overflow:hidden}'
 '.nhc-plate img{width:100%;height:100%;object-fit:cover;display:block}'
 '.nhc-plate .pn{position:absolute;left:18px;bottom:16px;font-weight:700;font-size:20px;line-height:1.05;max-width:80%}'
 '.nhc-plate .pi{position:absolute;left:18px;top:16px;font-family:var(--font-mono,monospace);font-size:10px;text-transform:uppercase;opacity:.6}'
 '.nhc-plate .pf{position:absolute;right:-5%;bottom:-10%;width:48%;height:48%;opacity:.16;color:#000}'
 '.nhc-dots{display:flex;justify-content:center;gap:8px;margin-top:16px}'
 '.nhc-dots span{width:8px;height:8px;border-radius:50px;background:rgba(0,0,0,.22);cursor:pointer;transition:all .3s}.nhc-dots span.on{width:22px;background:#000}'
 '@media(max-width:760px){.nhc-slide{padding:22px 20px;min-height:0;gap:14px;flex-direction:column;align-items:stretch}.nhc-h{font-size:28px;letter-spacing:-1px}.nhc-h2{font-size:24px}.nhc-amt{font-size:21px}.nhc-p{font-size:13px;max-width:none}.nhc-ill{width:100%}.nhc-cmp{padding:13px 14px}.nhc-cmp-row .nm{width:48px;font-size:10px}.nhc-s2{flex-direction:row;align-items:center}.nhc-s2 .nhc-txt{max-width:62%}.nhc-plate{position:absolute;right:-22px;bottom:18px;width:150px;transform:rotate(-10deg)}.nhc-face{width:84px;height:84px}.nhc-face-b{width:96px;height:96px}}'
 # --- B · 이번달 최고 커플 ---
 '.ncpl-sec{margin-top:54px}'
 '.ncpl-emb{display:flex;align-items:center;gap:9px;margin-bottom:14px}'
 '.ncpl-emb .dh{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center}.ncpl-emb .dh svg{width:26px;height:26px;color:#000}'
 '.ncpl-emb .l{background:var(--block-lilac)}.ncpl-emb .r{background:var(--block-lime)}.ncpl-emb .r svg{transform:scaleX(-1)}'
 '.ncpl-emb .ht{width:18px;height:18px;color:var(--accent-magenta)}'
 '.ncpl-t{font-weight:400;font-size:32px;letter-spacing:-.9px;margin:0}'
 '.ncpl-s{font-weight:400;font-size:14.5px;color:rgba(0,0,0,.62);margin:8px 0 0}.ncpl-s .dim{color:rgba(0,0,0,.45)}'
 '.ncpl-g{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}'
 '.ncpl-row{border:1px solid var(--hairline);border-radius:16px;padding:16px 18px;display:flex;align-items:center;gap:14px}'
 '.ncpl-row .iss{font-weight:700;font-size:15.5px;white-space:nowrap;flex-shrink:0;width:84px}'
 '.ncpl-row .ht{width:18px;height:18px;color:#000;opacity:.82;flex-shrink:0}'
 '.ncpl-row .chips{display:flex;align-items:center;gap:6px;flex-wrap:wrap;flex:1;min-width:0}'
 '.ncpl-chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:50px;background:var(--surface-soft);white-space:nowrap}.ncpl-chip i{width:8px;height:8px;border-radius:50%;flex-shrink:0}.ncpl-chip span{font-weight:540;font-size:13px}'
 '.ncpl-amt{text-align:right;flex-shrink:0}.ncpl-amt .l{font-family:var(--font-mono,monospace);font-size:9px;color:rgba(0,0,0,.42);margin-bottom:2px;text-transform:uppercase;letter-spacing:.3px}'
 '.ncpl-amt .v{font-weight:700;font-size:21px;letter-spacing:-.5px;white-space:nowrap}.ncpl-amt .tie{font-family:var(--font-mono,monospace);font-size:9px;color:var(--accent-magenta);margin-right:5px}'
 '.ncpl-amt .cnt{font-weight:400;font-size:11.5px;color:rgba(0,0,0,.5);margin-top:1px;white-space:nowrap}'
 '@media(max-width:760px){.ncpl-t{font-size:24px}.ncpl-g{grid-template-columns:1fr;gap:0;margin-top:14px}.ncpl-row{border:0;border-top:1px solid var(--hairline-soft);border-radius:0;padding:13px 2px;gap:9px}.ncpl-row .iss{font-size:14px;width:62px}.ncpl-amt .v{font-size:15px}.ncpl-emb .dh{width:32px;height:32px}.ncpl-emb .dh svg{width:20px;height:20px}}'
 '.nbest-sec,.nmos-sec,.ntip-sec{margin-top:54px}'
 '.nbest-h,.ntip-h{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:18px}'
 '.nbest-t,.nmos-t,.ntip-t{font-weight:400;font-size:30px;letter-spacing:-.7px;margin:6px 0 0}'
 '.nbest-s{font-size:14px;color:rgba(0,0,0,.6);margin:8px 0 0}'
 '.nbest-g{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}'
 '.nbest-tile{border:1px solid var(--hairline,#e6e6e6);border-radius:18px;padding:18px;text-decoration:none;color:#000;display:block;transition:border-color .14s}.nbest-tile:hover{border-color:#000}'
 '.nbest-tile .bi{font-size:16px;font-weight:800}'
 '.nbest-tile .bp{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;margin-top:9px;background:var(--surface-soft,#f4f4f5);border-radius:50px;padding:5px 11px}.nbest-tile .bp i{width:7px;height:7px;border-radius:50%}'
 '.nbest-tile .ba{font-size:22px;font-weight:900;margin-top:12px;letter-spacing:-.4px}.nbest-tile .ba .bal{font-size:10.5px;color:#999;font-weight:600}'
 '.nbest-tile .bc{font-size:11.5px;color:#888;margin-top:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.nbest-note{font-size:11.5px;color:#aaa;margin-top:14px}'
 '.nmos-eb{font:800 11px var(--font-mono,monospace);letter-spacing:.05em;text-transform:uppercase;color:#9a9a9a}.nmos-s{font-size:12px;color:#aaa;margin-top:6px}.nmos-h{margin-bottom:16px}'
 '.nmos{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}'
 '.nmt{border-radius:20px;padding:22px;text-decoration:none;color:#000;display:flex;flex-direction:column;justify-content:space-between;min-height:128px}'
 '.nmt .adm{font:800 10.5px var(--font-mono,monospace);letter-spacing:.04em;opacity:.66}.nmt .adh{font-size:18px;font-weight:800;line-height:1.3;margin-top:8px}.nmt .ads{font-size:11.5px;opacity:.62;margin-top:6px}.nmt .adgo{font-size:12px;font-weight:700;margin-top:14px}'
 '.ntip-card{display:flex;gap:22px;align-items:center;border:1px solid var(--hairline,#e6e6e6);border-radius:20px;padding:22px;text-decoration:none;color:#000}'
 '.ntip-thumb{width:170px;aspect-ratio:1.6/1;flex:0 0 auto;border-radius:14px;background:var(--block-lime,#dceeb1);display:flex;align-items:center;justify-content:center}.ntip-thumb svg{width:54px;height:40px;color:#33402a}'
 '.ntip-card .tb{flex:1;min-width:0}.ntip-card .tm{font:700 11.5px var(--font-mono,monospace);color:#9a9a9a}.ntip-card .th{font-size:21px;font-weight:800;letter-spacing:-.4px;margin:8px 0 0;line-height:1.35}.ntip-card .ts{font-size:13.5px;color:#777;margin:8px 0 0;line-height:1.55}.ntip-card .tgo{font-size:13px;font-weight:700;margin-top:14px;display:inline-block}'
 '@media(max-width:760px){.nbest-g{grid-template-columns:1fr 1fr}.nbest-t,.nmos-t,.ntip-t{font-size:23px}.nmos{grid-template-columns:1fr}.ntip-card{flex-direction:column;align-items:stretch}.ntip-thumb{width:100%}}'
 '</style>'
 '<section class="ncpl-sec">'
 '<div class="ncpl-emb"><span class="dh l"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span><svg class="ht" viewBox="0 0 24 24"><use href="#ic-heart-f"/></svg><span class="dh r"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span></div>'
 '<h2 class="ncpl-t">이번달 최고 커플</h2>'
 '<p class="ncpl-s">카드사마다 이번 달 가장 잘 맞는 플랫폼을 찾았어요. <span class="dim">공개 데이터 기준 자동 정렬</span></p>'
 '<div class="ncpl-g" id="cplGrid"></div>'
 '</section>'
 '<section class="nmos-sec"><div class="nmos-h"><div class="nmos-eb">SPONSORED · 상품·이벤트</div><h2 class="nmos-t">이달의 카드·이벤트 모음</h2><div class="nmos-s">외부 광고 링크 · 카드사·플랫폼으로 이동</div></div><div class="nmos">'
   '<a class="nmt" style="background:var(--block-coral,#f6c9c0)" href="cards.html" rel="sponsored nofollow"><div><div class="adm">광고(AD) · 신차 구매자</div><div class="adh">자동차 할부 무이자<br>+ 주유 할인 카드</div><div class="ads">최대 금액 기준, 조건 충족 시</div></div><div class="adgo">자세히 보기 ›</div></a>'
   '<a class="nmt" style="background:var(--block-mint,#c8e6cd)" href="cards.html" rel="sponsored nofollow"><div><div class="adm">광고(AD) · 해외여행</div><div class="adh">수수료 면제 · 라운지 무료</div><div class="ads">이달의 한정 프로모션</div></div><div class="adgo">자세히 보기 ›</div></a>'
   '<a class="nmt" style="background:var(--block-cream,#f4ecd6)" href="cards.html" rel="sponsored nofollow"><div><div class="adm">광고(AD) · 구독</div><div class="adh">OTT·멤버십 12% 적립</div></div><div class="adgo">자세히 보기 ›</div></a>'
   '<a class="nmt" style="background:var(--block-lilac,#c5b0f4)" href="issue.html" rel="sponsored nofollow"><div><div class="adm">광고(AD) · 신규발급</div><div class="adh">첫 결제 즉시 캐시백</div><div class="ads">최대 7만원</div></div><div class="adgo">자세히 보기 ›</div></a>'
 '</div></section>'
 '<section class="ntip-sec"><div class="ntip-h"><div><div class="nhe-eb dim">티라노TIP</div><h2 class="ntip-t">이번 달 발급 전략</h2></div><a class="nmore" href="content.html">전체 콘텐츠 ›</a></div>'
 '<a class="ntip-card" id="tipLatest" href="content.html"><div class="ntip-thumb"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></div><div class="tb"><div class="tm">티라노TIP · 2026.06</div><div class="th">불러오는 중…</div></div></a></section>'
 +FAQ_HTML+'</div>')
INDEX_JS=r"""
var PMETA={cardgorilla:{n:'카드고릴라',c:'#FF6A13'},banksalad:{n:'뱅크샐러드',c:'#19C37D'},toss:{n:'토스',c:'#3182F6'},ajungdang:{n:'아정당',c:'#1B64DA'},naver:{n:'네이버페이',c:'#03C75A'},kakaopay:{n:'카카오페이',c:'#FEE500'}};
function _nk2(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _won(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
Promise.all([
 fetch('cards.json').then(r=>r.json()).catch(function(){return{cards:{}};}),
 fetch('platform_events.json?t='+Date.now()).then(r=>r.json()).catch(function(){return{products:[]};}),
 fetch('hero.json').then(r=>r.json()).catch(function(){return{items:[]};})
]).then(function(A){
 var cj=A[0].cards||{},PE=A[1].products||[],HR=A[2].items||[];
 var NAME2ID={},IMG={};for(var k in cj){(cj[k]||[]).forEach(function(c){var n=_nk2(c.name);if(NAME2ID[n]==null)NAME2ID[n]=c.id;if(c.img&&!IMG[n])IMG[n]=c.img;});}
 function href(name){var id=NAME2ID[_nk2(name||'')];if(id==null)id=NAME2ID[_nk2((name||'').replace(/^토스\s*/,''))];return id!=null?('carddetail.html?id='+id):'chart.html';}
 var EVMAP={};PE.forEach(function(p){var n=_nk2(p.name);EVMAP[n]=(p.events||[]);if(p.img&&!IMG[n])IMG[n]=p.img;});
 function plate(name,img){return imgTag(img||IMG[_nk2(name)]);}
 function hasEv(name){return (EVMAP[_nk2(name)]||[]).some(function(e){return e.reward_won;});}
 var HRf=HR.filter(function(d){return hasEv(d.card);});if(!HRf.length)HRf=HR;   // 발급 이벤트 있는 카드만(집계중 방지)
 var best=null,bw=-1;PE.forEach(function(p){(p.events||[]).forEach(function(e){if((e.reward_won||0)>bw){bw=e.reward_won;best=p;}});});
 // 히어로 슬라이드1 · 6개 플랫폼 캐시백 비교 막대(최고값=검정 하이라이트)
 var platMax={};PE.forEach(function(p){(p.events||[]).forEach(function(e){var w=e.reward_won||0;if(w>(platMax[e.platform]||0))platMax[e.platform]=w;});});
 var cmpRows=Object.keys(PMETA).map(function(k){return{k:k,m:PMETA[k],v:platMax[k]||0};}).sort(function(a,b){return b.v-a.v;});
 var cmpTop=cmpRows.length?cmpRows[0].v:0;var cbb=document.getElementById('heroCmpBars');
 if(cbb){cbb.innerHTML=cmpRows.map(function(r,ri){var w=cmpTop?Math.max(8,Math.round(r.v/cmpTop*100)):8;return '<div class="nhc-cmp-row"><i style="background:'+r.m.c+'"></i><span class="nm">'+r.m.n+'</span><div class="tr"><i style="width:'+w+'%;background:'+(ri===0?'#000':'#cfcfcf')+'"></i></div></div>';}).join('');}
 // 히어로 슬라이드2 · 이번달 최고 캐시백 상품 배너
 if(best){var bMx=0,bPlat='';(best.events||[]).forEach(function(e){if((e.reward_won||0)>bMx){bMx=e.reward_won;bPlat=e.platform;}});var bm=PMETA[bPlat]||{n:bPlat};var _e;
  if(_e=document.getElementById('heroS2Name'))_e.textContent=best.name;
  if(_e=document.getElementById('heroS2Amt'))_e.textContent='최대 '+_won(bMx);
  if(_e=document.getElementById('heroS2Sub'))_e.innerHTML='6개 플랫폼을 비교한 결과, <b>'+bm.n+'에서 받을 때</b> 캐시백이 가장 커요.';
  if(_e=document.getElementById('heroS2'))_e.setAttribute('href',href(best.name));
  if(_e=document.getElementById('heroS2Plate'))_e.innerHTML=plate(best.name,best.img);}
 var im={};PE.forEach(function(p){var k=p.issuer||'';if(!k)return;(p.events||[]).forEach(function(e){if((e.reward_won||0)>(im[k]||0))im[k]=e.reward_won;});});
 var ta=Object.keys(im).map(function(k){return[k,im[k]];}).sort(function(a,b){return b[1]-a[1];}).slice(0,8);
 var lt=document.getElementById('liveTk');if(lt&&ta.length){var s=ta.map(function(r){return r[0].replace('카드','')+' '+_won(r[1]);}).join('     /     ');lt.textContent=s+'     /     '+s;}
 function evRows(name){var evs=(EVMAP[_nk2(name)]||[]).slice().filter(function(e){return e.reward_won;}).sort(function(a,b){return b.reward_won-a.reward_won;}).slice(0,3);
  if(!evs.length)return '<div class="row" style="border:0;opacity:.45"><span class="p">집계 중</span></div>';
  return evs.map(function(e){var m=PMETA[e.platform]||{n:e.platform,c:'#888'};return '<div class="row"><span class="p"><i style="background:'+m.c+'"></i>'+m.n+'</span><span class="v">'+_won(e.reward_won)+'</span></div>';}).join('');}
 // TOP3 = 당월 이벤트 최고금액 상품, 카드사별 1개씩
 var prodMax=PE.map(function(p){var mx=0;(p.events||[]).forEach(function(e){if((e.reward_won||0)>mx)mx=e.reward_won;});return {card:p.name,issuer:p.issuer||'',img:p.img,mx:mx,reward:_won(mx)};})
   .filter(function(x){return x.mx>0;}).sort(function(a,b){return b.mx-a.mx;});
 var seenIss={},top3=[];prodMax.forEach(function(x){if(top3.length>=3)return;var key=x.issuer||x.card;if(seenIss[key])return;seenIss[key]=1;top3.push(x);});
 var pod=document.getElementById('t3pod');
 if(pod){var lifts=['transform:translateY(-22px)','','transform:translateY(-10px)'];
  pod.innerHTML=top3.map(function(d,i){return '<a class="npc" href="'+href(d.card)+'" style="'+(lifts[i]||'')+'"><div class="npc-rk"><b>'+(i+1)+'</b><span>'+(d.reward||'')+'</span></div><div class="npc-plate">'+plate(d.card,d.img)+'</div><div><div class="npc-nm">'+d.card+'</div><div class="npc-bn">'+(d.issuer||'')+'</div></div><div class="npc-ev"><div class="lab">플랫폼 발급 이벤트</div>'+evRows(d.card)+'</div></a>';}).join('');}
 // B · 이번달 최고 커플 (카드사 8종 ❤ 최고 플랫폼) — ① 전체 캐시백 최대 플랫폼, 동점이면 공동 1위
 (function(){var ISS8=['삼성카드','현대카드','KB국민카드','신한카드','롯데카드','우리카드','하나카드','BC카드'];
  function alias(s){s=s||'';if(/국민/.test(s))return 'KB국민카드';if(/^비씨|^bc/i.test(s))return 'BC카드';if(/신한/.test(s))return '신한카드';if(/현대/.test(s))return '현대카드';if(/삼성/.test(s))return '삼성카드';if(/롯데/.test(s))return '롯데카드';if(/우리/.test(s))return '우리카드';if(/하나/.test(s))return '하나카드';return s;}
  var cpl={};PE.forEach(function(p){var iss=alias(p.issuer||'');if(!iss)return;var o=cpl[iss]||(cpl[iss]={});(p.events||[]).forEach(function(e){var w=e.reward_won||0;if(!w)return;var pp=o[e.platform]||(o[e.platform]={tot:0,max:0,prods:{}});pp.tot+=w;if(w>pp.max)pp.max=w;pp.prods[_nk2(p.name)]=1;});});
  var cg=document.getElementById('cplGrid');if(!cg)return;
  var rows=ISS8.map(function(iss){var o=cpl[iss];if(!o)return null;
   var arr=Object.keys(o).map(function(pk){return{pk:pk,tot:o[pk].tot,max:o[pk].max,cnt:Object.keys(o[pk].prods).length};}).sort(function(a,b){return b.tot-a.tot;});
   if(!arr.length)return null;var top=arr[0];var tie=arr.length>1&&arr[1].tot===top.tot&&top.tot>0;
   var m1=PMETA[top.pk]||{n:top.pk,c:'#888'};var chips='<span class="ncpl-chip"><i style="background:'+m1.c+'"></i><span>'+m1.n+'</span></span>';var maxc=top.max,cnt=top.cnt;
   if(tie){var t2=arr[1];var m2=PMETA[t2.pk]||{n:t2.pk,c:'#888'};chips+='<span class="ncpl-chip"><i style="background:'+m2.c+'"></i><span>'+m2.n+'</span></span>';if(t2.max>maxc)maxc=t2.max;cnt+=t2.cnt;}
   return '<a class="ncpl-row" href="issue.html?issuer='+encodeURIComponent(iss)+'"><span class="iss">'+iss+'</span><svg class="ht" viewBox="0 0 24 24"><use href="#ic-heart-f"/></svg><div class="chips">'+chips+'</div><div class="ncpl-amt"><div class="l">최대 캐시백</div><div>'+(tie?'<span class="tie">공동 1위</span>':'')+'<span class="v">'+_won(maxc)+'</span></div><div class="cnt">대상 '+cnt+'개 상품</div></div></a>';
  }).filter(Boolean);
  cg.innerHTML=rows.join('')||'<div style="color:#aaa;font-size:13px;grid-column:1/-1">집계 중</div>';})();
 if(window.repairImages)repairImages();
}).catch(function(){});
// 티라노TIP 최신 전략 콘텐츠 1건
fetch('content.json').then(function(r){return r.json();}).then(function(cd){var its=(cd.items||[]);var t=its.filter(function(x){return /전략|발급/.test(x.cat||'');})[0]||its[0];if(!t)return;var el=document.getElementById('tipLatest');if(!el)return;
 el.setAttribute('href','content.html?id='+encodeURIComponent(t.id));
 el.innerHTML='<div class="ntip-thumb"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></div><div class="tb"><div class="tm">'+(t.cat||'티라노TIP')+' · 2026.06</div><div class="th">'+(t.title||'')+'</div><div class="ts">'+(t.summary||'')+'</div><div class="tgo">전략 보러가기 ›</div></div>';
}).catch(function(){});
// A · 히어로 롤링 캐러셀 (자동 4.2s + 도트 + prefers-reduced-motion 정지)
(function(){var tr=document.getElementById('nhcTrack'),dots=document.getElementById('nhcDots'),wrap=document.getElementById('nhc');if(!tr||!dots)return;
 var i=0,n=dots.children.length,rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches,iv=null;
 function go(k){i=((k%n)+n)%n;tr.style.transform='translateX(-'+(i*50)+'%)';for(var d=0;d<n;d++)dots.children[d].className=(d===i?'on':'');}
 function restart(){if(iv)clearInterval(iv);if(rm)return;iv=setInterval(function(){go(i+1);},4200);}
 for(var d=0;d<n;d++)(function(di){dots.children[di].addEventListener('click',function(){go(di);restart();});})(d);
 go(0);restart();
 if(wrap){wrap.addEventListener('mouseenter',function(){if(iv)clearInterval(iv);});wrap.addEventListener('mouseleave',restart);}
})();
"""

# ===== DISCOUNT =====
DISC_BODY=('<div class="wrap"><section><div class="sec-h"><h2>카드 할인 혜택</h2></div>'
 '<div class="filterbar"><div class="seg" id="seg"><button data-g="전체" class="on">전체</button><button data-g="온라인">온라인</button><button data-g="오프라인">오프라인</button></div>'
 '<select id="tabSel"></select><select id="platSel"></select></div>'
 '<div class="list" id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></section></div>')
DISC_JS=r"""
var DATA=[],cur="전체",curG="전체",curPlat="전체",Q=(new URLSearchParams(location.search).get('q')||'').trim();
function fmt(s){return (s&&s!=="-"&&s!=="없음")?s:"";}
function base(){return DATA.filter(function(d){var ok=(cur==="전체"||d.tab===cur)&&(curG==="전체"||d.gubun===curG);if(ok&&Q){var hay=(d.plat+d.card+d.type+d.disc+d.cond).toLowerCase();ok=hay.indexOf(Q.toLowerCase())>=0;}return ok;});}
function syncSel(){var t=document.getElementById('tabSel');var tabs=[...new Set(DATA.map(d=>d.tab))];t.innerHTML='<option value="전체">카드사 전체</option>'+tabs.map(x=>'<option'+(x===cur?' selected':'')+'>'+x+'</option>').join("");
 var p=document.getElementById('platSel');var ps=[...new Set(base().map(d=>d.plat))].sort((a,b)=>a.localeCompare(b,'ko'));if(!ps.includes(curPlat))curPlat="전체";p.innerHTML='<option value="전체">가맹점 전체 ('+base().length+')</option>'+ps.map(x=>'<option'+(x===curPlat?' selected':'')+'>'+x+'</option>').join("");}
function render(){var L=document.getElementById('list');var items=base().filter(d=>curPlat==="전체"||d.plat===curPlat);if(!items.length){L.innerHTML='<div class="empty">조건에 맞는 혜택이 없어요.</div>';return;}
 L.innerHTML=items.map(function(d){var t=thumbOf(d.plat);var sub=[fmt(d.card),fmt(d.min)?'최소 '+d.min:'',fmt(d.cond),d.period].filter(Boolean).join(' · ');
 return '<a class="item" href="detail.html?id='+d.id+'"><div class="th">'+favico(d.domain,t.e,t.bg)+'</div><div class="body"><div class="l1"><span class="store">'+d.plat+'</span><span class="tag '+(d.gubun==="오프라인"?"off":"")+'">'+d.gubun+'</span></div><div class="l2"><span class="hl">'+d.disc+'</span> '+d.type+'</div><div class="l3">'+sub+'</div></div><div class="chev">›</div></a>';}).join("");}
document.getElementById('seg').onclick=function(e){var b=e.target.closest('button');if(!b)return;curG=b.dataset.g;curPlat="전체";document.querySelectorAll('#seg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');syncSel();render();};
document.getElementById('tabSel').onchange=function(){cur=this.value;curPlat="전체";syncSel();render();};
document.getElementById('platSel').onchange=function(){curPlat=this.value;render();};
fetch('data.json').then(r=>r.json()).then(function(j){DATA=j.items;if(Q){var s=document.getElementById('siteSearch');if(s)s.value=Q;}syncSel();render();});
"""

# ===== CARDS =====
CARDS_BODY=('<style>'
 '.cf-hero{background:var(--block-cream);border-radius:24px;padding:44px 40px;margin:24px 0 0}'
 '.cf-eb{font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:rgba(0,0,0,.55)}'
 '.cf-h{font-weight:340;font-size:46px;letter-spacing:-1.4px;margin:12px 0 0}'
 '.cf-sub{font-weight:400;font-size:16px;color:rgba(0,0,0,.66);margin:12px 0 0}'
 '.cf-filt{margin-top:26px;display:flex;flex-direction:column;gap:13px}'
 '.cf-frow{display:flex;align-items:flex-start;gap:14px}'
 '.cf-fl{font-size:11.5px;font-weight:700;color:rgba(0,0,0,.5);text-transform:uppercase;letter-spacing:.4px;flex:0 0 78px;padding-top:9px}'
 '.cf-chips{display:flex;flex-wrap:wrap;gap:7px;flex:1}'
 '.cf-chips button{font-weight:500;font-size:13.5px;padding:9px 15px;border-radius:50px;border:1px solid var(--hairline);background:var(--surface-soft);color:#000;cursor:pointer;white-space:nowrap}'
 '.cf-chips button.on{background:#000;color:#fff;border-color:#000}'
 '.cf-feew{display:flex;align-items:center;gap:12px;flex:1;padding-top:5px}'
 '.cf-feew input{flex:1;max-width:300px;accent-color:#000}.cf-feel{font-weight:700;font-size:13px;min-width:64px}'
 '.cf-bar{display:flex;align-items:center;justify-content:space-between;margin:26px 0 16px;gap:12px;flex-wrap:wrap}'
 '.cf-cnt{font-weight:500;font-size:14px;color:rgba(0,0,0,.7)}'
 '.cf-sort{display:inline-flex;gap:3px;background:var(--surface-soft);border-radius:50px;padding:3px}'
 '.cf-sort button{border:0;background:transparent;padding:8px 15px;border-radius:50px;font-weight:500;font-size:13px;cursor:pointer;color:#000}'
 '.cf-sort button.on{background:#000;color:#fff}'
 '.cf-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}'
 '.cf-card{border:1px solid var(--hairline);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:13px;text-decoration:none;color:#000;position:relative;background:#fff;transition:border-color .15s}'
 '.cf-card:hover{border-color:#000}'
 '.cf-info{display:flex;flex-direction:column;gap:11px;flex:1;min-width:0}'
 '.cf-sortbtn{display:none;align-items:center;gap:6px;border:1px solid var(--hairline);background:var(--surface-soft);color:#000;font-weight:500;font-size:13.5px;padding:9px 15px;border-radius:50px;cursor:pointer}'
 '.cf-scrim{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:60}.cf-scrim.open{display:block}'
 '.cf-sheet{position:fixed;left:0;right:0;bottom:0;background:#fff;border-radius:20px 20px 0 0;padding:6px 16px calc(18px + env(safe-area-inset-bottom));z-index:61;transform:translateY(110%);transition:transform .25s}.cf-sheet.open{transform:none}'
 '.cf-sheet-h{font-weight:700;font-size:12px;color:rgba(0,0,0,.5);padding:14px 4px 6px;text-align:center;letter-spacing:.4px}'
 '.cf-sheet button{display:block;width:100%;text-align:left;border:0;background:transparent;padding:15px 6px;font-size:16px;font-weight:500;border-top:1px solid var(--hairline-soft);cursor:pointer;color:#000}.cf-sheet button.on{font-weight:800}'
 '.cf-fav{position:absolute;right:13px;top:13px;width:34px;height:34px;border-radius:50px;background:rgba(255,255,255,.88);display:flex;align-items:center;justify-content:center;color:var(--dim);z-index:2;cursor:pointer}'
 '.cf-fav.on{color:var(--accent-magenta)}.cf-fav svg{width:19px;height:19px}'
 '.cf-plate{width:100%;aspect-ratio:1.586/1;border-radius:10px;overflow:hidden;border:1px solid var(--hairline-soft)}.cf-plate img{width:100%;height:100%;object-fit:cover;display:block}'
 '.cf-nm{font-weight:700;font-size:17.5px;letter-spacing:-.3px;padding-right:30px}'
 '.cf-iss{font-size:12px;color:rgba(0,0,0,.5);margin-top:-4px}'
 '.cf-ev{align-self:flex-start;font-size:11px;font-weight:700;padding:3px 10px;border-radius:50px;background:var(--block-lime);color:#000}'
 '.cf-perks{display:flex;flex-direction:column;gap:6px}'
 '.cf-perk{display:flex;align-items:flex-start;gap:7px;font-size:13px;font-weight:400;line-height:1.35;color:rgba(0,0,0,.82)}'
 '.cf-perk svg{width:15px;height:15px;color:var(--success);flex:0 0 auto;margin-top:2px}'
 '.cf-foot{display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:11px;border-top:1px solid var(--hairline-soft)}'
 '.cf-fee2{font-size:12.5px;color:rgba(0,0,0,.6)}'
 '.cf-go{font-weight:540;font-size:13px;padding:9px 16px;border-radius:50px;background:#000;color:#fff}'
 '.cf-empty{text-align:center;padding:64px 0;color:rgba(0,0,0,.5)}.cf-empty svg{width:46px;height:46px;opacity:.25}'
 '@media(max-width:900px){.cf-grid{grid-template-columns:1fr 1fr}}'
 '@media(max-width:600px){.cf-hero{padding:30px 20px}.cf-h{font-size:29px}.cf-grid{grid-template-columns:1fr}.cf-frow{flex-direction:column;gap:6px}.cf-fl{flex-basis:auto;padding-top:0}.cf-chips{flex-wrap:wrap}.cf-chips button{font-size:13px;padding:8px 13px}'
   '.cf-card{flex-direction:row;align-items:stretch;gap:13px;padding:13px}'
   '.cf-plate{width:104px;flex:0 0 104px;align-self:flex-start}'
   '.cf-nm{padding-right:0;font-size:15.5px}.cf-fav{right:11px;top:11px;width:30px;height:30px}.cf-fav svg{width:17px;height:17px}'
   '.cf-perks .cf-perk:nth-child(n+2){display:none}'
   '.cf-feew input{max-width:none}.cf-bar{align-items:center}.cf-sort{display:none}.cf-sortbtn{display:inline-flex}}'
 '</style>'
 '<div class="wrap">'
 '<div class="cf-hero"><div class="cf-eb">FIND A CARD</div><h1 class="cf-h">혜택부터 골라보세요.</h1>'
 '<p class="cf-sub">혜택과 업종을 고르면 리워드 순으로 카드를 정렬해드려요.</p></div>'
 '<div class="cf-filt">'
   '<div class="cf-frow"><span class="cf-fl">혜택</span><div class="cf-chips" id="cfBtype"></div></div>'
   '<div class="cf-frow"><span class="cf-fl">업종</span><div class="cf-chips" id="cfCat"></div></div>'
   '<div class="cf-frow"><span class="cf-fl">카드사</span><div class="cf-chips" id="cfIss"></div></div>'
   '<div class="cf-frow"><span class="cf-fl">이번달 이벤트</span><div class="cf-chips" id="cfEv"></div></div>'
   '<div class="cf-frow"><span class="cf-fl">연회비</span><div class="cf-feew"><input type="range" id="cfFee" min="0" max="100000" step="5000" value="100000"><span class="cf-feel" id="cfFeeL">무제한</span></div></div>'
 '</div>'
 '<div class="cf-bar"><div class="cf-cnt" id="cfCnt"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div>'
   '<div class="cf-sort" id="cfSort"><button data-s="reward" class="on">리워드순</button><button data-s="pop">인기순</button><button data-s="fee">연회비순</button></div>'
   '<button class="cf-sortbtn" id="cfSortBtn">리워드순 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 9l6 6 6-6"/></svg></button></div>'
 '<div class="cf-scrim" id="cfScrim"></div>'
 '<div class="cf-sheet" id="cfSheet"><div class="cf-sheet-h">정렬</div><button data-s="reward" class="on">리워드순</button><button data-s="pop">인기순</button><button data-s="fee">연회비순</button></div>'
 '<div class="cf-grid" id="list"></div>'
 '<div class="cf-empty" id="cfEmpty" style="display:none"><svg><use href="#ic-grid"/></svg><div style="margin-top:10px">조건에 맞는 카드가 없어요.</div></div>'
 '</div>')
CARDS_JS=r"""
var ALL=[],EVN={},EVMX={},PEIMG={},st={btype:'전체',cat:'전체',iss:'전체',ev:'전체',fee:100000,sort:'reward'};
function _nkc(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _feeNum(s){s=(''+s);var m=s.match(/([0-9.]+)\s*만/);if(m)return Math.round(parseFloat(m[1])*10000);m=s.replace(/[, ]/g,'').match(/([0-9]{4,})/);return m?parseInt(m[1]):0;}
function _wm(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
var CHK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.2 4.2L19 6.8"/></svg>';
var BTYPES=['전체','할인','적립'];
var CATS=['전체','식음료','쇼핑','주유','통신','여행','마트','카페','문화','구독','자동차','병원'];
var CATKW={'식음료':['외식','식당','음식','배달','맛집','다이닝'],'쇼핑':['쇼핑','백화점','온라인','아울렛','쿠팡','11번가'],'주유':['주유','충전','lpg','전기차','정유'],'통신':['통신','휴대폰','요금'],'여행':['여행','항공','해외','면세','라운지','마일','트래블','호텔'],'마트':['마트','편의점','대형마트','이마트','홈플러스'],'카페':['카페','커피','스타벅스','투썸'],'문화':['영화','문화','도서','ott','스트리밍','공연'],'구독':['구독','멤버십','스트리밍','넷플','유튜브'],'자동차':['자동차','차량','하이패스','정비','렌터카'],'병원':['병원','의료','약국','헬스','피트니스']};
function btypeOf(b,hasEv){var r=[];if(/적립|캐시백|포인트|마일/.test(b))r.push('적립');if(/할인/.test(b))r.push('할인');if(!r.length)r.push('할인');return r;}
function catsOf(b){var lb=(b||'').toLowerCase(),r=[];for(var c in CATKW){if(CATKW[c].some(function(k){return lb.indexOf(k)>=0;}))r.push(c);}return r;}
function perksOf(b){var a=(b||'').split(/[·,\/・\n]+/).map(function(x){return x.trim();}).filter(Boolean);return a.length?a.slice(0,3):[b];}
function chips(id,arr,key){var el=document.getElementById(id);if(!el)return;el.innerHTML=arr.map(function(x){return '<button data-v="'+x+'"'+(st[key]===x?' class="on"':'')+'>'+x+'</button>';}).join('');
 el.querySelectorAll('button').forEach(function(b){b.onclick=function(){st[key]=b.dataset.v;el.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');render();};});}
function pass(c){
 if(st.btype!=='전체'&&c.btype.indexOf(st.btype)<0)return false;
 if(st.cat!=='전체'&&c.cats.indexOf(st.cat)<0)return false;
 if(st.iss!=='전체'&&c.issuer!==st.iss)return false;
 if(st.ev==='있음'&&!c.ev)return false; if(st.ev==='없음'&&c.ev)return false;
 if(st.fee<100000&&c.feeN>st.fee)return false;
 return true;}
function render(){
 var rows=ALL.filter(pass);
 rows.sort(function(a,b){if(st.sort==='fee')return a.feeN-b.feeN;if(st.sort==='pop')return b.pop-a.pop;return (b.reward-a.reward)||(b.ev-a.ev);});
 document.getElementById('cfCnt').textContent=rows.length+'개 카드'+(st.iss!=='전체'?' · '+st.iss:'')+(st.cat!=='전체'?' · '+st.cat:'')+(st.btype!=='전체'?' · '+st.btype:'');
 document.getElementById('cfEmpty').style.display=rows.length?'none':'block';
 document.getElementById('list').innerHTML=rows.map(function(c){
  var fav='<span class="cf-fav'+(isFav(c.id)?' on':'')+'" onclick="event.preventDefault();event.stopPropagation();favClick(this,'+c.id+')">'+favSvg(isFav(c.id))+'</span>';
  var perks=c.perks.map(function(p){return '<div class="cf-perk">'+CHK+'<span>'+p+'</span></div>';}).join('');
  var ev=c.ev?'<span class="cf-ev">발급 이벤트'+(c.ev>1?' '+c.ev+'곳':'')+'</span>':'';
  return '<a class="cf-card" href="carddetail.html?id='+c.id+'">'+fav+'<div class="cf-plate">'+imgTag(c.img)+'</div><div class="cf-info"><div class="cf-nm">'+c.name+'</div><div class="cf-iss">'+c.issuer+'</div>'+ev+'<div class="cf-perks">'+perks+'</div><div class="cf-foot"><span class="cf-fee2">'+(c.fee?'연회비 '+c.fee:'연회비 정보 없음')+'</span><span class="cf-go">자세히</span></div></div></a>';
 }).join('');
 if(window.repairImages)repairImages();
}
Promise.all([fetch('cards.json').then(function(r){return r.json();}),fetch('platform_events.json?t='+Date.now()).then(function(r){return r.json();}).catch(function(){return{products:[]};})]).then(function(A){
 var cj=A[0].cards||{},ord=A[0].order||[];
 (A[1].products||[]).forEach(function(p){var n=_nkc(p.name);var evs=(p.events||[]).filter(function(e){return e.reward_won;});EVN[n]=new Set(evs.map(function(e){return e.platform;})).size;var mx=0;evs.forEach(function(e){if(e.reward_won>mx)mx=e.reward_won;});EVMX[n]=mx;if(p.img)PEIMG[n]=p.img;});
 ord.forEach(function(iss){(cj[iss]||[]).forEach(function(c,i){var n=_nkc(c.name);var ev=EVN[n]||0;var rk=(c.rank&&c.rank!=='None')?parseInt(c.rank):9999;
   ALL.push({id:c.id,name:c.name,issuer:iss,img:c.img||PEIMG[n],benefit:c.benefit||'',fee:c.fee||'',feeN:_feeNum(c.fee),reward:Math.round((EVMX[n]||0)/10000),pop:-(isNaN(rk)?9999:rk)-i*0.001,ev:ev,btype:btypeOf(c.benefit||'',ev>0),cats:catsOf(c.benefit||''),perks:perksOf(c.benefit||'')});});});
 var availCats=['전체'].concat(CATS.slice(1).filter(function(c){return ALL.some(function(x){return x.cats.indexOf(c)>=0;});}));   // 대상 상품 있는 업종만
 var availIss=['전체'].concat(ord.filter(function(o){return ALL.some(function(x){return x.issuer===o;});}));
 chips('cfBtype',BTYPES,'btype');chips('cfCat',availCats,'cat');chips('cfIss',availIss,'iss');chips('cfEv',['전체','있음','없음'],'ev');
 var fr=document.getElementById('cfFee'),fl=document.getElementById('cfFeeL');
 fr.oninput=function(){st.fee=parseInt(fr.value);fl.textContent=(st.fee>=100000?'무제한':_wm(st.fee)+' 이하');render();};
 var SLABEL={reward:'리워드순',pop:'인기순',fee:'연회비순'};
 function setSort(v){st.sort=v;document.querySelectorAll('#cfSort button,#cfSheet button').forEach(function(x){x.classList.toggle('on',x.dataset.s===v);});var sb=document.getElementById('cfSortBtn');if(sb)sb.firstChild.textContent=SLABEL[v]+' ';render();}
 document.getElementById('cfSort').querySelectorAll('button').forEach(function(b){b.onclick=function(){setSort(b.dataset.s);};});
 var sheet=document.getElementById('cfSheet'),scrim=document.getElementById('cfScrim');
 function closeSheet(){sheet.classList.remove('open');scrim.classList.remove('open');}
 document.getElementById('cfSortBtn').onclick=function(){sheet.classList.add('open');scrim.classList.add('open');};
 scrim.onclick=closeSheet;
 sheet.querySelectorAll('button').forEach(function(b){b.onclick=function(){setSort(b.dataset.s);closeSheet();};});
 render();
}).catch(function(){document.getElementById('cfCnt').textContent='데이터를 불러오지 못했어요.';});
"""

# ===== ISSUE =====
ISSUE_BODY=('<style>'
 '.subnav2{display:flex;gap:8px;margin:2px 0 12px}'
 '.subnav2 button{flex:1;padding:11px 8px;border-radius:11px;border:1px solid var(--line);background:var(--surface);color:var(--sub);font-weight:800;font-size:13px;cursor:pointer}'
 '.subnav2 button.on{background:var(--accent);color:#fff;border-color:var(--accent)}'
 '.cmpctl{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:11px 13px;margin-bottom:13px}'
 '.ctlrow{display:flex;flex-wrap:wrap;align-items:center;gap:7px}.ctlrow+.ctlrow{margin-top:9px;padding-top:9px;border-top:1px solid var(--line)}'
 '.ctll{font-size:11.5px;font-weight:800;color:var(--sub);margin-right:3px;flex:0 0 auto}'
 '.ctlb,.ctlf{padding:6px 11px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--sub);font-size:12px;font-weight:800;cursor:pointer}'
 '.ctlb.on{background:var(--accent);color:#fff;border-color:var(--accent)}.ctlf.on{background:#2f6bff;color:#fff;border-color:#2f6bff}'
 '.prodcnt{margin-left:auto;font-size:11.5px;font-weight:700;color:var(--dim)}'
 '.noevline{font-size:11.5px;color:var(--dim);padding:9px 0 2px;border-top:1px solid var(--line);margin-top:8px}.noevline b{color:var(--sub);font-weight:700}'
 '.cmpnote{font-size:12px;color:var(--sub);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 13px;margin-bottom:14px;line-height:1.5}'
 '.cmpcard{border:1px solid var(--line);border-radius:14px;padding:13px 15px;margin-bottom:12px;background:var(--surface)}'
 '.cmpcard .ch{font-size:15px;font-weight:800;letter-spacing:-.01em}'
 '.cmpcard .csub{font-size:11.5px;color:var(--sub);margin-top:2px}'
 '.cmphd{display:flex;align-items:baseline;justify-content:space-between;gap:10px}'
 '.chmax{font-size:15px;font-weight:900;color:#f5b301;white-space:nowrap}.chmax small{font-size:11px;color:var(--sub);font-weight:600;margin-left:2px}'
 '.cmpcard.prodc{padding:0;overflow:hidden}'
 '.prodc .phead{display:flex;gap:13px;align-items:center;padding:14px 15px;background:linear-gradient(180deg,rgba(255,255,255,.03),transparent)}'
 '.prodc .cplate{width:96px;height:60px;flex:0 0 auto;border-radius:8px;overflow:hidden;background:#eef0f3;box-shadow:0 4px 12px rgba(0,0,0,.12)}'
 '.prodc .cplate img{width:100%;height:100%;object-fit:cover}'
 '.prodc .cinfo{min-width:0}.prodc .cinfo .ch{font-size:15.5px;font-weight:800;line-height:1.25}'
 '.prodc .cinfo .chmax{font-size:21px;margin-top:5px;display:block}'
 '.csave{margin:0 15px 4px;padding:9px 12px;border-radius:9px;background:rgba(25,195,125,.12);border:1px solid rgba(25,195,125,.32);color:#34e29b;font-size:12.5px;font-weight:800}'
 '.csave b{color:#5cf0b6;font-size:13.5px}'
 '.bd{font-size:11px;color:var(--dim);padding:0 0 8px 0;margin-top:-4px;line-height:1.4}.bd b{color:var(--sub)}.bd .bdt{color:#7a7a82;margin-left:5px}'
 '.prodc .prows{padding:2px 15px 14px}'
 '.prow{display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid var(--line);margin-top:8px}'
 '.prank{flex:0 0 auto;width:20px;height:20px;border-radius:50%;font-size:11px;font-weight:900;display:flex;align-items:center;justify-content:center;background:#edeef2;color:#7c7c86}'
 '.prank.r1{background:#ffcf33;color:#6f4e00}.prank.r2{background:#cfd3da;color:#474a52}.prank.r3{background:#eab277;color:#6e3f12}'
 '.prow.lk{cursor:pointer;text-decoration:none;color:inherit;border-radius:8px;padding-left:8px;padding-right:8px;margin-left:-8px;margin-right:-8px;transition:.12s}'
 '.prow.lk:hover{background:rgba(255,255,255,.05)}'
 '.prow .go{margin-left:auto;color:var(--dim);font-weight:900;font-size:15px;flex:0 0 auto}'
 '.prow.lk:hover .go{color:var(--accent)}'
 '.prow.f{border-top:0;margin-top:10px}'
 '.prow .pf{font-size:11px;font-weight:800;color:#fff;padding:5px 9px;border-radius:7px;flex:0 0 auto;min-width:74px;text-align:center}'
 '.prow .pv{flex:0 0 auto;margin-left:auto;font-size:14px;font-weight:800;color:var(--text);white-space:nowrap;text-align:right;min-width:96px}'
 '.prow .pv.none{color:var(--dim);font-weight:600;font-size:13px}'
 '.prow.best .pv{color:var(--accent)}'
 '.pick{font-size:10px;font-weight:900;color:#fff;background:var(--accent);padding:4px 8px;border-radius:7px;flex:0 0 auto;white-space:nowrap}'
 '.pcmp-hero{background:#c5b0f4;border-radius:24px;padding:40px 34px;margin:4px 0 16px;position:relative;overflow:hidden}'
 '.pcmp-hero .eb{font:800 11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.5px;color:rgba(0,0,0,.55)}'
 '.pcmp-hero h1{font-size:46px;font-weight:340;line-height:1.05;letter-spacing:-1.4px;margin:13px 0 0;color:#0c0b14}'
 '.pcmp-hero p{font-size:16px;color:rgba(0,0,0,.62);margin:13px 0 0;max-width:520px;font-weight:500;line-height:1.45}'
 '.pcmp-spread{background:#1f1d3d;color:#fff;border-radius:22px;padding:28px 30px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between;gap:20px;overflow:hidden}'
 '.pcmp-spread .sl{font:800 11px ui-monospace,Menlo,monospace;opacity:.72;letter-spacing:.4px}'
 '.pcmp-spread .st{font-size:30px;font-weight:800;letter-spacing:-.6px;margin-top:9px;line-height:1.16}'
 '.pcmp-spread .ss{font-size:14px;opacity:.76;margin-top:9px}'
 '.pcmp-spread .splate{width:168px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:11px;overflow:hidden;transform:rotate(-7deg);box-shadow:0 16px 36px rgba(0,0,0,.34);background:#c5b0f4;transition:.2s}'
 '.pcmp-spread:hover .splate{transform:rotate(-3deg) scale(1.03)}'
 '.pcmp-spread .splate img{width:100%;height:100%;object-fit:cover}'
 '.pbasis{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:4px 0 12px}'
 '.pbasis .bl{font-size:11.5px;color:var(--sub);font-weight:700}.pbasis .bt{font-size:16px;font-weight:800;margin-top:3px;letter-spacing:-.2px}'
 '.pchips{display:flex;gap:5px;background:var(--surface2);border-radius:50px;padding:5px;flex-wrap:wrap}'
 '.pchips button{border:0;background:transparent;font-size:12.5px;font-weight:700;color:var(--sub);padding:8px 14px;border-radius:50px;cursor:pointer;transition:.12s}'
 '.pchips button.on{background:#fff;color:var(--text);box-shadow:0 1px 3px rgba(0,0,0,.13)}'
 '.ptbl{border:1px solid var(--line);border-radius:20px;overflow:hidden}'
 '.ptr{display:grid;grid-template-columns:1.6fr repeat(6,1fr);align-items:center;border-top:1px solid var(--line);text-decoration:none;color:var(--text);transition:.12s}'
 '.ptbl .ptr:first-child{border-top:0}'
 '.ptr.hd{background:var(--surface2);font:800 11px ui-monospace,Menlo,monospace;letter-spacing:.3px;color:var(--dim)}'
 '.ptr.hd>div{padding:14px 8px;text-align:center}.ptr.hd>div:first-child{text-align:left;padding-left:18px}'
 '.ptr:hover{background:var(--surface2)}'
 '.ptr a.pc,.ptr a.cell{text-decoration:none;color:inherit}'
 '.ptr a.cell:hover .chip{outline:2px solid var(--accent,#000);outline-offset:1px}'
 '.ptr .chip .hrt{color:inherit}'
 '.ptr .pc{padding:12px 16px;display:flex;align-items:center;gap:12px;min-width:0}'
 '.ptr .pcimg{width:60px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:7px;overflow:hidden;background:#eef0f3;transition:.16s}'
 '.ptr:hover .pcimg{transform:scale(1.07)}'
 '.ptr .pcimg img{width:100%;height:100%;object-fit:cover}'
 '.ptr .pc>div{min-width:0;overflow:hidden}'
 '.ptr .pcn{font-size:15px;font-weight:800;letter-spacing:-.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.ptr .pci{font:10px ui-monospace,Menlo,monospace;color:var(--dim);margin-top:3px}'
 '.ptr .issmk{width:46px;height:34px;flex:0 0 auto;border-radius:7px;background:var(--surface-soft,#f4f4f5);display:flex;align-items:center;justify-content:center}.ptr .issmk svg{width:22px;height:16px;color:#1f1d3d}'
 '.ptr .cell{padding:12px 5px;text-align:center}'
 '.ptr .chip{display:inline-block;min-width:50px;padding:7px 8px;border-radius:50px;font-size:13px;font-weight:700;background:var(--surface2);color:var(--sub)}'
 '.ptr .chip.mx{background:#000;color:#fff;font-weight:800}.ptr .chip.no{background:transparent;color:var(--dim);font-weight:600}'
 '.pcmpnote{font-size:12px;color:var(--sub);margin-top:13px;display:flex;align-items:center;gap:8px;line-height:1.5}.pcmpnote .dot{width:13px;height:13px;border-radius:50%;background:#000;flex:0 0 auto}'
 '.tybox{margin:12px 0 2px;background:#f3f0fb;border:1px solid #e4dcf6;border-radius:13px;padding:13px 15px}'
 '.tyhd{font-size:12.5px;font-weight:900;color:#5b3fb0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}'
 '.tyai{font-size:10px;font-weight:800;color:#6f5bb0;background:#ece5fb;border-radius:999px;padding:3px 8px;letter-spacing:.2px}'
 '.tytxt{font-size:13px;color:var(--text);line-height:1.65;margin-top:8px}.tytxt b{color:#5b3fb0;font-weight:800}'
 '.pcardlist{display:none}'
 '.pcardm{display:block;border:1px solid var(--line);border-radius:16px;padding:13px 14px;margin-bottom:11px;text-decoration:none;color:inherit;background:var(--surface)}'
 '.pcardm-top{display:flex;align-items:center;gap:12px}'
 '.pcardm .pcimg{width:66px;aspect-ratio:1.586/1;flex:0 0 auto;border-radius:8px;overflow:hidden;background:#eceef2}'
 '.pcardm .pcimg img{width:100%;height:100%;object-fit:cover}'
 '.pcardm-info{flex:1;min-width:0}.pcardm .pcn{font-size:14.5px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pcardm .pci{font-size:11px;color:var(--dim);margin-top:2px}'
 '.pcardm-best{text-align:right;flex:0 0 auto}.pcardm-best .bl{font-size:9px;color:var(--dim)}.pcardm-best .bv{font-size:15px;font-weight:900;white-space:nowrap}'
 '.pcardm-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}'
 '.pcardm .pmc{flex:1;min-width:56px;text-align:center;background:var(--surface2);border-radius:10px;padding:7px 6px}'
 '.pcardm .pmc.mx{background:#000000;color:#fff}.pcardm .pmc-n{font-size:9.5px;opacity:.7}.pcardm .pmc-v{font-size:13px;font-weight:800;margin-top:2px}'
 '@media(max-width:680px){.pcmp-hero{padding:28px 22px}.pcmp-hero h1{font-size:29px}.pcmp-spread{flex-direction:column;align-items:flex-start}.pcmp-spread .splate{width:128px;align-self:flex-end;margin-top:-30px}.pbasis{flex-direction:column;align-items:stretch;gap:8px}.pchips{flex-wrap:wrap}.ptblwrap{display:none}.pcardlist{display:block}}'
 # 이번달 캐시백 = 가로 플레이트 카드 3열 그리드(시안: 발급 이벤트.dc.html repeat(3,1fr))
 '#view-ev #list{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:6px}'
 '#view-ev #list .empty{grid-column:1/-1}'
 '.evc{display:flex;flex-direction:column;gap:11px;border:1px solid var(--line);border-radius:18px;padding:14px;text-decoration:none;color:inherit;background:var(--surface);transition:border-color var(--dur-fast,.15s) var(--ease,ease),transform var(--dur-fast,.15s) var(--ease,ease)}'
 '.evc:hover{border-color:#000;transform:translateY(-2px)}'
 '.evc .evc-plate{width:100%;aspect-ratio:1.586/1;border-radius:11px;overflow:hidden;background:var(--surface-soft,#f4f4f5);border:1px solid var(--hairline-soft,#eee)}'
 '.evc .evc-plate img{width:100%;height:100%;object-fit:cover;display:block}'
 '.evc .evc-pf{align-self:flex-start;font-size:10.5px;font-weight:800;color:#fff;background:#000;border-radius:999px;padding:3px 9px;letter-spacing:.2px}'
 '.evc .evc-nm{font-size:15px;font-weight:800;letter-spacing:-.2px;line-height:1.32;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}'
 '.evc .evc-iss{font-size:11.5px;color:var(--dim);margin-top:3px}'
 '.evc .evc-foot{display:flex;align-items:flex-end;justify-content:space-between;gap:8px;margin-top:auto;padding-top:4px}'
 '.evc .evc-amtl{font-size:9.5px;color:var(--dim);font-weight:600}'
 '.evc .evc-amt{font-size:16px;font-weight:900;color:var(--accent-magenta,#ff3d8b);letter-spacing:-.3px}'
 '.evc .evc-go{font-size:12px;font-weight:700;color:var(--sub);white-space:nowrap}'
 '@media(max-width:820px){#view-ev #list{grid-template-columns:1fr 1fr;gap:12px}}'
 '@media(max-width:520px){#view-ev #list{grid-template-columns:1fr}}'
 # 캐시백 전체/주요/부가 토글·범례·셀 분해 캡션·인라인 넛지(NEW-6)
 '.cashtogwrap{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin:14px 0 4px}'
 '.cashtog{display:inline-flex;align-items:center;gap:2px;background:var(--surface2,#f7f7f5);border-radius:50px;padding:4px}'
 '.cashtog .ctgl{font-size:11px;font-weight:700;color:var(--dim);padding:0 8px 0 6px}'
 '.cashtog button{border:0;background:transparent;font-size:13px;font-weight:700;color:var(--sub);padding:7px 15px;border-radius:50px;cursor:pointer}'
 '.cashtog button.on{background:#000;color:#fff}'
 '.cmplegend{display:flex;flex-wrap:wrap;gap:13px;font-size:11.5px;color:var(--sub)}'
 '.cmplegend span{display:inline-flex;align-items:center;gap:5px}'
 '.cmplegend i{width:9px;height:9px;border-radius:2px;display:inline-block}'
 '.cmplegend .lg-t{background:#000}.cmplegend .lg-m{background:var(--block-navy,#1f1d3d)}.cmplegend .lg-b{background:#b9b2e6}'
 '.ptr .cell .cap{font:9.5px ui-monospace,Menlo,monospace;color:var(--dim);margin-top:3px;white-space:nowrap}'
 '.cmpnudge{display:flex;align-items:center;gap:11px;background:var(--block-cream,#f4ecd6);border-radius:13px;padding:11px 14px;margin:2px 0 9px}'
 '.cmpnudge .nb{flex:0 0 auto;width:26px;height:26px;border-radius:50%;background:#000;color:#fff;display:flex;align-items:center;justify-content:center}'
 '.cmpnudge .nb svg{width:14px;height:14px}'
 '.cmpnudge .nt{font-size:12.5px;line-height:1.5;color:#000;flex:1}.cmpnudge .nt b{font-weight:800}'
 '.cmpnudge .nx{flex:0 0 auto;font-size:10.5px;font-weight:700;background:#000;color:#fff;border-radius:50px;padding:5px 10px;white-space:nowrap}'
 '@media(max-width:680px){.cmpnudge{align-items:flex-start}.cmpnudge .nx{display:none}}'
 # 플랫폼 비교 — 커플 엠블럼·표시 플랫폼 토글·전략/AD 배너
 '.pcmp-emb{display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--block-lilac);border-radius:14px;padding:13px 16px;margin:2px 0 12px}'
 '.pcmp-emb .t{font-weight:700;font-size:15px;letter-spacing:-.3px}.pcmp-emb .s{font-size:11.5px;color:rgba(0,0,0,.6);margin-top:2px}'
 '.pcmp-emb .emb{display:inline-flex;align-items:center;gap:3px;flex-shrink:0}.pcmp-emb .dh{width:30px;height:30px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}.pcmp-emb .dh svg{width:18px;height:14px;color:#000}.pcmp-emb .dh.r{background:var(--block-lime)}.pcmp-emb .dh.r svg{transform:scaleX(-1)}.pcmp-emb .ht{width:14px;height:14px;color:var(--accent-magenta)}'
 '.ptogwrap{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--surface-soft);border-radius:14px;padding:11px 14px;margin-bottom:12px}'
 '.ptogl{font:700 11px ui-monospace,Menlo,monospace;color:var(--dim);margin-right:2px}'
 '.ptog{display:flex;gap:6px;flex-wrap:wrap}'
 '.ptogb{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:50px;border:1px solid var(--hairline);background:#fff;color:rgba(0,0,0,.7);font-weight:540;font-size:12px;cursor:pointer}'
 '.ptogb.on{background:#000;color:#fff;border-color:#000}.ptogb i{width:7px;height:7px;border-radius:50%;flex:0 0 auto}'
 '.pcmp-banners{display:grid;grid-template-columns:1.7fr 1fr;gap:14px;margin-top:18px}'
 '.pcb-strat{display:grid;grid-template-columns:170px 1fr;border:1px solid var(--hairline);border-radius:16px;overflow:hidden;text-decoration:none;color:#000}.pcb-strat img{width:170px;height:100%;object-fit:cover;display:block}.pcb-strat .mono{font:700 9px ui-monospace,Menlo,monospace;color:rgba(0,0,0,.5);text-transform:uppercase}.pcb-strat>div{padding:18px 22px;display:flex;flex-direction:column;justify-content:center}.pcb-strat .t{font-weight:700;font-size:18px;letter-spacing:-.4px;margin-top:5px}.pcb-strat .d{font-size:13px;color:rgba(0,0,0,.6);margin-top:6px}.pcb-strat .go{font-weight:540;font-size:13px;margin-top:12px}'
 '.pcb-ad{background:var(--block-coral);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none;color:#000}.pcb-ad .mono{font:700 9px ui-monospace,Menlo,monospace;opacity:.6;text-transform:uppercase}.pcb-ad .t{font-weight:700;font-size:18px;letter-spacing:-.4px;line-height:1.2}.pcb-ad .d{font-size:12px;color:rgba(0,0,0,.6);margin-top:5px}.pcb-ad .go{font-weight:540;font-size:13px}'
 '@media(max-width:680px){.pcmp-banners{grid-template-columns:1fr}.pcb-strat{grid-template-columns:110px 1fr}.pcb-strat img{width:110px}}'
 '</style>'
 '<div class="wrap"><section><div class="sec-h"><h2 id="issTitle">이번달 캐시백</h2></div>'
 '<div id="view-ev">'
 '<a class="evhero" href="issue.html?v=cmp"><svg class="evh-wm" viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg><div class="evh-body"><div class="eb">이번 달 최대</div><div class="evh-t">이번 달, 카드값<br>최대 <b id="evhMax">119만원</b> 돌려받기</div><span class="evh-cta">플랫폼별 비교 ↗</span></div></a>'
 '<div class="cmpctl"><div class="ctlrow"><span class="ctll">정렬</span><button class="ctlb on" data-esort="amt">금액순</button><button class="ctlb" data-esort="plat">플랫폼순</button><button class="ctlb" data-esort="iss">카드사순</button></div>'
 '<div class="ctlrow"><span class="ctll">플랫폼</span><button class="ctlf on" data-eplat="">전체</button><button class="ctlf" data-eplat="카드고릴라">카드고릴라</button><button class="ctlf" data-eplat="뱅크샐러드">뱅크샐러드</button><button class="ctlf" data-eplat="토스">토스</button><button class="ctlf" data-eplat="아정당">아정당</button><button class="ctlf" data-eplat="네이버페이">네이버페이</button><button class="ctlf" data-eplat="카카오페이">카카오페이</button></div></div>'
 '<div class="tabs" id="tabs"></div><div id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div id="view-cmp" style="display:none">'
 '<div class="pcmp-hero"><div class="eb">PLATFORM COMPARE · 플랫폼 비교</div><h1>같은 카드, 채널마다<br>다른 캐시백.</h1><p>토스·카드고릴라·아정당·카카오페이·네이버페이·뱅크샐러드의 발급 캐시백을 한 표로 모았어요.</p></div>'
 '<div id="pcmp-spread"></div>'
 '<div class="pcmp-emb"><div><div class="t">카드 ❤ 플랫폼, 최고 궁합 비교</div><div class="s">가장 잘 맞는 발급 플랫폼을 찾아요</div></div><span class="emb"><span class="dh"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span><svg class="ht" viewBox="0 0 24 24"><use href="#ic-heart-f"/></svg><span class="dh r"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span></span></div>'
 '<div class="subnav2"><button data-c="iss" class="on">카드사별 비교</button><button data-c="prod">카드별 비교</button></div>'
 '<div class="ptogwrap"><span class="ptogl">표시 플랫폼 · 2개 이상</span><div class="ptog" id="platToggle"></div></div>'
 '<div class="cashtogwrap"><div class="cashtog" id="cashtog"><span class="ctgl">캐시백 기준</span><button data-cm="t" class="on">전체</button><button data-cm="m">주요</button></div>'
 '<div class="cmplegend"><span><i class="lg-t"></i>전체 = 주요 + 부가</span><span><i class="lg-m"></i>주요 = 발급·결제 기본 캐시백</span></div></div>'
 '<div id="cmp-iss"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
 '<div id="cmp-prod" style="display:none"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
 '<div class="pcmp-banners"><a class="pcb-strat" href="content.html"><img src="assets/tip-headers/header-strategy.png" alt="이번 달 발급 전략"><div><div class="mono">티라노TIP</div><div class="t">이번 달 어디서 받는 게 이득일까?</div><div class="d">카드사별 최대 플랫폼과 마감 임박 이벤트를 정리했어요.</div><span class="go">전략 보기 ›</span></div></a>'
 '<a class="pcb-ad" href="cards.html" rel="sponsored nofollow"><div class="mono">광고(AD) · 제휴</div><div><div class="t">해외 수수료 면제 여행카드</div><div class="d">최대 금액 기준, 조건 충족 시</div></div><span class="go">자세히 ›</span></a></div>'
 '</div>'
 '</section></div>')
ISSUE_JS=r"""
var EV=[],ORD=[],cur="전체",evSort="amt",evPlat="";
var PRODALL=[],pSort="amt",pFilter="",basis="cardgorilla",renderProd=function(){},renderIss=function(){},issFilter="",issSort="amt",cashMode="t";
function _spl(e){var t=e.reward_won||0;var m=(e.main_won!=null?e.main_won:null);var b=(e.bonus_won||0);
 if(m==null){if(b>=t)b=0;m=Math.max(t-b,0);}else{if(m>t)m=t;b=Math.max(t-m,0);}
 return {t:t,m:m,b:b};}
function mval(o,md){return !o?0:(md==='m'?o.m:md==='b'?o.b:o.t);}
function _capBD(o){if(!o||(o.b<=0&&o.m>=o.t))return '';return '<div class="cap">주'+Math.round(o.m/10000)+'·부'+Math.round(o.b/10000)+'</div>';}
var PCOL={"카드고릴라":"#ff4d4f","뱅크샐러드":"#2f6bff","아정당":"#3b5bdb","카카오페이":"#e8b800","토스":"#3182f6","네이버페이":"#03c75a","네이버":"#03c75a"};
function pcol(p){return PCOL[p]||"#7a8088";}
function render(){var items=(cur==="전체"?EV:EV.filter(x=>x.issuer===cur)).slice();
 if(evPlat)items=items.filter(x=>x.platform===evPlat);
 items.sort(function(a,b){return evSort==='plat'?(a.platform||'').localeCompare(b.platform||'','ko'):evSort==='iss'?(a.issuer||'').localeCompare(b.issuer||'','ko'):(num(b.benefit)-num(a.benefit));});
 var L=document.getElementById('list');if(!items.length){L.innerHTML='<div class="empty">조건에 맞는 이벤트가 없어요.</div>';return;}
 L.innerHTML=items.map(function(x){
   return '<a class="evc" href="events.html?n='+encodeURIComponent(x.card)+(x.pk?'&p='+x.pk:'')+'"><div class="evc-plate">'+imgTag(x.img)+'</div><span class="evc-pf">'+_pdk(x.pk,true)+'</span><div><div class="evc-nm">'+x.card+'</div><div class="evc-iss">'+x.issuer+(x.period?' · '+x.period:'')+'</div></div><div class="evc-foot"><div><div class="evc-amtl">최대 혜택</div><div class="evc-amt">'+x.benefit+'</div></div><span class="evc-go">자세히 ›</span></div></a>';}).join("");}
function tabs(){var T=["전체"].concat(ORD);var t=document.getElementById('tabs');t.innerHTML=T.map(function(o){var c=o==="전체"?EV.length:EV.filter(x=>x.issuer===o).length;return '<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'<span class="cnt">'+c+'</span></div>';}).join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};});}
// 발급이벤트 / 플랫폼비교는 별도 화면(서브탭 제거). ?v=cmp로 진입 화면 결정.
document.querySelector('.subnav2').onclick=function(e){var b=e.target.closest('button');if(!b)return;document.querySelectorAll('.subnav2 button').forEach(x=>x.classList.remove('on'));b.classList.add('on');var iss=b.dataset.c==='iss';document.getElementById('cmp-iss').style.display=iss?'':'none';document.getElementById('cmp-prod').style.display=iss?'none':'';var cn=document.getElementById('cmpnote-iss');if(cn)cn.style.display=iss?'':'none';};
// 캐시백 기준 토글(전체/주요/부가) — 두 탭 동시 갱신
var _ctg=document.getElementById('cashtog');if(_ctg)_ctg.addEventListener('click',function(e){var b=e.target.closest('button[data-cm]');if(!b)return;cashMode=b.dataset.cm;_ctg.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});renderProd();renderIss();});
// 표시 플랫폼 토글(최소 2개 유지) — 표 열·모바일 칩 즉시 가감, 최고값(❤) 재계산
var PNAME={cardgorilla:"카드고릴라",banksalad:"뱅크샐러드",toss:"토스",ajungdang:"아정당",naver:"네이버페이",kakaopay:"카카오페이"};
function renderPlatToggle(){var el=document.getElementById('platToggle');if(!el)return;el.innerHTML=PORD.map(function(pk){var on=!!VIS[pk];return '<button class="ptogb'+(on?' on':'')+'" data-pt="'+pk+'"><i style="background:'+(PBC[pk]||"#888")+'"></i>'+(PSHORT[pk]||PNAME[pk]||pk)+'</button>';}).join('');}
var _pt=document.getElementById('platToggle');if(_pt)_pt.addEventListener('click',function(e){var b=e.target.closest('button[data-pt]');if(!b)return;var pk=b.getAttribute('data-pt');var on=PORD.filter(function(k){return VIS[k];}).length;if(VIS[pk]&&on<=2)return;VIS[pk]=VIS[pk]?0:1;renderPlatToggle();renderProd();renderIss();});
// 기준 플랫폼 칩(테이블 정렬 기준 변경) — cmp-prod 내부에 렌더되므로 위임 처리
document.getElementById('cmp-prod').addEventListener('click',function(e){var b=e.target.closest('#pchips button');if(!b)return;e.preventDefault();basis=b.dataset.b;renderProd();renderIss();});
// 카드사별: 기준 플랫폼·카드사 필터·정렬 위임 처리
document.getElementById('cmp-iss').addEventListener('click',function(e){
 var pb=e.target.closest('[data-pchips] button');if(pb){e.preventDefault();basis=pb.getAttribute('data-b');renderProd();renderIss();return;}
 var fb=e.target.closest('[data-if]');if(fb){issFilter=fb.getAttribute('data-if');renderIss();return;}
 var sb=e.target.closest('[data-is]');if(sb){issSort=sb.getAttribute('data-is');renderIss();return;}});
// 발급이벤트 화면 정렬(금액/플랫폼/카드사)+플랫폼 필터
document.getElementById('view-ev').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 if(b.dataset.esort!==undefined){evSort=b.dataset.esort;document.querySelectorAll('[data-esort]').forEach(x=>x.classList.remove('on'));b.classList.add('on');render();}
 else if(b.dataset.eplat!==undefined){evPlat=b.dataset.eplat;document.querySelectorAll('[data-eplat]').forEach(x=>x.classList.remove('on'));b.classList.add('on');render();}});
// 진입 화면 결정: ?v=cmp면 플랫폼 비교, 아니면 발급 이벤트 (서브탭 없이 분리)
(function(){var isCmp=new URLSearchParams(location.search).get('v')==='cmp';
 document.getElementById('view-ev').style.display=isCmp?'none':'';
 document.getElementById('view-cmp').style.display=isCmp?'':'none';
 var t=document.getElementById('issTitle');if(t)t.textContent=isCmp?'사이트 비교':'이번달 캐시백';
 document.title=(isCmp?'사이트 비교':'이번달 캐시백')+' | 카드티라노';})();
function num(s){var m=(s||"").match(/([0-9]+(?:\.[0-9]+)?)\s*만/);return m?parseFloat(m[1]):-1;}
// 발급이벤트(EV) 목록은 아래 platform_events.json 집계에서 구성(5개 플랫폼·네이버 포함). 구형 events.json(네이버 0건) 의존 제거.
// 카드사·카드상품 비교 모두 콜렉터 platform_events.json에서 집계(뱅샐·아정당 포함, 카카오페이 제외)
var PN={cardgorilla:"카드고릴라",banksalad:"뱅크샐러드",toss:"토스",naver:"네이버페이",ajungdang:"아정당",kakaopay:"카카오페이"};
var PSHORT={cardgorilla:"고릴라",banksalad:"뱅샐",toss:"토스",naver:"네이버",ajungdang:"아정당",kakaopay:"카카오"};
var PBC={cardgorilla:"#FF6A13",banksalad:"#19C37D",toss:"#3182F6",ajungdang:"#1B64DA",naver:"#03C75A",kakaopay:"#FEE500"};
function _pdk(pk,shrt){return '<span style="display:inline-flex;align-items:center;gap:5px;white-space:nowrap"><i style="width:7px;height:7px;border-radius:50%;background:'+(PBC[pk]||"#888")+';flex:0 0 auto"></i>'+((shrt?PSHORT[pk]:PN[pk])||pk)+'</span>';}
var PORD=["cardgorilla","banksalad","toss","ajungdang","naver","kakaopay"];
var VIS={cardgorilla:1,banksalad:1,toss:1,ajungdang:1,naver:1,kakaopay:1};   // 표시 플랫폼(최소 2)
function visList(){return PORD.filter(function(pk){return VIS[pk];});}
var HEART='<svg class="hrt" viewBox="0 0 24 24" width="11" height="11" style="vertical-align:-1px;margin-right:3px"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg>';
function _wm(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
// 이벤트명 통일: 캐시백 리워드(금액 있음)면 플랫폼 불문 '최대 N만원 캐시백'으로 표기, 아니면 원문 유지
function _rwd(text,won){return (won&&won>0)?('최대 '+_wm(won)+' 캐시백'):(text||'');}
// A안 티라노 픽 점수 = 메인 + 0.35×부가 (조건부 부가는 달성난도 반영해 35% 가중)
function _pick(e){var m=(e.main_won!=null?e.main_won:(e.reward_won||0));var b=(e.bonus_won||0);return m+0.35*b;}
// 메인/부가 분리 표기(부가가 있을 때만)
function _bd(e){var b=(e.bonus_won||0);if(b<=0)return '';var m=(e.main_won!=null?e.main_won:(e.reward_won||0));return '<div class="bd">메인 <b>'+_wm(m)+'</b> + 부가 '+_wm(b)+' <span class="bdt">최대 합 '+_wm((e.reward_won||0))+'</span></div>';}
function _nk2(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
Promise.all([fetch('platform_events.json').then(r=>r.json()),fetch('cards.json').then(r=>r.json()).catch(function(){return {cards:{}};})]).then(function(A){
 var prods=(A[0].products||[]);var IMG={},cj=A[1].cards||{};for(var ik in cj){(cj[ik]||[]).forEach(function(c){if(c.img&&!IMG[_nk2(c.name)])IMG[_nk2(c.name)]=c.img;});}
 // (0) 발급이벤트 EV 목록 = 전 플랫폼(네이버 포함) 평탄화. 각 행은 실제 플랫폼 이벤트로 아웃링크.
 (function(){var tmp=[],mx={};
  prods.forEach(function(p){var iss=p.issuer||'기타';(p.events||[]).forEach(function(e){var _pp=(p.platforms||{})[e.platform]||{};var u=_best(e.platform,e.url||_pp.url,_pp.id);if(e.platform==='cardgorilla'){var _cg=_cgUrl(iss,_pp.id);if(_cg)u=_cg;}
   tmp.push({issuer:iss,card:p.name,platform:(PN[e.platform]||e.platform),pk:e.platform,benefit:_rwd(e.reward_text,e.reward_won),url:u||('carddetail.html?n='+encodeURIComponent(p.name)),period:(e.period_end?('~'+String(e.period_end).slice(5).replace('-','/')):''),pe:(e.period_end||''),won:(e.reward_won||0),img:(p.img||IMG[_nk2(p.name)]||'')});
   mx[iss]=Math.max(mx[iss]||0,e.reward_won||0);});});
  EV=tmp;ORD=Object.keys(mx).sort(function(a,b){return mx[b]-mx[a];});
  var _mxv=Math.max.apply(null,tmp.map(function(x){return x.won||0;}).concat([0]));var _eh=document.getElementById('evhMax');if(_eh&&_mxv)_eh.textContent=_wm(_mxv);
  var sp=new URLSearchParams(location.search);var qi=sp.get('issuer');if(qi&&(qi==='전체'||ORD.indexOf(qi)>=0))cur=qi;
  var qp=sp.get('plat');if(qp){evPlat=qp;var pb=document.querySelector('[data-eplat="'+qp+'"]');if(pb){document.querySelectorAll('[data-eplat]').forEach(function(x){x.classList.remove('on');});pb.classList.add('on');}}
  tabs();render();var at=document.querySelector('#tabs .tab.active');if(at)at.scrollIntoView({inline:'center',block:'nearest'});})();
 // (1) 카드사별 비교 — 카드사 × 플랫폼 최대 집계 + 보유 종수·대표카드 (시안 표형)
 function _es(s){return String(s==null?'':s).replace(/[<>&]/g,'');}
 var byIss={},issMeta={};
 prods.forEach(function(p){if(!(p.events||[]).length)return;var iss=p.issuer||'기타';byIss[iss]=byIss[iss]||{};
  var pmax=0;p.events.forEach(function(e){var w=e.reward_won||0;if(w>pmax)pmax=w;var c=byIss[iss][e.platform];if(!c||w>(c.t||0))byIss[iss][e.platform]=_spl(e);});
  var m=issMeta[iss]=issMeta[iss]||{count:0,rep:'',repv:-1};m.count++;if(pmax>m.repv){m.repv=pmax;m.rep=p.name;}});
 var ISSROWS=Object.keys(byIss).map(function(iss){var o={};PORD.forEach(function(pk){var c=byIss[iss][pk];if(c&&c.t)o[pk]=c;});return {iss:iss,o:o,count:(issMeta[iss]||{}).count||0,rep:(issMeta[iss]||{}).rep||''};});
 var ISSF=[['','전체'],['삼성','삼성'],['현대','현대'],['KB국민','KB국민'],['신한','신한'],['롯데','롯데'],['우리','우리']];
 renderIss=function(){
  var rows=ISSROWS.filter(function(r){return !issFilter||r.iss.indexOf(issFilter)>=0;});
  var VL=visList(),gc='1.6fr repeat('+VL.length+',1fr)';
  rows.forEach(function(r){var mx=0;VL.forEach(function(pk){var v=mval(r.o[pk],cashMode);if(v>mx)mx=v;});r.mx=mx;});
  rows.sort(function(a,b){return issSort==='basis'?(mval(b.o[basis],cashMode)-mval(a.o[basis],cashMode)):(b.mx-a.mx);});
  var ctl='<div class="cmpctl"><div class="ctlrow"><span class="ctll">카드사</span>'+ISSF.map(function(f){return '<button class="ctlf'+(issFilter===f[0]?' on':'')+'" data-if="'+f[0]+'">'+f[1]+'</button>';}).join('')+'</div>'+
   '<div class="ctlrow"><span class="ctll">정렬</span><button class="ctlb'+(issSort==='amt'?' on':'')+'" data-is="amt">최고 캐시백순</button><button class="ctlb'+(issSort==='basis'?' on':'')+'" data-is="basis">기준 플랫폼순</button></div></div>';
  var chips='<div class="pbasis"><div><div class="bl">기준 플랫폼</div><div class="bt">'+PN[basis]+' 캐시백 순으로 정렬돼요</div></div><div class="pchips" data-pchips>'+PORD.map(function(pk){return '<button data-b="'+pk+'"'+(pk===basis?' class="on"':'')+'>'+_pdk(pk,true)+'</button>';}).join('')+'</div></div>';
  var head='<div class="ptr hd" style="grid-template-columns:'+gc+'"><div>카드사 ('+rows.length+')</div>'+VL.map(function(pk){return '<div'+(pk===basis?' style="color:var(--text);font-weight:800"':'')+'>'+_pdk(pk,true)+'</div>';}).join('')+'</div>';
  var body=rows.map(function(r){var cells=VL.map(function(pk){var o=r.o[pk];var v=mval(o,cashMode);if(!v)return '<span class="cell"><span class="chip no">–</span></span>';var top=(v===r.mx);return '<a class="cell" href="issue.html?issuer='+encodeURIComponent(r.iss)+'&plat='+encodeURIComponent(PN[pk]||pk)+'"><span class="chip'+(top?' mx':'')+'">'+(top?HEART:'')+_chipW(v)+'</span>'+(cashMode==='t'?_capBD(o):'')+'</a>';}).join('');
   return '<div class="ptr" style="grid-template-columns:'+gc+'"><a class="pc" href="issue.html?issuer='+encodeURIComponent(r.iss)+'"><span class="issmk"><svg viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg></span><div><div class="pcn">'+_es(r.iss)+'</div><div class="pci" style="font-family:inherit;font-size:11.5px;color:var(--sub)">보유 '+r.count+'종 · 대표 '+_es(r.rep)+'</div></div></a>'+cells+'</div>'+_nudge(r.o);}).join('');
  var mc='<div class="pcardlist">'+rows.map(function(r){var c2=VL.filter(function(pk){return mval(r.o[pk],cashMode);}).sort(function(a,b){return mval(r.o[b],cashMode)-mval(r.o[a],cashMode);}).map(function(pk){var v=mval(r.o[pk],cashMode);return '<div class="pmc'+(v===r.mx?' mx':'')+'"><div class="pmc-n">'+PN[pk]+'</div><div class="pmc-v">'+(v===r.mx?HEART:'')+_chipW(v)+'</div></div>';}).join('');
   return '<a class="pcardm" href="issue.html?issuer='+encodeURIComponent(r.iss)+'"><div class="pcardm-top"><div class="pcardm-info"><div class="pcn">'+_es(r.iss)+'</div><div class="pci">보유 '+r.count+'종 · 대표 '+_es(r.rep)+'</div></div><div class="pcardm-best"><div class="bl">최대</div><div class="bv">'+_chipW(r.mx)+'</div></div></div><div class="pcardm-chips">'+c2+'</div>'+_nudge(r.o)+'</a>';}).join('')+'</div>';
  var note='<div class="pcmpnote"><span class="dot"></span><svg viewBox="0 0 24 24" width="13" height="13" style="color:#000"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> = 이 카드사의 최고 궁합(커플) 플랫폼 · 셀을 누르면 그 카드사·플랫폼 캐시백 목록으로 · 금액은 수집 시점 기준이에요.</div>';
  document.getElementById('cmp-iss').innerHTML=rows.length?(ctl+chips+'<div class="ptblwrap"><div class="ptbl">'+head+body+'</div></div>'+mc+note):'<div class="empty">데이터 준비 중</div>';
 };
 renderIss();
 // (2) 카드상품별 플랫폼 비교 — 시안 테이블형(카드 × 플랫폼, 검은 칩=최대 채널)
 // 2개 이상 플랫폼에 이벤트가 있는 카드만(교차비교 의미). o={플랫폼:원}.
 var TBL=prods.filter(function(p){return new Set((p.events||[]).map(e=>e.platform)).size>1;}).map(function(p){
  var o={};(p.events||[]).forEach(function(e){var w=e.reward_won||0;var c=o[e.platform];if(!c||w>c.t)o[e.platform]=_spl(e);});
  return {id:p.id,name:p.name,issuer:p.issuer||'',img:p.img||IMG[_nk2(p.name)]||'',o:o};});
 PRODALL=TBL;
 // 기준 플랫폼 기본값 = 비표시 셀이 가장 적은(=커버리지 큰) 플랫폼
 (function(){var cnt={};PORD.forEach(function(pk){cnt[pk]=0;});TBL.forEach(function(c){PORD.forEach(function(pk){if(c.o[pk])cnt[pk]++;});});var bp=PORD[0],mx=-1;PORD.forEach(function(pk){if(cnt[pk]>mx){mx=cnt[pk];bp=pk;}});if(mx>0)basis=bp;})();
 // 이 달의 최대 격차(피처카드) — 플랫폼 간 전체 캐시백 max-min 차이가 가장 큰 카드
 (function(){var best=null,gap=-1,bp,wp,mxv,mnv;TBL.forEach(function(c){var ks=PORD.filter(function(pk){return c.o[pk];});if(ks.length<2)return;var mx=Math.max.apply(null,ks.map(function(pk){return c.o[pk].t;})),mn=Math.min.apply(null,ks.map(function(pk){return c.o[pk].t;}));if(mx-mn>gap){gap=mx-mn;best=c;mxv=mx;mnv=mn;bp=ks.reduce(function(a,b){return c.o[b].t>c.o[a].t?b:a;});wp=ks.reduce(function(a,b){return c.o[b].t<c.o[a].t?b:a;});}});
  var el=document.getElementById('pcmp-spread');if(!el)return;
  if(best&&gap>0){el.innerHTML='<div class="pcmp-spread"><div><div class="sl">이 달의 최대 격차</div><div class="st">'+best.name+', 채널 따라<br>최대 '+_wm(gap)+' 차이</div><div class="ss">'+PN[bp]+' '+_wm(mxv)+' · '+PN[wp]+' '+_wm(mnv)+'</div></div><div class="splate">'+imgTag(best.img)+'</div></div>';}else{el.innerHTML='';}})();
 function _chipW(w){var s=_wm(w);return s.replace('만원','만').replace('원','');}
 // 인라인 넛지: 전체1위 ≠ 주요1위 & 주요격차 ≥ 2만원 → 크림 띠(전체 모드 한정)
 function _nudge(o){if(cashMode!=='t')return '';var ks=PORD.filter(function(pk){return o[pk]&&o[pk].t;});if(ks.length<2)return '';
  var bt=ks.reduce(function(a,b){return o[b].t>o[a].t?b:a;});var bm=ks.reduce(function(a,b){return o[b].m>o[a].m?b:a;});
  if(bt===bm||(o[bm].m-o[bt].m)<20000)return '';var pct=o[bt].t?Math.round(o[bt].b/o[bt].t*100):0;
  return '<div class="cmpnudge"><span class="nb"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L4.5 13.5H11l-1 8.5L19.5 10H13z"/></svg></span><div class="nt">실속 체크 · 전체 캐시백은 <b>'+PN[bt]+' '+_chipW(o[bt].t)+'</b>으로 가장 높지만 핵심(주요) 혜택은 '+_chipW(o[bt].m)+'이에요. 실속만 보면 <b>'+PN[bm]+' 주요 '+_chipW(o[bm].m)+'</b>이 더 높아요.</div><span class="nx">'+PN[bt]+' 전체의 '+pct+'%가 부가</span></div>';}
 renderProd=function(){
  var rows=TBL.slice().sort(function(a,b){return mval(b.o[basis],cashMode)-mval(a.o[basis],cashMode);});
  var VL=visList(),gc='1.6fr repeat('+VL.length+',1fr)';
  var head='<div class="ptr hd" style="grid-template-columns:'+gc+'"><div>카드 ('+rows.length+')</div>'+VL.map(function(pk){return '<div'+(pk===basis?' style="color:var(--text);font-weight:800"':'')+'>'+_pdk(pk,true)+'</div>';}).join('')+'</div>';
  var body=rows.map(function(c){
   var vals=VL.map(function(pk){return mval(c.o[pk],cashMode);});var mx=Math.max.apply(null,vals);
   var cells=VL.map(function(pk){var o=c.o[pk];var v=mval(o,cashMode);if(!v)return '<span class="cell"><span class="chip no">–</span></span>';var top=(v===mx);return '<a class="cell" href="events.html?platform='+pk+'&n='+encodeURIComponent(c.name||'')+'"><span class="chip'+(top?' mx':'')+'">'+(top?HEART:'')+_chipW(v)+'</span>'+(cashMode==='t'?_capBD(o):'')+'</a>';}).join('');
   var plate='<div class="pcimg">'+imgTag(c.img)+'</div>';
   return '<div class="ptr" style="grid-template-columns:'+gc+'"><a class="pc" href="carddetail.html?n='+encodeURIComponent(c.name||'')+'" data-track="cmp" data-label="'+(c.name||'')+'">'+plate+'<div><div class="pcn">'+c.name+'</div><div class="pci">'+c.issuer+'</div></div></a>'+cells+'</div>'+_nudge(c.o);}).join('');
  var chips='<div class="pbasis"><div><div class="bl">기준 플랫폼</div><div class="bt">'+PN[basis]+' 캐시백 순으로 정렬돼요</div></div><div class="pchips" id="pchips">'+PORD.map(function(pk){return '<button data-b="'+pk+'"'+(pk===basis?' class="on"':'')+'>'+_pdk(pk,true)+'</button>';}).join('')+'</div></div>';
  var note='<div class="pcmpnote"><span class="dot"></span><svg viewBox="0 0 24 24" width="13" height="13" style="color:#000"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> = 이 카드의 최고 궁합(커플) 플랫폼 · 행 최대값 · 셀을 누르면 이번달 캐시백 상세로 이동 · 금액은 수집 시점 기준이에요.</div>';
  // 모바일 시안: 카드별 스택 카드(플레이트+이름+최대+사이트별 캐시백 칩, 최대=검은칩)
  var pcards='<div class="pcardlist">'+rows.map(function(c){var vals=VL.map(function(pk){return mval(c.o[pk],cashMode);});var mx=Math.max.apply(null,vals);
    var chips2=VL.filter(function(pk){return mval(c.o[pk],cashMode);}).sort(function(a,b){return mval(c.o[b],cashMode)-mval(c.o[a],cashMode);}).map(function(pk){var v=mval(c.o[pk],cashMode);return '<div class="pmc'+(v===mx?' mx':'')+'"><div class="pmc-n">'+PN[pk]+'</div><div class="pmc-v">'+(v===mx?HEART:'')+_chipW(v)+'</div></div>';}).join('');
    return '<a class="pcardm" href="carddetail.html?n='+encodeURIComponent(c.name||'')+'" data-track="cmp" data-label="'+(c.name||'')+'"><div class="pcardm-top"><div class="pcimg">'+imgTag(c.img)+'</div><div class="pcardm-info"><div class="pcn">'+c.name+'</div><div class="pci">'+c.issuer+'</div></div><div class="pcardm-best"><div class="bl">최대</div><div class="bv">'+_chipW(mx)+'</div></div></div><div class="pcardm-chips">'+chips2+'</div>'+_nudge(c.o)+'</a>';}).join('')+'</div>';
  document.getElementById('cmp-prod').innerHTML=rows.length?(chips+'<div class="ptblwrap"><div class="ptbl">'+head+body+'</div></div>'+pcards+note):'<div class="empty">교차비교 카드가 없어요.</div>';
  if(window.repairImages)repairImages();};
 renderProd();renderPlatToggle();
}).catch(function(){document.getElementById('cmp-iss').innerHTML='<div class="empty">데이터 준비 중</div>';document.getElementById('cmp-prod').innerHTML='<div class="empty">교차비교 데이터 준비 중이에요.</div>';});
"""

# ===== DETAIL =====
DETAIL_BODY='<div style="padding:12px 0"><div class="wrap"><a class="bk" href="discount.html">‹</a></div></div><div id="root"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
DETAIL_JS=r"""
function fmt(s){return (s&&s!=="-"&&s!=="없음")?s:"-";}
var id=Number(new URLSearchParams(location.search).get('id'));
fetch('data.json').then(r=>r.json()).then(function(j){var d=j.items.find(x=>x.id===id);if(!d){document.getElementById('root').innerHTML='<div class="empty">혜택을 찾을 수 없어요. <a class="accent" href="discount.html">목록</a></div>';return;}var t=thumbOf(d.plat);
 document.getElementById('root').innerHTML='<div class="wrap"><div class="hero-detail"><div class="th">'+favico(d.domain,t.e,t.bg)+'</div><div class="store">'+d.plat+'</div><div class="disc"><span class="hl">'+d.disc+'</span></div><div class="type">'+d.type+'</div></div>'+
 '<div class="rows"><div class="r"><div class="k">카드/페이</div><div class="v">'+fmt(d.card)+'</div></div><div class="r"><div class="k">할인유형</div><div class="v">'+fmt(d.type)+'</div></div><div class="r"><div class="k">최소결제</div><div class="v">'+fmt(d.min)+'</div></div><div class="r"><div class="k">조건/한도</div><div class="v">'+fmt(d.cond)+'</div></div><div class="r"><div class="k">행사기간</div><div class="v">'+fmt(d.period)+'</div></div></div>'+
 '<div class="cta"><a href="'+d.url+'" target="_blank" rel="noopener">혜택 받으러 가기 ›</a></div></div>';});
"""

# ===== CONTENT =====
CONTENT_BODY=('<style>'
 '.tip-hero{background:var(--block-lime,#dceeb1);border-radius:24px;padding:42px 40px;margin:24px 0 0;display:flex;align-items:flex-start;justify-content:space-between;gap:20px;position:relative;overflow:hidden}'
 '.tip-eb{font:800 11.5px var(--font-mono,monospace);letter-spacing:.04em;text-transform:uppercase;color:rgba(0,0,0,.55)}'
 '.tip-h{font-weight:340;font-size:40px;letter-spacing:-1.2px;margin:12px 0 0;line-height:1.06}'
 '.tip-sub{font-size:15.5px;color:rgba(0,0,0,.66);margin:12px 0 0;max-width:500px;line-height:1.5}'
 '.tip-cta{display:inline-flex;align-items:center;gap:7px;background:#000;color:#fff;font-weight:600;font-size:14px;padding:12px 22px;border-radius:50px;text-decoration:none;margin-top:20px}'
 '.tip-hero-badge{flex:0 0 auto;font:800 10.5px var(--font-mono,monospace);letter-spacing:.04em;background:rgba(0,0,0,.86);color:#fff;border-radius:50px;padding:7px 13px}'
 '.tip-types{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:18px}'
 '.tip-type{border:1px solid var(--hairline,#e6e6e6);border-radius:16px;padding:16px 18px;cursor:pointer;background:#fff;transition:border-color .14s;display:flex;align-items:center;gap:13px}'
 '.tip-type:hover{border-color:#000}.tip-type.on{border-color:#000;background:var(--surface-soft,#f4f4f5)}'
 '.tip-type .tt-ic{display:inline-flex;width:40px;height:40px;border-radius:11px;align-items:center;justify-content:center;flex:0 0 auto}'
 '.tip-type .tt-ic .ic{width:20px;height:20px;color:#000}'
 '.tip-type .tt-tag{font:800 9.5px var(--font-mono,monospace);text-transform:uppercase;letter-spacing:.04em;color:rgba(0,0,0,.45)}'
 '.tip-type .tt-h{font-size:15px;font-weight:800;margin:3px 0 0;letter-spacing:-.2px}'
 '.tip-type .tt-d,.tip-type .tt-go{display:none}'
 '.tip-list{display:flex;flex-direction:column;gap:2px;margin-top:12px}'
 '.tip-row{display:flex;align-items:flex-start;gap:14px;padding:18px 4px;border-top:1px solid var(--hairline);text-decoration:none;color:#000}'
 '.tip-row:hover{background:var(--surface-soft)}'
 '.tip-cat{font-size:11px;font-weight:700;padding:4px 11px;border-radius:50px;background:var(--block-lime);color:#000;white-space:nowrap;flex:0 0 auto;margin-top:2px}'
 '.tip-rt{font-size:17px;font-weight:700;letter-spacing:-.3px}.tip-rs{font-size:13.5px;color:rgba(0,0,0,.58);margin-top:4px;line-height:1.45}'
 '.tip-min{font-size:12px;color:rgba(0,0,0,.45);margin-top:6px}'
 '.tip-sech{font-size:12px;font-weight:700;color:rgba(0,0,0,.55);margin:40px 0 0;text-transform:uppercase;letter-spacing:.4px}'
 '@media(max-width:760px){.tip-types{grid-template-columns:1fr}.tip-h{font-size:26px}.tip-hero{padding:28px 22px;flex-direction:column}.tip-hero-badge{order:-1;align-self:flex-start}}'
 '</style>'
 '<div class="wrap"><section id="listwrap">'
 '<div class="tip-hero"><div><div class="tip-eb">이번달 캐시백 획득 전략 · 2026.06</div><h1 class="tip-h">6월엔 어떤 카드를,<br>어느 플랫폼에서</h1><p class="tip-sub">카드사별로 이번 달 캐시백이 가장 큰 플랫폼과 상품, 마감 임박 이벤트까지 한 번에 정리했어요.</p><a class="tip-cta" id="tipStrat" href="content.html">전략 보기 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></div><div class="tip-hero-badge">이달의 1순위</div></div>'
 '<div class="tip-types" id="tipTypes"></div>'
 '<div class="tip-sech" id="tipSech">최신 글</div>'
 '<div class="tip-list" id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></section>'
 '<div id="detail" style="display:none"></div></div>')
CONTENT_JS=r"""
var C=[],cur="전체";
var TYPES=[{k:'발급 팁',tag:'STRATEGY',h:'이달의 캐시백 획득 전략',d:'지금 받아야 할 카드와 채널, 놓치면 아까운 캐시백 타이밍.',ic:'ic-search',bg:'var(--block-lime)'},
 {k:'기초 상식',tag:'KNOWLEDGE',h:'카드 지식',d:'연회비·전월실적·적립 vs 할인 — 처음 고르는 사람을 위한 쉬운 설명.',ic:'ic-grid',bg:'var(--block-cream)'},
 {k:'할인 활용',tag:'ANATOMY',h:'신용카드 해부',d:'카드 한 장을 영역별로 뜯어보고 손익까지 따져봐요.',ic:'ic-cart',bg:'var(--block-mint)'}];
var CATBG={'발급 팁':'var(--block-lime)','기초 상식':'var(--block-cream)','할인 활용':'var(--block-mint)','여행':'var(--block-mint)'};
function _rt(b){var n=(b||[]).join('').length;return Math.max(2,Math.round(n/450))+'분';}
function rowHtml(x){return '<a class="tip-row" href="content.html?id='+x.id+'"><span class="tip-cat">'+x.cat+'</span><div><div class="tip-rt">'+x.title+'</div>'+(x.summary?'<div class="tip-rs">'+x.summary+'</div>':'')+'<div class="tip-min">읽는 데 '+_rt(x.body)+'</div></div></a>';}
function renderList(){var items=cur==="전체"?C:C.filter(function(x){return x.cat===cur;});document.getElementById('list').innerHTML=items.length?items.map(rowHtml).join(''):'<div class="empty" style="padding:30px 0">글이 없어요.</div>';document.getElementById('tipSech').textContent=cur==="전체"?'최신 글':cur+' 글';}
function types(){var t=document.getElementById('tipTypes');t.innerHTML=TYPES.map(function(ty){var on=cur===ty.k;return '<div class="tip-type'+(on?' on':'')+'" data-k="'+ty.k+'"><span class="tt-ic" style="background:'+(ty.bg||'var(--surface-soft)')+'"><svg class="ic"><use href="#'+ty.ic+'"/></svg></span><div class="tt-tag">'+ty.tag+'</div><div class="tt-h">'+ty.h+'</div><div class="tt-d">'+ty.d+'</div><div class="tt-go">보러가기 ›</div></div>';}).join('');
 t.querySelectorAll('.tip-type').forEach(function(b){b.onclick=function(){cur=(cur===b.dataset.k)?'전체':b.dataset.k;types();renderList();};});}
function detail(d){document.getElementById('listwrap').style.display='none';var el=document.getElementById('detail');el.style.display='';
 var hero=d.img?'<div class="ghero"><img src="'+d.img+'" alt="'+d.cat+'" loading="eager"/></div>':'';
 el.innerHTML='<div class="adt">'+hero+'<div class="acat" style="display:inline-block;background:'+(CATBG[d.cat]||'var(--block-lime)')+';color:#000;padding:6px 14px;border-radius:50px;font-size:12px;font-weight:700">'+d.cat+'</div><div class="ah">'+d.title+'</div>'+(d.summary?'<div class="asum">'+d.summary+'</div>':'')+d.body.map(function(p){return '<p>'+p+'</p>';}).join("")+'<a class="bk2" href="content.html">← 티라노TIP</a></div>';document.title=d.title+' | 카드티라노';}
var id=new URLSearchParams(location.search).get('id');
fetch('content.json').then(function(r){return r.json();}).then(function(j){C=j.items;if(id!==null){var d=C.find(function(x){return String(x.id)===String(id);});if(d){detail(d);return;}}
 var st=C.filter(function(x){return /발급|전략/.test(x.cat||'');})[0]||C[0];var sb=document.getElementById('tipStrat');if(sb&&st)sb.setAttribute('href','content.html?id='+encodeURIComponent(st.id));
 types();renderList();});
"""

# ===== CARD DETAIL =====
CARDDETAIL_BODY=('<style>'
 '#root{padding-bottom:96px}'
 # --- 히어로 ---
 '.cdhero{display:flex;gap:36px;align-items:center;padding:14px 0 30px;flex-wrap:wrap}'
 '.cdh-info{flex:1;min-width:260px}'
 '.cdh-eb{font-family:var(--font-mono,ui-monospace,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.5)}'
 '.cdh-nm{font-size:44px;font-weight:340;margin-top:10px;letter-spacing:-1.5px;line-height:1.02}'
 '.cdh-tag{font-size:15px;color:rgba(0,0,0,.66);margin-top:13px;line-height:1.45;max-width:440px}'
 '.cdh-stats{display:flex;align-items:stretch;gap:22px;margin-top:22px;flex-wrap:wrap}'
 '.cdh-stats>div.st{display:flex;flex-direction:column;gap:4px}.cdh-stats .sl{font-family:var(--font-mono,monospace);font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:rgba(0,0,0,.45);display:flex;align-items:center;gap:4px}.cdh-stats .sv{font-size:21px;font-weight:700;letter-spacing:-.4px;white-space:nowrap}'
 '.cdh-stats .sep{width:1px;background:var(--hairline)}.cdh-stats .sl .star{width:12px;height:12px;color:var(--accent-magenta)}'
 '.cdh-cta{display:flex;gap:12px;margin-top:20px;align-items:center;flex-wrap:wrap}'
 '.cdh-fav{display:inline-flex;align-items:center;gap:7px;padding:11px 18px;border-radius:50px;border:1px solid var(--hairline);background:var(--surface,#fff);color:var(--text);font-weight:540;font-size:14px;cursor:pointer}.cdh-fav.on{color:var(--accent-magenta);border-color:var(--accent-magenta)}.cdh-fav .ic{width:18px;height:18px}'
 '.cdh-hint{font-size:13px;color:rgba(0,0,0,.5)}'
 '.cdh-disc{font-size:12px;color:rgba(0,0,0,.5);margin-top:14px;max-width:460px;line-height:1.55}'
 '.cdh-plate{width:290px;max-width:44%;border-radius:14px;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.2);transform:rotate(-6deg);flex:0 0 auto;background:var(--surface-soft);aspect-ratio:1.586/1}'
 '.cdh-plate img{width:100%;height:100%;display:block;object-fit:cover}'
 '@media(max-width:680px){.cdhero{gap:18px}.cdh-plate{width:160px;max-width:42%;transform:rotate(-5deg)}.cdh-nm{font-size:27px;letter-spacing:-1px}.cdh-stats{gap:0;border:1px solid var(--hairline);border-radius:14px;overflow:hidden;margin-top:18px}.cdh-stats>div.st{flex:1;padding:11px 10px;text-align:center;align-items:center}.cdh-stats .sv{font-size:15px}.cdh-stats .sep{align-self:stretch}}'
 # --- 캐시백 추이 차트 ---
 '.cdt{background:var(--block-lime);border-radius:22px;padding:28px 30px;margin-top:6px}'
 '.cdt-h{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:10px}'
 '.cdt-eb{font-family:var(--font-mono,monospace);font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.55)}'
 '.cdt-t{font-size:24px;font-weight:340;letter-spacing:-.6px;margin:6px 0 0}.cdt-s{font-size:13px;color:rgba(0,0,0,.6);margin:5px 0 0}'
 '.cdt-cur{text-align:right}.cdt-cur .l{font-family:var(--font-mono,monospace);font-size:10px;opacity:.5;text-transform:uppercase}.cdt-cur .v{font-size:24px;font-weight:700;letter-spacing:-.5px}'
 '.cdt-plot{position:relative;display:flex;align-items:flex-end;gap:16px;height:170px;margin-top:22px}'
 '.cdt-col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px}'
 '.cdt-col .lbl{font-weight:700;font-size:14px}.cdt-col .mm{font-family:var(--font-mono,monospace);font-size:11px;color:rgba(0,0,0,.55)}'
 '.cdt-bar{width:62%;max-width:70px;border-radius:8px 8px 0 0;transition:height .45s cubic-bezier(.22,1,.36,1)}'
 '.cdt-bar.miss{background:repeating-linear-gradient(135deg,transparent,transparent 5px,rgba(0,0,0,.05) 5px,rgba(0,0,0,.05) 6px);border:1.5px dashed rgba(0,0,0,.22);border-bottom:none}'
 '.cdt-note{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);display:flex;justify-content:center;pointer-events:none}.cdt-note span{font-weight:540;font-size:13px;color:rgba(0,0,0,.55);background:rgba(220,238,177,.9);padding:6px 14px;border-radius:50px}'
 '@media(max-width:680px){.cdt{padding:18px 18px}.cdt-plot{height:120px;gap:10px}.cdt-bar{max-width:40px}.cdt-t{font-size:20px}}'
 '@media(prefers-reduced-motion:reduce){.cdt-bar{transition:none}}'
 # --- 발급 이벤트 통합 ---
 '.cde-sec{margin-top:34px}'
 '.cde-eb{font-family:var(--font-mono,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.5)}'
 '.cde-t{font-size:24px;font-weight:340;letter-spacing:-.6px;margin:6px 0 2px}.cde-s{font-size:13.5px;color:rgba(0,0,0,.6);margin:0 0 16px}.cde-s .dim{color:rgba(0,0,0,.45)}'
 '.cde-list{display:flex;flex-direction:column;gap:10px}'
 '.cde-row{display:grid;grid-template-columns:1.6fr auto auto;gap:16px;align-items:center;border:1px solid var(--hairline);border-radius:16px;padding:15px 18px;text-decoration:none;color:#000}'
 '.cde-row.top{background:var(--block-lime);border-color:#000}'
 '.cde-pi{display:flex;align-items:center;gap:11px;min-width:0}.cde-pi .pdot{width:10px;height:10px;border-radius:50%;flex:0 0 auto}'
 '.cde-pn{display:flex;align-items:center;gap:8px}.cde-pn b{font-weight:700;font-size:16px;white-space:nowrap}'
 '.cde-tag{font-family:var(--font-mono,monospace);font-size:9px;padding:3px 8px;border-radius:50px;background:#000;color:#fff}.cde-tag.iss{background:var(--block-cream);color:#000}'
 '.cde-cond{font-size:12.5px;color:rgba(0,0,0,.55);margin-top:4px}'
 '.cde-cash{text-align:right}.cde-cash .cl{font-family:var(--font-mono,monospace);font-size:9px;opacity:.45}.cde-cash .cv{font-size:21px;font-weight:700;letter-spacing:-.5px;white-space:nowrap}'
 '.cde-go{display:inline-flex;align-items:center;gap:6px;padding:11px 17px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:13.5px;white-space:nowrap}.cde-row.top .cde-go{background:var(--accent-magenta)}'
 '.cde-go svg{width:14px;height:14px}'
 '@media(max-width:680px){.cde-row{grid-template-columns:1fr;gap:11px}.cde-cash{text-align:left;display:flex;align-items:baseline;gap:8px}.cde-go{justify-content:center}}'
 # --- 카드 혜택 아코디언(최하단) ---
 '.cda{margin-top:26px;border:1px solid var(--hairline);border-radius:16px;overflow:hidden}'
 '.cda-hd{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:18px 22px;cursor:pointer}'
 '.cda-hd .t{font-weight:700;font-size:16px}.cda-hd .s{font-size:13px;color:rgba(0,0,0,.5);margin-top:2px}'
 '.cda-ic{width:34px;height:34px;border-radius:50%;background:var(--surface-soft);display:flex;align-items:center;justify-content:center;flex:0 0 auto;transition:transform .25s}.cda-ic svg{width:18px;height:18px;color:rgba(0,0,0,.55)}'
 '.cda.open .cda-ic{transform:rotate(180deg)}'
 '.cda-bd{display:none;padding:2px 22px 20px}.cda.open .cda-bd{display:block}'
 # 혜택 렌더 클래스(renderBenefit 재사용)
 '.bhead{font-size:12.5px;color:var(--sub);font-weight:700;margin:6px 0 10px}'
 '.bgrp{border:1px solid var(--line);border-radius:14px;padding:2px 14px;margin-bottom:12px}'
 '.lcap{font-size:12px;font-weight:800;color:var(--accent);padding:11px 0 2px}'
 '.bitem{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}.bitem:last-child{border-bottom:0}'
 '.bareas{flex:1;display:flex;flex-wrap:wrap;gap:5px}.ba{font-size:12px;font-weight:700;color:#55555e;background:var(--surface2);padding:3px 8px;border-radius:6px}'
 '.bval{flex:0 0 auto;text-align:right}.bv{font-size:15px;font-weight:900;color:var(--accent)}.bm{font-size:11px;color:var(--sub);margin-left:3px}'
 '.btier{font-size:10px;font-weight:800;color:#e8a33c;background:#fbf0df;padding:2px 6px;border-radius:5px;margin-left:6px}'
 '.bnone{color:var(--sub);font-size:13.5px;padding:6px 0 14px}'
 # --- 하단 고정 플로팅 CTA ---
 '.cdf{position:fixed;left:0;right:0;bottom:0;z-index:55;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--hairline);padding:12px 0}'
 '.cdf .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px}'
 '.cdf .lab{font-size:14px;font-weight:540;color:rgba(0,0,0,.62);min-width:0}.cdf .lab b{color:#000;font-weight:700}'
 '.cdf .go{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none;white-space:nowrap;flex:0 0 auto}.cdf .go svg{width:16px;height:16px}'
 '@media(max-width:680px){.cdf .lab{font-size:12px}.cdf .go{padding:12px 16px;font-size:14px}}'
 '@media(max-width:480px){.mtab{display:none}.cdf .lab{display:none}.cdf .go{flex:1;justify-content:center}}'
 '</style>'
 '<div style="padding:12px 0"><div class="wrap"><a class="bk" href="cards.html">‹</a></div></div>'
 '<div class="wrap"><div id="root"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div id="cdFloat"></div>')
CARDDETAIL_JS=r"""
var _ARW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg>';
var _UR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M9 7h8v8"/></svg>';
var _CHEV='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>';
var _STAR='<svg class="star" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l2.4 5 5.4.7-3.9 3.7 1 5.4-4.9-2.7-4.9 2.7 1-5.4L4.2 9.7 9.6 9z"/></svg>';
var _qp=new URLSearchParams(location.search);
var id=Number(_qp.get('id'));var nParam=_qp.get('n');
function _nk(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _wmc(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function _man(n){return Math.round((n||0)/10000);}
function _mlbl(m){var mm=(''+m).split('-')[1];return mm?(parseInt(mm,10)+'월'):m;}
Promise.all([
 fetch('cards.json').then(r=>r.json()),
 fetch('events.json').then(r=>r.json()).catch(function(){return {items:[]};}),
 fetch('platform_events.json').then(r=>r.json()).catch(function(){return {products:[]};}),
 fetch('rank.json').then(r=>r.json()).catch(function(){return {items:[]};}),
 fetch('history/index.json').then(r=>r.json()).catch(function(){return {months:[]};})
]).then(function(A){
 var j=A[0],PE=(A[2]&&A[2].products)||[],RK=(A[3]&&A[3].items)||[],HIX=(A[4]&&A[4].months)||[];
 var CH={toss:'토스',cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
 var PCOL={토스:'#3182F6',카드고릴라:'#FF6A13',뱅크샐러드:'#19C37D',아정당:'#1B64DA',네이버페이:'#03C75A',카카오페이:'#FEE500'};
 var card=null,issuer='';
 if(nParam){var nk0=_nk(nParam);
  for(var k in j.cards){var f=(j.cards[k]||[]).filter(function(c){return _nk(c.name)===nk0;})[0];if(f){card=f;issuer=k;break;}}
  if(!card){for(var k2 in j.cards){var f2=(j.cards[k2]||[]).filter(function(c){var cn=_nk(c.name);return cn&&(cn.indexOf(nk0)>=0||nk0.indexOf(cn)>=0);})[0];if(f2){card=f2;issuer=k2;break;}}}
 }
 if(!card&&!isNaN(id)){for(var k3 in j.cards){var f3=(j.cards[k3]||[]).filter(function(c){return c.id===id;})[0];if(f3){card=f3;issuer=k3;break;}}}
 var matchName=card?card.name:(nParam||'');var ck=_nk(matchName);
 var pmatch=PE.filter(function(p){return _nk(p.name)===ck;})[0]||PE.filter(function(p){var pn=_nk(p.name);return pn&&ck&&(pn.indexOf(ck)>=0||ck.indexOf(pn)>=0);})[0];
 if(!card&&pmatch){card={name:pmatch.name,issuer:pmatch.issuer||'',benefit:'',fee:'',detail:null};issuer=pmatch.issuer||'';}
 if(!card){document.getElementById('root').innerHTML='<div class="empty">카드를 찾을 수 없어요. <a class="accent" href="cards.html">카드찾기</a></div>';return;}
 var ckN=_nk(card.name);
 var img=imgTag(card.img||(pmatch&&pmatch.img));
 // ===== 플랫폼별 발급 이벤트(채널) + 카드사 자체 이벤트 분리 =====
 var chEv={},issEv=[];
 if(pmatch){(pmatch.events||[]).forEach(function(e){var w=e.reward_won||0;
   if(CH[e.platform]){var c=chEv[e.platform];if(!c||w>c.won){var _pp=(pmatch.platforms||{})[e.platform]||{};var _u=_best(e.platform,e.url||_pp.url,_pp.id);if(e.platform==='cardgorilla'){var _cg=_cgUrl(pmatch.issuer||issuer,_pp.id);if(_cg)_u=_cg;}chEv[e.platform]={key:e.platform,name:CH[e.platform],won:w,cond:(e.reward_text||''),url:_u};}}
   else if(w>0){issEv.push({won:w,text:(e.reward_text||''),url:(e.url||'')});}
 });}
 var plats=Object.keys(chEv).map(function(k){return chEv[k];}).filter(function(p){return p.won>0;}).sort(function(a,b){return b.won-a.won;});
 var topP=plats[0]||null;var maxCash=topP?topP.won:0;
 // ===== 티라노 순위 =====
 var rkItem=RK.filter(function(x){return _nk(x.name)===ckN;})[0]||RK.filter(function(x){var n=_nk(x.name);return n&&ckN&&(n.indexOf(ckN)>=0||ckN.indexOf(n)>=0);})[0];
 var rankLabel=(rkItem&&rkItem.rank)?(rkItem.rank+'위'):'';
 // ===== 히어로 (플랫폼 버튼 제거 · 순위 추가) =====
 var favOn=(card.id!=null)&&isFav(card.id);
 var favBtn=(card.id!=null)?('<span class="cdh-fav'+(favOn?' on':'')+'" onclick="favClick(this,'+card.id+')">'+favSvg(favOn)+' 관심</span>'):'';
 var stats='';
 if(card.fee)stats+='<div class="st"><span class="sl">연회비</span><span class="sv">'+card.fee+'</span></div>';
 if(maxCash){if(stats)stats+='<div class="sep"></div>';stats+='<div class="st"><span class="sl">최대 캐시백</span><span class="sv">'+_wmc(maxCash)+'</span></div>';}
 if(rankLabel){if(stats)stats+='<div class="sep"></div>';stats+='<div class="st"><span class="sl">'+_STAR+'티라노 순위</span><span class="sv">'+rankLabel+'</span></div>';}
 var heroHtml='<div class="cdhero"><div class="cdh-info"><div class="cdh-eb">'+issuer+' · CARD DETAIL</div><h1 class="cdh-nm">'+card.name+'</h1>'+(card.benefit?'<p class="cdh-tag">'+card.benefit+'</p>':'')
  +'<div class="cdh-stats">'+stats+'</div>'
  +'<div class="cdh-cta">'+favBtn+'<span class="cdh-hint">↓ 아래 발급 이벤트에서 플랫폼·카드사를 선택하세요</span></div>'
  +'<div class="cdh-disc">카드티라노는 발급을 중개·접수하지 않습니다. 신청·발급은 선택한 제휴 플랫폼·카드사 페이지에서 진행됩니다.</div>'
  +'</div><div class="cdh-plate">'+img+'</div></div>';
 // ===== 캐시백 추이 차트(핵심 자리, 항상 노출) =====
 var chartHtml='<div class="cdt"><div class="cdt-h"><div><div class="cdt-eb">티라노차트 · 캐시백 추이</div><h2 class="cdt-t">최근 4개월 최대 캐시백</h2><p class="cdt-s">전 플랫폼 통합 · 당월 포함</p></div>'
  +'<div class="cdt-cur"><div class="l">당월</div><div class="v">'+(maxCash?_wmc(maxCash):'—')+'</div></div></div>'
  +'<div class="cdt-plot" id="cdtPlot"></div></div>';
 // ===== 발급 이벤트 통합 =====
 var rows=plats.map(function(p,pi){var top=(pi===0);
  var href='events.html?platform='+p.key+'&n='+encodeURIComponent(card.name);
  return '<a class="cde-row'+(top?' top':'')+'" href="'+href+'" data-track="plat" data-label="'+p.name+'">'
   +'<div class="cde-pi"><span class="pdot" style="background:'+(PCOL[p.name]||'#888')+'"></span><div><div class="cde-pn"><b>'+p.name+'</b>'+(top?'<span class="cde-tag">최대</span>':'')+'</div>'+(p.cond?'<div class="cde-cond">'+p.cond+'</div>':'')+'</div></div>'
   +'<div class="cde-cash"><div class="cl">캐시백</div><div class="cv">'+_wmc(p.won)+'</div></div>'
   +'<span class="cde-go">자세히 보기 '+_ARW+'</span></a>';
 }).join('');
 // 카드사 직행 버튼은 항상 1개 — 자체 이벤트 있으면 그 행, 없으면 공식 홈
 var issBest=issEv.sort(function(a,b){return b.won-a.won;})[0];
 if(issBest){var ihref=issBest.url||card.url||'#';
  rows+='<a class="cde-row" href="'+ihref+'" target="_blank" rel="sponsored nofollow noopener" data-track="issuer-event" data-label="'+issuer+'">'
   +'<div class="cde-pi"><span class="pdot" style="background:#000"></span><div><div class="cde-pn"><b>'+issuer+' 공식 이벤트</b><span class="cde-tag iss">카드사 공식</span></div><div class="cde-cond">카드사 직접 발급 이벤트</div></div></div>'
   +'<div class="cde-cash"><div class="cl">캐시백</div><div class="cv">'+_wmc(issBest.won)+'</div></div>'
   +'<span class="cde-go">'+issuer+'에서 확인 '+_UR+'</span></a>';
 }else if(card.url){
  rows+='<a class="cde-row" href="'+card.url+'" target="_blank" rel="sponsored nofollow noopener" data-track="official" data-label="'+issuer+'">'
   +'<div class="cde-pi"><span class="pdot" style="background:#000"></span><div><div class="cde-pn"><b>'+issuer+' 공식 홈페이지</b></div><div class="cde-cond">카드사 안내 페이지로 이동</div></div></div>'
   +'<div class="cde-cash"></div>'
   +'<span class="cde-go">바로가기 '+_UR+'</span></a>';
 }
 var eventsHtml=rows?('<div class="cde-sec"><div class="cde-eb">발급 이벤트</div><h2 class="cde-t">어디서 받을지 골라보세요</h2><p class="cde-s">플랫폼별 발급 이벤트와 카드사 공식 이벤트를 한곳에. <span class="dim">캐시백 많은 순 · 공개 데이터 기준 자동 정렬</span></p><div class="cde-list">'+rows+'</div></div>'):'';
 // ===== 카드 혜택 = 최하단 접힘 아코디언 =====
 var accHtml='<div class="cda" id="cdAcc"><div class="cda-hd" id="cdAccHd"><div><div class="t">카드 혜택 · 상품 정보</div><div class="s">눌러서 펼치기 — 적립·할인 등 상품 상세</div></div><span class="cda-ic">'+_CHEV+'</span></div><div class="cda-bd">'+renderBenefit(card.detail)+'</div></div>';
 document.getElementById('root').innerHTML=heroHtml+chartHtml+eventsHtml+accHtml;
 document.title=card.name+' | 카드티라노';
 // 아코디언 토글
 var acc=document.getElementById('cdAcc'),accHd=document.getElementById('cdAccHd');
 if(accHd)accHd.onclick=function(){acc.classList.toggle('open');};
 // 하단 고정 플로팅 CTA — 최대 캐시백 플랫폼 이벤트로 이동
 if(topP){var fhref='events.html?platform='+topP.key+'&n='+encodeURIComponent(card.name);
  document.getElementById('cdFloat').innerHTML='<div class="cdf"><div class="wrap"><div class="lab">최대 캐시백 <b>'+_wmc(maxCash)+'</b> · '+topP.name+'에서 가장 큼</div><a class="go" href="'+fhref+'">'+topP.name+' 이벤트 보기 '+_ARW+'</a></div></div>';}
 // ===== 차트 데이터(히스토리 스냅샷) 비동기 로드 =====
 var _now=new Date();var _cm=_now.getFullYear()+'-'+('0'+(_now.getMonth()+1)).slice(-2);
 var months=HIX.slice().sort().filter(function(m){return m<_cm;}).slice(-3).concat([_cm]);
 if(months.length<2)months=[_cm];
 Promise.all(months.map(function(m){return m===_cm?Promise.resolve(null):fetch('history/'+m+'.json').then(function(r){return r.json();}).catch(function(){return null;});})).then(function(MS){
  var series=months.map(function(m,i){if(m===_cm)return {m:m,v:(maxCash||0)};
   var snap=MS[i],v=null;if(snap){var c=(snap.cards||[]).filter(function(x){return _nk(x.name)===ckN;})[0];if(c&&c.max)v=c.max;
    if(v==null&&snap.issuers&&issuer&&snap.issuers[issuer]){var im=snap.issuers[issuer];var vv=Object.keys(im).map(function(k){return im[k];});if(vv.length)v=Math.max.apply(null,vv);}}
   return {m:m,v:v};});
  var vals=series.filter(function(s){return s.v!=null&&s.v>0;}).map(function(s){return s.v;});
  var plot=document.getElementById('cdtPlot');if(!plot)return;
  if(!vals.length){plot.innerHTML=series.map(function(s){return '<div class="cdt-col"><div class="cdt-bar miss" style="height:26px"></div><div class="mm">'+_mlbl(s.m)+'</div></div>';}).join('')+'<div class="cdt-note"><span>이번 달 집계된 캐시백이 아직 없어요</span></div>';return;}
  var peak=Math.max.apply(null,vals);var scale=Math.max(peak*1.12,10000);
  plot.innerHTML=series.map(function(s,i){var last=(i===series.length-1);
   if(s.v==null||s.v<=0)return '<div class="cdt-col"><div class="lbl" style="opacity:.4">—</div><div class="cdt-bar miss" style="height:24px"></div><div class="mm">'+_mlbl(s.m)+'</div></div>';
   var hp=Math.max(s.v/scale*100,4);var bg=last?'var(--accent-magenta)':'var(--block-navy)';
   return '<div class="cdt-col"><div class="lbl" style="color:'+(last?'var(--accent-magenta)':'#000')+'">'+_man(s.v)+'만</div><div class="cdt-bar" style="height:'+hp+'%;background:'+bg+'"></div><div class="mm">'+_mlbl(s.m)+'</div></div>';
  }).join('');
 });
});
"""

# ===== EVENT DETAIL (이벤트 상세, 차트 최우선) =====
EVENTDETAIL_BODY=('<style>'
 '#root,.rg-wrap{}'
 '.rg-wrap{max-width:1080px;margin:0 auto;padding:0 20px 96px}'
 '.rg-back{display:inline-flex;align-items:center;gap:6px;color:var(--text);font-weight:600;font-size:14px;padding:16px 0 6px}'
 '.rg-head{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;padding:8px 0 4px}'
 '.rg-pchip{display:inline-flex;align-items:center;gap:10px;background:var(--surface-soft);padding:8px 16px 8px 12px;border-radius:50px}.rg-pchip i{width:14px;height:14px;border-radius:50%}.rg-pchip b{font-weight:700;font-size:24px;letter-spacing:-.6px;line-height:1}.rg-pchip .mono{font-family:var(--font-mono,monospace);font-size:10px;color:rgba(0,0,0,.45)}'
 '.rg-h{font-weight:340;font-size:38px;line-height:1.02;letter-spacing:-1.2px;margin:14px 0 0}'
 '.rg-sub{font-weight:400;font-size:15px;color:rgba(0,0,0,.62);margin:10px 0 0}.rg-sub b{font-weight:700}'
 '.rg-cta{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none;margin-top:18px}.rg-cta svg{width:17px;height:17px}'
 '.rg-deco{width:200px;height:160px;flex-shrink:0;background:var(--block-lime);border-radius:20px;display:flex;align-items:center;justify-content:center;overflow:hidden}.rg-deco svg{width:96px;height:80px;color:#33402a;opacity:.9}'
 '.rg-sec{margin-top:30px}'
 '.rg-sec-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap}'
 '.rg-eb{font-family:var(--font-mono,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.5)}'
 '.rg-t{font-weight:340;font-size:24px;letter-spacing:-.6px;margin:6px 0 0}'
 '.rg-hint{font-weight:400;font-size:13px;color:rgba(0,0,0,.5)}'
 '.rg-plist{display:flex;flex-direction:column;gap:8px;margin-top:14px}'
 '.rg-prow{display:grid;grid-template-columns:auto 1fr auto auto;gap:16px;align-items:center;border:1px solid var(--hairline);background:#fff;border-radius:14px;padding:12px 16px;cursor:pointer;text-align:left;width:100%;font:inherit;color:inherit}'
 '.rg-prow.sel{border:2px solid #000;background:var(--surface-soft)}'
 '.rg-pl{width:62px;flex-shrink:0;aspect-ratio:1.586/1;border-radius:8px;overflow:hidden;background:var(--surface-soft)}.rg-pl img{width:100%;height:100%;object-fit:cover;display:block}'
 '.rg-pn{display:flex;align-items:center;gap:7px}.rg-pn b{font-weight:700;font-size:16px}.rg-pi{font-family:var(--font-mono,monospace);font-size:10px;opacity:.5;margin-top:3px}'
 '.rg-tag{font-family:var(--font-mono,monospace);font-size:9px;padding:3px 8px;border-radius:50px}.rg-tag.mx{background:#000;color:#fff}.rg-tag.se{background:var(--accent-magenta);color:#fff}'
 '.rg-pcash{text-align:right}.rg-pcash .l{font-family:var(--font-mono,monospace);font-size:9px;opacity:.45}.rg-pcash .v{font-weight:700;font-size:20px;letter-spacing:-.4px;white-space:nowrap}'
 '.rg-parr{width:18px;height:18px;color:rgba(0,0,0,.35)}'
 '.rg-chart{background:var(--block-lime);border-radius:22px;padding:28px 30px;margin-top:14px}'
 '.rg-chart-h{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:10px}'
 '.rg-sums{display:flex;gap:18px}.rg-sums>div{text-align:right}.rg-sums .l{font-family:var(--font-mono,monospace);font-size:9px;opacity:.5}.rg-sums .v{font-weight:700;font-size:22px}'
 '.rg-bars{display:flex;align-items:flex-end;gap:16px;height:190px;margin-top:22px}.rg-bars.rg-note{position:relative}'
 '.rg-col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px}'
 '.rg-col .lbl{font-weight:700;font-size:14px}.rg-col .mm{font-family:var(--font-mono,monospace);font-size:11px;color:rgba(0,0,0,.55)}'
 '.rg-bar{width:54%;max-width:62px;border-radius:8px 8px 0 0;background:var(--block-navy);transition:height .4s}'
 '.rg-bar.miss{background:repeating-linear-gradient(135deg,transparent,transparent 5px,rgba(0,0,0,.05) 5px,rgba(0,0,0,.05) 6px);border:1.5px dashed rgba(0,0,0,.22);border-bottom:none}'
 '.rg-curbar{width:54%;max-width:62px;border-radius:8px 8px 0 0;overflow:hidden;display:flex;flex-direction:column;transition:height .4s}.rg-curbar .sub{background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.55)),var(--accent-magenta)}.rg-curbar .main{flex:1;background:var(--accent-magenta)}'
 '.rg-note-c{position:absolute;left:0;right:0;top:42%;text-align:center}.rg-note-c span{font-weight:540;font-size:13px;color:rgba(0,0,0,.55);background:rgba(220,238,177,.9);padding:6px 14px;border-radius:50px}'
 '.rg-legend{display:flex;align-items:center;gap:18px;margin-top:18px;flex-wrap:wrap}.rg-legend span{display:inline-flex;align-items:center;gap:7px;font-size:13px;color:rgba(0,0,0,.6)}.rg-legend i{width:12px;height:12px;border-radius:3px;display:inline-block}'
 '.rg-main{background:var(--block-navy);color:#fff;border-radius:18px;padding:22px 26px;margin-top:14px}.rg-main .l{font-family:var(--font-mono,monospace);font-size:10px;opacity:.6;margin-bottom:12px}.rg-main .row{display:flex;align-items:center;justify-content:space-between;gap:16px}.rg-main .row .t{font-weight:540;font-size:16px;opacity:.92}.rg-main .row .v{font-weight:700;font-size:24px;letter-spacing:-.5px;white-space:nowrap}'
 '.rg-subh{font-family:var(--font-mono,monospace);font-size:10px;color:rgba(0,0,0,.5);margin:16px 0 12px}'
 '.rg-subs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}'
 '.rg-sub{border:1px solid var(--hairline);border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:12px}.rg-sub .ic{width:38px;height:38px;border-radius:50%;background:var(--surface-soft);display:flex;align-items:center;justify-content:center;flex-shrink:0}.rg-sub .ic svg{width:20px;height:20px;color:#000}.rg-sub .t{font-weight:700;font-size:14px}.rg-sub .c{font-size:12px;color:rgba(0,0,0,.55);margin-top:2px}.rg-sub .v{font-weight:700;font-size:14px;margin-left:auto;white-space:nowrap}'
 '.rg-subnone{color:rgba(0,0,0,.5);font-size:13px;padding:6px 0}'
 '.rg-coach{background:var(--surface-soft);border-radius:20px;padding:26px 28px;margin-top:14px;display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center}'
 '.rg-coach-ring{width:84px;height:84px;border-radius:50%;border:3px solid currentColor;color:var(--success);display:flex;align-items:center;justify-content:center;margin:0 auto}.rg-coach-ring.hold{color:#cf9220}.rg-coach-ring.no{color:rgba(0,0,0,.3)}.rg-coach-ring span{width:46px;height:46px;border-radius:50%;border:3px solid currentColor;display:block}'
 '.rg-coach-badge{text-align:center}.rg-coach-badge .lab{font-weight:700;font-size:16px;margin-top:10px}.rg-coach-badge .mono{font-family:var(--font-mono,monospace);font-size:9px;opacity:.5;margin-top:2px}'
 '.rg-coach-body .t{font-weight:540;font-size:19px;letter-spacing:-.4px;line-height:1.35}.rg-coach-leg{display:flex;gap:18px;margin-top:16px;flex-wrap:wrap}.rg-coach-leg span{font-size:13px;color:rgba(0,0,0,.65)}'
 '.rg-others{display:flex;flex-direction:column;gap:10px;margin-top:14px}'
 '.rg-orow{display:grid;grid-template-columns:auto 1fr auto auto;gap:16px;align-items:center;border:1px solid var(--hairline);border-radius:16px;padding:14px 18px;text-decoration:none;color:#000}'
 '.rg-otag{display:inline-block;padding:4px 10px;border-radius:50px;font-family:var(--font-mono,monospace);font-size:9px;text-transform:uppercase;margin-bottom:6px}'
 '.rg-foot{font-size:12px;color:rgba(0,0,0,.45);margin:28px 0 10px;line-height:1.6}.rg-foot b{font-weight:600;color:rgba(0,0,0,.6)}'
 '.rg-float{position:fixed;left:0;right:0;bottom:0;z-index:55;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--hairline);padding:12px 0}.rg-float .in{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;gap:14px}.rg-float .lab{font-size:14px;font-weight:540;color:rgba(0,0,0,.62)}.rg-float .lab b{color:#000;font-weight:700}.rg-float .go{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none;white-space:nowrap}.rg-float .go svg{width:16px;height:16px}'
 '@media(max-width:680px){.rg-head{grid-template-columns:1fr;gap:14px}.rg-deco{width:100%;height:96px}.rg-h{font-size:25px}.rg-prow{grid-template-columns:auto 1fr auto;gap:12px}.rg-parr{display:none}.rg-chart{padding:18px}.rg-bars{height:130px;gap:10px}.rg-subs{grid-template-columns:1fr}.rg-coach{grid-template-columns:1fr;gap:14px;text-align:center}.rg-coach-leg{justify-content:center}.rg-float .lab{display:none}.rg-float .go{flex:1;justify-content:center}.mtab{display:none}}'
 '@media(prefers-reduced-motion:reduce){.rg-bar,.rg-curbar{transition:none}}'
 '</style>'
 '<div class="rg-wrap"><a class="rg-back" href="issue.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 6l-6 6 6 6"/></svg>이번달 캐시백으로</a>'
 '<div id="edroot"><div class="empty" style="padding:60px 0"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div id="rgFloat"></div>')
EVENTDETAIL_JS=r"""
var PBC={cardgorilla:'#FF6A13',banksalad:'#19C37D',toss:'#3182F6',ajungdang:'#1B64DA',naver:'#03C75A',kakaopay:'#FEE500'};
var PNM={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
var PLATEC=['var(--block-lilac)','var(--block-coral)','var(--block-mint)','var(--block-cream)','var(--block-navy)','var(--block-lime)'];
function _nk(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _wm(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function _man(n){return n?Math.round(n/10000):0;}
function _mlabel(m){var mm=(''+m).split('-')[1];return mm?(parseInt(mm,10)+'월'):m;}
function _short(nm){nm=(nm||'').replace(/^(삼성|현대|KB국민|국민|신한|롯데|우리|하나|BC|비씨|NH농협|농협|IBK기업|기업|토스)카?드?\s*/,'');return nm.slice(0,4)||(nm||'').slice(0,4);}
var ARW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg>';
var UR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M9 7h8v8"/></svg>';
var _qp=new URLSearchParams(location.search);
var qPlat=_qp.get('platform')||_qp.get('p')||'';var qn=_qp.get('n')||'';var qid=_qp.get('card')||_qp.get('id')||'';
Promise.all([
 fetch('platform_events.json?t='+Date.now()).then(function(r){return r.json();}).catch(function(){return{products:[]};}),
 fetch('cards.json').then(function(r){return r.json();}).catch(function(){return{cards:{}};}),
 fetch('history/index.json').then(function(r){return r.json();}).catch(function(){return{months:[]};})
]).then(function(A){
 var _now=new Date();var _cm=_now.getFullYear()+'-'+('0'+(_now.getMonth()+1)).slice(-2);
 var PE=A[0].products||[],cj=A[1].cards||{},HIX=A[2].months||[];
 var months=HIX.slice().sort().filter(function(m){return m<_cm;}).slice(-3).concat([_cm]);
 var ID2={};for(var k in cj){(cj[k]||[]).forEach(function(c){if(c.id!=null)ID2[String(c.id)]=_nk(c.name);});}
 var root=document.getElementById('edroot');
 var focusNk=qn?_nk(qn):(qid&&ID2[String(qid)]?ID2[String(qid)]:'');
 var P=qPlat;
 if(!P&&focusNk){var fp=PE.filter(function(p){return _nk(p.name)===focusNk;})[0];if(fp){var mx=0;(fp.events||[]).forEach(function(e){if((e.reward_won||0)>mx){mx=e.reward_won;P=e.platform;}});}}
 if(!P){root.innerHTML='<div class="empty" style="padding:60px 0">플랫폼 정보가 없어요. <a class="accent" href="issue.html">이번달 캐시백</a></div>';return;}
 function evOf(p){return (p.events||[]).filter(function(e){return e.platform===P&&e.reward_won;}).sort(function(a,b){return b.reward_won-a.reward_won;})[0];}
 // 캠페인 키 = 이벤트 랜딩 URL(쿼리·해시 제거). 같은 URL = 같은 발급 캐시백(캠페인).
 function _cu(p,e){var pp=(p.platforms||{})[P]||{};var u=(e&&e.url)||pp.url||'';return (''+u).split('?')[0].split('#')[0].replace(/\/+$/,'');}
 var platGroup=PE.map(function(p){var e=evOf(p);return e?{p:p,e:e,cu:_cu(p,e)}:null;}).filter(Boolean).sort(function(a,b){return b.e.reward_won-a.e.reward_won;});
 if(!platGroup.length){root.innerHTML='<div class="empty" style="padding:60px 0">이 플랫폼의 발급 캐시백이 없어요. <a class="accent" href="issue.html">이번달 캐시백</a></div>';return;}
 var anchor=(focusNk?platGroup.filter(function(g){return _nk(g.p.name)===focusNk;})[0]:null)||platGroup[0];
 var campaignCu=anchor.cu;
 var sameCu=campaignCu?platGroup.filter(function(g){return g.cu===campaignCu;}):[anchor];
 // 진짜 캠페인 = 2개 이상이 같은 URL 공유 & 플랫폼 전체는 아님(네이버 등 제네릭 랜딩 제외). 그 외 = 진입 카드 1건.
 var isCampaign=(sameCu.length>=2 && sameCu.length<platGroup.length);
 var group=(isCampaign?sameCu.slice():[anchor]).sort(function(a,b){return b.e.reward_won-a.e.reward_won;});
 var focusIdx=0;for(var gi=0;gi<group.length;gi++){if(group[gi]===anchor){focusIdx=gi;break;}}
 var col=PBC[P]||'#888',pnm=PNM[P]||P;
 Promise.all(months.map(function(m){return m===_cm?Promise.resolve(null):fetch('history/'+m+'.json').then(function(r){return r.json();}).catch(function(){return null;});})).then(function(MS){
  var head='<div class="rg-head"><div><div class="rg-pchip"><i style="background:'+col+'"></i><b>'+pnm+'</b><span class="mono">플랫폼</span></div>'
   +'<h1 class="rg-h">이번달 발급 캐시백</h1>'
   +'<p class="rg-sub">'+(group.length>1?(pnm+'의 이 발급 캐시백 이벤트에 <b>'+group.length+'개 카드</b>가 함께 들어 있어요.'):(pnm+'에서 <b>'+anchor.p.name+'</b>를 발급하면 받는 캐시백이에요.'))+'</p>'
   +'<a class="rg-cta" id="rgHeadCta" href="#" target="_blank" rel="sponsored nofollow noopener">'+pnm+'에서 자세히보기 '+UR+'</a></div>'
   +'<div class="rg-deco"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></div></div>';
  var listRows=group.map(function(g,i){var p=g.p,e=g.e;var pc=PLATEC[i%6];var ink=(pc.indexOf('navy')>=0)?'#fff':'#000';
   return '<button type="button" class="rg-prow'+(i===focusIdx?' sel':'')+'" data-i="'+i+'"><div class="rg-pl">'+imgTag(p.img)+'</div>'
    +'<div><div class="rg-pn"><b>'+p.name+'</b>'+(i===0?'<span class="rg-tag mx">최대</span>':'')+'<span class="rg-tag se" data-sel hidden>선택됨</span></div><div class="rg-pi">'+(p.issuer||'')+'</div></div>'
    +'<div class="rg-pcash"><div class="l">최대 캐시백</div><div class="v">'+_wm(e.reward_won)+'</div></div>'
    +'<svg class="rg-parr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></button>';
  }).join('');
  var listSec=group.length>1?('<div class="rg-sec"><div class="rg-sec-h"><div><div class="rg-eb">발급 캐시백 그룹</div><h2 class="rg-t">이 캐시백을 받는 카드</h2></div><span class="rg-hint">상품을 누르면 아래 차트·구성이 바뀌어요</span></div><div class="rg-plist" id="rgList">'+listRows+'</div></div>'):'';
  root.innerHTML=head+listSec+'<div id="rgDyn"></div>';
  function buildSeries(p,e){var nk=_nk(p.name);var total=e.reward_won||0,bonus=e.bonus_won||0;if(bonus>=total)bonus=0;var main=Math.max(total-bonus,0);
   var series=months.map(function(m,i){if(m===_cm)return {m:m,v:total,main:main,sub:bonus,cur:true};
    var snap=MS[i],v=null;if(snap){var c=(snap.cards||[]).filter(function(x){return _nk(x.name)===nk;})[0];if(c&&c.max)v=c.max;
     if(v==null&&snap.issuers&&p.issuer&&snap.issuers[p.issuer]){var im=snap.issuers[p.issuer];var vv=Object.keys(im).map(function(kk){return im[kk];});if(vv.length)v=Math.max.apply(null,vv);}}
    return {m:m,v:v};});
   return {series:series,total:total,main:main,sub:bonus};}
  function renderDyn(i){var g=group[i],p=g.p,e=g.e;var S=buildSeries(p,e);
   var vals=S.series.filter(function(s){return s.v!=null&&s.v>0;}).map(function(s){return s.v;});
   var peak=vals.length?Math.max.apply(null,vals):S.total;var scale=Math.max(peak*1.12,10000);
   var bars=S.series.map(function(s){
    if(s.cur){var hp=Math.max(s.v/scale*100,4);var subH=s.v?(s.sub/s.v*100):0;
     return '<div class="rg-col"><div class="lbl" style="color:var(--accent-magenta)">'+_man(s.v)+'만</div><div class="rg-curbar" style="height:'+hp+'%">'+(s.sub>0?'<div class="sub" style="height:'+subH+'%"></div>':'')+'<div class="main"></div></div><div class="mm" style="color:var(--accent-magenta);font-weight:700">이번달('+_mlabel(s.m)+')</div></div>';}
    if(s.v==null||s.v<=0)return '<div class="rg-col"><div class="lbl" style="opacity:.4">—</div><div class="rg-bar miss" style="height:24px"></div><div class="mm">'+_mlabel(s.m)+'</div></div>';
    var hp2=Math.max(s.v/scale*100,4);
    return '<div class="rg-col"><div class="lbl">'+_man(s.v)+'만</div><div class="rg-bar" style="height:'+hp2+'%"></div><div class="mm">'+_mlabel(s.m)+'</div></div>';
   }).join('');
   var hasCur=S.total>0;var emptyNote=hasCur?'':'<div class="rg-note-c"><span>이번 달 집계된 캐시백이 아직 없어요</span></div>';
   var chart='<div class="rg-sec"><div class="rg-chart"><div class="rg-chart-h"><div><div class="rg-eb">티라노차트 · 캐시백 추이</div><h2 class="rg-t">'+p.name+' · 최근 4개월</h2></div>'
    +'<div class="rg-sums"><div><div class="l">당월 전체</div><div class="v">'+(S.total?_wm(S.total):'—')+'</div></div><div><div class="l">주요</div><div class="v" style="color:var(--block-navy)">'+(S.main?_wm(S.main):'—')+'</div></div><div><div class="l">부가</div><div class="v" style="color:rgba(31,29,61,.55)">'+(S.sub?_wm(S.sub):'—')+'</div></div></div></div>'
    +'<div class="rg-bars'+(hasCur?'':' rg-note')+'">'+bars+emptyNote+'</div>'
    +'<div class="rg-legend"><span><i style="background:var(--accent-magenta)"></i>이번달 · 주요</span><span><i style="background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.55)),var(--accent-magenta)"></i>이번달 · 부가</span><span><i style="background:var(--block-navy)"></i>직전 3개월</span></div></div></div>';
   var subItems='';var bd=(e.breakdown||[]).filter(function(b){return b.won&&b.won>0&&b.won<S.total;});
   if(S.sub>0){if(bd.length){subItems=bd.map(function(b){return '<div class="rg-sub"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg></span><div><div class="t">부가 캐시백</div><div class="c">'+(b.text||'조건 충족 시')+'</div></div><span class="v">+'+_wm(b.won)+'</span></div>';}).join('');}
    else{subItems='<div class="rg-sub"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg></span><div><div class="t">부가 캐시백</div><div class="c">조건 충족 시</div></div><span class="v">+'+_wm(S.sub)+'</span></div>';}}
   var comp='<div class="rg-sec"><div class="rg-eb">캐시백 구성</div><h2 class="rg-t">전체 캐시백 구성</h2><p class="rg-hint" style="margin-top:4px"><b style="font-weight:700;color:#000">'+p.name+'</b> 기준 · 주요(조건 금액 이상 이용 시) + 부가(조건별)</p>'
    +'<div class="rg-main"><div class="l">주요 캐시백</div><div class="row"><span class="t">조건 금액 이상 이용 시</span><span class="v">'+(S.main?_wm(S.main):'—')+'</span></div></div>'
    +(S.sub>0?('<div class="rg-subh">부가 캐시백 · 조건별</div><div class="rg-subs">'+subItems+'</div>'):'<div class="rg-subh">부가 캐시백</div><div class="rg-subnone">이 상품은 부가 캐시백 없이 주요 캐시백으로 구성돼요.</div>')+'</div>';
   var maxOther=0;(p.events||[]).forEach(function(x){if(x.platform!==P&&(x.reward_won||0)>maxOther)maxOther=x.reward_won;});
   var rec=(S.total>=maxOther)?'rec':(S.total>=maxOther*0.8?'hold':'no');
   var recLab=rec==='rec'?'추천':(rec==='hold'?'보류':'비추천');var recCls=rec==='rec'?'':(rec==='hold'?'hold':'no');
   var recColor=rec==='rec'?'var(--success)':(rec==='hold'?'#cf9220':'rgba(0,0,0,.55)');
   var recMsg=rec==='rec'?(p.name+'은 지금 '+pnm+' 발급이 유리해요.'+(maxOther?' 다른 채널보다 최대 '+_wm(S.total-maxOther)+' 더 받아요.':'')):(rec==='hold'?(pnm+' 캐시백도 괜찮지만, 다른 채널이 최대 '+_wm(maxOther-S.total)+' 더 클 수 있어요.'):('다른 채널이 최대 '+_wm(maxOther-S.total)+' 더 커요. 비교 후 결정하세요.'));
   var coach='<div class="rg-sec"><div class="rg-eb">티라노 코칭</div><h2 class="rg-t">발급 적기</h2><div class="rg-coach"><div class="rg-coach-badge"><span class="rg-coach-ring '+recCls+'"><span></span></span><div class="lab" style="color:'+recColor+'">'+recLab+'</div><div class="mono">티라노 코칭</div></div>'
    +'<div class="rg-coach-body"><div class="t">'+recMsg+'</div><div class="rg-coach-leg"><span>○ 추천 — 지금 발급</span><span>△ 보류 — 추이 지켜보기</span><span>✕ 비추천 — 다음 달 권장</span></div></div></div></div>';
   var nk=_nk(p.name);var orows=[];
   var op=null,opw=0;(p.events||[]).forEach(function(x){if(x.platform!==P&&(x.reward_won||0)>opw){opw=x.reward_won;op=x;}});
   if(op&&opw>S.total)orows.push({tag:'다른 플랫폼 · 더 큼',tagBg:'var(--block-lime)',tagFg:'#000',name:p.name,issuer:p.issuer,plat:op.platform,amt:opw,img:p.img,href:'events.html?platform='+op.platform+'&n='+encodeURIComponent(p.name)});
   var si=PE.filter(function(q){return q.issuer===p.issuer&&_nk(q.name)!==nk;}).map(function(q){var ee=evOf(q);return ee?{q:q,w:ee.reward_won}:null;}).filter(Boolean).sort(function(a,b){return b.w-a.w;})[0];
   if(si)orows.push({tag:'같은 카드사 · '+pnm,tagBg:'var(--surface-soft)',tagFg:'rgba(0,0,0,.7)',name:si.q.name,issuer:si.q.issuer,plat:P,amt:si.w,img:si.q.img,href:'events.html?platform='+P+'&n='+encodeURIComponent(si.q.name)});
   var top=group[0];if(top&&top.e.reward_won!==S.total)orows.push({tag:'이번달 최대 혜택',tagBg:'#000',tagFg:'#fff',name:top.p.name,issuer:top.p.issuer,plat:P,amt:top.e.reward_won,img:top.p.img,href:'events.html?platform='+P+'&n='+encodeURIComponent(top.p.name)});
   var othersHtml=orows.length?('<div class="rg-sec"><h2 class="rg-t">이런 이벤트도 있어요</h2><div class="rg-others">'+orows.map(function(o){var oc=PBC[o.plat]||'#888';return '<a class="rg-orow" href="'+o.href+'"><div class="rg-pl" style="width:54px">'+imgTag(o.img)+'</div><div><span class="rg-otag" style="background:'+o.tagBg+';color:'+o.tagFg+'">'+o.tag+'</span><div class="rg-pn"><b style="font-size:15px">'+o.name+'</b></div><div class="rg-pi"><i style="display:inline-block;width:6px;height:6px;border-radius:50%;background:'+oc+';margin-right:5px"></i>'+(o.issuer||'')+' · '+(PNM[o.plat]||o.plat)+'</div></div><div class="rg-pcash"><div class="l">캐시백</div><div class="v">'+_wm(o.amt)+'</div></div><svg class="rg-parr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a>';}).join('')+'</div></div>'):'';
   var foot='<div class="rg-foot">· 표기된 캐시백·조건은 공개 데이터 수집 시점 기준이며 실제 적용 금액·조건은 달라질 수 있어요. <b>상세한 캐시백 정보는 각 플랫폼사에서 최종 확인하세요.</b> 카드티라노는 발급을 중개·접수하지 않는 광고·정보제공 매체입니다.</div>';
   document.getElementById('rgDyn').innerHTML=chart+comp+coach+othersHtml+foot;
   var _ppd=(p.platforms||{})[P]||{};var edUrl=_best(P,e.url||_ppd.url,_ppd.id);if(P==='cardgorilla'){var _cg=_cgUrl(p.issuer,_ppd.id);if(_cg)edUrl=_cg;}if(!edUrl)edUrl=e.url||'#';
   var hc=document.getElementById('rgHeadCta');if(hc)hc.setAttribute('href',edUrl);
   document.getElementById('rgFloat').innerHTML='<div class="rg-float"><div class="in"><div class="lab"><b>'+pnm+'</b> 발급 캐시백 · 최대 '+_wm(S.total)+'</div><a class="go" href="'+edUrl+'" target="_blank" rel="sponsored nofollow noopener">'+pnm+'에서 자세히보기 '+UR+'</a></div></div>';
   document.title=pnm+' 발급 캐시백 · '+p.name+' | 카드티라노';
   if(window.repairImages)repairImages();
  }
  var listEl=document.getElementById('rgList');
  if(listEl){listEl.addEventListener('click',function(ev2){var b=ev2.target.closest('.rg-prow');if(!b)return;var i=+b.getAttribute('data-i');
   listEl.querySelectorAll('.rg-prow').forEach(function(x){x.classList.remove('sel');var s=x.querySelector('[data-sel]');if(s)s.hidden=true;});
   b.classList.add('sel');var sb=b.querySelector('[data-sel]');if(sb)sb.hidden=false;renderDyn(i);});}
  renderDyn(focusIdx);
  if(listEl){var selB=listEl.querySelector('.rg-prow.sel [data-sel]');if(selB)selB.hidden=false;
  if(focusIdx>0){var fb=listEl.querySelector('.rg-prow[data-i="'+focusIdx+'"]');if(fb)fb.scrollIntoView({block:'nearest'});}}
 });
}).catch(function(){var r=document.getElementById('edroot');if(r)r.innerHTML='<div class="empty" style="padding:60px 0">데이터를 불러오지 못했어요.</div>';});
"""

# ===== CHART (독자 인기순위) =====
CHART_BODY=('<style>'
 '.crow{display:flex;align-items:center;gap:15px;padding:14px 4px;border-bottom:1px solid var(--line)}'
 '.crow .no{width:26px;font-size:18px;font-weight:900;text-align:center;font-style:italic}.crow .no.top{color:var(--accent)}'
 '.crow .pl{width:74px;height:47px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;overflow:hidden;border-radius:6px;background:#eef0f3}'
 '.crow .pl img{width:100%;height:100%;object-fit:cover;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.14)}.crow .pl .ph{font-size:22px}'
 '.crow .ci{flex:1;min-width:0}.crow .cn{font-size:14.5px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.crow .cs{font-size:11.5px;color:var(--sub);margin-top:3px}.crow .src{color:var(--dim)}'
 '</style>'
 '<div class="wrap">'
 +tybnr("chart.html","CARDTYRANNO · 티라노차트","시중 플랫폼 순위를 한 표로","토스·카드고릴라·뱅크샐러드 2곳 이상에서 공통 발급되는 범용 카드만 순위 평균을 냈어요.")
 +'<section><div class="sec-h"><h2>티라노차트</h2></div>'
 '<div class="muted" style="font-size:12.5px;padding-bottom:10px">여러 플랫폼에서 공통 발급되는 범용 카드 순위 평균이에요. (특정 채널 전용 제휴카드 제외)</div>'
 '<div class="tabs" id="tabs"></div><div id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></section></div>')
CHART_JS=r"""
var R=[],ORD=[],cur="전체";
function render(){var items=cur==="전체"?R:R.filter(function(x){return x.issuer===cur;});
 document.getElementById('list').innerHTML=items.map(function(x,i){var rs=[];if(x.toss)rs.push('토스 '+x.toss+'위');if(x.cg)rs.push('고릴라 '+x.cg+'위');if(x.bs)rs.push('뱅샐 '+x.bs+'위');
  var href=(x.id!=null)?('carddetail.html?id='+x.id):'cards.html';var rk=i+1;
  return '<a class="crow" href="'+href+'"><span class="no'+(rk<=3?' top':'')+'">'+rk+'</span><span class="pl">'+imgTag(x.img)+'</span><div class="ci"><div class="cn">'+x.name+'</div><div class="cs">'+(x.issuer||'')+' · <span class="src">'+rs.join(' / ')+'</span></div></div></a>';}).join("");}
function tabs(){var T=["전체"].concat(ORD);var t=document.getElementById('tabs');t.innerHTML=T.map(function(o){return '<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'</div>';}).join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};});}
function _nk(s){return (s||'').replace(/[\s()（）·\-_/+]+/g,'').toLowerCase();}
/* 채널 전용 제휴카드 제외: (1)카드명에 토스/toss 포함, (2)1개 플랫폼에서만 노출되는 카드.
   → 여러 플랫폼(토스·카드고릴라·뱅크샐러드)에서 공통 발급되는 범용 카드만 순위 산출. */
function _isChannelExclusive(n){n=(n||'').toLowerCase();return n.indexOf('토스')>=0||n.indexOf('toss')>=0;}
function _platCount(x){var c=0;if(x.toss)c++;if(x.cg)c++;if(x.bs)c++;return c;}
function _universal(x){return _platCount(x)>=2&&!_isChannelExclusive(x.name);}
Promise.all([fetch('rank.json').then(r=>r.json()),fetch('cards.json').then(r=>r.json())]).then(function(a){
 R=(a[0].items||[]).filter(_universal);var m={};for(var k in a[1].cards){(a[1].cards[k]||[]).forEach(function(c){m[_nk(c.name)]=c.id;});}
 R.forEach(function(x){var k=_nk(x.name);if(m[k]!=null)x.id=m[k];else{var alt=_nk((x.name||'').replace(/^토스\s*/,''));if(m[alt]!=null)x.id=m[alt];}});
 ORD=[...new Set(R.map(function(x){return x.issuer;}).filter(Boolean))];tabs();render();});
"""

# ===== FAVORITES (관심카드) =====
FAV_BODY=('<style>'
 '.pushbox{display:flex;align-items:center;justify-content:space-between;gap:14px;border:1px solid var(--hairline,#e6e6e6);border-radius:16px;padding:15px 17px;margin:6px 0 18px;background:var(--surface-soft,#fafafa)}'
 '.pushbox .pb-t{font-weight:800;font-size:14.5px}'
 '.pushbox .pb-d{font-size:12px;color:#666;margin-top:3px;line-height:1.5;max-width:none}'
 '.pb-sw{position:relative;flex:0 0 auto;cursor:pointer;display:inline-block}'
 '.pb-sw input{position:absolute;opacity:0;width:0;height:0}'
 '.pb-track{display:block;width:46px;height:27px;border-radius:50px;background:#d6d6db;transition:.2s}'
 '.pb-thumb{position:absolute;top:3px;left:3px;width:21px;height:21px;border-radius:50%;background:#fff;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.25)}'
 '.pb-sw input:checked+.pb-track{background:var(--accent-magenta,#ff3d8b)}'
 '.pb-sw input:checked+.pb-track .pb-thumb{transform:translateX(19px)}'
 '.pb-sw input:disabled+.pb-track{opacity:.5}'
 '.pb-test{display:inline-flex;align-items:center;gap:6px;margin:-8px 0 18px;padding:9px 15px;border-radius:50px;border:1px solid var(--hairline,#e6e6e6);background:#fff;color:var(--text,#000);font-size:12.5px;font-weight:700;cursor:pointer}'
 '.pb-test:active{transform:scale(.97)}.pb-test:disabled{opacity:.55;cursor:default}'
 '</style>'
 '<div class="wrap"><section><div class="sec-h"><h2>관심 카드</h2></div>'
 '<div class="muted" style="font-size:12.5px;padding-bottom:8px">로그인 없이 이 브라우저에 저장돼요. 담은 카드를 한눈에 비교하세요.</div>'
 '<div class="pushbox" id="pushbox"><div class="pb-l"><div class="pb-t">🔔 새 이벤트 알림</div>'
 '<div class="pb-d" id="pbDesc">관심 카드에 다음 달 새 캐시백 이벤트가 등록되면 알려드려요.</div></div>'
 '<label class="pb-sw"><input type="checkbox" id="pushTg"><span class="pb-track"><span class="pb-thumb"></span></span></label></div>'
 '<button type="button" class="pb-test" id="pushTest">🔔 테스트 알림 보내기</button>'
 '<div class="cgrid" id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></section></div>')
FAV_JS=r"""
fetch('cards.json').then(r=>r.json()).then(function(j){
 var all=[];for(var k in j.cards){(j.cards[k]||[]).forEach(function(c){c._iss=k;all.push(c);});}
 function render(){var fav=getFav();var items=all.filter(function(c){return fav.indexOf(c.id)>=0;});var L=document.getElementById('list');
  if(!items.length){L.innerHTML='<div class="empty">아직 관심 카드가 없어요.<br><br><a class="accent" href="cards.html">카드찾기에서 하트를 눌러 담아보세요 ›</a></div>';updateFavCount();return;}
  L.innerHTML=items.map(function(c){var fee=c.fee?('연회비 '+c.fee):'';
   var hb='<span class="favbtn on" onclick="event.preventDefault();event.stopPropagation();favClick(this,'+c.id+')">'+favSvg(true)+'</span>';
   return '<a class="ctile" href="carddetail.html?id='+c.id+'">'+hb+'<div class="plate">'+imgTag(c.img)+'</div><div class="cbody"><div class="cn">'+c.name+'</div>'+(fee?'<div class="cfee">'+fee+'</div>':'')+'<div class="cd">'+c._iss+' · '+c.benefit+'</div></div></a>';}).join("");updateFavCount();}
 window._fr=render; render();
});
/* 알림 토글 */
(function(){var tg=document.getElementById('pushTg'),desc=document.getElementById('pbDesc');if(!tg)return;
 if(!ctPushSupported()){desc.textContent='이 브라우저는 알림을 지원하지 않아요.';tg.disabled=true;return;}
 if(typeof Notification!=='undefined'&&Notification.permission==='denied'){desc.textContent='알림이 차단돼 있어요. 브라우저 주소창 옆 설정에서 알림을 허용해 주세요.';}
 tg.checked=ctPushOn();
 if(tg.checked)desc.textContent='알림이 켜져 있어요. 관심 카드에 새 캐시백 이벤트가 뜨면 알려드려요.';
 tg.addEventListener('change',function(){
  if(tg.checked){tg.disabled=true;desc.textContent='알림 권한 확인 중…';
   ctPushEnable(function(ok,msg){tg.disabled=false;if(ok){tg.checked=true;desc.textContent='알림이 켜졌어요! 관심 카드에 새 이벤트가 등록되면 알려드려요.';}else{tg.checked=false;desc.textContent=msg||'알림을 켤 수 없어요.';}});
  }else{ctPushDisable();desc.textContent='알림을 껐어요. 언제든 다시 켤 수 있어요.';}
 });
 var tb=document.getElementById('pushTest');
 if(tb){tb.addEventListener('click',function(){var o=tb.textContent;tb.disabled=true;tb.textContent='보내는 중…';
  ctPushTest(function(ok,msg){tb.disabled=false;tb.textContent=o;
   desc.textContent=ok?'테스트 알림을 보냈어요! 알림이 안 보이면 브라우저·OS 알림 설정을 확인해 주세요.':(msg||'테스트 알림을 보낼 수 없어요.');});
 });}
})();
"""

# ===== SEARCH (통합검색) =====
SEARCH_BODY=('<style>'
 '.srch{max-width:760px;margin:0 auto}'
 '.srch-bar{display:flex;align-items:center;gap:11px;border:1px solid var(--hairline,#e6e6e6);border-radius:50px;padding:13px 18px;margin:16px 0 24px;background:#fff;position:sticky;top:10px;z-index:6}'
 '.srch-bar .ic{width:20px;height:20px;color:#999;flex:0 0 auto}'
 '.srch-bar input{flex:1;min-width:0;border:0;outline:0;background:transparent;font-size:16px;color:#000;font-family:inherit}'
 '.srch-bar .clr{flex:0 0 auto;cursor:pointer;border:0;background:0;color:#bbb;font-size:21px;line-height:1;display:none;padding:0 2px}'
 '.srch-sec{margin:0 0 28px}'
 '.srch-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px}'
 '.srch-eb{font-size:11px;font-weight:800;letter-spacing:.05em;font-family:"JetBrains Mono",ui-monospace,monospace;color:#9a9a9a;text-transform:uppercase}'
 '.srch-act{border:0;background:0;color:#999;font-size:12px;cursor:pointer}'
 '.srch-chips{display:flex;flex-wrap:wrap;gap:8px}'
 '.srch-chip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--hairline,#e6e6e6);border-radius:50px;padding:8px 14px;font-size:13px;font-weight:600;cursor:pointer;background:#fff;color:#000;line-height:1}'
 '.srch-chip .x{color:#c4c4c4;font-size:13px;line-height:1}'
 '.srch-pop{list-style:none;margin:0;padding:0}'
 '.srch-pop li{display:flex;align-items:center;gap:13px;padding:11px 4px;cursor:pointer;border-bottom:1px solid #f3f3f3}'
 '.srch-pop .rk{width:18px;text-align:center;font-style:italic;font-weight:900;font-size:15px;color:#c4c4c4;flex:0 0 auto}'
 '.srch-pop li:nth-child(-n+3) .rk{color:var(--accent-magenta,#ff3d8b)}'
 '.srch-pop .t{font-size:14.5px;font-weight:600}'
 '.srch-tiles{display:grid;grid-template-columns:1fr 1fr;gap:11px}'
 '.srch-tile{border-radius:18px;padding:17px 16px;text-decoration:none;color:#000;display:block}'
 '.srch-tile .tl{font-weight:800;font-size:15px}.srch-tile .td{font-size:12px;font-weight:500;color:rgba(0,0,0,.62);margin-top:4px;line-height:1.4}'
 '.srch-tf{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 18px}'
 '.srch-tf button{border:1px solid var(--hairline,#e6e6e6);border-radius:50px;padding:8px 15px;font-size:13px;font-weight:700;cursor:pointer;background:#fff;color:#000;line-height:1}'
 '.srch-tf button.on{background:#000;color:#fff;border-color:#000}'
 '.srch-tf button .c{opacity:.55;margin-left:4px;font-weight:600}'
 '.srch-rh{font-size:13px;color:#666;margin:2px 0 18px}.srch-rh b{color:#000;font-weight:700}'
 '.srch-rs{margin:0 0 24px}'
 '.srch-row{display:flex;align-items:center;gap:13px;padding:12px 4px;border-bottom:1px solid #f3f3f3;text-decoration:none;color:#000}'
 '.srch-pl{width:62px;height:39px;border-radius:7px;overflow:hidden;background:#f3f3f3;flex:0 0 auto}'
 '.srch-pl img{width:100%;height:100%;object-fit:cover}'
 '.srch-rb{flex:1;min-width:0}'
 '.srch-rn{font-size:14.5px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.srch-rm{font-size:12px;color:#8a8a8a;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.srch-ra{flex:0 0 auto;text-align:right;font-size:13.5px;font-weight:800;color:var(--accent-magenta,#ff3d8b)}'
 '.srch-ra .u{display:block;font-size:10px;color:#b3b3b3;font-weight:600;margin-top:1px}'
 '.srch-tag{display:inline-block;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;background:var(--block-lime,#dceeb1);color:#33402a}'
 '.srch-no{text-align:center;padding:64px 20px 40px}'
 '.srch-no .nmk{width:54px;height:54px;opacity:.14;margin:0 auto 18px;display:block}'
 '.srch-no h3{font-size:18px;font-weight:800;margin-bottom:9px}'
 '.srch-no p{font-size:13.5px;color:#777;line-height:1.65;max-width:380px;margin:0 auto 22px}'
 '.srch-legal{font-size:11.5px;color:#a0a0a0;line-height:1.65;border-top:1px solid #f0f0f0;padding-top:16px;margin-top:6px}'
 '.srch mark{background:transparent;color:inherit;font-weight:800}'
 '@media(max-width:560px){.srch-bar{top:6px}.srch-ra{font-size:12.5px}}'
 '</style>'
 '<div class="wrap"><div class="srch">'
 '<div class="srch-bar"><svg class="ic"><use href="#ic-search"/></svg>'
 '<input id="sq" placeholder="카드 · 카드사 · 혜택 · 콘텐츠 검색" autocomplete="off" enterkeyhint="search">'
 '<button class="clr" id="sclr" aria-label="지우기">&times;</button></div>'
 '<div id="sbody"></div>'
 '</div></div>')
SEARCH_JS=r"""
var Q0=(new URLSearchParams(location.search).get('q')||'').trim();
var CC=[],KK=[],MM=[],curT='all';
var POPULAR=['삼성카드','현대카드','주유','해외 결제','카카오페이','스타벅스','대중교통','쿠팡'];
var SUGGEST=['삼성카드','주유 할인','해외 결제','연회비','대중교통'];
var SHORTCUTS=[
 {l:'카드찾기',d:'카드사별 대표 카드',h:'cards.html',bg:'var(--block-lime,#dceeb1)'},
 {l:'이번달 캐시백',d:'플랫폼별 발급 캐시백',h:'issue.html',bg:'var(--block-lilac,#c5b0f4)'},
 {l:'티라노TIP',d:'캐시백 전략·카드 지식',h:'content.html',bg:'var(--block-cream,#f4ecd6)'},
 {l:'커뮤니티',d:'카드 라운지 후기·꿀팁',h:'community.html',bg:'var(--block-mint,#c8e6cd)'}];
function _e(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function _hl(s,q){s=_e(s);if(!q)return s;try{return s.replace(new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>');}catch(e){return s;}}
function _won(s){var m=String(s||'').match(/([\d.,]+)\s*만원/);return m?Math.round(parseFloat(m[1].replace(/,/g,''))*10000):0;}
function _wm(n){return n>=10000?(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원':((n||0).toLocaleString()+'원');}
function _rec(){try{return JSON.parse(localStorage.getItem('ct_recent')||'[]');}catch(e){return[];}}
function _setRec(a){try{localStorage.setItem('ct_recent',JSON.stringify(a.slice(0,8)));}catch(e){}}
function _addRec(q){q=(q||'').trim();if(!q)return;var a=_rec().filter(function(x){return x!==q;});a.unshift(q);_setRec(a);}
var B=function(){return document.getElementById('sbody');};
function setQ(q){var inp=document.getElementById('sq');inp.value=q;toggleClr();onInput();}
function toggleClr(){var inp=document.getElementById('sq'),c=document.getElementById('sclr');if(c)c.style.display=inp.value?'block':'none';}

function renderEmpty(){
 var rec=_rec(),h='';
 if(rec.length){h+='<div class="srch-sec"><div class="srch-hd"><div class="srch-eb">최근 검색어</div><button class="srch-act" onclick="_setRec([]);renderEmpty();">전체 삭제</button></div><div class="srch-chips">'+
  rec.map(function(t){return '<span class="srch-chip" data-q="'+_e(t)+'"><span class="qx">'+_e(t)+'</span><span class="x" data-del="'+_e(t)+'">&times;</span></span>';}).join('')+'</div></div>';}
 h+='<div class="srch-sec"><div class="srch-hd"><div class="srch-eb">인기 검색어</div><div class="srch-eb" style="color:#c0c0c0">자동 집계</div></div><ul class="srch-pop">'+
  POPULAR.map(function(t,i){return '<li data-q="'+_e(t)+'"><span class="rk">'+(i+1)+'</span><span class="t">'+_e(t)+'</span></li>';}).join('')+'</ul></div>';
 h+='<div class="srch-sec"><div class="srch-hd"><div class="srch-eb">바로가기</div></div><div class="srch-tiles">'+
  SHORTCUTS.map(function(s){return '<a class="srch-tile" href="'+s.h+'" style="background:'+s.bg+'"><div class="tl">'+s.l+'</div><div class="td">'+s.d+'</div></a>';}).join('')+'</div></div>';
 B().innerHTML=h;
 B().querySelectorAll('[data-q]').forEach(function(el){el.addEventListener('click',function(ev){if(ev.target.getAttribute('data-del'))return;setQ(el.getAttribute('data-q'));_addRec(el.getAttribute('data-q'));});});
 B().querySelectorAll('[data-del]').forEach(function(el){el.addEventListener('click',function(ev){ev.stopPropagation();_setRec(_rec().filter(function(x){return x!==el.getAttribute('data-del');}));renderEmpty();});});
}

function search(q){var ql=q.toLowerCase();
 var cards=CC.filter(function(x){return (x.name+' '+x.issuer+' '+x.benefit).toLowerCase().indexOf(ql)>=0;}).slice(0,40);
 var cont=KK.filter(function(x){return (x.title+' '+x.cat+' '+(x.summary||'')).toLowerCase().indexOf(ql)>=0;}).slice(0,30);
 var comm=MM.filter(function(x){return (x.title+' '+(x.cat||'')).toLowerCase().indexOf(ql)>=0;}).slice(0,30);
 return {card:cards,content:cont,community:comm};}

function renderResults(q,res){
 var n={card:res.card.length,content:res.content.length,community:res.community.length};
 var total=n.card+n.content+n.community;
 var TF=[['all','전체',total],['card','카드',n.card],['content','콘텐츠',n.content],['community','커뮤니티',n.community]];
 var h='<div class="srch-tf">'+TF.map(function(t){return '<button data-t="'+t[0]+'"'+(curT===t[0]?' class="on"':'')+'>'+t[1]+'<span class="c">'+t[2]+'</span></button>';}).join('')+'</div>';
 h+='<div class="srch-rh">‘<b>'+_e(q)+'</b>’ 검색 결과 '+total+'건 · 공개 데이터 기준 자동 정렬</div>';
 function sec(key,label,rows,html){if(!rows.length||(curT!=='all'&&curT!==key))return '';return '<div class="srch-rs"><div class="srch-eb" style="margin-bottom:10px">'+label+'</div>'+html+'</div>';}
 h+=sec('card','카드',res.card,res.card.map(function(c){
   return '<a class="srch-row" href="carddetail.html?id='+c.id+'"><span class="srch-pl">'+imgTag(c.img)+'</span><div class="srch-rb"><div class="srch-rn">'+_hl(c.name,q)+'</div><div class="srch-rm">'+_hl(c.issuer,q)+' · '+_hl(c.benefit,q)+'</div></div>'+(c.awon?'<div class="srch-ra">'+_wm(c.awon)+'<span class="u">최대 캐시백</span></div>':'')+'</a>';}).join(''));
 h+=sec('content','티라노TIP 콘텐츠',res.content,res.content.map(function(c){
   return '<a class="srch-row" href="content.html?id='+_e(c.id)+'"><div class="srch-rb"><div style="margin-bottom:6px"><span class="srch-tag">'+_e(c.cat)+'</span></div><div class="srch-rn" style="white-space:normal">'+_hl(c.title,q)+'</div></div></a>';}).join(''));
 h+=sec('community','커뮤니티',res.community,res.community.map(function(c){
   return '<a class="srch-row" href="community.html?post='+_e(c.id)+'"><div class="srch-rb"><div class="srch-rn" style="white-space:normal">'+_hl(c.title,q)+'</div><div class="srch-rm">'+_e(c.cat||'자유')+' · 공감 '+(c.likes||0)+' · 댓글 '+(c.comments||0)+'</div></div></a>';}).join(''));
 h+='<div class="srch-legal">검색 결과의 혜택·캐시백은 수집 시점 기준이며, 신청 전 각 카드사·플랫폼에서 최종 확인이 필요합니다. 카드티라노는 광고·정보제공 매체로 발급을 중개·접수하지 않습니다.</div>';
 B().innerHTML=h;
 B().querySelectorAll('.srch-tf button').forEach(function(b){b.onclick=function(){curT=b.getAttribute('data-t');renderResults(q,res);};});
}

function renderNo(q){
 B().innerHTML='<div class="srch-no"><svg class="nmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>'+
  '<h3>‘'+_e(q)+'’에 대한 결과가 없어요</h3>'+
  '<p>철자를 확인하거나 더 짧은 키워드로 검색해보세요. 카드명·혜택·플랫폼·콘텐츠를 찾을 수 있어요.</p>'+
  '<div class="srch-chips" style="justify-content:center">'+SUGGEST.map(function(t){return '<span class="srch-chip" data-q="'+_e(t)+'">'+_e(t)+'</span>';}).join('')+'</div></div>';
 B().querySelectorAll('[data-q]').forEach(function(el){el.addEventListener('click',function(){setQ(el.getAttribute('data-q'));_addRec(el.getAttribute('data-q'));});});
}

function onInput(){var q=(document.getElementById('sq').value||'').trim();curT='all';
 if(!q){renderEmpty();return;}
 var res=search(q);
 if(res.card.length+res.content.length+res.community.length===0)renderNo(q);
 else renderResults(q,res);}

var _dt;
function bindSearch(){
 var inp=document.getElementById('sq'),clr=document.getElementById('sclr');
 inp.addEventListener('input',function(){toggleClr();clearTimeout(_dt);_dt=setTimeout(onInput,200);});
 inp.addEventListener('keydown',function(ev){if(ev.key==='Enter'){clearTimeout(_dt);onInput();_addRec(inp.value);}});
 if(clr)clr.onclick=function(){inp.value='';toggleClr();inp.focus();renderEmpty();};
}

// 데이터 로드: 카드(+최대 캐시백)·티라노TIP 콘텐츠·(가능 시)커뮤니티
Promise.all([
 fetch('cards.json').then(function(r){return r.json();}).catch(function(){return{cards:{}};}),
 fetch('content.json').then(function(r){return r.json();}).catch(function(){return{items:[]};})
]).then(function(a){
 var cj=a[0].cards||{};
 for(var k in cj){(cj[k]||[]).forEach(function(c){
   var aw=0;(c.events||[]).forEach(function(e){var w=_won(e.amount);if(w>aw)aw=w;});
   CC.push({id:c.id,name:c.name||'',issuer:k,benefit:c.benefit||'',img:c.img||'',awon:aw});});}
 KK=(a[1].items||[]).map(function(x){return {id:x.id,title:x.title||'',cat:x.cat||'티라노TIP',summary:x.summary||''};});
 // 커뮤니티(API 있으면): 실패해도 무시
 var capi=(window.COMMUNITY_API)||((document.querySelector('meta[name=community-api]')||{}).content)||'';
 var done=function(){
   bindSearch();
   var inp=document.getElementById('sq');
   if(Q0){inp.value=Q0;toggleClr();onInput();}else{renderEmpty();}
   setTimeout(function(){try{inp.focus();}catch(e){}},80);
 };
 if(capi&&/^https?:/.test(capi)){
   fetch(capi.replace(/\/$/,'')+'/api/posts?size=100').then(function(r){return r.json();}).then(function(j){
     (((j&&j.items)||j||[])).forEach(function(p){MM.push({id:p.id,title:p.title||'',cat:p.category||'',likes:p.likes||0,comments:p.comments||0});});
   }).catch(function(){}).then(done);
 }else done();
});
"""

# ===== DASHBOARD (관리자 통계) =====
DASHBOARD_BODY=('<style>'
 '.dwrap{padding:8px 0 44px}'
 '.dnote{background:#f4f5f7;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:12px;color:#55555e;line-height:1.6;margin:10px 0 16px}'
 '.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}'
 '.kpi{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}'
 '.kpi .n{font-size:24px;font-weight:900;color:var(--accent);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.kpi .l{font-size:12px;color:var(--sub);margin-top:4px}'
 '.dsec{margin:0 0 24px}.dsec h3{font-size:15px;font-weight:900;margin-bottom:12px}'
 '.bar{display:flex;align-items:center;gap:10px;margin-bottom:8px;font-size:13px}'
 '.bar .bl{flex:0 0 40%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#55555e}'
 '.bar .bt{flex:1;background:#eef0f3;border-radius:6px;height:18px;overflow:hidden}'
 '.bar .bf{height:100%;background:linear-gradient(90deg,var(--accent),#ff7a59);border-radius:6px}'
 '.bar .bn{flex:0 0 34px;font-weight:800;color:#fff;text-align:right}'
 '.dbtns{display:flex;gap:10px;flex-wrap:wrap;margin:4px 0 20px}'
 '.dbtns button{background:var(--surface2);border:1px solid var(--line);color:var(--text);border-radius:10px;padding:10px 14px;font-weight:700;font-size:12.5px;cursor:pointer}'
 '.log{font-size:11.5px;color:var(--sub);border-top:1px solid var(--line);padding:7px 0;display:flex;gap:10px}'
 '.log .lt{color:var(--accent);font-weight:800;flex:0 0 64px}.log .lp{flex:0 0 84px;color:var(--dim)}'
 '.empty2{color:var(--sub);font-size:13px;padding:12px 0}'
 '.hgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:12px}'
 '.hcard{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:13px 10px;text-align:center}'
 '.hcard .hp{font-size:12.5px;font-weight:800;margin-bottom:7px}.hcard .hn{font-size:22px;font-weight:900;color:var(--text)}.hcard .hl{font-size:10.5px;color:var(--dim);margin-top:2px}.hcard .hs{font-size:11px;margin-top:6px;font-weight:800}'
 '.ok{color:#16a34a}.warn{color:#d97706}.bad{color:#dc2626}'
 '.hrow{display:flex;align-items:center;gap:10px;font-size:13px;padding:8px 0;border-top:1px solid var(--line)}.hrow .hi{flex:0 0 34%;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.hrow .hb{flex:1;display:flex;gap:4px}.hrow .hd2{flex:0 0 92px;text-align:right;font-weight:800;color:var(--accent)}'
 '.pdot{width:22px;height:22px;border-radius:6px;font-size:9px;font-weight:800;color:#fff;display:flex;align-items:center;justify-content:center}.pdot.off{background:#e3e4ea!important;color:#aaa}'
 '@media(max-width:560px){.kpis{grid-template-columns:repeat(2,1fr)}.bar .bl{flex-basis:48%}.hgrid{grid-template-columns:repeat(2,1fr)}}'
 '</style>'
 '<div class="wrap dwrap"><div class="sec-h"><h2>카드티라노 대시보드</h2></div>'
 '<div class="dnote">📡 <b>스크래핑 헬스</b>는 콜렉터 산출물(platform_events.json)을 실시간 분석해 플랫폼·카드사별 수집 상태를 보여줍니다.<br>👣 아래 <b>방문 지표(시간/일/월별)</b>는 <b>이 브라우저</b> 로컬 집계예요. <b>전체 방문자</b>는 개인정보(IP) 미저장 <b>Cloudflare Web Analytics</b>(자동 연동됨)에서 집계됩니다.</div>'
 '<div class="dsec"><h3>🌐 Cloudflare 실측 방문 (전체 방문자)</h3>'
 '<div class="kpis"><div class="kpi"><div class="n" id="cfPV">225</div><div class="l">페이지뷰 · 최근 24h</div></div>'
 '<div class="kpi"><div class="n" id="cfVisit">100</div><div class="l">방문(Visits) · 최근 24h</div></div>'
 '<div class="kpi"><div class="n">자동</div><div class="l">수집 방식(Automatic)</div></div>'
 '<div class="kpi"><div class="n" id="cfAsOf">06/27</div><div class="l">스냅샷 기준일</div></div></div>'
 '<div style="margin-top:4px"><a href="https://dash.cloudflare.com/?to=/:account/web-analytics" target="_blank" rel="noopener" style="display:inline-block;background:#f6821f;color:#fff;font-weight:800;font-size:13px;padding:11px 17px;border-radius:10px;text-decoration:none">Cloudflare에서 실시간 방문자 보기 ↗</a></div>'
 '<div class="dnote" style="margin-top:10px">위 수치는 Cloudflare Web Analytics <b>스냅샷</b>입니다(IP 미저장). <b>시간/일/월별 실시간 추세·국가·인기 페이지</b>는 위 버튼의 Cloudflare 대시보드에서 기간 필터로 확인하세요. (페이지 내 자동 실시간 표시는 토큰 기반 프록시 연동 시 가능 — 원하면 설정해 드립니다.)</div></div>'
 '<div class="dsec"><h3>📡 플랫폼별 스크래핑 상태</h3><div class="hgrid" id="hplat"></div><div id="hfresh" class="empty2"></div></div>'
 '<div class="dsec"><h3>카드사별 커버리지</h3><div id="hiss"></div></div>'
 '<div class="sec-h" style="margin-top:8px"><h2 style="font-size:18px">👣 방문 지표 (이 브라우저)</h2></div>'
 '<div class="dbtns"><button id="rf">↻ 새로고침</button><button id="csv">⬇ CSV 내보내기</button><button id="rs">🗑 이 브라우저 초기화</button></div>'
 '<div class="kpis" id="kpis"></div><div id="secs"></div>'
 '<div class="dsec"><h3>🕒 최근 활동</h3><div id="log"></div></div></div>')
DASHBOARD_JS=r"""
// === 스크래핑 헬스 — 콜렉터 산출물(platform_events.json) 실시간 분석 ===
(function(){var PN={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};var PORD=['cardgorilla','banksalad','toss','ajungdang','naver','kakaopay'];var PC={cardgorilla:'#ff4d4f',banksalad:'#2f6bff',toss:'#3182f6',ajungdang:'#3b5bdb',naver:'#03c75a',kakaopay:'#e8b800'};
 function wm(n){return n>=10000?(Math.round(n/1000)/10+'만'):(n||0);}
 fetch('platform_events.json').then(function(r){return r.json();}).then(function(d){
  var prods=d.products||[];var withEv=prods.filter(function(p){return (p.events||[]).length;});
  var cross=prods.filter(function(p){return new Set((p.events||[]).map(function(e){return e.platform;})).size>1;});
  var pc={};PORD.forEach(function(k){pc[k]=0;});prods.forEach(function(p){var seen={};(p.events||[]).forEach(function(e){if(pc[e.platform]!=null&&!seen[e.platform]){pc[e.platform]++;seen[e.platform]=1;}});});
  var hp=document.getElementById('hplat');if(hp)hp.innerHTML=PORD.map(function(k){var n=pc[k]||0;var st=n>0?'<span class="hs ok">정상 ✓</span>':'<span class="hs bad">수집 0 ✗</span>';return '<div class="hcard"><div class="hp" style="color:'+PC[k]+'">'+PN[k]+'</div><div class="hn">'+n+'</div><div class="hl">이벤트 카드</div>'+st+'</div>';}).join('');
  var days='';if(d.updated){days=Math.round((Date.now()-new Date(d.updated).getTime())/86400000);}
  var fr=document.getElementById('hfresh');if(fr)fr.innerHTML='마지막 빌드 <b>'+(d.updated||'-')+'</b> ('+(days===''?'-':(days<=0?'오늘':days+'일 전'))+') · 총 '+prods.length+'개 상품 · 이벤트 보유 '+withEv.length+' · 교차비교(2개+) '+cross.length+'개';
  var iss={};prods.forEach(function(p){if(!(p.events||[]).length)return;var k=p.issuer||'기타';iss[k]=iss[k]||{mx:0,pl:{}};(p.events||[]).forEach(function(e){iss[k].pl[e.platform]=1;if((e.reward_won||0)>iss[k].mx)iss[k].mx=e.reward_won||0;});});
  var rows=Object.keys(iss).map(function(k){return [k,iss[k]];}).sort(function(a,b){return b[1].mx-a[1].mx;});
  var hi=document.getElementById('hiss');if(hi)hi.innerHTML=rows.length?rows.map(function(r){var dots=PORD.map(function(k){var on=r[1].pl[k];return '<span class="pdot'+(on?'':' off')+'"'+(on?' style="background:'+PC[k]+'"':'')+' title="'+PN[k]+'">'+PN[k].slice(0,1)+'</span>';}).join('');return '<div class="hrow"><span class="hi">'+esc(r[0])+'</span><span class="hb">'+dots+'</span><span class="hd2">최대 '+wm(r[1].mx)+'원</span></div>';}).join(''):'<div class="empty2">데이터 준비 중</div>';
 }).catch(function(){var hp=document.getElementById('hplat');if(hp)hp.innerHTML='<div class="empty2">platform_events.json을 불러오지 못했어요.</div>';});
})();
function esc(s){return (s||'').toString().replace(/[<>&]/g,function(c){return {'<':'&lt;','>':'&gt;','&':'&amp;'}[c];});}
function PG(p){var M={'index.html':'홈','discount.html':'카드 혜택','cards.html':'카드찾기','issue.html':'발급 이벤트','chart.html':'티라노차트','content.html':'티라노TIP','carddetail.html':'카드 상세','detail.html':'혜택 상세','favorites.html':'관심카드','search.html':'검색','dashboard.html':'대시보드'};return M[p]||p;}
function agg(ev,type,keyfn){var m={};ev.forEach(function(e){if(type&&e.t!==type)return;var k=keyfn(e);if(!k)return;m[k]=(m[k]||0)+1;});return Object.keys(m).map(function(k){return [k,m[k]];}).sort(function(a,b){return b[1]-a[1];});}
function bars(rows,n){rows=rows.slice(0,n||8);if(!rows.length)return '<div class="empty2">아직 데이터가 없어요.</div>';var max=rows[0][1]||1;return rows.map(function(r){return '<div class="bar"><span class="bl">'+esc(r[0])+'</span><span class="bt"><span class="bf" style="width:'+Math.max(6,Math.round(r[1]/max*100))+'%"></span></span><span class="bn">'+r[1]+'</span></div>';}).join('');}
function kpi(n,l){return '<div class="kpi"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';}
// 시간/일/월별 방문(페이지뷰) 집계 — 시계열은 시간순 정렬(값순 아님)
function tagg(ev,unit){var m={};ev.forEach(function(e){if(e.t!=='pageview')return;var d=new Date(e.ts);if(isNaN(d))return;var k;if(unit==='month')k=d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2);else if(unit==='day')k=('0'+(d.getMonth()+1)).slice(-2)+'/'+('0'+d.getDate()).slice(-2);else k=('0'+d.getHours()).slice(-2)+'시';m[k]=(m[k]||0)+1;});var arr=Object.keys(m).sort().map(function(k){return [k,m[k]];});if(unit==='day')arr=arr.slice(-14);return arr;}
function tbars(rows){if(!rows.length)return '<div class="empty2">아직 데이터가 없어요.</div>';var max=Math.max.apply(null,rows.map(function(r){return r[1];}))||1;return rows.map(function(r){return '<div class="bar"><span class="bl">'+esc(r[0])+'</span><span class="bt"><span class="bf" style="width:'+Math.max(6,Math.round(r[1]/max*100))+'%"></span></span><span class="bn">'+r[1]+'</span></div>';}).join('');}
function render(){
 var ev=[];try{ev=JSON.parse(localStorage.getItem('ct_evt')||'[]');}catch(_){}
 var pv=ev.filter(function(e){return e.t==='pageview';}).length;
 var first=Number(localStorage.getItem('ct_first')||0);var fd=first?new Date(first).toLocaleDateString('ko-KR'):'-';
 document.getElementById('kpis').innerHTML=kpi(pv,'페이지뷰')+kpi(ev.length,'총 이벤트')+kpi(new Set(ev.map(function(e){return e.p;})).size,'방문 페이지수')+kpi(fd,'첫 방문');
 var secs=[
  ['📅 월별 방문(페이지뷰)', tbars(tagg(ev,'month'))],
  ['🗓 일별 방문 (최근 14일)', tbars(tagg(ev,'day'))],
  ['🕐 시간대별 방문', tbars(tagg(ev,'hour'))],
  ['📄 페이지별 조회', bars(agg(ev,'pageview',function(e){return PG(e.l||e.p);}))],
  ['🧭 메뉴 클릭', bars(agg(ev,'menu',function(e){return e.l;}))],
  ['카드 클릭(상품)', bars(agg(ev,'card',function(e){return e.l;}))],
  ['필터·카드사 탭', bars(agg(ev,'filter',function(e){return e.l;}))],
  ['📂 업종 카테고리 클릭', bars(agg(ev,'category',function(e){return e.l;}))],
  ['🔗 플랫폼 상세 클릭', bars(agg(ev,'plat',function(e){return e.l;}))],
  ['카드사 공식 클릭', bars(agg(ev,'official',function(e){return e.l;}))],
  ['발급 이벤트 클릭', bars(agg(ev,'event',function(e){return e.l;}))],
  ['리스트/검색 클릭', bars(agg(ev,'item',function(e){return e.l;}))]
 ];
 document.getElementById('secs').innerHTML=secs.map(function(s){return '<div class="dsec"><h3>'+s[0]+'</h3>'+s[1]+'</div>';}).join('');
 var log=ev.slice(-30).reverse();
 document.getElementById('log').innerHTML=log.length?log.map(function(e){return '<div class="log"><span class="lt">'+esc(e.t)+'</span><span class="lp">'+esc(PG(e.p))+'</span><span>'+esc(e.l)+'</span></div>';}).join(''):'<div class="empty2">아직 기록이 없어요. 사이트를 둘러보면 쌓입니다.</div>';
}
document.getElementById('rf').onclick=render;
document.getElementById('rs').onclick=function(){if(confirm('이 브라우저에 저장된 통계 데이터를 모두 지울까요?')){localStorage.removeItem('ct_evt');localStorage.removeItem('ct_first');render();}};
document.getElementById('csv').onclick=function(){var ev=[];try{ev=JSON.parse(localStorage.getItem('ct_evt')||'[]');}catch(_){}var rows=[['time','type','page','label']].concat(ev.map(function(e){return [new Date(e.ts).toISOString(),e.t,e.p,'"'+(e.l||'').replace(/"/g,'""')+'"'];}));var csv=rows.map(function(r){return r.join(',');}).join('\n');var a=document.createElement('a');a.href='data:text/csv;charset=utf-8,'+encodeURIComponent('﻿'+csv);a.download='cardtyranno_events.csv';a.click();};
render();
"""

# ===== 무이자할부 (Phase4) =====
_inst=json.load(open(os.path.join(OUT,"scrape","installment.json"),encoding="utf-8"))
_gen="".join('<div class="irow"><div class="ii"><span class="ib">%s</span><span class="itag">%s</span></div><div class="im">%s</div>%s</div>'%(g["issuer"],g["type"],g["months"],('<div class="idt">%s</div>'%g["detail"] if g.get("detail") else '')) for g in _inst["general"])
_cat="".join('<div class="irow"><div class="ii"><span class="icat">%s</span><span class="ib">%s</span></div><div class="im">%s</div><div class="idt">%s%s</div></div>'%(c["cat"],c["issuer"],c["months"],c["merchants"],(' · '+c["period"] if c.get("period") else '')) for c in _inst["category"])
INSTALLMENT_BODY=('<style>'
 '.iwrap{padding:8px 0 42px}.isec{margin-bottom:26px}.isec h3{font-size:16px;font-weight:900;margin:0 0 12px}'
 '.irow{border:1px solid var(--line);border-radius:13px;padding:13px 15px;margin-bottom:10px;background:var(--surface)}'
 '.irow .ii{display:flex;align-items:center;gap:8px;margin-bottom:6px}'
 '.irow .ib{font-size:14px;font-weight:800}.irow .itag{font-size:10.5px;font-weight:800;color:#fff;background:var(--accent);border-radius:6px;padding:2px 7px}'
 '.irow .icat{font-size:10.5px;font-weight:800;color:var(--accent);background:#fbf0df;border:1px solid #f3d8b6;border-radius:6px;padding:2px 8px}'
 '.irow .im{font-size:14.5px;font-weight:800;color:var(--accent)}.irow .idt{font-size:12px;color:var(--sub);margin-top:4px}'
 '</style>'
 '<div class="wrap iwrap"><div class="sec-h"><h2>무이자·부분무이자 할부 (2026년 6월)</h2></div>'
 '<div class="muted" style="font-size:12.5px;padding-bottom:14px">카드사별·업종별 무이자/부분무이자 할부를 모았어요. 건별 최소금액·회차 수수료 등 조건은 결제 전 카드사에서 확인하세요.</div>'
 '<div class="isec"><h3>카드사별 할부</h3>'+_gen+'</div>'
 '<div class="isec"><h3>업종별 할부 (항공·백화점·가전)</h3>'+_cat+'</div>'
 '<div class="muted" style="font-size:11.5px;line-height:1.6">※ 2026년 6월 기준 수집 정보로 실제와 다를 수 있어요. 무이자할부는 보통 건별 5만원 이상 결제 시 적용되며, 부분무이자는 일부 회차 수수료가 발생합니다.</div>'
 '</div>')

# ===== 월별 캐시백 추이 (history 스냅샷 기반) =====
TRENDS_BODY=('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>'
 '<style>'
 '.twrap{padding:8px 0 46px}'
 '.tnote{background:#f3f0fb;border:1px solid #e4dcf6;border-radius:12px;padding:13px 15px;font-size:12.5px;color:#3a2d5e;line-height:1.6;margin:10px 0 14px}'
 '.tsel{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:14px 0 4px}'
 '.tsel label{font-size:12px;font-weight:800;color:var(--sub)}'
 '.tsel select{flex:1;min-width:200px;max-width:420px;background:var(--surface);border:1px solid var(--line);color:var(--text);border-radius:10px;padding:11px 12px;font-size:14px;font-weight:700}'
 '.chartbox{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 14px 10px;margin-top:10px}'
 '.tempty{color:var(--sub);font-size:13px;padding:26px 0;text-align:center}'
 '</style>'
 '<div class="wrap twrap"><div class="sec-h"><h2>월별 캐시백 추이</h2></div>'
 '<div class="tnote">매월 스냅샷을 누적해 <b>카드사·상품별 발급 캐시백의 월별 변화</b>를 보여줘요. 2026-06부터 자동 누적되며, 데이터가 쌓일수록 추이가 뚜렷해집니다. (1~5월은 플랫폼이 과거 이벤트를 공개하지 않아 미수집)</div>'
 '<div class="subnav"><button data-t="iss" class="on">카드사별 최대금액</button><button data-t="prod">카드 상품별</button></div>'
 '<div id="v-iss"><div class="tsel"><label>카드사</label><select id="selIss"></select></div><div class="chartbox"><canvas id="chIss" height="150"></canvas></div></div>'
 '<div id="v-prod" style="display:none"><div class="tsel"><label>카드 상품</label><select id="selProd"></select></div><div class="chartbox"><canvas id="chProd" height="150"></canvas></div></div>'
 '<div id="tempty" class="tempty" style="display:none"></div>'
 '</div>')
TRENDS_JS=r"""
var TPN={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
var TPORD=['cardgorilla','banksalad','toss','ajungdang','naver','kakaopay'];
var TPC={cardgorilla:'#ff4d4f',banksalad:'#2f6bff',toss:'#3182f6',ajungdang:'#3b5bdb',naver:'#03c75a',kakaopay:'#e8b800'};
var TMONTHS=[],SNAP={},chIss=null,chProd=null;
function tesc(s){return (s||'').toString().replace(/</g,'&lt;');}
function wan(w){return Math.round((w||0)/1000)/10;}
function noChart(msg){var e=document.getElementById('tempty');e.style.display='';e.textContent=msg;}
fetch('history/index.json').then(function(r){return r.json();}).then(function(ix){
  var _n=new Date();var _cur=_n.getFullYear()+'-'+('0'+(_n.getMonth()+1)).slice(-2);   // 당월(진행중) 제외
  TMONTHS=(ix.months||[]).slice().sort().filter(function(m){return m<_cur;}).slice(-3);  // 직전 완료 3개월(0628 §C)
  if(!TMONTHS.length){noChart('아직 누적된 스냅샷이 없어요.');return null;}
  return Promise.all(TMONTHS.map(function(m){return fetch('history/'+m+'.json').then(function(r){return r.json();}).then(function(j){SNAP[m]=j;});}));
}).then(function(ok){if(!TMONTHS.length)return;
  if(TMONTHS.length<2){var e=document.getElementById('tempty');e.style.display='';e.textContent='현재 '+TMONTHS.length+'개월('+TMONTHS.join(', ')+') 데이터예요. 다음 달부터 추이선이 그려집니다.';}
  initIss();initProd();drawIss();
}).catch(function(){noChart('추이 데이터를 불러오지 못했어요.');});
function mlabel(m){return m.replace('2026-','').replace(/^0/,'')+'월';}
function initIss(){var set={};TMONTHS.forEach(function(m){Object.keys((SNAP[m]||{}).issuers||{}).forEach(function(k){set[k]=1;});});
  function cnt(k){return TMONTHS.filter(function(m){return (SNAP[m]||{}).issuers&&(SNAP[m].issuers[k]);}).length;}   // 데이터 보유 월수
  var arr=Object.keys(set).sort(function(a,b){return cnt(b)-cnt(a)||a.localeCompare(b,'ko');});                       // 데이터 많은 카드사 우선(기본 선택)
  var sel=document.getElementById('selIss');sel.innerHTML=arr.map(function(k){return '<option>'+tesc(k)+'</option>';}).join('');sel.onchange=drawIss;}
function drawIss(){var iss=document.getElementById('selIss').value;
  var ds=TPORD.map(function(pk){return {label:TPN[pk],data:TMONTHS.map(function(m){var v=(((SNAP[m]||{}).issuers||{})[iss]||{})[pk];return v?wan(v):null;}),borderColor:TPC[pk],backgroundColor:TPC[pk],spanGaps:false,tension:.3,borderWidth:2,pointRadius:4,pointHoverRadius:6};}).filter(function(d){return d.data.some(function(v){return v!=null;});});
  chIss=mkChart('chIss',chIss,ds);}
function initProd(){var set={},mc={};TMONTHS.forEach(function(m){((SNAP[m]||{}).cards||[]).forEach(function(c){set[c.name]=1;mc[c.name]=(mc[c.name]||0)+1;});});
  var arr=Object.keys(set).sort(function(a,b){return (mc[b]-mc[a])||a.localeCompare(b,'ko');});   // 데이터 많은 상품 우선
  if(!arr.length){var vp=document.getElementById('v-prod');if(vp)vp.innerHTML='<div class="empty" style="padding:48px 16px;line-height:1.7">카드 상품별 추이는 <b>2026년 6월부터</b> 누적되고 있어요.<br>직전 완료월(3~5월) 구간은 카드 상품 단위 데이터가 아직 없어, 다음 달부터 상품별 비교가 표시됩니다.</div>';return;}
  var sel=document.getElementById('selProd');sel.innerHTML=arr.map(function(k){return '<option>'+tesc(k)+'</option>';}).join('');sel.onchange=drawProd;}
function drawProd(){var nm=document.getElementById('selProd').value;
  var ds=TPORD.map(function(pk){return {label:TPN[pk],data:TMONTHS.map(function(m){var c=((SNAP[m]||{}).cards||[]).filter(function(x){return x.name===nm;})[0];var v=c&&c.platforms?c.platforms[pk]:null;return v?wan(v):null;}),borderColor:TPC[pk],backgroundColor:TPC[pk],spanGaps:false,tension:.3,borderWidth:2,pointRadius:4,pointHoverRadius:6};}).filter(function(d){return d.data.some(function(v){return v!=null;});});
  chProd=mkChart('chProd',chProd,ds);}
function mkChart(id,old,ds){if(old)old.destroy();if(typeof Chart==='undefined'){noChart('차트 라이브러리를 불러오지 못했어요.');return null;}
  var opt={responsive:true,interaction:{mode:"index",intersect:false},plugins:{legend:{position:"bottom",labels:{font:{size:12}}},tooltip:{callbacks:{label:function(c){return c.dataset.label+": "+c.parsed.y+"만원";}}}},scales:{y:{beginAtZero:true,title:{display:true,text:"최대 캐시백(만원)"}},x:{grid:{display:false}}}};
  return new Chart(document.getElementById(id),{type:"line",data:{labels:TMONTHS.map(mlabel),datasets:ds},options:opt});}
document.querySelector('.subnav').onclick=function(e){var b=e.target.closest('button');if(!b)return;document.querySelectorAll('.subnav button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');var iss=b.dataset.t==='iss';document.getElementById('v-iss').style.display=iss?'':'none';document.getElementById('v-prod').style.display=iss?'none':'';if(iss)drawIss();else drawProd();};
"""

# ===== 네이버/구글 색인용 정적 콘텐츠(JS 미실행 크롤러 대응) =====
# 네이버 Yeti 등 일부 봇은 JS 렌더링이 약해 fetch로 그리는 랭킹/표를 못 읽음.
# 빌드 시점에 site/*.json을 읽어 실제 수치를 정적 HTML로 박아둔다(숨김 X · 사용자에게도 노출).
def _seo_static_index():
    try:_iss=json.load(open(os.path.join(SITE,"issue.json"),encoding="utf-8"))
    except Exception:_iss={"platforms":[],"items":[],"month":"2026-06"}
    try:_rk=json.load(open(os.path.join(SITE,"rank.json"),encoding="utf-8"))
    except Exception:_rk={"items":[]}
    pf=_iss.get("platforms",[]);rows=_iss.get("items",[]);mon=_iss.get("month","2026-06")
    thead="".join("<th scope=\"col\">%s</th>"%p["name"] for p in pf)
    trs=""
    for it in rows:
        tds="".join("<td>%s</td>"%(it.get(p["key"]) or "-") for p in pf)
        trs+="<tr><th scope=\"row\">%s</th>%s</tr>"%(it.get("issuer",""),tds)
    table=('<table class="seo-tbl"><caption>%s 카드사별 신규 발급 캐시백 — 플랫폼별 최대 혜택 비교</caption>'
      '<thead><tr><th scope="col">카드사</th>%s</tr></thead><tbody>%s</tbody></table>'%(mon,thead,trs)) if rows else ""
    items=[x for x in _rk.get("items",[]) if x.get("name")][:12]
    lis="".join('<li><b>%d위</b> %s%s</li>'%(x.get("rank",i+1),x.get("name",""),(' <span class="seo-iss">'+x["issuer"]+'</span>') if x.get("issuer") else "") for i,x in enumerate(items))
    rank=('<h3>이번 달 카드 발급·할인 랭킹 TOP %d</h3><ol class="seo-rank">%s</ol>'%(len(items),lis)) if items else ""
    intro=('<p class="seo-intro">카드티라노는 토스 카드라운지·카드고릴라·아정당·뱅크샐러드·카카오페이 등 여러 카드 발급 '
      '플랫폼의 <strong>신규 발급 캐시백</strong>과 가맹점 <strong>결제 할인 이벤트</strong>를 한곳에서 비교·분석하는 카드 비교 '
      '서비스입니다. 같은 카드라도 발급 채널에 따라 혜택 금액이 달라지므로, %s 기준으로 카드사·플랫폼별 최대 혜택을 매달 자동 집계합니다.</p>'%mon)
    links=('<nav class="seo-links" aria-label="카드티라노 주요 메뉴"><h3>카드티라노 주요 메뉴</h3><ul>'
      '<li><a href="discount.html">카드 할인 혜택 (가맹점·업종별)</a></li>'
      '<li><a href="issue.html">이번달 캐시백 (플랫폼별 비교)</a></li>'
      '<li><a href="cards.html">카드 찾기 (카드사별 신용카드)</a></li>'
      '<li><a href="content.html">카드 가이드·티라노TIP</a></li>'
      '<li><a href="chart.html">티라노차트 (인기 순위)</a></li>'
      '<li><a href="installment.html">무이자 할부</a></li></ul></nav>')
    style=('<style>.seo-static{border-top:1px solid var(--line);background:var(--surface-soft);padding:34px 0 8px}'
      '.seo-static h2{font-size:20px;font-weight:900;letter-spacing:-.5px;margin-bottom:12px}'
      '.seo-static h3{font-size:15px;font-weight:800;margin:22px 0 10px}'
      '.seo-intro{font-size:14px;color:var(--sub);line-height:1.7;margin-bottom:18px}'
      '.seo-tbl{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}'
      '.seo-tbl caption{caption-side:top;text-align:left;font-size:12.5px;color:var(--dim);padding:0 0 8px}'
      '.seo-tbl th,.seo-tbl td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}'
      '.seo-tbl thead th{background:var(--surface2);font-weight:800}'
      '.seo-tbl tbody th[scope=row]{text-align:left;font-weight:700;background:#fff}'
      '.seo-tbl tr:last-child td,.seo-tbl tr:last-child th{border-bottom:0}'
      '.seo-tbl-wrap{overflow-x:auto}'
      '.seo-rank{margin:0;padding-left:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px}'
      '.seo-rank li{font-size:13.5px;padding:8px 12px;background:#fff;border:1px solid var(--line);border-radius:9px}'
      '.seo-rank b{color:var(--blue);margin-right:6px}.seo-iss{color:var(--dim);font-size:12px;margin-left:4px}'
      '.seo-links ul{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}'
      '.seo-links a{display:inline-block;font-size:13px;font-weight:700;color:var(--text);background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px}'
      '.seo-links a:hover{border-color:var(--accent)}</style>')
    return ('<section class="seo-static">'+style+'<div class="wrap"><h2>이번 달 카드 발급 혜택·할인 한눈에 보기</h2>'
      +intro+'<div class="seo-tbl-wrap">'+table+'</div>'+rank+links+'</div></section>')
SEO_STATIC_INDEX=_seo_static_index()

# ===== BUILD =====
page("index.html",BRAND+" | 카드 발급 캐시백·할인 혜택 비교","같은 카드도 채널 따라 혜택이 달라요. 토스·카드고릴라·아정당·카카오페이의 발급 캐시백·할인을 카드티라노가 매달 비교해 드려요.","/index.html",INDEX_BODY+SEO_STATIC_INDEX,INDEX_JS,faq_jsonld(),searchbar=False,catstrip=False,active="")
page("discount.html",BRAND+" | 카드 할인 혜택 (가맹점·업종별)","네이버·쿠팡·무신사·이마트·GS25 등 가맹점의 카드 즉시할인·청구할인·캐시백·무이자할부를 업종·카드사별로.","/discount.html",DISC_BODY,DISC_JS,searchbar=True,catstrip=True,active="discount")
page("cards.html",BRAND+" | 카드 찾기 (카드사별 신용카드)","삼성·현대·신한·KB국민·롯데·우리·하나·NH농협·BC·IBK 카드사별 대표 신용카드를 플레이트 이미지·연회비·혜택으로 비교.","/cards.html",CARDS_BODY,CARDS_JS,active="cards")
page("issue.html",BRAND+" | 이번달 캐시백 (플랫폼별 비교)","카드사별 신규 발급 캐시백을 아정당·카드고릴라·토스·카카오페이 등 플랫폼별로 비교. 이번달 캐시백 리스트와 최대 혜택 비교표.","/issue.html",ISSUE_BODY,ISSUE_JS,active="issue")
page("detail.html",BRAND+" | 혜택 상세","카드 할인 혜택 상세와 공식 안내 링크.","/detail.html",DETAIL_BODY,DETAIL_JS,active="discount")
# ===== COMMUNITY (Cloudflare Workers + D1 백엔드 연동) =====
COMMUNITY_BODY=('<meta name="community-api" content="https://cardtyranno-community.yyty12.workers.dev">'   # 운영 라우트(/api/community) 쓰면 이 값을 "/api/community"로 교체. 현재는 배포된 Worker 직접 호출
 '<style>'
 '.cmwide{max-width:1320px}'
 '.cm-grid{display:grid;grid-template-columns:212px 1fr 300px;gap:30px;align-items:start;margin:22px 0 0}'
 '.cm-side,.cm-rail{position:sticky;top:78px}'
 '.cm-sh{font:800 11px var(--font-mono,monospace);letter-spacing:.05em;text-transform:uppercase;color:#9a9a9a;margin:0 0 10px;padding:0 6px}'
 '.cm-board{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px 12px;border-radius:11px;font-size:13.5px;font-weight:500;color:#000;cursor:pointer;text-decoration:none}'
 '.cm-board:hover{background:#f6f6f6}.cm-board.on{background:var(--surface-soft,#f4f4f5);font-weight:700}'
 '.cm-board .bd{width:8px;height:8px;border-radius:50%;flex:0 0 auto}.cm-board .nm{flex:1;min-width:0;display:flex;align-items:center;gap:8px}'
 '.cm-board .ct{font:11px var(--font-mono,monospace);color:#b0b0b0}'
 '.cm-rule{background:var(--block-cream,#f4ecd6);border-radius:16px;padding:16px;margin-top:18px}'
 '.cm-rule h4{font-size:13px;font-weight:800;margin:0 0 7px}.cm-rule p{font-size:11.5px;color:rgba(0,0,0,.62);line-height:1.55;margin:0}'
 '.cm-rule button{margin-top:10px;font-size:11.5px;font-weight:700;background:0;border:0;color:#000;text-decoration:underline;cursor:pointer;padding:0}'
 '.cm-mh{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:14px}'
 '.cm-eb{font:800 11px var(--font-mono,monospace);letter-spacing:.05em;text-transform:uppercase;color:#9a9a9a}'
 '.cm-mt{font-size:25px;font-weight:800;letter-spacing:-.5px;margin:5px 0 0}'
 '.cm-new{display:inline-flex;align-items:center;gap:6px;background:#000;color:#fff;font-weight:600;font-size:14px;padding:11px 20px;border-radius:50px;cursor:pointer;border:0;white-space:nowrap;flex:0 0 auto}'
 '.cm-sortrow{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--hairline,#e6e6e6);padding-bottom:11px;margin-bottom:2px}'
 '.cm-sort{font-size:13px;font-weight:600;color:#999;cursor:pointer;background:0;border:0;padding:0}.cm-sort.on{color:#000;font-weight:800}'
 '.cm-sortnote{margin-left:auto;font-size:11.5px;color:#b0b0b0}'
 '.cm-chips{display:none;flex-wrap:wrap;gap:7px;margin-bottom:14px}'
 '.cm-chip{font-weight:500;font-size:13px;padding:8px 13px;border-radius:50px;border:1px solid var(--hairline,#e6e6e6);background:#fff;color:#000;cursor:pointer}.cm-chip.on{background:#000;color:#fff;border-color:#000}'
 '.cm-list{display:flex;flex-direction:column}'
 '.cm-row{display:flex;align-items:center;gap:14px;padding:16px 4px;border-bottom:1px solid var(--hairline,#e6e6e6);text-decoration:none;color:#000;cursor:pointer}'
 '.cm-cat{font:800 10.5px var(--font-mono,monospace);text-transform:uppercase;letter-spacing:.03em;padding:4px 10px;border-radius:50px;color:#33402a;white-space:nowrap;flex:0 0 auto}'
 '.cm-rb{flex:1;min-width:0}.cm-rt{font-size:15.5px;font-weight:700;letter-spacing:-.2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
 '.cm-rm{font-size:12px;color:#8a8a8a;margin-top:5px}'
 '.cm-rs{flex:0 0 auto;font-size:12px;color:#8a8a8a;text-align:right;white-space:nowrap}.cm-rs b{color:var(--accent-magenta,#ff3d8b);font-weight:800}'
 '.cm-th{width:60px;height:46px;border-radius:8px;overflow:hidden;background:#f3f3f3;flex:0 0 auto}.cm-th img{width:100%;height:100%;object-fit:cover}'
 '.cm-more{display:block;width:100%;margin:18px 0;padding:13px;border:1px solid var(--hairline,#e6e6e6);border-radius:50px;background:#fff;font-weight:600;cursor:pointer}'
 '.cm-empty{padding:48px 0;text-align:center;color:#999}'
 '.cm-rail-card{border:1px solid var(--hairline,#e6e6e6);border-radius:16px;padding:16px;margin-bottom:16px}'
 '.cm-pop{list-style:none;margin:0;padding:0}.cm-pop li{display:flex;gap:10px;padding:9px 0;border-top:1px solid #f2f2f2;cursor:pointer}.cm-pop li:first-child{border-top:0}'
 '.cm-pop .rk{font-style:italic;font-weight:900;font-size:13px;color:#c4c4c4;width:14px;flex:0 0 auto}.cm-pop li:first-child .rk{color:var(--accent-magenta,#ff3d8b)}'
 '.cm-pop .pt{font-size:13px;font-weight:600;line-height:1.4;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}'
 '.cm-ad{border:1px dashed #d6d6d6;border-radius:16px;padding:18px 16px;text-align:center;text-decoration:none;color:#000;display:block}'
 '.cm-ad .adl{font:800 10px var(--font-mono,monospace);color:#b0b0b0;letter-spacing:.05em}.cm-ad .adt{font-size:14px;font-weight:800;margin-top:7px}.cm-ad .ads{font-size:11px;color:#999;margin-top:5px}'
 '.cm-form{border:1px solid var(--hairline,#e6e6e6);border-radius:20px;padding:22px;margin:6px 0 18px;background:#fff}'
 '.cm-form h3{font-size:17px;font-weight:800;margin:0 0 16px}'
 '.cm-f{display:flex;flex-direction:column;gap:5px;margin-bottom:13px}.cm-f label{font-size:12px;font-weight:700;color:#777}'
 '.cm-f input,.cm-f select,.cm-f textarea{border:1px solid var(--hairline,#e6e6e6);border-radius:10px;padding:11px 13px;font-size:14.5px;font-family:inherit;background:#fff;width:100%}'
 '.cm-f textarea{min-height:150px;resize:vertical;line-height:1.6}'
 '.cm-frow{display:flex;gap:10px;flex-wrap:wrap}.cm-frow .cm-f{flex:1;min-width:120px}'
 '.cm-bchips{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:14px}.cm-bchip{font-size:13px;font-weight:600;padding:8px 13px;border-radius:50px;border:1px solid var(--hairline,#e6e6e6);background:#fff;cursor:pointer}.cm-bchip.on{background:#000;color:#fff;border-color:#000}'
 '.cm-noticebox{background:var(--block-cream,#f4ecd6);border-radius:13px;padding:14px 16px;font-size:12px;color:rgba(0,0,0,.66);line-height:1.6;margin:6px 0 14px}'
 '.cm-actions{display:flex;gap:8px;margin-top:6px}'
 '.cm-btn{background:#000;color:#fff;font-weight:600;font-size:14px;padding:12px 22px;border-radius:50px;border:0;cursor:pointer}.cm-btn.ghost{background:#fff;color:#000;border:1px solid var(--hairline,#e6e6e6)}'
 '.cm-err{color:#d33;font-size:13px;margin-top:8px;min-height:18px}'
 '.cm-back{font:600 12.5px var(--font-mono,monospace);color:#888;text-decoration:none;display:inline-flex;align-items:center;gap:5px;margin:0 0 16px}'
 '.cm-d-top{display:flex;align-items:center;justify-content:space-between;gap:10px}'
 '.cm-d-cat{display:inline-block;font:800 10.5px var(--font-mono,monospace);text-transform:uppercase;padding:5px 12px;border-radius:50px;color:#33402a}'
 '.cm-flag{font-size:12px;color:#aaa;background:0;border:0;cursor:pointer;display:inline-flex;align-items:center;gap:4px}'
 '.cm-d-title{font-size:26px;font-weight:800;letter-spacing:-.5px;line-height:1.3;margin:12px 0 8px}'
 '.cm-ava{width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto}.cm-ava svg{width:15px;height:15px;color:#fff}'
 '.cm-d-meta{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#888;border-bottom:1px solid var(--hairline,#e6e6e6);padding-bottom:16px}'
 '.cm-d-body{font-size:15.5px;line-height:1.8;color:#222;white-space:pre-wrap;padding:18px 0}'
 '.cm-d-card{display:block;border:1px solid var(--hairline,#e6e6e6);border-radius:14px;padding:13px 15px;margin:4px 0 16px;text-decoration:none;color:#000}'
 '.cm-d-card .ct{display:flex;align-items:center;justify-content:space-between;gap:8px}.cm-d-card .cn{font-size:14px;font-weight:700}.cm-d-card .cg{font-size:12px;color:#888}'
 '.cm-d-card .disc{font-size:11px;color:#999;margin-top:7px;line-height:1.5}'
 '.cm-dacts{display:flex;gap:8px;border-top:1px solid var(--hairline,#e6e6e6);border-bottom:1px solid var(--hairline,#e6e6e6);padding:12px 0;margin-bottom:6px}'
 '.cm-actb{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--hairline,#e6e6e6);background:#fff;border-radius:50px;padding:9px 16px;font-weight:700;font-size:13.5px;cursor:pointer}.cm-actb.on{background:#000;color:#fff;border-color:#000}.cm-actb svg{width:16px;height:16px}'
 '.cm-owner{display:flex;gap:8px;margin:10px 0}'
 '.cm-ctitle{font-size:15px;font-weight:800;margin:22px 0 4px}.cm-ctitle b{color:var(--accent-magenta,#ff3d8b)}'
 '.cm-cmt{padding:14px 0;border-bottom:1px solid #f2f2f2}.cm-cmt.reply{margin-left:40px;border-bottom:0;padding:10px 0 4px}'
 '.cm-cmt-h{display:flex;align-items:center;justify-content:space-between;gap:10px}'
 '.cm-cmt-n{font-weight:700;font-size:13.5px;display:inline-flex;align-items:center;gap:7px}.cm-cmt-t{font-size:11px;color:#aaa}'
 '.cm-cmt-c{font-size:14.5px;line-height:1.6;margin-top:6px;white-space:pre-wrap}'
 '.cm-cmt-a{font-size:12px;color:#999;cursor:pointer;background:none;border:0;padding:2px 4px}.cm-cmt-a.lk.on{color:var(--accent-magenta,#ff3d8b);font-weight:700}'
 '.cm-fab{position:fixed;right:18px;bottom:78px;width:54px;height:54px;border-radius:50%;background:#000;color:#fff;border:0;display:none;align-items:center;justify-content:center;z-index:30;box-shadow:0 6px 18px rgba(0,0,0,.28);cursor:pointer}.cm-fab svg{width:24px;height:24px}'
 '.cm-modal{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;align-items:center;justify-content:center;z-index:60;padding:20px}.cm-modal.on{display:flex}'
 '.cm-modal .mc{background:#fff;border-radius:20px;max-width:480px;width:100%;max-height:84vh;overflow:auto;padding:26px}'
 '.cm-modal h3{font-size:18px;font-weight:800;margin:0 0 14px}.cm-modal ol{margin:0;padding-left:18px}.cm-modal li{font-size:13px;line-height:1.7;color:#333;margin-bottom:10px}.cm-modal li b{font-weight:800}'
 '.cm-modal .mx{float:right;font-size:22px;line-height:1;background:0;border:0;cursor:pointer;color:#999;margin:-6px -4px 0 0}'
 '.cm-legal{margin-top:48px;background:#16161b;color:#cfcfd6;border-radius:20px;padding:26px 28px;font-size:12px;line-height:1.7}.cm-legal a{color:#fff;text-decoration:none;margin-right:14px;font-weight:600}'
 '@media(max-width:900px){.cm-grid{grid-template-columns:1fr;gap:0}.cm-side{position:static;display:none}.cm-rail{position:static;order:3;margin-top:30px}.cm-chips{display:flex}.cm-fab{display:flex}.cm-mt{font-size:21px}.cm-d-title{font-size:21px}.cm-cmt.reply{margin-left:24px}}'
 '</style>'
 '<div class="wrap cmwide"><div class="cm-grid">'
 '<aside class="cm-side"><div class="cm-sh">게시판</div><nav id="cmBoards"></nav>'
 '<div class="cm-rule"><h4>커뮤니티 운영 원칙</h4><p>이용자 간 후기·정보를 나누는 공간이에요. 허위·과장, 영리 광고·발급 유도는 제한됩니다.</p><button id="cmRuleOpen">운영정책 전문 보기</button></div></aside>'
 '<main class="cm-main"><div id="cmView"></div></main>'
 '<aside class="cm-rail"><div class="cm-rail-card"><div class="cm-sh" style="margin-bottom:12px">주간 인기글</div><ol class="cm-pop" id="cmPop"></ol><div style="font-size:10.5px;color:#b8b8b8;margin-top:10px">공감·조회수 기준 자동 집계</div></div>'
 '<a class="cm-ad" href="issue.html?v=cmp" rel="sponsored nofollow noopener"><div class="adl">광고(AD)</div><div class="adt">이번 달 최대 캐시백 카드</div><div class="ads">외부 광고 링크 · 카드사·플랫폼으로 이동</div></a></aside>'
 '</div></div>'
 '<button class="cm-fab" id="cmFab" aria-label="글쓰기"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></button>'
 '<div class="cm-modal" id="cmRuleModal"><div class="mc"><button class="mx" id="cmRuleClose">&times;</button><h3>커뮤니티 운영정책</h3><ol>'
 '<li><b>정보 공유 공간</b> · 게시물은 이용자 개인 의견이며 카드티라노가 내용을 보증하지 않습니다. 발급을 중개·접수하지 않습니다.</li>'
 '<li><b>금지 행위</b> · 허위·과장, 영리 목적 광고·발급 유도, 비방·개인정보 노출, 도배를 금지합니다.</li>'
 '<li><b>혜택 정보 책임</b> · 캐시백·혜택은 작성 시점 기준이며, 신청 전 각 카드사·플랫폼에서 최종 확인이 필요합니다.</li>'
 '<li><b>신고·제재</b> · 신고된 게시물·댓글은 검토 후 조치하며, 반복 위반 시 작성이 영구 제한될 수 있습니다.</li>'
 '</ol></div></div>'
 '<div class="wrap cmwide"><div class="cm-legal">커뮤니티는 이용자 간 후기·정보 공유 공간이며 게시물은 작성자 개인 의견입니다. 카드티라노는 광고·정보제공 매체로 발급을 중개·접수하지 않습니다. 혜택은 수집 시점 기준이며 일부 제휴(광고) 링크가 포함됩니다.<div style="margin-top:14px"><a href="terms.html">이용약관</a><a href="privacy.html">개인정보처리방침</a><a href="#" id="cmRuleLink2">운영정책</a><a href="business.html">사업자정보</a></div></div></div>')
COMMUNITY_JS=r"""
var CAPI=(window.COMMUNITY_API)||((document.querySelector('meta[name=community-api]')||{}).content)||'https://cardtyranno-community.yyty12.workers.dev';
if(CAPI && CAPI.indexOf('/api')<0 && CAPI.indexOf('http')!==0) CAPI=location.origin+CAPI;
var BOARDS=[{k:'발급 후기',s:'발급후기',c:'#c8e6cd'},{k:'혜택·캐시백 후기',s:'혜택후기',c:'#dceeb1'},{k:'질문 Q&A',s:'질문',c:'#c5b0f4'},{k:'카드 추천 요청',s:'추천요청',c:'#f6c9c0'},{k:'꿀팁 공유',s:'꿀팁',c:'#f4ecd6'},{k:'자유게시판',s:'자유',c:'#f0f0f1'}];
var BMAP={};BOARDS.forEach(function(b){BMAP[b.k]=b;});
var cmCat='전체',cmSort='new',cmPage=1;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function api(path,opt){return fetch(CAPI.replace(/\/$/,'')+path,opt).then(function(r){return r.json().then(function(j){if(!r.ok)throw new Error(j.error||('오류 '+r.status));return j;});}).catch(function(e){if(e&&(e.name==='TypeError'||/Failed to fetch|NetworkError|fetch/i.test(e.message||'')))throw new Error('커뮤니티 서버에 연결할 수 없어요. 백엔드(Worker)가 아직 배포·연결되지 않았어요.');throw e;});}
function ago(s){if(!s)return'';var d=new Date(s.replace(' ','T')+'Z');var m=Math.floor((Date.now()-d.getTime())/60000);if(m<1)return'방금';if(m<60)return m+'분 전';if(m<1440)return Math.floor(m/60)+'시간 전';return Math.floor(m/1440)+'일 전';}
function _o(k){try{return JSON.parse(localStorage.getItem(k)||'{}');}catch(e){return{};}}
function lks(id){return !!_o('cmlk')[id];}
function setLk(id,v){var o=_o('cmlk');if(v)o[id]=1;else delete o[id];try{localStorage.setItem('cmlk',JSON.stringify(o));}catch(e){}}
function scr(id){return !!_o('cmsc')[id];}
function setScr(id,v){var o=_o('cmsc');if(v)o[id]=1;else delete o[id];try{localStorage.setItem('cmsc',JSON.stringify(o));}catch(e){}}
function val(id){return (document.getElementById(id).value||'').trim();}
function err(id,m){var e=document.getElementById(id);if(e)e.textContent=m||'';}
function V(){return document.getElementById('cmView');}
function tag(cat){var b=BMAP[cat];return '<span class="cm-cat" style="background:'+(b?b.c:'#f0f0f1')+'">'+esc(b?b.s:cat)+'</span>';}
function ava(cat){var b=BMAP[cat];return '<span class="cm-ava" style="background:'+(b?b.c:'#c5b0f4')+'"><svg viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg></span>';}
function go(q){history.pushState({},'','community.html'+(q||''));route();}
// 좌측 게시판 사이드바
function renderBoards(){var n=document.getElementById('cmBoards');var all=[{k:'전체',s:'전체',c:'#000'}].concat(BOARDS);
 n.innerHTML=all.map(function(b){return '<a class="cm-board'+(b.k===cmCat?' on':'')+'" href="community.html?cat='+encodeURIComponent(b.k)+'" data-c="'+esc(b.k)+'"><span class="nm">'+(b.k==='전체'?'':'<span class="bd" style="background:'+b.c+'"></span>')+esc(b.k)+'</span></a>';}).join('');
 n.querySelectorAll('[data-c]').forEach(function(a){a.onclick=function(e){e.preventDefault();cmCat=a.getAttribute('data-c');renderBoards();go('?cat='+encodeURIComponent(cmCat));};});}
// 우측 주간 인기글
function renderPop(){var P=document.getElementById('cmPop');api('/api/posts?sort=popular&size=5').then(function(j){var ps=j.posts||[];if(!ps.length){P.innerHTML='<li style="color:#bbb;font-size:12px">아직 인기글이 없어요</li>';return;}
 P.innerHTML=ps.map(function(p,i){return '<li data-id="'+p.id+'"><span class="rk">'+(i+1)+'</span><div class="pt">'+esc(p.title)+'</div></li>';}).join('');
 P.querySelectorAll('[data-id]').forEach(function(l){l.onclick=function(){go('?id='+l.getAttribute('data-id'));};});
}).catch(function(){P.innerHTML='<li style="color:#bbb;font-size:12px">불러올 수 없어요</li>';});}
// 피드
function feed(){cmPage=1;var ttl=cmCat==='전체'?'카드 라운지':cmCat;
 V().innerHTML='<div class="cm-mh"><div><div class="cm-eb">COMMUNITY · '+esc(cmCat)+'</div><h2 class="cm-mt">'+esc(ttl)+'</h2></div><button class="cm-new" id="cmNew">글쓰기 <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button></div>'
  +'<div class="cm-chips" id="cmChips"></div>'
  +'<div class="cm-sortrow"><button class="cm-sort'+(cmSort==='new'?' on':'')+'" data-s="new">최신순</button><button class="cm-sort'+(cmSort==='popular'?' on':'')+'" data-s="popular">공감순</button><button class="cm-sort'+(cmSort==='cmt'?' on':'')+'" data-s="cmt">댓글순</button><span class="cm-sortnote">공개 데이터 기준 자동 정렬</span></div>'
  +'<div class="cm-list" id="cmRows"><div class="cm-empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
  +'<button class="cm-more" id="cmMore" style="display:none">더 보기</button>';
 var ch=document.getElementById('cmChips');var all=['전체'].concat(BOARDS.map(function(b){return b.k;}));
 ch.innerHTML=all.map(function(k){return '<button class="cm-chip'+(k===cmCat?' on':'')+'" data-c="'+esc(k)+'">'+esc(BMAP[k]?BMAP[k].s:k)+'</button>';}).join('');
 ch.querySelectorAll('[data-c]').forEach(function(b){b.onclick=function(){cmCat=b.getAttribute('data-c');renderBoards();go('?cat='+encodeURIComponent(cmCat));};});
 document.getElementById('cmNew').onclick=function(){go('?view=write');};
 V().querySelectorAll('.cm-sort').forEach(function(b){b.onclick=function(){cmSort=b.getAttribute('data-s');feed();};});
 document.getElementById('cmMore').onclick=function(){cmPage++;loadList(false);};
 loadList(true);}
function rowHtml(p){var img=p.image||p.img||'';return '<a class="cm-row" href="community.html?id='+p.id+'" data-id="'+p.id+'">'+tag(p.category)+'<div class="cm-rb"><div class="cm-rt">'+esc(p.title)+(p.comment_count?' <span style="color:var(--accent-magenta);font-weight:800">['+p.comment_count+']</span>':'')+'</div><div class="cm-rm">'+esc(p.author_nickname||'익명')+' · '+ago(p.created_at)+' · 조회 '+(p.views||0)+'</div></div><div class="cm-rs"><b>♥ '+(p.likes||0)+'</b><br>댓글 '+(p.comment_count||0)+'</div>'+(img?'<span class="cm-th"><img src="'+esc(img)+'" alt=""></span>':'')+'</a>';}
function loadList(reset){var R=document.getElementById('cmRows');if(!R)return;if(reset)R.innerHTML='';
 var srt=cmSort==='cmt'?'popular':cmSort;
 var q='?page='+cmPage+'&size=20&sort='+srt+(cmCat!=='전체'?'&category='+encodeURIComponent(cmCat):'');
 api('/api/posts'+q).then(function(j){var ps=j.posts||[];if(cmSort==='cmt')ps=ps.slice().sort(function(a,b){return (b.comment_count||0)-(a.comment_count||0);});
  if(reset)R.innerHTML='';
  if(cmPage===1&&!ps.length){R.innerHTML='<div class="cm-empty">아직 글이 없어요. 첫 글을 남겨보세요!</div>';var mm=document.getElementById('cmMore');if(mm)mm.style.display='none';return;}
  ps.forEach(function(p){R.insertAdjacentHTML('beforeend',rowHtml(p));});
  R.querySelectorAll('[data-id]').forEach(function(a){a.onclick=function(e){e.preventDefault();go('?id='+a.getAttribute('data-id'));};});
  var mm=document.getElementById('cmMore');if(mm)mm.style.display=(cmPage*(j.size||20)>=(j.total||0))?'none':'block';
 }).catch(function(e){R.innerHTML='<div class="cm-empty">목록을 불러오지 못했어요.<br><span style="font-size:12px;color:#bbb">API 미연결 시 community-worker 배포 후 API 주소를 설정하세요.</span></div>';});}
// 글쓰기
function writeForm(){V().innerHTML='<a class="cm-back" id="cmBack"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>커뮤니티로</a>'
  +'<div class="cm-form"><h3>글쓰기</h3><div class="cm-bchips" id="wfboards"></div>'
  +'<div class="cm-frow"><div class="cm-f"><label>닉네임</label><input id="wfn" maxlength="20" placeholder="닉네임(비우면 익명)"></div><div class="cm-f"><label>비밀번호(4자리)</label><input id="wfp" maxlength="4" inputmode="numeric" placeholder="0000"></div></div>'
  +'<div class="cm-f"><label>제목</label><input id="wft" maxlength="120" placeholder="제목"></div>'
  +'<div class="cm-f"><label>내용</label><textarea id="wfb" placeholder="혜택·후기를 자유롭게 남겨주세요"></textarea></div>'
  +'<div class="cm-f"><label>카드 태그 (선택)</label><input id="wfe" maxlength="120" placeholder="예: KB국민 굿데이카드"></div>'
  +'<div class="cm-noticebox">허위·과장, 영리 목적 광고·발급 유도, 비방·개인정보는 제한됩니다. 게시 혜택 정보는 수집 시점 기준이며 신청 전 카드사·플랫폼에서 최종 확인이 필요합니다.</div>'
  +'<div class="cm-err" id="wferr"></div><div class="cm-actions"><button class="cm-btn" id="wfsave">등록</button><button class="cm-btn ghost" id="wfcancel">취소</button></div></div>';
 var sel=BMAP[cmCat]?cmCat:BOARDS[0].k;var wb=document.getElementById('wfboards');
 wb.innerHTML=BOARDS.map(function(b){return '<button class="cm-bchip'+(b.k===sel?' on':'')+'" data-b="'+esc(b.k)+'">'+esc(b.s)+'</button>';}).join('');
 wb.querySelectorAll('[data-b]').forEach(function(x){x.onclick=function(){sel=x.getAttribute('data-b');wb.querySelectorAll('.cm-bchip').forEach(function(y){y.classList.remove('on');});x.classList.add('on');};});
 document.getElementById('cmBack').onclick=document.getElementById('wfcancel').onclick=function(){go('?cat='+encodeURIComponent(cmCat));};
 document.getElementById('wfsave').onclick=function(){
  var body={nickname:val('wfn')||'익명',password:val('wfp'),category:sel,title:val('wft'),content:val('wfb'),card_event_id:val('wfe')};
  if(!body.title||!body.content){err('wferr','제목·내용을 입력해주세요.');return;}
  if(!/^\d{4}$/.test(body.password)){err('wferr','비밀번호는 4자리 숫자예요.');return;}
  api('/api/posts',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}).then(function(j){go('?id='+j.id);}).catch(function(e){err('wferr',e.message);});};}
// 글 상세
function detail(id){V().innerHTML='<div class="cm-empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div>';
 api('/api/posts/'+id).then(function(j){var p=j.post;document.title=p.title+' | 카드티라노 커뮤니티';
  var liked=lks('p'+id),scrap=scr('p'+id);
  var ct=p.card_event_id?('<a class="cm-d-card" href="'+(/\.html|^http/.test(p.card_event_id)?esc(p.card_event_id):('carddetail.html?n='+encodeURIComponent(p.card_event_id)))+'" rel="sponsored nofollow noopener"><div class="ct"><span class="cn">'+esc(p.card_event_id)+'</span><span class="cg">자세히 보기 ›</span></div><div class="disc">이용자 후기 · 최대 금액 기준, 조건 충족 시 · 카드티라노는 발급을 중개하지 않습니다.</div></a>'):'';
  V().innerHTML='<a class="cm-back" id="cmBack"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>커뮤니티로</a>'
   +'<div class="cm-d-top">'+tag(p.category)+'<button class="cm-flag" id="cmFlag"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V4h13l-2 4 2 4H4"/></svg>신고</button></div>'
   +'<div class="cm-d-title">'+esc(p.title)+'</div>'
   +'<div class="cm-d-meta">'+ava(p.category)+'<b>'+esc(p.author_nickname||'익명')+'</b> · '+ago(p.created_at)+' · 조회 '+p.views+'</div>'
   +'<div class="cm-d-body">'+esc(p.content)+'</div>'+ct
   +'<div class="cm-dacts"><button class="cm-actb'+(liked?' on':'')+'" id="cmLike"><svg viewBox="0 0 24 24" fill="'+(liked?'currentColor':'none')+'" stroke="currentColor" stroke-width="2"><path d="M12 20S4 15.3 4 9.8A3.9 3.9 0 0 1 12 7.6 3.9 3.9 0 0 1 20 9.8C20 15.3 12 20 12 20Z"/></svg>공감 <span id="cmLikeN">'+p.likes+'</span></button>'
   +'<button class="cm-actb'+(scrap?' on':'')+'" id="cmScrap"><svg viewBox="0 0 24 24" fill="'+(scrap?'currentColor':'none')+'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h12v16l-6-4-6 4z"/></svg>스크랩</button></div>'
   +'<div class="cm-owner"><button class="cm-btn ghost" id="cmEdit">수정</button><button class="cm-btn ghost" id="cmDel">삭제</button></div><div class="cm-err" id="cmoerr"></div>'
   +'<div class="cm-ctitle">댓글 <b>'+j.comments.length+'</b></div><div class="cm-cmts" id="cmCmts"></div>'
   +'<div class="cm-form" style="margin-top:14px"><div class="cm-frow"><div class="cm-f"><label>닉네임</label><input id="cfn" maxlength="20" placeholder="익명"></div><div class="cm-f"><label>비밀번호(4자리)</label><input id="cfp" maxlength="4" inputmode="numeric"></div></div><div class="cm-f"><label>댓글</label><textarea id="cfb" style="min-height:74px" placeholder="댓글을 남겨주세요"></textarea></div><div class="cm-err" id="cferr"></div><div class="cm-actions"><button class="cm-btn" id="cfsave">댓글 등록</button></div></div>';
  renderCmts(j.comments,id);
  document.getElementById('cmBack').onclick=function(){go('?cat='+encodeURIComponent(cmCat));};
  document.getElementById('cmFlag').onclick=function(){if(confirm('이 게시물을 신고할까요? 검토 후 조치됩니다.')){alert('신고가 접수되었어요. 검토 후 조치할게요.');}};
  document.getElementById('cmScrap').onclick=function(){var v=!scr('p'+id);setScr('p'+id,v);this.classList.toggle('on',v);this.querySelector('svg').setAttribute('fill',v?'currentColor':'none');};
  document.getElementById('cmLike').onclick=function(){var b=this;api('/api/posts/'+id+'/like',{method:'POST'}).then(function(r){document.getElementById('cmLikeN').textContent=r.likes;b.classList.toggle('on',r.liked);b.querySelector('svg').setAttribute('fill',r.liked?'currentColor':'none');setLk('p'+id,r.liked);});};
  document.getElementById('cfsave').onclick=function(){var body={nickname:val('cfn')||'익명',password:val('cfp'),content:val('cfb')};if(!body.content){err('cferr','내용을 입력해주세요.');return;}if(!/^\d{4}$/.test(body.password)){err('cferr','비밀번호 4자리.');return;}api('/api/posts/'+id+'/comments',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}).then(function(){detail(id);}).catch(function(e){err('cferr',e.message);});};
  document.getElementById('cmDel').onclick=function(){var pw=prompt('글 비밀번호(4자리)');if(!pw)return;api('/api/posts/'+id,{method:'DELETE',headers:{'content-type':'application/json'},body:JSON.stringify({password:pw})}).then(function(){go('?cat='+encodeURIComponent(cmCat));}).catch(function(e){err('cmoerr',e.message);});};
  document.getElementById('cmEdit').onclick=function(){editForm(p);};
 }).catch(function(e){V().innerHTML='<a class="cm-back" href="community.html">← 커뮤니티로</a><div class="cm-empty">'+esc(e.message)+'</div>';});}
function renderCmts(cs,pid){var C=document.getElementById('cmCmts');if(!cs.length){C.innerHTML='<div style="color:#aaa;font-size:13px;padding:12px 0">첫 댓글을 남겨보세요.</div>';return;}
 C.innerHTML=cs.map(function(c){var liked=lks('c'+c.id);var rep=c.parent_id?' reply':'';return '<div class="cm-cmt'+rep+'"><div class="cm-cmt-h"><span class="cm-cmt-n">'+ava(BMAP[c.category]?c.category:'자유게시판').replace('cm-ava','cm-ava" style="width:20px;height:20px')+esc(c.author_nickname||'익명')+' <span class="cm-cmt-t">'+ago(c.created_at)+'</span></span><span><button class="cm-cmt-a lk'+(liked?' on':'')+'" data-lc="'+c.id+'">♥ <span>'+(c.likes||0)+'</span></button> <button class="cm-cmt-a" data-dc="'+c.id+'">삭제</button></span></div><div class="cm-cmt-c">'+esc(c.content)+'</div></div>';}).join('');
 C.querySelectorAll('[data-lc]').forEach(function(b){b.onclick=function(){var cid=b.dataset.lc;api('/api/comments/'+cid+'/like',{method:'POST'}).then(function(r){b.querySelector('span').textContent=r.likes;b.classList.toggle('on',r.liked);setLk('c'+cid,r.liked);});};});
 C.querySelectorAll('[data-dc]').forEach(function(b){b.onclick=function(){var pw=prompt('댓글 비밀번호(4자리)');if(!pw)return;api('/api/comments/'+b.dataset.dc,{method:'DELETE',headers:{'content-type':'application/json'},body:JSON.stringify({password:pw})}).then(function(){detail(pid);}).catch(function(e){alert(e.message);});};});}
function editForm(p){V().innerHTML='<a class="cm-back" id="cmBack"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>취소</a><div class="cm-form"><h3>글 수정</h3><div class="cm-bchips" id="efboards"></div><div class="cm-f"><label>비밀번호(4자리)</label><input id="efp" maxlength="4" inputmode="numeric"></div><div class="cm-f"><label>제목</label><input id="eft" maxlength="120"></div><div class="cm-f"><label>내용</label><textarea id="efb"></textarea></div><div class="cm-err" id="eferr"></div><div class="cm-actions"><button class="cm-btn" id="efsave">수정 저장</button></div></div>';
 var sel=p.category;var eb=document.getElementById('efboards');eb.innerHTML=BOARDS.map(function(b){return '<button class="cm-bchip'+(b.k===sel?' on':'')+'" data-b="'+esc(b.k)+'">'+esc(b.s)+'</button>';}).join('');
 eb.querySelectorAll('[data-b]').forEach(function(x){x.onclick=function(){sel=x.getAttribute('data-b');eb.querySelectorAll('.cm-bchip').forEach(function(y){y.classList.remove('on');});x.classList.add('on');};});
 document.getElementById('eft').value=p.title;document.getElementById('efb').value=p.content;
 document.getElementById('cmBack').onclick=function(){go('?id='+p.id);};
 document.getElementById('efsave').onclick=function(){var body={password:val('efp'),title:val('eft'),content:val('efb'),category:sel};if(!/^\d{4}$/.test(body.password)){err('eferr','비밀번호 4자리.');return;}api('/api/posts/'+p.id,{method:'PUT',headers:{'content-type':'application/json'},body:JSON.stringify(body)}).then(function(){go('?id='+p.id);}).catch(function(e){err('eferr',e.message);});};}
// 내 활동(스크랩)
function profile(){var ids=Object.keys(_o('cmsc')).map(function(k){return k.replace(/^p/,'');});
 V().innerHTML='<div class="cm-mh"><div><div class="cm-eb">COMMUNITY · 내 활동</div><h2 class="cm-mt">스크랩한 글</h2></div></div><div class="cm-list" id="cmRows"></div>';
 var R=document.getElementById('cmRows');if(!ids.length){R.innerHTML='<div class="cm-empty">스크랩한 글이 없어요. 글 상세에서 스크랩해 보세요.</div>';return;}
 Promise.all(ids.map(function(id){return api('/api/posts/'+id).then(function(j){return j.post;}).catch(function(){return null;});})).then(function(ps){
  ps=ps.filter(Boolean);R.innerHTML=ps.length?'':'<div class="cm-empty">스크랩한 글을 불러올 수 없어요.</div>';
  ps.forEach(function(p){R.insertAdjacentHTML('beforeend',rowHtml(p));});
  R.querySelectorAll('[data-id]').forEach(function(a){a.onclick=function(e){e.preventDefault();go('?id='+a.getAttribute('data-id'));};});});}
// 운영정책 모달
function bindModal(){var m=document.getElementById('cmRuleModal');function open(){m.classList.add('on');}function close(){m.classList.remove('on');}
 document.getElementById('cmRuleOpen').onclick=open;document.getElementById('cmRuleClose').onclick=close;
 var l2=document.getElementById('cmRuleLink2');if(l2)l2.onclick=function(e){e.preventDefault();open();};
 m.onclick=function(e){if(e.target===m)close();};document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
 document.getElementById('cmFab').onclick=function(){go('?view=write');};}
function route(){var sp=new URLSearchParams(location.search);var id=sp.get('id'),view=sp.get('view'),cat=sp.get('cat');
 if(cat&&(cat==='전체'||BMAP[cat])){cmCat=cat;}renderBoards();
 if(id){detail(id);}else if(view==='write'||sp.get('new')){writeForm();}else if(view==='profile'){profile();}else{feed();}
 window.scrollTo(0,0);}
window.addEventListener('popstate',route);
renderBoards();renderPop();bindModal();route();
"""
page("community.html",BRAND+" | 커뮤니티 (카드 라운지)","카드 발급 후기·추천·이벤트 공유 커뮤니티. 닉네임으로 글·댓글·좋아요.","/community.html",COMMUNITY_BODY,COMMUNITY_JS,active="community")
page("content.html",BRAND+" | 카드 가이드","연회비 캐시백, 전월실적, 즉시할인 vs 청구할인, 해외카드까지 카드 똑똑하게 쓰는 법.","/content.html",CONTENT_BODY,CONTENT_JS,active="content")
page("carddetail.html",BRAND+" | 카드 상세 혜택","카드별 영역 혜택·연회비·전월실적·발급 이벤트를 한눈에. 플랫폼별 신청 링크 제공.","/carddetail.html",CARDDETAIL_BODY,CARDDETAIL_JS,active="cards")
page("events.html",BRAND+" | 발급 이벤트 상세","카드 발급 이벤트의 최근 캐시백 추이(당월 포함)·주요/부가 혜택·발급 적기 진단·추천 이벤트를 한눈에.","/events.html",EVENTDETAIL_BODY,EVENTDETAIL_JS,active="issue")
page("chart.html",BRAND+" | 티라노차트","시중 플랫폼(토스·카드고릴라·뱅크샐러드) 순위를 평균낸 카드티라노 티라노차트.","/chart.html",CHART_BODY,CHART_JS,active="charts")
page("trends.html",BRAND+" | 월별 캐시백 추이","카드사·카드상품별 발급 캐시백의 월별 변화를 플랫폼별로 보여주는 추이 차트. 매월 스냅샷 누적.","/trends.html",TRENDS_BODY,TRENDS_JS,active="trends")
page("favorites.html",BRAND+" | 관심 카드","담아둔 관심 카드를 한눈에 비교. 로그인 없이 브라우저에 저장.","/favorites.html",FAV_BODY,FAV_JS,active="")
page("search.html",BRAND+" | 검색","카드·카드사·가맹점·혜택을 한 번에 검색.","/search.html",SEARCH_BODY,SEARCH_JS,active="")
page("installment.html",BRAND+" | 무이자·부분무이자 할부","카드사별·업종별(항공·백화점·가전) 무이자/부분무이자 할부를 매월 갱신해 한곳에 정리.","/installment.html",INSTALLMENT_BODY,"",active="discount")
page("dashboard.html",BRAND+" | 통계 대시보드","방문·클릭 통계 (관리자 전용).","/dashboard.html",DASHBOARD_BODY,DASHBOARD_JS,active="",noindex=True)

# ===== 법적 페이지 (LEGAL.md §6 · 0628 §F11) =====
_LGL_DOCS=[("terms.html","이용약관"),("privacy.html","개인정보처리방침"),("business.html","사업자정보")]
def _legal_nav(cur):
    n='<nav class="lgl-nav"><div class="lnh">LEGAL</div>'
    for href,label in _LGL_DOCS:
        on=' class="on"' if href==cur else ''
        n+='<a href="'+href+'"'+on+'>'+label+'</a>'
    n+='</nav>'
    return n
def _legal_body(badge,title,updated,sections,foot="",cur=""):
    h=('<div class="wrap" style="max-width:980px"><div class="lgl lgl-grid">'
       +_legal_nav(cur)+'<div class="lgl-main">'
       '<div class="lgl-eb">'+badge+'</div><h1 class="lgl-h">'+title+'</h1>'
       '<div class="lgl-date">시행일·최종 개정일 '+updated+'</div>')
    for st,bd in sections:
        h+='<section class="lgl-sec"><h2>'+st+'</h2>'+bd+'</section>'
    h+=foot+'</div></div></div>'
    return h

_TERMS=[
 ("제1조 (목적)","<p>본 약관은 쥬라기랩스(이하 \"회사\")가 운영하는 카드티라노(CARDTYRANNO, 이하 \"서비스\")의 이용 조건과 절차, 회사와 이용자의 권리·의무 및 책임사항을 규정함을 목적으로 합니다.</p>"),
 ("제2조 (정의)","<p>① \"서비스\"란 회사가 카드사·제휴 플랫폼의 카드 상품 및 이벤트 정보를 수집·비교·제공하는 광고·정보제공 매체를 말합니다.<br>② \"이용자\"란 본 약관에 따라 서비스를 이용하는 모든 방문자를 말합니다.<br>③ \"제휴(광고) 링크\"란 이용자를 카드사·플랫폼 등 외부 페이지로 연결하는 링크로, 이를 통해 회사가 광고 수수료를 받을 수 있는 링크를 말합니다.</p>"),
 ("제3조 (서비스의 성격 · 비중개 고지)","<p>① 회사는 <b>광고·정보제공 매체</b>로서 공개된 정보를 수집·정리하여 제공할 뿐, <b>카드 발급을 중개·접수·대리하지 않습니다.</b><br>② 카드의 신청·발급·심사·승인 및 혜택의 최종 지급은 전적으로 각 카드사 및 제휴 플랫폼이 자신의 기준과 책임 하에 수행합니다.<br>③ 서비스의 순위·정렬은 공개 데이터를 기준으로 한 자동 정렬이며, 특정 상품의 가입을 권유하거나 그 우수성을 보증하지 않습니다.</p>"),
 ("제4조 (정보의 정확성과 면책)","<p>① 게시된 혜택·캐시백·연회비·이벤트 조건은 <b>수집 시점 기준</b>이며, 카드사·플랫폼의 사정으로 사전 통지 없이 변경·종료될 수 있어 실제와 다를 수 있습니다.<br>② 이용자는 신청 전 반드시 각 카드사·플랫폼에서 최신 내용을 직접 확인해야 하며, 회사는 정보의 오류·지연·변경 또는 외부 페이지의 내용으로 인해 발생한 손해에 대해 책임을 지지 않습니다.<br>③ 회사는 천재지변, 시스템 장애 등 불가항력으로 인한 서비스 제공 중단에 대해 책임을 지지 않습니다.</p>"),
 ("제5조 (제휴 · 광고 링크)","<p>서비스에 포함된 일부 링크는 제휴(광고) 링크로, 이용자가 해당 링크를 통해 외부 페이지로 이동하거나 상품에 가입할 경우 회사가 카드사·플랫폼으로부터 광고 수수료를 받을 수 있습니다. 이러한 수수료는 이용자가 부담하는 비용에 영향을 주지 않습니다.</p>"),
 ("제6조 (지식재산권)","<p>서비스가 제공하는 편집·분석·디자인 등 콘텐츠에 대한 저작권은 회사에 귀속됩니다. 각 카드 상품명·브랜드·로고의 권리는 해당 카드사·플랫폼에 있으며, 식별 목적의 공정이용 범위에서 사용됩니다.</p>"),
 ("제7조 (준거법 및 관할)","<p>본 약관은 대한민국 법령에 따라 해석되며, 서비스 이용과 관련한 분쟁은 관계 법령 및 상관례에 따릅니다.</p>"),
]
_PRIV=[
 ("1. 수집하는 개인정보 항목","<p>① 자동 수집: 접속 IP, 브라우저·기기 정보, 방문 일시, 쿠키, 서비스 이용 기록(클릭·페이지 조회).<br>② 문의 시: 이용자가 제휴·광고 문의 등으로 직접 제공하는 이메일 주소 및 문의 내용.<br>회사는 별도의 회원가입을 받지 않으며, 주민등록번호 등 고유식별정보나 금융정보를 수집하지 않습니다.</p>"),
 ("2. 수집 · 이용 목적","<p>서비스 운영 및 통계 분석을 통한 품질 개선, 부정 이용 방지, 제휴·광고 문의에 대한 응대를 위해 이용합니다.</p>"),
 ("3. 보유 및 이용기간","<p>수집 목적 달성 시 지체 없이 파기합니다. 다만 관련 법령에 따라 보존이 필요한 경우 해당 기간 동안 보관합니다(예: 통신비밀보호법에 따른 접속기록 3개월).</p>"),
 ("4. 제3자 제공 및 처리위탁","<p>회사는 이용자의 개인정보를 외부에 제공하지 않습니다. 다만 서비스 운영에 필요한 범위에서 통계·호스팅 등 일부 업무를 외부 사업자(예: Cloudflare, 분석 도구)에 위탁할 수 있으며, 이 경우 관련 법령에 따라 안전하게 관리합니다.</p>"),
 ("5. 쿠키 및 로그","<p>서비스는 이용 통계와 편의 제공을 위해 쿠키 및 브라우저 저장소를 사용할 수 있습니다. 이용자는 브라우저 설정에서 쿠키 저장을 거부할 수 있으며, 이 경우 일부 기능 이용이 제한될 수 있습니다.</p>"),
 ("6. 이용자의 권리","<p>이용자는 자신의 개인정보에 대한 열람·정정·삭제·처리정지를 요청할 수 있으며, 아래 연락처로 요청 시 관련 법령에 따라 지체 없이 조치합니다.</p>"),
 ("7. 개인정보 보호책임자","<p>개인정보 관련 문의·민원은 <a href=\"mailto:contact@cardtyranno.com\">contact@cardtyranno.com</a> 으로 접수해 주시기 바랍니다.</p>"),
]
_BIZ=[
 ("매체 정보","<table class=\"lgl-tbl\"><tr><th>서비스명</th><td>카드티라노 (CARDTYRANNO)</td></tr>"
  "<tr><th>운영</th><td>쥬라기랩스</td></tr>"
  "<tr><th>서비스 성격</th><td>카드 혜택 광고·정보제공 매체 (금융상품 비중개)</td></tr>"
  "<tr><th>호스팅</th><td>Cloudflare, Inc.</td></tr>"
  "<tr><th>제휴·광고 문의</th><td><a href=\"mailto:contact@cardtyranno.com\">contact@cardtyranno.com</a></td></tr>"
  "<tr><th>일반·개인정보 문의</th><td><a href=\"mailto:contact@cardtyranno.com\">contact@cardtyranno.com</a></td></tr></table>"
  "<p class=\"lgl-note\">상호·대표자·사업자등록번호·주소·통신판매업신고번호 등 사업자 등록 정보는 사업자 등록 완료 후 게재 예정입니다.</p>"),
]
_LGL_FOOT=('<div class="lgl-back"><a href="index.html">← 카드티라노 홈으로</a></div>')
page("terms.html",BRAND+" | 이용약관","카드티라노 이용약관 — 서비스의 성격(광고·정보제공 매체, 비중개), 정보 면책, 제휴 링크 고지, 준거법.","/terms.html",
     _legal_body("TERMS OF SERVICE","이용약관","2026-06-28",_TERMS,_LGL_FOOT,cur="terms.html"),active="")
page("privacy.html",BRAND+" | 개인정보처리방침","카드티라노 개인정보처리방침 — 수집 항목·목적·보유기간·제3자 제공·쿠키·이용자 권리.","/privacy.html",
     _legal_body("PRIVACY POLICY","개인정보처리방침","2026-06-28",_PRIV,_LGL_FOOT,cur="privacy.html"),active="")
page("business.html",BRAND+" | 사업자정보","카드티라노(쥬라기랩스) 사업자정보 및 문의처.","/business.html",
     _legal_body("BUSINESS INFO","사업자정보","2026-06-28",_BIZ,_LGL_FOOT,cur="business.html"),active="")

# robots.txt — AI 크롤러 환영 (AEO)
# ===== 관심카드 푸시 알림 서비스워커 (옵션 A: 백엔드 불필요, 로컬 체크) =====
# 관심카드(ct_fav)에 다음 달 새 캐시백 이벤트가 등록되면 로컬 알림 표시.
# platform_events.json 을 주기적/방문 시 체크 → 카드별 이벤트 시그니처 변화 감지.
SW_JS=r"""// 카드티라노 관심카드 푸시 SW — 백엔드 없이 platform_events.json 로컬 체크
var DB='ctpush',STORE='kv';
function idb(){return new Promise(function(res,rej){var q=indexedDB.open(DB,1);q.onupgradeneeded=function(){q.result.createObjectStore(STORE);};q.onsuccess=function(){res(q.result);};q.onerror=function(){rej(q.error);};});}
function kvGet(k){return idb().then(function(db){return new Promise(function(res){var t=db.transaction(STORE,'readonly').objectStore(STORE).get(k);t.onsuccess=function(){res(t.result);};t.onerror=function(){res(undefined);};});});}
function kvSet(k,v){return idb().then(function(db){return new Promise(function(res){var t=db.transaction(STORE,'readwrite').objectStore(STORE).put(v,k);t.onsuccess=function(){res();};t.onerror=function(){res();};});});}
function _nk2(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function won(n){if(!n)return '';if(n>=10000)return (Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function curMonthLabel(){return (new Date().getMonth()+1)+'월';}
function fetchEvents(){return fetch('/platform_events.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();}).catch(function(){return {products:[]};});}
function sigOf(events){var a=(events||[]).filter(function(e){return e.reward_won;}).map(function(e){return (e.platform||'')+':'+e.reward_won;});a.sort();return a.join('|');}
function maxOf(events){var m=0;(events||[]).forEach(function(e){if((e.reward_won||0)>m)m=e.reward_won;});return m;}
function runCheck(mode){ // 'all'(기준선 전체) | 'new'(신규 찜만 기준선) | 'check'(변경 시 알림)
 return Promise.all([kvGet('enabled'),kvGet('favList'),kvGet('seen')]).then(function(v){
  var enabled=v[0],favList=v[1]||[],seen=v[2]||{};
  if(!enabled)return;
  return fetchEvents().then(function(d){
   var byNk={};(d.products||[]).forEach(function(p){byNk[_nk2(p.name)]={sig:sigOf(p.events),max:maxOf(p.events),name:p.name};});
   var notifs=[];
   favList.forEach(function(f){
    var info=byNk[f.nk];if(!info||!info.sig)return;          // 아직 이벤트 없는 카드는 skip
    var prev=seen[f.nk];
    if(mode==='all'){seen[f.nk]=info.sig;return;}            // 알림 켤 때: 현 상태를 조용히 기준선으로
    if(prev===undefined){seen[f.nk]=info.sig;return;}        // 새로 찜한 카드: 조용히 기준선만
    if(mode==='check'&&prev!==info.sig){notifs.push({name:f.name,max:info.max});seen[f.nk]=info.sig;}
   });
   var keep={};favList.forEach(function(f){if(seen[f.nk]!==undefined)keep[f.nk]=seen[f.nk];});  // 찜 해제 카드 정리
   return kvSet('seen',keep).then(function(){
    notifs.forEach(function(n){
     var body=n.name+'에 '+curMonthLabel()+' 캐시백 이벤트가 등록됐어요!'+(n.max?(' 최대 '+won(n.max)):'');
     self.registration.showNotification('관심카드 새 이벤트 🦖',{body:body,tag:'ct-'+_nk2(n.name),renotify:true,data:{url:'/favorites.html'}});
    });
   });
  });
 });
}
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});
self.addEventListener('message',function(e){var m=e.data||{};
 if(m.type==='enable'){e.waitUntil(Promise.all([kvSet('enabled',1),kvSet('favList',m.favList||[])]).then(function(){return runCheck('all');}));}
 else if(m.type==='test'){e.waitUntil(self.registration.showNotification('🦖 카드티라노 알림 테스트',{body:'관심카드 알림이 정상 동작합니다! 새 이벤트가 등록되면 이렇게 알려드릴게요.',icon:'/og-image.png',badge:'/og-image.png',tag:'ct-test',renotify:true,data:{url:'/favorites.html'}}));}
 else if(m.type==='disable'){e.waitUntil(kvSet('enabled',0));}
 else if(m.type==='sync'){e.waitUntil(kvSet('favList',m.favList||[]).then(function(){return runCheck('new');}));}
 else if(m.type==='check'){e.waitUntil(runCheck('check'));}
});
self.addEventListener('periodicsync',function(e){if(e.tag==='ct-events')e.waitUntil(runCheck('check'));});
self.addEventListener('notificationclick',function(e){e.notification.close();var url=(e.notification.data&&e.notification.data.url)||'/favorites.html';
 e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(function(cl){for(var i=0;i<cl.length;i++){if(cl[i].url.indexOf('favorites')>=0&&'focus' in cl[i])return cl[i].focus();}if(self.clients.openWindow)return self.clients.openWindow(url);}));
});
"""
open(os.path.join(SITE,"sw.js"),"w",encoding="utf-8").write(SW_JS)

robots="User-agent: *\nAllow: /\nDisallow: /dashboard.html\n\n# AI / Answer engines welcome\n"
for ua in ["GPTBot","OAI-SearchBot","ChatGPT-User","Google-Extended","PerplexityBot","PerplexityBot-User","ClaudeBot","Claude-Web","anthropic-ai","Applebot-Extended","CCBot","Bytespider","Amazonbot","Meta-ExternalAgent"]:
    robots+="User-agent: %s\nAllow: /\n"%ua
robots+="\nSitemap: %s/sitemap.xml\n"%BASE
open(os.path.join(SITE,"robots.txt"),"w").write(robots)

# llms.txt — LLM용 사이트 요약 (AEO)
llms="""# 카드티라노 (CardTyranno)

> 한국 신용카드 비교 플랫폼. 여러 카드 중개 플랫폼(토스 카드라운지·카드고릴라·아정당·뱅크샐러드)의 **카드 발급 혜택**과 **결제(할인) 이벤트**를 한곳에서 비교·분석합니다. 데이터 기준: 2026년 6월.

## 무엇을 제공하나
- 카드 발급 혜택 비교: 카드사별 신규 발급 캐시백을 플랫폼(토스·카드고릴라·아정당·카카오페이)별로 비교
- 카드 할인 혜택: 가맹점/업종별 카드 즉시할인·청구할인·캐시백·무이자할부
- 카드 찾기: 카드사별 대표 신용카드(연회비·핵심혜택)
- 카드 가이드: 연회비 캐시백·전월실적·즉시 vs 청구할인 등 활용법

## 이번 달 핵심 수치(예시)
- 발급 최대 혜택: 삼성카드 최대 119만원, 현대카드 최대 89만원, KB국민카드 최대 86만원, 우리카드 최대 78만원
- 카카오페이 채널 우위: 신한카드 최대 39만원, 현대카드 최대 44만 포인트

## 주요 페이지
- [카드 할인 혜택](%s/discount.html)
- [카드 발급 혜택](%s/issue.html)
- [카드 찾기](%s/cards.html)
- [카드 가이드](%s/content.html)

## 자주 묻는 질문
%s
"""%(BASE,BASE,BASE,BASE,"\n".join("- %s → %s"%(q,a) for q,a in FAQ))
open(os.path.join(SITE,"llms.txt"),"w",encoding="utf-8").write(llms)

# sitemap — 공개 색인 페이지 전체 + 빌드일 기준 lastmod 자동화
_today=datetime.date.today().isoformat()
# (path, changefreq, priority)
SITEMAP_PAGES=[
 ("/","daily","1.0"),("/discount.html","daily","0.9"),("/issue.html","daily","0.9"),
 ("/cards.html","daily","0.8"),("/content.html","weekly","0.8"),("/chart.html","daily","0.7"),
 ("/events.html","daily","0.7"),("/cashback.html","weekly","0.6"),("/installment.html","weekly","0.6"),
 ("/trends.html","weekly","0.6"),("/community.html","daily","0.6"),("/business.html","monthly","0.4"),
 ("/search.html","weekly","0.4"),("/terms.html","yearly","0.2"),("/privacy.html","yearly","0.2"),
]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p,cf,pr in SITEMAP_PAGES:
    fn=(p[1:] or "index.html")
    fp=os.path.join(SITE,fn)
    lm=datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat() if os.path.exists(fp) else _today
    sm+='<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n'%(BASE,p,lm,cf,pr)
sm+='</urlset>\n'
open(os.path.join(SITE,"sitemap.xml"),"w").write(sm)

# RSS 2.0 피드 — 네이버 서치어드바이저 RSS 제출용(색인 속도 향상). 발급 이벤트 기반.
def _rss():
    try:_ev=json.load(open(os.path.join(SITE,"events.json"),encoding="utf-8"))
    except Exception:_ev={"items":[]}
    items=_ev.get("items",[])[:30]
    now=datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    def esc(s):
        return (str(s or "")).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    parts=[]
    for it in items:
        title="%s %s — %s (%s)"%(it.get("issuer",""),it.get("card",""),it.get("benefit",""),it.get("platform",""))
        link=BASE+"/issue.html"
        guid=BASE+"/issue.html#%s-%s"%(esc(it.get("issuer","")),esc(it.get("platform","")))
        desc="%s 발급 시 %s. 제공 플랫폼: %s. 기준: %s"%(it.get("issuer",""),it.get("benefit",""),it.get("platform",""),it.get("period",""))
        parts.append('<item><title>%s</title><link>%s</link><guid isPermaLink="false">%s</guid>'
          '<description>%s</description><pubDate>%s</pubDate></item>'%(esc(title),link,esc(guid),esc(desc),now))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
      '<title>카드티라노 — 이번 달 카드 발급 캐시백</title>'
      '<link>%s/issue.html</link>'
      '<description>토스·카드고릴라·아정당·카카오페이 등 플랫폼별 카드 신규 발급 캐시백을 매달 집계한 카드티라노 피드.</description>'
      '<language>ko</language><lastBuildDate>%s</lastBuildDate>%s</channel></rss>\n'%(BASE,now,"".join(parts)))
open(os.path.join(SITE,"rss.xml"),"w",encoding="utf-8").write(_rss())
print("dark site built:",[f for f in sorted(os.listdir(SITE)) if f.endswith(('.html','.txt','.xml'))])
"""
"""
