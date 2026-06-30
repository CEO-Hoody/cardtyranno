# -*- coding: utf-8 -*-
"""카드티라노 프론트엔드 v2 — 다크테마(무신사 감성·카드고릴라 구조) + SEO/AEO 최적화.
데이터는 site/*.json(DB export) 런타임 fetch. AEO: JSON-LD, llms.txt, FAQ, AI 크롤러 허용.
"""
import os, json, datetime, re
OUT=os.path.dirname(os.path.abspath(__file__)); SITE=os.path.join(OUT,"site")
BASE="https://cardtyranno.com"; BRAND="카드티라노"; BRAND_EN="CardTyranno"
# Cloudflare Web Analytics 토큰(대시보드 Web Analytics에서 발급). 값 채우면 전 페이지에 beacon 자동 삽입.
CF_BEACON_TOKEN=""
# 검색엔진 사이트 소유확인 코드(등록 후 발급값 입력하면 전 페이지 <head>에 자동 삽입)
#  네이버 서치어드바이저(searchadvisor.naver.com) → 사이트 등록 → HTML 태그 방식의 content 값만 붙여넣기
NAVER_SITE_VERIFICATION=""
#  구글 서치콘솔(search.google.com/search-console) → HTML 태그 방식의 content 값만 붙여넣기
GOOGLE_SITE_VERIFICATION="CJtR_-EgzygFicvG6SX4pkTjKKCQC88HGHKgMy0brzM"
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
.hd .row{display:flex;align-items:stretch;gap:22px;min-height:66px}
.logo{font-size:21px;font-weight:900;letter-spacing:-1px;display:flex;align-items:center;gap:7px}
.logo .rx{width:23px;height:23px;color:var(--text);display:block;flex:0 0 auto}.logo b{color:var(--text);font-weight:400}
.gnb{display:flex;gap:20px;align-items:stretch}
.gnb a{display:flex;flex-direction:column;justify-content:center;gap:3px;color:inherit;position:relative;padding:14px 0}
.gnb a .nm{font-weight:500;font-size:15px;letter-spacing:-.2px;color:#55555e;white-space:nowrap;display:inline-flex;align-items:center;gap:5px}
.gnb a .sub{font-weight:400;font-size:11px;color:rgba(0,0,0,.5);white-space:nowrap}
.gnb a:hover .nm{color:#000}
.gnb a.on .nm{color:#000;font-weight:700}
.gnb a.on::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:#000}
.gnb a.soon{opacity:.55}
.gnb .soon-tag{font-family:var(--font-mono,monospace);font-size:8px;font-weight:600;background:var(--surface-soft);color:rgba(0,0,0,.45);padding:2px 6px;border-radius:50px;letter-spacing:0}
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
.adt .tip{display:block;position:relative;background:var(--block-cream,#f7f3e9);border-left:3px solid var(--accent-magenta,#ff3d8b);border-radius:10px;padding:13px 16px;margin:18px 0;font-size:14.5px;line-height:1.65;color:#3a3a42}
.adt .tip.warn{border-left-color:#e8843c}
footer{border-top:1px solid var(--line);margin-top:40px;background:#f5f5f7}
.foot{display:flex;gap:50px;padding:42px 0 10px;flex-wrap:wrap}
.foot .col h4{font-size:12px;color:var(--dim);font-weight:800;margin-bottom:13px}.foot .col a{display:block;font-size:13.5px;color:#55555e;margin-bottom:9px}.foot .col a:hover{color:var(--accent)}
.foot .brand{flex:1;min-width:220px}.foot .brand .lg{font-size:20px;font-weight:900;letter-spacing:-1px}.foot .brand .lg b{color:var(--text);font-weight:400}.foot .brand p{font-size:12px;color:var(--sub);margin-top:12px;line-height:1.7;max-width:400px}
.legal{border-top:1px solid var(--line);padding:18px 0 40px;font-size:11.5px;color:var(--dim);line-height:1.8}.legal .biz{margin-top:8px}
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.16);opacity:0;visibility:hidden;transition:.2s;z-index:60}.scrim.on{opacity:1;visibility:visible}
.drawer{position:fixed;top:0;left:0;bottom:0;width:320px;max-width:88%;background:#ffffff;border-right:1px solid var(--line);transform:translateX(-100%);transition:.24s;z-index:61;padding:0;overflow-y:auto}.drawer.on{transform:translateX(0)}
.drawer-hd{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--hairline)}
.drawer-x{width:34px;height:34px;border-radius:50%;background:var(--surface-soft);border:0;display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text);flex:0 0 auto}.drawer-x svg{width:18px;height:18px}
.drawer a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:15px 18px;border-bottom:1px solid var(--hairline-soft);color:inherit}
.drawer a .dn{font-weight:700;font-size:16px;letter-spacing:-.2px;display:inline-flex;align-items:center;gap:6px}
.drawer a .ds{font-weight:400;font-size:12px;color:rgba(0,0,0,.5);margin-top:2px}
.drawer a.on .dn{color:var(--accent)}
.drawer a.soon{opacity:.55}
.drawer a .dchev{width:18px;height:18px;color:rgba(0,0,0,.3);flex:0 0 auto}
.drawer .soon-tag{font-family:var(--font-mono,monospace);font-size:8px;font-weight:600;background:var(--surface-soft);color:rgba(0,0,0,.45);padding:2px 6px;border-radius:50px;letter-spacing:0}
/* 공유하기 — 사이드패널·페이지 하단 공통 */
.drawer-share-wrap{padding:16px 18px 24px}
.drawer-share{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:13px;border:1.5px solid var(--hairline);border-radius:50px;background:#fff;color:var(--text);font-weight:600;font-size:14px;cursor:pointer;font-family:inherit;transition:transform .12s ease,border-color .12s ease}
.drawer-share svg{width:17px;height:17px;flex:0 0 auto}
.drawer-share:hover{border-color:rgba(0,0,0,.4)}.drawer-share:active{transform:scale(.97)}
.pgshare{padding:30px 0 6px;text-align:center}
.pgshare .pgshare-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 28px;border:1.5px solid var(--hairline);border-radius:50px;background:#fff;color:var(--text);font-weight:600;font-size:14px;cursor:pointer;font-family:inherit;transition:transform .12s ease,border-color .12s ease}
.pgshare .pgshare-btn svg{width:17px;height:17px;flex:0 0 auto}
.pgshare .pgshare-btn:hover{border-color:rgba(0,0,0,.4)}.pgshare .pgshare-btn:active{transform:scale(.97)}
.ct-toast{position:fixed;left:50%;bottom:84px;transform:translateX(-50%) translateY(12px);background:#1a1714;color:#fff;font-weight:540;font-size:13.5px;padding:12px 20px;border-radius:50px;box-shadow:0 8px 24px rgba(0,0,0,.22);opacity:0;pointer-events:none;transition:opacity .25s ease,transform .25s ease;z-index:2000;white-space:nowrap}
.ct-toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
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
.nhe-ctas{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:30px}.nhe-ctas .nhe-cta{margin-top:0}
.nhe-cta.sec{background:#fff;color:#000;border:1.5px solid var(--line,#e6e6e6)}.nhe-cta.sec:hover{border-color:#000}
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
/* 리스트형 메인 페이지 타이틀 규격(타이틀 점검 가이드): mono 아이브로우 + display 32/34·w340·-0.8 */
.pg-eb{font-family:var(--font-mono),'JetBrains Mono',ui-monospace,monospace;font-size:12px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:rgba(0,0,0,.5);display:block;line-height:1.3}
"""

HELPERS = r"""
// 모바일 하단 탭바 활성 표시(현재 페이지 기준)
(function(){var mt=document.getElementById('mtab');if(!mt)return;var pn=(location.pathname.split('/').pop()||'index').replace(/\.html$/,'');var qs=location.search||'';var cur='';
 if(pn==='cards'||pn==='carddetail')cur='cards';else if(pn==='issue')cur=/v=cmp/.test(qs)?'compare':'issue';else if(pn===''||pn==='index')cur='home';
 mt.querySelectorAll('a').forEach(function(a){if(a.dataset.tab===cur)a.classList.add('on');});})();
// 상단 GNB 활성(서버 active로 구분 안 되는 issue?v=cmp·events 등 보정)
(function(){var gnb=document.querySelector('.gnb');if(!gnb)return;var pn=(location.pathname.split('/').pop()||'index').replace(/\.html$/,'');var qs=location.search||'';var href=null;
 if(pn==='issue')href=/v=cmp/.test(qs)?'issue.html?v=cmp':'issue.html';
 else if(pn==='events')href='issue.html';else if(pn==='cards'||pn==='carddetail')href='cards.html';
 else if(pn==='chart'||pn==='trends')href='chart.html';else if(pn==='content')href='content.html';else if(pn==='community')href='community.html';else if(pn==='diagnose')href='diagnose.html';
 if(href)gnb.querySelectorAll('a').forEach(function(a){a.classList.toggle('on',a.getAttribute('href')===href);});})();
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
// SEO: JS 렌더 상세(카드·이벤트·콘텐츠)에서 제목·설명·canonical·OG를 해당 항목으로 갱신(구글 렌더 색인 대응)
function _setMeta(sel,val){var m=document.querySelector(sel);if(m&&val!=null)m.setAttribute('content',val);}
function ctSeo(title,desc,canonPath){try{
 if(title){document.title=title;_setMeta('meta[property="og:title"]',title);_setMeta('meta[name="twitter:title"]',title);}
 if(desc){desc=(''+desc).replace(/\s+/g,' ').trim().slice(0,158);_setMeta('meta[name="description"]',desc);_setMeta('meta[property="og:description"]',desc);_setMeta('meta[name="twitter:description"]',desc);}
 if(canonPath){var u=canonPath.indexOf('http')===0?canonPath:('https://cardtyranno.com/'+canonPath.replace(/^\//,''));var c=document.querySelector('link[rel="canonical"]');if(c)c.setAttribute('href',u);_setMeta('meta[property="og:url"]',u);}
}catch(e){}}
// 공유하기: Web Share API 우선, 미지원 시 클립보드 복사 + 토스트
function ctToast(msg){var t=document.getElementById('ctToast');if(!t){t=document.createElement('div');t.id='ctToast';t.className='ct-toast';document.body.appendChild(t);}t.textContent=msg;void t.offsetWidth;t.classList.add('on');clearTimeout(ctToast._t);ctToast._t=setTimeout(function(){t.classList.remove('on');},2000);}
function _ctCopyFallback(text){try{var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.top='-1000px';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=document.execCommand('copy');document.body.removeChild(ta);return ok;}catch(e){return false;}}
function ctCopyLink(url){var ok=function(){ctToast('링크가 복사됐어요');};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(ok,function(){if(_ctCopyFallback(url))ok();else ctToast('복사에 실패했어요');});}else if(_ctCopyFallback(url)){ok();}else{ctToast('복사에 실패했어요');}}
function ctShare(url,title,text){try{if(navigator.share){navigator.share({title:title,text:text,url:url}).catch(function(){});return;}}catch(e){}ctCopyLink(url);}
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
function bindUI(){var d=document.getElementById('drawer'),s=document.getElementById('scrim'),m=document.getElementById('menuBtn');if(m)m.onclick=function(){d.classList.add('on');s.classList.add('on');};if(s)s.onclick=function(){d.classList.remove('on');s.classList.remove('on');};var dx=document.getElementById('drawerX');if(dx)dx.onclick=function(){d.classList.remove('on');s.classList.remove('on');};
 var dsh=document.getElementById('drawerShare');if(dsh)dsh.onclick=function(){ctShare(location.origin+'/','카드티라노','같은 카드도 발급 채널 따라 캐시백이 달라요. 토스·네이버페이·카카오페이·아정당·카드고릴라·뱅크샐러드 6개 플랫폼 캐시백을 한눈에 비교하세요.');};
 var psh=document.getElementById('pageShare');if(psh)psh.onclick=function(){ctShare(location.href,document.title||'카드티라노','카드티라노에서 확인해 보세요.');};
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
    # 전역 네비게이션(가이드): 순서·명칭 + 메뉴별 서브텍스트. (key,url,name,sub,soon)
    L=[("compare","issue.html?v=cmp","한눈에 비교","카드·카드사별 캐시백 한 표에서",False),
       ("issue","issue.html","캐시백","이번 달 플랫폼별 최대 캐시백",False),
       ("cards","cards.html","카드찾기","조건으로 내 카드 탐색",False),
       ("diagnose","diagnose.html","카드 진단","내 소비에 맞는 맞춤 카드 찾기",False),
       ("charts","chart.html","티라노 차트","캐시백 추이·랭킹 데이터",False),
       ("content","content.html","티라노 TIP","발급 전략·꿀팁 콘텐츠",False),
       ("community","community.html","커뮤니티","발급 후기·정보 공유",False),
       ("about","about.html","카드티라노란?","서비스 소개",False)]
    _st='<span class="soon-tag">예정</span>'
    gnb="".join('<a href="%s" class="%s%s"><span class="nm">%s%s</span><span class="sub">%s</span></a>'%(u,("on" if k==active else ""),(" soon" if soon else ""),t,(_st if soon else ''),s) for k,u,t,s,soon in L)
    drawer="".join('<a href="%s" class="%s"><div class="dt"><div class="dn">%s%s</div><div class="ds">%s</div></div><svg class="dchev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg></a>'%(u,("on" if k==active else "")+(" soon" if soon else ""),t,(_st if soon else ''),s) for k,u,t,s,soon in L)
    return (ICONS+'<div class="scrim" id="scrim"></div><aside class="drawer" id="drawer">'
            '<div class="drawer-hd"><div class="logo"><svg class="rx" viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.4 4.6 H19 A2 2 0 0 1 21 6.6 V9.2 A2 2 0 0 1 19 11.2 H15.4 A2 2 0 0 1 13.4 9.2 V6.6 A2 2 0 0 1 15.4 4.6 Z M17.6 6.5 a0.8 0.8 0 1 1 -1.6 0 a0.8 0.8 0 1 1 1.6 0 Z M18.2 7.8 H19.9 A0.5 0.5 0 0 1 20.4 8.3 V9.6 A0.5 0.5 0 0 1 19.9 10.1 H18.2 A0.5 0.5 0 0 1 17.7 9.6 V8.3 A0.5 0.5 0 0 1 18.2 7.8 Z M18.05 8.87 H20.05 V9.03 H18.05 Z M18.78 8.13 H18.94 V9.77 H18.78 Z"/></svg>CARD<b>TYRANNO</b></div><button class="drawer-x" id="drawerX" aria-label="닫기"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'+drawer
            +'<div class="drawer-share-wrap"><button class="drawer-share" id="drawerShare"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5v11"/><path d="M8 7l4-3.5L16 7"/><path d="M5.5 12v6.5a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1V12"/></svg>카드티라노 홈 공유하기</button></div></aside>'
            '<div class="util"><div class="wrap"><a href="content.html">가이드</a><a href="mailto:contact@cardtyranno.com">제휴·광고 문의</a></div></div>'
            '<header class="hd"><div class="wrap row">'
            '<span class="icbtn menu" id="menuBtn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span>'
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
 '<div class="col"><h4>약관·정책</h4><a href="terms.html">이용약관</a><a href="privacy.html">개인정보처리방침</a><a href="sitemap.html">사이트맵</a></div></div>'
 '<div class="wrap legal">카드티라노는 카드사·제휴 플랫폼의 광고/정보를 제공하는 <b>광고·정보제공 매체</b>이며, 카드 발급을 중개·접수하지 않습니다. 카드 신청·발급·심사는 각 카드사에서 진행됩니다. 게시된 캐시백·이벤트는 제휴 플랫폼·카드사의 <b>공개 데이터를 기준으로 자동 정렬</b>되며, 금액은 <b>최대 금액 기준</b>(전월실적·사용처·한도 등 조건 충족 시)입니다. 게시된 혜택·캐시백·연회비는 수집 시점 기준이며 실제와 다를 수 있어 신청 전 각 카드사·플랫폼에서 최종 확인이 필요합니다. <b>일부 링크는 제휴(광고) 링크</b>로, 이를 통해 수수료를 받을 수 있습니다.'
 '<div class="biz muted">카드티라노(CardTyranno) · 쥬라기랩스 · 제휴/광고 contact@cardtyranno.com</div>'
 '<div class="biz">© 2026 CARDTYRANNO. All rights reserved.</div></div></footer>')

# 각 페이지 하단 공유하기(현재 페이지 URL 공유) — page()가 본문 뒤·푸터 앞에 삽입
PAGE_SHARE=('<div class="pgshare"><div class="wrap"><button class="pgshare-btn" id="pageShare">'
 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5v11"/><path d="M8 7l4-3.5L16 7"/><path d="M5.5 12v6.5a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1V12"/></svg>'
 '이 페이지 공유하기</button></div></div>')

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
      '<link rel="icon" type="image/x-icon" href="/favicon.ico">'
      '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">'
      '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">'
      '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
      +('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token":"'+CF_BEACON_TOKEN+'"}\'></script>' if CF_BEACON_TOKEN else '')
      +ld)

def page(fname,title,desc,path,body,script="",extra_jsonld=None,searchbar=False,catstrip=False,active="",noindex=False):
    html=('<!DOCTYPE html><html lang="ko"><head>'+head(title,desc,path,extra_jsonld,noindex)
      +'<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">'
      +'<style>'+CSS+'</style></head><body>'
      +header(active)+(SEARCHBAR if searchbar else "")+(CATSTRIP if catstrip else "")
      +body+PAGE_SHARE+FOOTER+MTABBAR+'<script>'+HELPERS+script+'\nbindUI();</script></body></html>')
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
 '<div class="nhe-ctas"><a class="nhe-cta" id="heroTipCta" href="content.html">이번달 전문가 TIP <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a>'
 '<a class="nhe-cta sec" href="issue.html?v=cmp">한눈에 비교 <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></div></div>'
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
var PMETA={cardgorilla:{n:'카드고릴라',c:'#FF6A13'},banksalad:{n:'뱅크샐러드',c:'#19C37D'},toss:{n:'토스',c:'#3182F6'},ajungdang:{n:'아정당',c:'#1B64DA'},naver:{n:'네이버페이',c:'#03C75A'},kakaopay:{n:'카카오페이',c:'#FEE500'},issuer:{n:'카드사 직접',c:'#7a8088'}};
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
 var cmpRows=Object.keys(PMETA).filter(function(k){return k!=='issuer';}).map(function(k){return{k:k,m:PMETA[k],v:platMax[k]||0};}).sort(function(a,b){return b.v-a.v;});
 var cmpTop=cmpRows.length?cmpRows[0].v:0;var cbb=document.getElementById('heroCmpBars');
 if(cbb){cbb.innerHTML=cmpRows.map(function(r,ri){var w=cmpTop?Math.max(8,Math.round(r.v/cmpTop*100)):8;return '<div class="nhc-cmp-row"><i style="background:'+r.m.c+'"></i><span class="nm">'+r.m.n+'</span><div class="tr"><i style="width:'+w+'%;background:'+(ri===0?'#000':'#cfcfcf')+'"></i></div></div>';}).join('');}
 // 히어로 슬라이드2 · 이번달 최고 캐시백 상품 배너
 if(best){var bMx=0,bPlat='';(best.events||[]).forEach(function(e){if(e.platform!=='issuer'&&(e.reward_won||0)>bMx){bMx=e.reward_won;bPlat=e.platform;}});var bm=PMETA[bPlat]||{n:bPlat};var _e;
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
  var cpl={};PE.forEach(function(p){var iss=alias(p.issuer||'');if(!iss)return;var o=cpl[iss]||(cpl[iss]={});(p.events||[]).forEach(function(e){var w=e.reward_won||0;if(!w||e.platform==='issuer')return;var pp=o[e.platform]||(o[e.platform]={tot:0,max:0,prods:{}});pp.tot+=w;if(w>pp.max)pp.max=w;pp.prods[_nk2(p.name)]=1;});});
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
fetch('content.json').then(function(r){return r.json();}).then(function(cd){var its=(cd.items||[]);var t=its.filter(function(x){return /전략|발급/.test(x.cat||'');})[0]||its[0];if(!t)return;
 var hc=document.getElementById('heroTipCta');if(hc)hc.setAttribute('href','content.html?id='+encodeURIComponent(t.id));
 var el=document.getElementById('tipLatest');if(!el)return;
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
 '.cfx{max-width:880px;margin:0 auto}'
 '.cfx-top{padding:20px 0 0}.cfx-h{font-weight:340;font-size:32px;letter-spacing:-.8px;line-height:1.05;margin:6px 0 0}.cfx-sub{font-weight:400;font-size:13px;color:rgba(0,0,0,.6);margin:5px 0 0}'
 '.cfx-search{display:flex;align-items:center;gap:9px;padding:13px 15px;border:1px solid var(--line);border-radius:14px;margin-top:14px}.cfx-search svg{width:17px;height:17px;color:rgba(0,0,0,.45);flex:0 0 auto}.cfx-search input{flex:1;min-width:0;border:0;outline:0;background:0;font-family:inherit;font-size:14px;color:#000}'
 '.cfx-cats{display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:14px 0 0;scrollbar-width:none}.cfx-cats::-webkit-scrollbar{display:none}'
 '.cfx-cat{flex:0 0 auto;padding:8px 14px;border-radius:50px;border:1px solid var(--line);background:var(--surface-soft);color:rgba(0,0,0,.7);font-weight:540;font-size:12.5px;cursor:pointer;white-space:nowrap;font-family:inherit}.cfx-cat.on{background:#000;color:#fff;border-color:#000}'
 '.cfx-bar{display:flex;align-items:center;justify-content:space-between;padding:14px 0 0;gap:10px}'
 '.cfx-fbtn{display:inline-flex;align-items:center;gap:6px;font-weight:540;font-size:13px;background:0;border:0;cursor:pointer;font-family:inherit;color:#000}.cfx-fbtn svg{width:15px;height:15px}.cfx-fbtn .n{background:var(--accent-magenta);color:#fff;border-radius:50px;font-size:10px;padding:1px 6px;font-family:var(--font-mono,monospace)}'
 '.cfx-sortb{display:inline-flex;align-items:center;gap:5px;font-weight:540;font-size:13px;color:rgba(0,0,0,.6);background:0;border:0;cursor:pointer;font-family:inherit}.cfx-sortb svg{width:13px;height:13px}'
 '.cfx-list{display:grid;grid-template-columns:1fr;gap:10px;margin-top:14px}'
 '.cfr{display:flex;gap:13px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:14px 15px;text-decoration:none;color:#000;min-height:44px;background:#fff;min-width:0}'
 '.cfr-plate{width:62px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:8px;overflow:hidden;background:var(--surface-soft);box-shadow:0 3px 8px rgba(0,0,0,.12)}.cfr-plate img{width:100%;height:100%;object-fit:cover;display:block}'
 '.cfr-mid{flex:1;min-width:0}.cfr-iss{font-family:var(--font-mono,monospace);font-size:9px;color:rgba(0,0,0,.45);text-transform:uppercase}.cfr-nm{font-weight:700;font-size:15px;letter-spacing:-.3px;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.cfr-meta{display:flex;align-items:center;gap:7px;margin-top:7px;flex-wrap:wrap}'
 '.cfr-rank{font-family:var(--font-mono,monospace);font-size:9px;display:inline-flex;align-items:center;gap:3px;color:var(--accent-magenta)}.cfr-rank svg{width:10px;height:10px}'
 '.cfr-heart{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:50px;background:var(--surface-soft);white-space:nowrap}.cfr-heart svg{width:10px;height:10px;color:#000}.cfr-heart .dot{width:6px;height:6px;border-radius:50%}.cfr-heart .pn{font-weight:540;font-size:10.5px}'
 '.cfr-right{text-align:right;flex:0 0 auto}.cfr-rl{font-family:var(--font-mono,monospace);font-size:8px;color:rgba(0,0,0,.42)}.cfr-rv{font-weight:700;font-size:19px;letter-spacing:-.5px;white-space:nowrap}'
 '.cfx-empty{text-align:center;padding:60px 0;color:rgba(0,0,0,.5)}'
 '.cfx-scrim{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:60}.cfx-scrim.open{display:block}'
 '.cfx-sheet{position:fixed;left:0;right:0;bottom:0;background:#fff;border-radius:20px 20px 0 0;padding:8px 18px calc(20px + env(safe-area-inset-bottom));z-index:61;transform:translateY(110%);transition:transform .25s;max-width:560px;margin:0 auto}.cfx-sheet.open{transform:none}'
 '.cfx-sheet-h{font-weight:700;font-size:15px;padding:16px 2px 12px}'
 '.cfx-shsort button{display:block;width:100%;text-align:left;border:0;background:0;padding:15px 4px;font-size:16px;font-weight:500;border-top:1px solid var(--hairline-soft);cursor:pointer;color:#000;font-family:inherit}.cfx-shsort button.on{font-weight:800}'
 '.cfx-fl{font-weight:700;font-size:11.5px;color:rgba(0,0,0,.5);text-transform:uppercase;letter-spacing:.4px;margin:14px 0 9px}'
 '.cfx-chips{display:flex;flex-wrap:wrap;gap:7px}.cfx-chips button{font-weight:500;font-size:13px;padding:8px 13px;border-radius:50px;border:1px solid var(--line);background:var(--surface-soft);color:#000;cursor:pointer;font-family:inherit}.cfx-chips button.on{background:#000;color:#fff;border-color:#000}'
 '.cfx-feew{display:flex;align-items:center;gap:12px;margin-top:4px}.cfx-feew input{flex:1;accent-color:#000}.cfx-feel{font-weight:700;font-size:13px;min-width:80px;text-align:right}'
 '.cfx-apply{width:100%;margin-top:18px;padding:14px;border-radius:14px;background:#000;color:#fff;font-weight:700;font-size:15px;border:0;cursor:pointer;font-family:inherit}'
 '@media(min-width:761px){.cfx-h{font-size:34px}.cfx-list{grid-template-columns:1fr 1fr;gap:12px}.cfx-cats{flex-wrap:wrap;overflow:visible}}'
 '</style>'
 '<div class="wrap"><div class="cfx">'
 '<div class="cfx-top"><span class="pg-eb">FIND A CARD</span><h1 class="cfx-h">카드찾기</h1><p class="cfx-sub">조건을 고르면, 받을 수 있는 카드를 캐시백 순으로.</p></div>'
 '<div class="cfx-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6"/><path d="M19.5 19.5l-4.7-4.7"/></svg><input id="cfQ" type="search" placeholder="카드명·혜택으로 검색" autocomplete="off"></div>'
 '<div class="cfx-cats" id="cfCats"></div>'
 '<div class="cfx-bar"><button class="cfx-fbtn" id="cfFiltBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2.2"/><circle cx="8" cy="17" r="2.2"/></svg>연회비·카드사<span class="n" id="cfFiltN" style="display:none"></span></button>'
 '<button class="cfx-sortb" id="cfSortBtn">최고 캐시백순 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button></div>'
 '<div class="cfx-list" id="list"><div class="cfx-empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
 '<div class="cfx-empty" id="cfEmpty" style="display:none">조건에 맞는 카드가 없어요.</div>'
 '<div class="cfx-scrim" id="cfScrim"></div>'
 '<div class="cfx-sheet" id="cfSortSheet"><div class="cfx-sheet-h">정렬</div><div class="cfx-shsort"><button data-s="cash" class="on">최고 캐시백순</button><button data-s="rank">티라노 순위순</button><button data-s="fee">연회비 낮은순</button></div></div>'
 '<div class="cfx-sheet" id="cfFiltSheet"><div class="cfx-sheet-h">연회비 · 카드사</div>'
 '<div class="cfx-fl">카드사</div><div class="cfx-chips" id="cfIss"></div>'
 '<div class="cfx-fl">연회비</div><div class="cfx-feew"><input type="range" id="cfFee" min="0" max="100000" step="5000" value="100000"><span class="cfx-feel" id="cfFeeL">무제한</span></div>'
 '<button class="cfx-apply" id="cfApply">적용하기</button></div>'
 '</div></div>')
CARDS_JS=r"""
var PKO={toss:'토스',cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
var PCO={toss:'#3182F6',cardgorilla:'#FF6A13',banksalad:'#19C37D',ajungdang:'#1B64DA',naver:'#03C75A',kakaopay:'#FEE500'};
var PORDK=['toss','naver','kakaopay','ajungdang','cardgorilla','banksalad'];
var ALL=[],st={cat:'전체',iss:'전체',fee:100000,sort:'cash',q:''};
var CATS=['전체','여행','쇼핑','교통','구독','생활요금'];
var CATKW={'여행':['여행','항공','해외','면세','라운지','마일','트래블','호텔'],'쇼핑':['쇼핑','백화점','온라인','아울렛','쿠팡','11번가','마트','편의점','다이닝','외식','적립'],'교통':['교통','대중교통','버스','지하철','하이패스','주유','충전','자동차','대중'],'구독':['구독','멤버십','스트리밍','넷플','유튜브','ott','영화','문화','카페','커피'],'생활요금':['통신','공과금','관리비','자동이체','렌탈','요금','공공','생활']};
function _nkc(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _feeNum(s){s=(''+s);var m=s.match(/([0-9.]+)\s*만/);if(m)return Math.round(parseFloat(m[1])*10000);m=s.replace(/[, ]/g,'').match(/([0-9]{4,})/);return m?parseInt(m[1]):0;}
function wman(v){if(v==null||v===0)return '0';var m=v/10000;return (m>=10?Math.round(m):Math.round(m*10)/10)+'만원';}
function _wm(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function catsOf(b){var lb=(b||'').toLowerCase(),r=[];for(var c in CATKW){if(CATKW[c].some(function(k){return lb.indexOf(k)>=0;}))r.push(c);}return r;}
function bestPlat(pl){var bk=null,bv=-1;PORDK.forEach(function(k){var v=(pl||{})[k];if(v!=null&&v>bv){bv=v;bk=k;}});return {key:bk,val:bv};}
var STAR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l2.4 5 5.4.7-3.9 3.7 1 5.4-4.9-2.7-4.9 2.7 1-5.4L4.2 9.7 9.6 9z"/></svg>';
var HRT='<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg>';
function pass(c){
 if(st.cat!=='전체'&&c.cats.indexOf(st.cat)<0)return false;
 if(st.iss!=='전체'&&c.issuer!==st.iss)return false;
 if(st.fee<100000&&c.feeN>st.fee)return false;
 if(st.q){var q=st.q.toLowerCase();if((c.name+' '+c.issuer+' '+c.benefit).toLowerCase().indexOf(q)<0)return false;}
 return true;}
function render(){
 var rows=ALL.filter(pass);
 rows.sort(function(a,b){if(st.sort==='fee')return a.feeN-b.feeN;if(st.sort==='rank')return a.rankN-b.rankN;return (b.cash-a.cash)||(a.rankN-b.rankN);});
 var L=document.getElementById('list'),E=document.getElementById('cfEmpty');
 if(!rows.length){L.innerHTML='';E.style.display='block';return;}E.style.display='none';
 L.innerHTML=rows.map(function(c){
  var rank=c.rankN<9999?'<span class="cfr-rank">'+STAR+'티라노 '+c.rankN+'위</span>':'';
  var heart=c.pkey?'<span class="cfr-heart">'+HRT+'<span class="dot" style="background:'+c.pColor+'"></span><span class="pn">'+c.platform+'</span></span>':'';
  return '<a class="cfr" href="carddetail.html?id='+c.id+'"><div class="cfr-plate">'+imgTag(c.img)+'</div>'
   +'<div class="cfr-mid"><div class="cfr-iss">'+c.issuer+'</div><div class="cfr-nm">'+c.name+'</div><div class="cfr-meta">'+rank+heart+'</div></div>'
   +'<div class="cfr-right"><div class="cfr-rl">최대 캐시백</div><div class="cfr-rv">'+(c.cash?wman(c.cash):'–')+'</div></div></a>';
 }).join('');
 if(window.repairImages)repairImages();
}
function chips(id,arr,key,cls){var el=document.getElementById(id);if(!el)return;el.innerHTML=arr.map(function(x){return '<button class="'+cls+(st[key]===x?' on':'')+'" data-v="'+x+'">'+x+'</button>';}).join('');
 el.querySelectorAll('button').forEach(function(b){b.onclick=function(){st[key]=b.dataset.v;el.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');if(key!=='iss')render();};});}
Promise.all([fetch('cards.json').then(function(r){return r.json();}),fetch('platform_events.json').then(function(r){return r.json();}).catch(function(){return {products:[]};})]).then(function(A){
 var cj=A[0],PEIMG={};((A[1].products)||[]).forEach(function(p){if(p.img&&!PEIMG[_nkc(p.name)])PEIMG[_nkc(p.name)]=p.img;});
 var ord=cj.order||Object.keys(cj.cards||{});
 return fetch('history/index.json').then(function(r){return r.json();}).then(function(idx){var ms=(idx.months||[]);var m=ms.length?ms[ms.length-1]:'2026-06';return fetch('history/'+m+'.json').then(function(r){return r.json();});}).catch(function(){return {cards:[]};}).then(function(hist){
  var H={};((hist.cards)||[]).forEach(function(hc){H[_nkc(hc.name)]=hc;});
  ord.forEach(function(iss){(cj.cards[iss]||[]).forEach(function(c){var n=_nkc(c.name);var h=H[n]||{};var bp=bestPlat(h.platforms);var rk=parseInt(c.rank);
    ALL.push({id:c.id,name:c.name,issuer:iss,img:c.img||PEIMG[n]||'',benefit:c.benefit||'',fee:c.fee||'',feeN:_feeNum(c.fee),cats:catsOf(c.benefit||''),rankN:(c.rank&&!isNaN(rk))?rk:9999,cash:h.max||0,pkey:bp.key,platform:PKO[bp.key]||'',pColor:PCO[bp.key]||'#888'});});});
  initUI(ord);render();
 });
}).catch(function(){var L=document.getElementById('list');if(L)L.innerHTML='<div class="cfx-empty">데이터를 불러오지 못했어요.</div>';});
function initUI(ord){
 chips('cfCats',CATS,'cat','cfx-cat');
 var availIss=['전체'].concat(ord.filter(function(o){return ALL.some(function(x){return x.issuer===o;});}));
 chips('cfIss',availIss,'iss','');
 var q=document.getElementById('cfQ');q.oninput=function(){st.q=q.value.trim();render();};
 var scrim=document.getElementById('cfScrim'),sortSheet=document.getElementById('cfSortSheet'),filtSheet=document.getElementById('cfFiltSheet');
 function close(){scrim.classList.remove('open');sortSheet.classList.remove('open');filtSheet.classList.remove('open');}
 document.getElementById('cfSortBtn').onclick=function(){scrim.classList.add('open');sortSheet.classList.add('open');};
 document.getElementById('cfFiltBtn').onclick=function(){scrim.classList.add('open');filtSheet.classList.add('open');};
 scrim.onclick=close;
 var SL={cash:'최고 캐시백순',rank:'티라노 순위순',fee:'연회비 낮은순'};
 sortSheet.querySelectorAll('button').forEach(function(b){b.onclick=function(){st.sort=b.dataset.s;sortSheet.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});document.getElementById('cfSortBtn').firstChild.textContent=SL[b.dataset.s]+' ';render();close();};});
 var fr=document.getElementById('cfFee'),fl=document.getElementById('cfFeeL');
 fr.oninput=function(){st.fee=parseInt(fr.value);fl.textContent=(st.fee>=100000?'무제한':_wm(st.fee)+' 이하');};
 document.getElementById('cfApply').onclick=function(){updFiltN();render();close();};
}
function updFiltN(){var n=0;if(st.iss!=='전체')n++;if(st.fee<100000)n++;var el=document.getElementById('cfFiltN');if(!el)return;if(n){el.textContent=n;el.style.display='';}else el.style.display='none';}
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
 # 모바일 B안: 미니 막대 슬롯(접힘/펼침)
 '.pbar-card{border:1px solid var(--line);border-radius:16px;padding:15px 16px;margin-bottom:11px;background:var(--surface);cursor:pointer}'
 '.pbar-hd{font-weight:800;font-size:15.5px;letter-spacing:-.3px}.pbar-hd .psub{font-family:var(--font-mono,monospace);font-size:9px;color:var(--dim);margin-left:7px;font-weight:400}'
 '.pbar-rows{display:flex;flex-direction:column;gap:9px;margin-top:12px}'
 '.pbar-row{display:flex;align-items:center;gap:9px}.pbar-row .dot{width:7px;height:7px;border-radius:50%;flex:0 0 auto}'
 '.pbar-row .pn{width:64px;flex:0 0 auto;font-weight:540;font-size:12px;color:rgba(0,0,0,.6);white-space:nowrap;display:inline-flex;align-items:center;gap:3px}.pbar-row .pn.best{color:#000}.pbar-row .pn svg{width:11px;height:11px;color:#000}'
 '.pbar-row .tr{flex:1;height:9px;border-radius:50px;background:var(--surface2);overflow:hidden}.pbar-row .tr i{display:block;height:100%;border-radius:50px}'
 '.pbar-row .amt{width:42px;text-align:right;flex:0 0 auto;font-weight:700;font-size:13px;color:rgba(0,0,0,.55);white-space:nowrap}.pbar-row .amt.best{color:#000}'
 '.pbar-row.extra{display:none}.pbar-card.open .pbar-row.extra{display:flex}'
 '.pbar-toggle{display:flex;align-items:center;justify-content:center;gap:5px;margin-top:13px;padding-top:12px;border-top:1px solid var(--hairline-soft);cursor:pointer;font-weight:540;font-size:12.5px;color:rgba(0,0,0,.6)}'
 '.pbar-toggle .chev{transition:transform .3s}.pbar-card.open .pbar-toggle .chev{transform:rotate(180deg)}'
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
 # 상단 컨트롤 바(가이드: 탭 좌 + 캐시백기준·카드사 우 한 줄) · 엠블럼은 모바일 전용
 '.cmpbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:2px 0 14px}'
 '.cmpbar-r{display:flex;align-items:center;gap:10px;flex-wrap:wrap}'
 '@media(min-width:681px){.pcmp-emb{display:none}}'
 '.ptogwrap{display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--surface-soft);border-radius:14px;padding:11px 14px;margin-bottom:12px}'
 '.ptogl{font:700 11px ui-monospace,Menlo,monospace;color:var(--dim);margin-right:2px}'
 '.ptog{display:flex;gap:6px;flex-wrap:wrap}'
 '.ptogb{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:50px;border:1px solid var(--hairline);background:#fff;color:rgba(0,0,0,.7);font-weight:540;font-size:12px;cursor:pointer}'
 '.ptogb.on{background:#000;color:#fff;border-color:#000}.ptogb i{width:7px;height:7px;border-radius:50%;flex:0 0 auto}'
 '.pcmp-banners{display:grid;grid-template-columns:1.7fr 1fr;gap:14px;margin-top:18px}'
 '.pcb-strat{display:grid;grid-template-columns:170px 1fr;border:1px solid var(--hairline);border-radius:16px;overflow:hidden;text-decoration:none;color:#000}.pcb-strat img{width:170px;height:100%;object-fit:cover;display:block}.pcb-strat .mono{font:700 9px ui-monospace,Menlo,monospace;color:rgba(0,0,0,.5);text-transform:uppercase}.pcb-strat>div{padding:18px 22px;display:flex;flex-direction:column;justify-content:center}.pcb-strat .t{font-weight:700;font-size:18px;letter-spacing:-.4px;margin-top:5px}.pcb-strat .d{font-size:13px;color:rgba(0,0,0,.6);margin-top:6px}.pcb-strat .go{font-weight:540;font-size:13px;margin-top:12px}'
 '.pcb-ad{background:var(--block-coral);border-radius:16px;padding:20px 22px;display:flex;flex-direction:column;justify-content:space-between;text-decoration:none;color:#000}.pcb-ad .mono{font:700 9px ui-monospace,Menlo,monospace;opacity:.6;text-transform:uppercase}.pcb-ad .t{font-weight:700;font-size:18px;letter-spacing:-.4px;line-height:1.2}.pcb-ad .d{font-size:12px;color:rgba(0,0,0,.6);margin-top:5px}.pcb-ad .go{font-weight:540;font-size:13px}'
 '@media(max-width:680px){.pcmp-banners{grid-template-columns:1fr}.pcb-strat{grid-template-columns:110px 1fr}.pcb-strat img{width:110px}}'
 # 캐시백 메인 — 이벤트 단위(가이드 B)
 '#view-ev{max-width:880px;margin:0 auto}'
 '.ev2-hd{display:flex;align-items:center;gap:8px;padding:2px 0 0}.ev2-h{font-weight:340;font-size:32px;letter-spacing:-.8px;line-height:1.05;margin:0}'
 '.ev2-month{display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:50px;background:var(--surface-soft);font-weight:540;font-size:12px}'
 '.ev2-sub{font-weight:400;font-size:13px;color:rgba(0,0,0,.6);margin:5px 0 0}'
 '.ev2-iss{display:inline-flex;align-items:center;gap:6px;margin-top:12px;padding:7px 13px;border-radius:50px;background:var(--block-lilac);font-weight:540;font-size:12.5px;cursor:pointer}.ev2-iss b{font-weight:800}.ev2-iss .x{font-size:11px;opacity:.6}'
 '.ev2-plats{display:flex;gap:7px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:13px 0 0;scrollbar-width:none}.ev2-plats::-webkit-scrollbar{display:none}'
 '.ev2pl{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:50px;border:1px solid var(--line);background:#fff;color:rgba(0,0,0,.7);font-weight:540;font-size:12.5px;cursor:pointer;white-space:nowrap;font-family:inherit}.ev2pl.on{background:#000;color:#fff;border-color:#000}.ev2pl .dot{width:7px;height:7px;border-radius:50%;flex:0 0 auto}'
 '.ev2-bar{display:flex;align-items:center;justify-content:space-between;padding:13px 0 0;gap:10px}.ev2-cnt{font-weight:540;font-size:12.5px;color:rgba(0,0,0,.55)}'
 '.ev2-sortb{display:inline-flex;align-items:center;gap:5px;font-weight:540;font-size:13px;color:rgba(0,0,0,.6);background:0;border:0;cursor:pointer;font-family:inherit}.ev2-sortb svg{width:13px;height:13px}'
 '#view-ev #list{display:flex;flex-direction:column;gap:10px;margin-top:13px}'
 '.ev2c{display:grid;grid-template-columns:1fr auto;grid-template-areas:"plwrap cash" "mid mid" "cond go";gap:12px 10px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:15px 16px;background:#fff;text-decoration:none;color:#000}'
 '.ev2c{cursor:pointer;transition:box-shadow .16s ease,transform .12s ease}.ev2c:hover{box-shadow:0 6px 18px rgba(0,0,0,.12)}.ev2c:active{transform:scale(.99)}'
 '.ev2c.top{background:var(--block-lime);border-color:var(--accent-magenta)}'
 '.ev2c-plwrap{grid-area:plwrap;display:flex;align-items:center;gap:7px;min-width:0}'
 '.ev2c-pl{display:inline-flex;align-items:center;gap:5px;padding:5px 11px;border-radius:50px;background:#000;color:#fff;flex-shrink:0;white-space:nowrap}.ev2c-pl .dot{width:7px;height:7px;border-radius:50%}.ev2c-pl .pn{font-weight:600;font-size:12px}'
 '.ev2c-topb{font:700 8px var(--font-mono,monospace);background:var(--accent-magenta);color:#fff;padding:3px 7px;border-radius:50px;flex-shrink:0;letter-spacing:.4px}'
 '.ev2c-cash{grid-area:cash;justify-self:end;font-weight:700;font-size:23px;letter-spacing:-.6px;white-space:nowrap}'
 '.ev2c-mid{grid-area:mid;display:flex;align-items:center;gap:11px;min-width:0}'
 '.ev2c-stack{display:flex;align-items:center;padding-left:13px;flex-shrink:0}'
 '.ev2c-mp{width:34px;flex-shrink:0;margin-left:-13px;aspect-ratio:1.586/1;border-radius:6px;overflow:hidden;border:1.5px solid #fff;background:var(--block-lilac);box-shadow:0 2px 5px rgba(0,0,0,.16);display:flex;align-items:center;justify-content:center;color:rgba(0,0,0,.3)}.ev2c-mp img{width:100%;height:100%;object-fit:cover;display:block}.ev2c-mp svg{width:16px;height:13px}'
 '.ev2c-more{width:34px;height:22px;flex-shrink:0;margin-left:-13px;border-radius:5px;border:1.5px solid #fff;background:#000;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 5px rgba(0,0,0,.16);color:#fff;font-weight:700;font-size:10px;letter-spacing:-.2px}'
 '.ev2c-rep{min-width:0;flex:1;display:flex;align-items:center;gap:7px}.ev2c-rep .rn{font-weight:700;font-size:13.5px;letter-spacing:-.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}'
 '.ev2c-cnt{font-weight:700;font-size:11px;padding:3px 9px;border-radius:50px;background:var(--surface-soft);white-space:nowrap;flex-shrink:0}'
 '.ev2-sort{display:inline-flex;align-items:center;gap:2px;padding:2px;border-radius:50px;background:var(--surface-soft);flex-shrink:0}.ev2-sort button{font-family:inherit;font-weight:540;font-size:11.5px;padding:5px 11px;border-radius:50px;border:0;background:0;color:rgba(0,0,0,.6);cursor:pointer;white-space:nowrap}.ev2-sort button.on{background:#000;color:#fff;font-weight:600}'
 '.ev2c-cond{grid-area:cond;font-weight:400;font-size:12px;color:rgba(0,0,0,.55);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
 '.ev2c-go{grid-area:go;justify-self:end;display:inline-flex;align-items:center;gap:5px;padding:9px 15px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:13px;flex-shrink:0;white-space:nowrap}.ev2c-go svg{width:13px;height:13px}'
 '@media(min-width:761px){.ev2-h{font-size:34px}.ev2-plats{flex-wrap:wrap;overflow:visible}'
 '.ev2c{grid-template-columns:auto 1fr auto auto;grid-template-areas:"plwrap mid cash go" "plwrap cond cash go";column-gap:18px;row-gap:3px;padding:16px 20px}'
 '.ev2c-cash{justify-self:end}.ev2c-go{justify-self:end}}'
 # 플랫폼 비교 — 카드사/정렬 드롭다운(가이드 .dd) + 배너 반응형
 '.cmphd2{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:2px 0 12px}'
 '.dd2{position:relative}'
 '.dd2b,.dd2-static{display:inline-flex;align-items:center;gap:7px;padding:9px 13px;border-radius:11px;border:1px solid var(--hairline);background:#fff;font-family:inherit;font-weight:540;font-size:13px;color:#000;cursor:pointer;white-space:nowrap}'
 '.dd2-static{cursor:default;color:rgba(0,0,0,.6)}.dd2b svg{width:14px;height:14px;color:rgba(0,0,0,.45)}'
 '.dd2menu{position:absolute;left:0;top:calc(100% + 6px);background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.1);padding:6px;z-index:20;min-width:150px;display:none;max-height:300px;overflow:auto}.dd2menu.open{display:block}'
 '.dd2menu button{display:block;width:100%;text-align:left;padding:9px 11px;border:0;background:0;border-radius:8px;font-family:inherit;font-size:13px;font-weight:500;cursor:pointer;color:#000;white-space:nowrap}.dd2menu button:hover{background:var(--surface-soft)}.dd2menu button.on{font-weight:800}'
 # 모바일 mint 전략 배너 / 배너 반응형(PC=전략+AD, 모바일=mint)
 '.pcmp-banner-mo{display:none}'
 '.pcmp-banner-mo a{display:block;background:var(--block-mint);border-radius:14px;padding:16px 18px;text-decoration:none;color:#000;margin-top:16px}.pcmp-banner-mo .mono{font:700 8px ui-monospace,Menlo,monospace;opacity:.55;text-transform:uppercase}.pcmp-banner-mo .t{font-weight:700;font-size:15px;letter-spacing:-.3px;margin-top:5px}.pcmp-banner-mo .go{display:inline-flex;align-items:center;gap:6px;font-weight:540;font-size:12px;margin-top:8px}.pcmp-banner-mo .go svg{width:14px;height:14px}'
 '@media(max-width:680px){.pcmp-banners{display:none}.pcmp-banner-mo{display:block}}'
 # ===== 통합 검색필터(UF) — 3필터(플랫폼사·카드사·캐시백유형)+정렬4 · PC 인라인 드롭다운 / 모바일 컴팩트바+바텀시트 =====
 '.uf{position:relative;margin:14px 0 4px}'
 '.uf-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap}'
 '.uf-fbtn{display:none}'
 '.uf-ddls{display:flex;gap:10px;flex-wrap:wrap}'
 '.uf-ddl{display:inline-flex;align-items:center;gap:7px;padding:10px 15px;border:1.5px solid var(--hairline);border-radius:50px;background:#fff;font-family:inherit;font-weight:540;font-size:14px;color:#000;cursor:pointer;white-space:nowrap}'
 '.uf-ddl svg{width:14px;height:14px;opacity:.5}.uf-ddl .cv{transition:transform .2s}.uf-ddl[aria-expanded="true"] .cv{transform:rotate(180deg)}'
 '.uf-ddl .uf-c{color:var(--accent-magenta);font-weight:700}.uf-ddl .uf-c:empty{display:none}.uf-ddl .uf-t{color:rgba(0,0,0,.55);font-weight:540}'
 '.uf-spacer{flex:1}'
 '.uf-sortb{display:inline-flex;align-items:center;gap:5px;font-weight:540;font-size:13.5px;color:rgba(0,0,0,.6);background:0;border:0;cursor:pointer;font-family:inherit;white-space:nowrap}.uf-sortb svg{width:13px;height:13px;opacity:.6}'
 '.uf-msort{display:none}'
 '.uf-chips{display:flex;gap:9px;flex-wrap:wrap}.uf-chips:empty{display:none}'
 '.uf-chip{display:inline-flex;align-items:center;gap:7px;padding:7px 8px 7px 13px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:13px;white-space:nowrap;border:0}'
 '.uf-chip .dot{width:7px;height:7px;border-radius:50%;flex:0 0 auto}'
 '.uf-chip .x{width:18px;height:18px;border-radius:50%;background:rgba(255,255,255,.22);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;flex:0 0 auto}.uf-chip .x svg{width:11px;height:11px;opacity:1}'
 '.uf-meta{display:flex;align-items:center;gap:10px;margin-top:14px}'
 '.uf-cnt{font-weight:540;font-size:13px;color:rgba(0,0,0,.55)}.uf-cnt b{color:#000;font-weight:700}'
 '.uf-reset{font-weight:540;font-size:13px;color:rgba(0,0,0,.45);text-decoration:underline;text-underline-offset:2px;cursor:pointer;background:0;border:0;font-family:inherit}'
 '.uf-mspacer{flex:1}'
 # PC 팝오버
 '.uf-pop{position:absolute;z-index:40;background:#fff;border:1px solid var(--hairline);border-radius:16px;box-shadow:0 12px 32px rgba(0,0,0,.12);padding:16px 18px;min-width:248px;display:none}.uf-pop.open{display:block}'
 '.uf-pop-sort{padding:8px;min-width:208px}'
 '.uf-poph{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}.uf-poph .pt{font-weight:700;font-size:14px}.uf-poph .pm{font-weight:540;font-size:12px;color:rgba(0,0,0,.45)}'
 '.uf-opt{display:flex;align-items:center;gap:11px;padding:9px 0;border-bottom:1px solid var(--hairline-soft);cursor:pointer}.uf-opt:last-child{border-bottom:0}'
 '.uf-cb{width:22px;height:22px;border-radius:6px;border:1.5px solid rgba(0,0,0,.2);background:#fff;display:flex;align-items:center;justify-content:center;color:#fff;flex:0 0 auto}.uf-cb svg{width:13px;height:13px;display:none}'
 '.uf-opt.on .uf-cb{border-color:#000;background:#000}.uf-opt.on .uf-cb svg{display:block}'
 '.uf-opt .dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}.uf-opt .nm{font-weight:540;font-size:14px}'
 '.uf-popft{display:flex;gap:8px;margin-top:14px}.uf-popft button{flex:1;text-align:center;padding:11px;border-radius:50px;font-weight:540;font-size:13.5px;font-family:inherit;cursor:pointer}.uf-popft .r{border:1.5px solid var(--hairline);background:#fff;color:#000}.uf-popft .a{border:0;background:#000;color:#fff}'
 '.uf-srow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 12px;border-radius:10px;cursor:pointer;background:transparent}.uf-srow:hover{background:var(--surface-soft)}.uf-srow.on{background:var(--surface-soft)}.uf-srow .sl{font-weight:540;font-size:14px;color:rgba(0,0,0,.7)}.uf-srow.on .sl{font-weight:700;color:#000}.uf-srow svg{width:15px;height:15px;display:none}.uf-srow.on svg{display:block}'
 # 캐시백 유형 세그먼트(팝오버·시트 공용)
 '.uf-seg{display:inline-flex;align-items:center;gap:2px;padding:3px;border-radius:50px;background:var(--surface-soft);flex-wrap:wrap}.uf-seg button{font-family:inherit;font-weight:540;font-size:13px;padding:8px 16px;border-radius:50px;border:0;background:0;color:rgba(0,0,0,.6);cursor:pointer}.uf-seg button.on{background:#000;color:#fff;font-weight:600}'
 # 모바일 바텀시트
 '.uf-sheet-bg{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:1200;display:none;opacity:0;transition:opacity .2s}.uf-sheet-bg.open{display:block;opacity:1}'
 '.uf-sheet{position:fixed;left:0;right:0;bottom:0;background:#fff;border-radius:26px 26px 0 0;box-shadow:0 -8px 30px rgba(0,0,0,.14);padding:8px 0 calc(20px + env(safe-area-inset-bottom));max-height:86vh;overflow:auto;transform:translateY(100%);transition:transform .26s cubic-bezier(.2,.8,.2,1)}.uf-sheet-bg.open .uf-sheet{transform:translateY(0)}'
 '.uf-grab{width:44px;height:5px;border-radius:50px;background:var(--hairline);margin:6px auto 0}'
 '.uf-sheet-h{display:flex;align-items:center;justify-content:space-between;padding:14px 20px 0}.uf-sheet-h span{font-weight:700;font-size:18px;letter-spacing:-.4px}'
 '.uf-sheet-x{width:32px;height:32px;border-radius:50%;background:var(--surface-soft);border:0;display:flex;align-items:center;justify-content:center;cursor:pointer}.uf-sheet-x svg{width:15px;height:15px}'
 '.uf-sg{padding:18px 20px 0}.uf-sg-t{font-weight:700;font-size:14px}.uf-sg-t span{font-weight:400;font-size:12px;color:rgba(0,0,0,.45);margin-left:4px}'
 '.uf-sg-opts{display:flex;flex-wrap:wrap;gap:8px;margin-top:11px}'
 '.uf-tag{display:inline-flex;align-items:center;gap:6px;padding:9px 13px;border-radius:50px;font-weight:540;font-size:13px;border:1.5px solid var(--hairline);background:#fff;color:#111;cursor:pointer}.uf-tag .dot{width:7px;height:7px;border-radius:50%}.uf-tag.on{border-color:#000;background:#000;color:#fff}'
 '.uf-sheet-ft{display:flex;gap:9px;padding:20px 20px 0}.uf-sheet-ft button{padding:14px;border-radius:50px;font-weight:600;font-size:14px;font-family:inherit;cursor:pointer}.uf-sheet-ft .r{flex:1;border:1.5px solid var(--hairline);background:#fff;color:#000;font-weight:540}.uf-sheet-ft .a{flex:2;border:0;background:#000;color:#fff}'
 '@media(max-width:760px){.uf-ddls{display:none}.uf-bar .uf-spacer,.uf-bar #ufSortPc{display:none}'
 '.uf-fbtn{display:inline-flex;align-items:center;gap:6px;padding:9px 14px;border-radius:50px;background:#000;color:#fff;flex-shrink:0;font-family:inherit;font-weight:600;font-size:13px;border:0;cursor:pointer}.uf-fbtn svg{width:15px;height:15px;opacity:1}.uf-fbtn .uf-fn{min-width:18px;height:18px;border-radius:50%;background:var(--accent-magenta);display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;padding:0 5px}.uf-fbtn .uf-fn:empty,.uf-fbtn .uf-fn.zero{display:none}'
 '.uf-bar{flex-wrap:nowrap;overflow:hidden}.uf-chips{overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch;scrollbar-width:none}.uf-chips::-webkit-scrollbar{display:none}'
 '.uf-msort{display:inline-flex}}'
 '</style>'
 '<div class="wrap"><section><div class="sec-h"><h2 id="issTitle">이번달 캐시백</h2></div>'
 '<div id="view-ev">'
 '<span class="pg-eb" style="padding-top:2px">MONTHLY CASHBACK</span><div class="ev2-hd"><h1 class="ev2-h">캐시백</h1><span class="ev2-month"><span id="evMonth">2026.06</span></span></div>'
 '<p class="ev2-sub">이번 달, 어디서 받는 게 가장 이득인지.</p>'
 '<div class="uf" id="uf">'
   '<div class="uf-bar">'
     '<button class="uf-fbtn" id="ufFbtn" type="button" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M3 6h18M6 12h12M10 18h4"/></svg>필터 <span class="uf-fn zero" id="ufFn"></span></button>'
     '<div class="uf-ddls">'
       '<button class="uf-ddl" type="button" data-uf="plat" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M3 6h18M6 12h12M10 18h4"/></svg>플랫폼사 <span class="uf-c" id="ufCplat"></span> <svg class="cv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button>'
       '<button class="uf-ddl" type="button" data-uf="iss" aria-expanded="false">카드사 <span class="uf-c" id="ufCiss"></span> <svg class="cv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button>'
       '<button class="uf-ddl" type="button" data-uf="type" aria-expanded="false">캐시백 유형 <span class="uf-t" id="ufTtype">주요</span> <svg class="cv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button>'
     '</div>'
     '<div class="uf-chips" id="ufChips"></div>'
     '<div class="uf-spacer"></div>'
     '<button class="uf-sortb" id="ufSortPc" type="button">캐시백 많은 순 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button>'
   '</div>'
   '<div class="uf-meta"><span class="uf-cnt" id="evCnt">이벤트 –건</span><button class="uf-reset" id="ufReset" type="button" style="display:none">초기화</button><span class="uf-mspacer"></span><button class="uf-sortb uf-msort" id="ufSortMo" type="button">캐시백 많은 순 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button></div>'
   '<div class="uf-pop" id="ufPopplat"></div><div class="uf-pop" id="ufPopiss"></div><div class="uf-pop" id="ufPoptype"></div><div class="uf-pop uf-pop-sort" id="ufPopsort"></div>'
 '</div>'
 '<div class="uf-sheet-bg" id="ufSheetBg"><div class="uf-sheet" id="ufSheet" role="dialog" aria-modal="true" aria-label="필터"><div class="uf-grab"></div>'
   '<div class="uf-sheet-h"><span id="ufSheetTtl">필터</span><button class="uf-sheet-x" id="ufSheetX" type="button" aria-label="닫기"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
   '<div id="ufSheetBody"></div>'
   '<div class="uf-sheet-ft"><button class="r" id="ufFtReset" type="button">초기화</button><button class="a" id="ufFtApply" type="button">결과 보기</button></div>'
 '</div></div>'
 '<div id="list"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div id="view-cmp" style="display:none">'
 '<div class="pcmp-emb"><div><div class="t" id="embT">카드사 ❤ 플랫폼, 최고 궁합</div><div class="s" id="embS">카드사별 최고 궁합 플랫폼</div></div><span class="emb"><span class="dh"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span><svg class="ht" viewBox="0 0 24 24"><use href="#ic-heart-f"/></svg><span class="dh r"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span></span></div>'
 '<div class="cmpbar"><div class="subnav2"><button data-c="iss" class="on">카드사별 비교</button><button data-c="prod">카드별 비교</button></div>'
 '<div class="cmpbar-r"><div class="cashtog" id="cashtog"><span class="ctgl">캐시백 기준</span><button data-cm="t" class="on">전체</button><button data-cm="m">주요</button></div>'
 '<div class="dd2" id="prodIssWrap" style="display:none"><button class="dd2b" id="prodIssBtn">카드사 · 전체 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button><div class="dd2menu" id="prodIssMenu"></div></div></div></div>'
 '<div class="ptogwrap"><span class="ptogl">표시 플랫폼 · 2개 이상</span><div class="ptog" id="platToggle"></div></div>'
 '<div id="cmp-iss"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
 '<div id="cmp-prod" style="display:none"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div>'
 # 하단 배너(가이드 변경10) — PC: 전략(170px)+AD / 모바일: mint 전략
 '<div class="pcmp-banners"><a class="pcb-strat" href="content.html"><img src="assets/tip-headers/header-strategy.png" alt="이번 달 발급 전략"><div><div class="mono">티라노TIP</div><div class="t">이번 달 어디서 받는 게 이득일까?</div><div class="d">카드사별 최대 플랫폼과 마감 임박 이벤트를 정리했어요.</div><span class="go">전략 보기 ›</span></div></a>'
 '<a class="pcb-ad" href="cards.html" rel="sponsored nofollow"><div class="mono">광고(AD) · 제휴</div><div><div class="t">해외 수수료 면제 여행카드</div><div class="d">최대 금액 기준, 조건 충족 시</div></div><span class="go">자세히 ›</span></a></div>'
 '<div class="pcmp-banner-mo"><a href="content.html"><div class="mono">티라노TIP</div><div class="t">이번 달 어디서 받는 게 이득일까?</div><span class="go">전략 보기 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></span></a></div>'
 '</div>'
 '</section></div>')
ISSUE_JS=r"""
var EV=[],ORD=[],cur="전체",evSort="won",evPlat="",evVis={},issuerFilter="",evMonth="";
// 통합 필터 상태: evVis=플랫폼사(다중), evIssF=카드사(다중), evType=캐시백유형(주요main/부가bonus/전체all), evSortK=정렬(cash/pop/iss/plat)
var evIssF={},evType="main",evSortK="cash";
var UFTYPES=[["main","주요"],["bonus","부가"],["all","전체"]];
var UFSORTS=[["cash","캐시백 많은 순"],["pop","인기 순"],["iss","카드사 순"],["plat","플랫폼사 순"]];
function ufTypeLabel(){var m={main:"주요",bonus:"부가",all:"전체"};return m[evType]||"주요";}
function ufSortLabel(){for(var i=0;i<UFSORTS.length;i++)if(UFSORTS[i][0]===evSortK)return UFSORTS[i][1];return "캐시백 많은 순";}
function ufTypeVal(g){return evType==="main"?(g.main||0):evType==="bonus"?(g.bonus||0):(g.won||0);}
var PRODALL=[],pSort="amt",pFilter="",basis="cardgorilla",renderProd=function(){},renderIss=function(){},issFilter="",issSort="amt",cashMode="t",prodIssF="";
function _spl(e){var t=e.reward_won||0;var m=(e.main_won!=null?e.main_won:null);var b=(e.bonus_won||0);
 if(m==null){if(b>=t)b=0;m=Math.max(t-b,0);}else{if(m>t)m=t;b=Math.max(t-m,0);}
 return {t:t,m:m,b:b};}
function mval(o,md){return !o?0:(md==='m'?o.m:md==='b'?o.b:o.t);}
function _capBD(o){if(!o||(o.b<=0&&o.m>=o.t))return '';return '<div class="cap">주'+Math.round(o.m/10000)+'·부'+Math.round(o.b/10000)+'</div>';}
var PCOL={"카드고릴라":"#ff4d4f","뱅크샐러드":"#2f6bff","아정당":"#3b5bdb","카카오페이":"#e8b800","토스":"#3182f6","네이버페이":"#03c75a","네이버":"#03c75a"};
function pcol(p){return PCOL[p]||"#7a8088";}
// 가이드 B: 이벤트 단위 리스트 — 플랫폼칩(검정+dot)·캐시백 금액(대형)·카드사(굵게)·상품(연회색)·조건·자세히
// 캐시백 메인 = 리워드그룹 슬롯(플랫폼·카드사·보상 동일 = 다중 카드 묶음). 시안: 겹친 플레이트+'+N'+'카드 N종'.
function _evIssKeys(){return Object.keys(evIssF).filter(function(k){return evIssF[k];});}
function _evGroups(){var sel=PORD.filter(function(k){return evVis[k];});var issl=_evIssKeys();
 var items=EV.filter(function(x){return (!issl.length||issl.indexOf(x.issuer)>=0)&&(!sel.length||sel.indexOf(x.pk)>=0);});
 var gm={},order=[];
 items.forEach(function(x){var key=x.pk+'|'+x.issuer+'|'+x.won;var g=gm[key];if(!g){g=gm[key]={pk:x.pk,platform:x.platform,issuer:x.issuer,won:x.won,main:0,bonus:0,cards:[],pe:'',period:'',text:''};order.push(g);}
  g.cards.push({name:x.card,img:x.img});if((x.main||0)>g.main)g.main=x.main||0;if((x.bonus||0)>g.bonus)g.bonus=x.bonus||0;if(x.pe&&(!g.pe||x.pe<g.pe)){g.pe=x.pe;g.period=x.period;}if(!g.text&&x.text)g.text=x.text;});
 // 대표 = 카드사명 제거한 가장 짧은 상품명(대표성). 플레이트는 이미지 있는 카드 우선.
 order.forEach(function(g){g.cards.sort(function(a,b){return (b.img?1:0)-(a.img?1:0);});g.rep=g.cards[0]?g.cards[0].name:g.issuer;});
 // 정렬 4종: 캐시백많은순(선택 유형 기준)·인기순(카드 종수)·카드사순·플랫폼사순
 order.sort(function(a,b){
  if(evSortK==='iss')return (a.issuer||'').localeCompare(b.issuer||'','ko')||(b.won-a.won);
  if(evSortK==='plat')return (PORD.indexOf(a.pk)-PORD.indexOf(b.pk))||(b.won-a.won);
  if(evSortK==='pop')return (b.cards.length-a.cards.length)||(b.won-a.won);
  return (ufTypeVal(b)-ufTypeVal(a))||(b.won-a.won);});
 return order;}
function render(){var groups=_evGroups();
 if(window.ufRender)ufRender(groups.length);
 var cn=document.getElementById('evCnt');if(cn)cn.innerHTML='이벤트 <b>'+groups.length+'</b>건';
 var L=document.getElementById('list');if(!groups.length){L.innerHTML='<div class="empty" style="padding:40px 0;text-align:center;color:rgba(0,0,0,.5)">조건에 맞는 이벤트가 없어요. <button class="uf-reset" type="button" id="ufEmptyReset" style="display:inline">조건 줄이기</button></div>';var er=document.getElementById('ufEmptyReset');if(er)er.onclick=function(){if(window.ufResetAll)ufResetAll();};return;}
 var topVal=0;groups.forEach(function(g){var v=ufTypeVal(g);if(v>topVal)topVal=v;});
 L.innerHTML=groups.map(function(g){var tv=ufTypeVal(g);var top=(topVal>0&&tv===topVal);var amt=tv||g.won;
   var href='events.html?platform='+g.pk+'&n='+encodeURIComponent(g.rep);
   var cond=g.cards.length>1?('카드별 조건 상이'+(g.period?' · 마감 '+g.period.replace(/^~/,''):'')):(g.period?('마감 '+g.period.replace(/^~/,'')):(g.text||'발급 이벤트 진행 중'));
   var shown=g.cards.slice(0,3),over=g.cards.length-shown.length;
   var stack=shown.map(function(c){return '<span class="ev2c-mp">'+(c.img?'<img src="'+encodeURI(c.img)+'" alt="" onerror="this.style.display=\'none\'">':'<svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>')+'</span>';}).join('')+(over>0?'<span class="ev2c-more">+'+over+'</span>':'');
   return '<a class="ev2c'+(top?' top':'')+'" href="'+href+'">'
    +'<div class="ev2c-plwrap"><span class="ev2c-pl"><span class="dot" style="background:'+(PBC[g.pk]||"#888")+'"></span><span class="pn">'+(PN[g.pk]||g.platform)+'</span></span>'+(top?'<span class="ev2c-topb">최고</span>':'')+'</div>'
    +'<div class="ev2c-cash">최대 '+_wm(amt)+'</div>'
    +'<div class="ev2c-mid"><span class="ev2c-stack">'+stack+'</span><span class="ev2c-rep"><span class="rn">'+g.rep+'</span><span class="ev2c-cnt">카드 '+g.cards.length+'종</span></span></div>'
    +'<div class="ev2c-cond">'+cond+'</div>'
    +'<span class="ev2c-go">자세히 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></span></a>';}).join("");
 if(window.repairImages)repairImages();}
function renderPlats(){var el=document.getElementById('evPlats');if(!el)return;var sel=PORD.filter(function(k){return evVis[k];});
 var all='<button class="ev2pl'+(sel.length?'':' on')+'" data-ep="">전체</button>';
 el.innerHTML=all+PORD.map(function(pk){return '<button class="ev2pl'+(evVis[pk]?' on':'')+'" data-ep="'+pk+'"><span class="dot" style="background:'+(PBC[pk]||"#888")+'"></span>'+(PN[pk]||pk)+'</button>';}).join('');}
function tabs(){}
// 발급이벤트 / 플랫폼비교는 별도 화면(서브탭 제거). ?v=cmp로 진입 화면 결정.
document.querySelector('.subnav2').onclick=function(e){var b=e.target.closest('button');if(!b)return;document.querySelectorAll('.subnav2 button').forEach(x=>x.classList.remove('on'));b.classList.add('on');var iss=b.dataset.c==='iss';document.getElementById('cmp-iss').style.display=iss?'':'none';document.getElementById('cmp-prod').style.display=iss?'none':'';var cn=document.getElementById('cmpnote-iss');if(cn)cn.style.display=iss?'':'none';var piw=document.getElementById('prodIssWrap');if(piw)piw.style.display=iss?'none':'';
 var et=document.getElementById('embT'),es=document.getElementById('embS');if(et)et.textContent=iss?'카드사 ❤ 플랫폼, 최고 궁합':'카드 ❤ 플랫폼, 최고 궁합 비교';if(es)es.textContent=iss?'카드사별 최고 궁합 플랫폼':'가장 잘 맞는 발급 플랫폼을 찾아요';};
// 캐시백 기준 토글(전체/주요/부가) — 두 탭 동시 갱신
var _ctg=document.getElementById('cashtog');if(_ctg)_ctg.addEventListener('click',function(e){var b=e.target.closest('button[data-cm]');if(!b)return;cashMode=b.dataset.cm;_ctg.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);});renderProd();renderIss();});
// 표시 플랫폼 토글(최소 2개 유지) — 표 열·모바일 칩 즉시 가감, 최고값(❤) 재계산
var PNAME={cardgorilla:"카드고릴라",banksalad:"뱅크샐러드",toss:"토스",ajungdang:"아정당",naver:"네이버페이",kakaopay:"카카오페이"};
function renderPlatToggle(){var el=document.getElementById('platToggle');if(!el)return;el.innerHTML=PORD.map(function(pk){var on=!!VIS[pk];return '<button class="ptogb'+(on?' on':'')+'" data-pt="'+pk+'"><i style="background:'+(PBC[pk]||"#888")+'"></i>'+(PSHORT[pk]||PNAME[pk]||pk)+'</button>';}).join('');}
var _pt=document.getElementById('platToggle');if(_pt)_pt.addEventListener('click',function(e){var b=e.target.closest('button[data-pt]');if(!b)return;var pk=b.getAttribute('data-pt');var on=PORD.filter(function(k){return VIS[k];}).length;if(VIS[pk]&&on<=2)return;VIS[pk]=VIS[pk]?0:1;renderPlatToggle();renderProd();renderIss();});
// 모바일 B안 막대 슬롯: '+N곳 더보기' 토글 + 카드 탭 시 상세 이동(위임)
function _pbarClick(e){var tg=e.target.closest('.pbar-toggle');if(tg){var card=tg.closest('.pbar-card');if(card){var op=card.classList.toggle('open');var more=card.getAttribute('data-more');var l=tg.querySelector('.lbl');if(l)l.textContent=op?'접기':('+'+more+'곳 더보기');}return true;}var pc=e.target.closest('.pbar-card');if(pc&&pc.getAttribute('data-href')){location.href=pc.getAttribute('data-href');return true;}return false;}
// 카드별: 카드사 드롭다운(가이드 변경4) 위임
document.getElementById('cmp-prod').addEventListener('click',function(e){_pbarClick(e);});
// 카드사 드롭다운(상단 바·정적): 토글/선택
(function(){var pw=document.getElementById('prodIssWrap');if(!pw)return;pw.addEventListener('click',function(e){
 var ib=e.target.closest('#prodIssBtn');if(ib){e.preventDefault();var m=document.getElementById('prodIssMenu');if(m)m.classList.toggle('open');return;}
 var io=e.target.closest('#prodIssMenu button[data-iss]');if(io){e.preventDefault();prodIssF=io.getAttribute('data-iss');renderProd();}});})();
// 카드사별: 셀·행은 <a> 네이티브 이동, 막대 토글만 위임
document.getElementById('cmp-iss').addEventListener('click',function(e){_pbarClick(e);});
// 드롭다운 외부 클릭 시 닫기
document.addEventListener('click',function(e){if(!e.target.closest('.dd2'))document.querySelectorAll('.dd2menu.open').forEach(function(m){m.classList.remove('open');});});
// 발급이벤트 화면 필터/정렬 = 통합 검색필터(UF). 컨트롤러는 ISSUE_JS 하단 ufInit()에서 바인딩.
// 진입 화면 결정: ?v=cmp면 플랫폼 비교, 아니면 발급 이벤트 (서브탭 없이 분리)
(function(){var isCmp=new URLSearchParams(location.search).get('v')==='cmp';
 document.getElementById('view-ev').style.display=isCmp?'none':'';
 document.getElementById('view-cmp').style.display=isCmp?'':'none';
 var t=document.getElementById('issTitle');var sh=t?t.closest('.sec-h'):null;
 if(isCmp){if(t)t.textContent='한눈에 비교';if(sh)sh.style.display='';}else if(sh){sh.style.display='none';}
 document.title=(isCmp?'한눈에 비교':'이번 달 캐시백')+' | 카드티라노';})();
function num(s){var m=(s||"").match(/([0-9]+(?:\.[0-9]+)?)\s*만/);return m?parseFloat(m[1]):-1;}
// 발급이벤트(EV) 목록은 아래 platform_events.json 집계에서 구성(5개 플랫폼·네이버 포함). 구형 events.json(네이버 0건) 의존 제거.
// 카드사·카드상품 비교 모두 콜렉터 platform_events.json에서 집계(뱅샐·아정당 포함, 카카오페이 제외)
var PN={cardgorilla:"카드고릴라",banksalad:"뱅크샐러드",toss:"토스",naver:"네이버페이",ajungdang:"아정당",kakaopay:"카카오페이"};
var PSHORT={cardgorilla:"고릴라",banksalad:"뱅샐",toss:"토스",naver:"네이버",ajungdang:"아정당",kakaopay:"카카오"};
var PBC={cardgorilla:"#FF6A13",banksalad:"#19C37D",toss:"#3182F6",ajungdang:"#1B64DA",naver:"#03C75A",kakaopay:"#FEE500"};
function _pdk(pk,shrt){return '<span style="display:inline-flex;align-items:center;gap:5px;white-space:nowrap"><i style="width:7px;height:7px;border-radius:50%;background:'+(PBC[pk]||"#888")+';flex:0 0 auto"></i>'+((shrt?PSHORT[pk]:PN[pk])||pk)+'</span>';}
var PORD=["toss","naver","kakaopay","ajungdang","cardgorilla","banksalad"];
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
   tmp.push({issuer:iss,card:p.name,platform:(PN[e.platform]||e.platform),pk:e.platform,benefit:_rwd(e.reward_text,e.reward_won),url:u||('carddetail.html?n='+encodeURIComponent(p.name)),period:(e.period_end?('~'+String(e.period_end).slice(5).replace('-','/')):''),pe:(e.period_end||''),won:(e.reward_won||0),main:(e.main_won!=null?e.main_won:(e.reward_won||0)),bonus:(e.bonus_won||0),text:(e.reward_text||''),img:(p.img||IMG[_nk2(p.name)]||'')});
   mx[iss]=Math.max(mx[iss]||0,e.reward_won||0);});});
  EV=tmp;ORD=Object.keys(mx).sort(function(a,b){return mx[b]-mx[a];});
  var _mxv=Math.max.apply(null,tmp.map(function(x){return x.won||0;}).concat([0]));var _eh=document.getElementById('evhMax');if(_eh&&_mxv)_eh.textContent=_wm(_mxv);
  evMonth=(A[0].month||'').replace('-','.');var _em=document.getElementById('evMonth');if(_em&&evMonth)_em.textContent=evMonth;
  // 통합필터 URL 동기화 복원: plat(키 콤마)·iss(카드사명 콤마)·type(main/bonus/all)·sort(cash/pop/iss/plat). 레거시 issuer/plat 단수도 흡수.
  var sp=new URLSearchParams(location.search);
  var qiss=sp.get('iss')||sp.get('issuer');if(qiss)qiss.split(',').forEach(function(n){n=n.trim();if(n&&ORD.indexOf(n)>=0)evIssF[n]=1;});
  var qp=sp.get('plat');if(qp)qp.split(',').forEach(function(t){t=t.trim();if(!t)return;if(PN[t]){evVis[t]=1;return;}for(var _k in PN){if(PN[_k]===t){evVis[_k]=1;break;}}});
  var qt=sp.get('type');if(qt&&['main','bonus','all'].indexOf(qt)>=0)evType=qt;
  var qs2=sp.get('sort');if(qs2&&['cash','pop','iss','plat'].indexOf(qs2)>=0)evSortK=qs2;
  if(window.ufInit)ufInit();render();})();
 // (1) 카드사별 비교 — 카드사 × 플랫폼 최대 집계 + 보유 종수·대표카드 (시안 표형)
 function _es(s){return String(s==null?'':s).replace(/[<>&]/g,'');}
 var byIss={},issMeta={};
 prods.forEach(function(p){if(!(p.events||[]).length)return;var iss=p.issuer||'기타';byIss[iss]=byIss[iss]||{};
  var pmax=0;p.events.forEach(function(e){var w=e.reward_won||0;if(w>pmax)pmax=w;var c=byIss[iss][e.platform];if(!c||w>(c.t||0))byIss[iss][e.platform]=_spl(e);});
  var m=issMeta[iss]=issMeta[iss]||{count:0,rep:'',repv:-1};m.count++;if(pmax>m.repv){m.repv=pmax;m.rep=p.name;}});
 var ISSROWS=Object.keys(byIss).map(function(iss){var o={};PORD.forEach(function(pk){var c=byIss[iss][pk];if(c&&c.t)o[pk]=c;});return {iss:iss,o:o,count:(issMeta[iss]||{}).count||0,rep:(issMeta[iss]||{}).rep||''};});
 var ISSF=[['','전체'],['삼성','삼성'],['현대','현대'],['KB국민','KB국민'],['신한','신한'],['롯데','롯데'],['우리','우리']];
 renderIss=function(){
  var rows=ISSROWS.slice();
  var VL=visList(),gc='1.6fr repeat('+VL.length+',1fr)';
  rows.forEach(function(r){var mx=0;VL.forEach(function(pk){var v=mval(r.o[pk],cashMode);if(v>mx)mx=v;});r.mx=mx;});
  rows.sort(function(a,b){return b.mx-a.mx;});
  var ctl='';
  var chips='';
  var head='<div class="ptr hd" style="grid-template-columns:'+gc+'"><div>카드사 ('+rows.length+')</div>'+VL.map(function(pk){return '<div>'+_pdk(pk,true)+'</div>';}).join('')+'</div>';
  var body=rows.map(function(r){var cells=VL.map(function(pk){var o=r.o[pk];var v=mval(o,cashMode);if(!v)return '<span class="cell"><span class="chip no">–</span></span>';var top=(v===r.mx);return '<a class="cell" href="issue.html?issuer='+encodeURIComponent(r.iss)+'&plat='+encodeURIComponent(PN[pk]||pk)+'"><span class="chip'+(top?' mx':'')+'">'+(top?HEART:'')+_chipW(v)+'</span>'+(cashMode==='t'?_capBD(o):'')+'</a>';}).join('');
   return '<div class="ptr" style="grid-template-columns:'+gc+'"><a class="pc" href="issue.html?issuer='+encodeURIComponent(r.iss)+'"><span class="issmk"><svg viewBox="2 3.6 20 16.4" aria-hidden="true"><use href="#mk"/></svg></span><div><div class="pcn">'+_es(r.iss)+'</div><div class="pci" style="font-family:inherit;font-size:11.5px;color:var(--sub)">보유 '+r.count+'종 · 대표 '+_es(r.rep)+'</div></div></a>'+cells+'</div>';}).join('');
  var mc='<div class="pcardlist">'+rows.map(function(r){return _pbar('issue.html?issuer='+encodeURIComponent(r.iss),_es(r.iss),'보유 '+r.count+'종 · 대표 '+_es(r.rep),r.o);}).join('')+'</div>';
  var note='<div class="pcmpnote"><span class="dot"></span><svg viewBox="0 0 24 24" width="13" height="13" style="color:#000"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> = 이 카드사의 최고 궁합(커플) 플랫폼 · 셀을 누르면 그 카드사·플랫폼 캐시백 목록으로 · 캐시백 기준: 전체=주요+부가, 주요=발급·결제 기본 · 금액은 수집 시점 기준이에요.</div>';
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
 function _chipW(w){var s=_wm(w);return s.replace('만원','만').replace('원','');}
 // 모바일 B안: 카드(사)별 미니 막대 슬롯 — 표시 플랫폼 중 상위3 기본, +N곳 더보기로 전체
 function _pbar(href,title,sub,o){var VL=visList();
  var bars=VL.map(function(pk){return {pk:pk,v:mval(o[pk],cashMode)};}).filter(function(x){return x.v>0;}).sort(function(a,b){return b.v-a.v;});
  if(!bars.length)return '';var mx=bars[0].v;
  function row(x,i,ex){var best=(i===0);return '<div class="pbar-row'+(ex?' extra':'')+'"><span class="dot" style="background:'+(PBC[x.pk]||"#888")+'"></span><span class="pn'+(best?" best":"")+'">'+(best?HEART:'')+(PN[x.pk]||x.pk)+'</span><span class="tr"><i style="width:'+Math.max(6,Math.round(x.v/mx*100))+'%;background:'+(best?"#000":"#cfcfcf")+'"></i></span><span class="amt'+(best?" best":"")+'">'+_chipW(x.v)+'</span></div>';}
  var html=bars.map(function(x,i){return row(x,i,i>=3);}).join('');
  var more=bars.length-3;
  var tg=more>0?'<div class="pbar-toggle"><span class="lbl">+'+more+'곳 더보기</span><svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></div>':'';
  return '<div class="pbar-card" data-href="'+href+'" data-more="'+(more>0?more:0)+'"><div class="pbar-hd">'+title+(sub?'<span class="psub">'+sub+'</span>':'')+'</div><div class="pbar-rows">'+html+'</div>'+tg+'</div>';}
 // 인라인 넛지: 전체1위 ≠ 주요1위 & 주요격차 ≥ 2만원 → 크림 띠(전체 모드 한정)
 function _nudge(o){if(cashMode!=='t')return '';var ks=PORD.filter(function(pk){return o[pk]&&o[pk].t;});if(ks.length<2)return '';
  var bt=ks.reduce(function(a,b){return o[b].t>o[a].t?b:a;});var bm=ks.reduce(function(a,b){return o[b].m>o[a].m?b:a;});
  if(bt===bm||(o[bm].m-o[bt].m)<20000)return '';var pct=o[bt].t?Math.round(o[bt].b/o[bt].t*100):0;
  return '<div class="cmpnudge"><span class="nb"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L4.5 13.5H11l-1 8.5L19.5 10H13z"/></svg></span><div class="nt">실속 체크 · 전체 캐시백은 <b>'+PN[bt]+' '+_chipW(o[bt].t)+'</b>으로 가장 높지만 핵심(주요) 혜택은 '+_chipW(o[bt].m)+'이에요. 실속만 보면 <b>'+PN[bm]+' 주요 '+_chipW(o[bm].m)+'</b>이 더 높아요.</div><span class="nx">'+PN[bt]+' 전체의 '+pct+'%가 부가</span></div>';}
 renderProd=function(){
  var rows=TBL.filter(function(c){return !prodIssF||(c.issuer||'').indexOf(prodIssF)>=0;});
  var VL=visList(),gc='1.6fr repeat('+VL.length+',1fr)';
  rows.forEach(function(c){var mx=0;VL.forEach(function(pk){var v=mval(c.o[pk],cashMode);if(v>mx)mx=v;});c.mx=mx;});
  rows.sort(function(a,b){return b.mx-a.mx;});
  var ISSL=['전체'].concat(Object.keys(TBL.reduce(function(a,c){if(c.issuer)a[c.issuer]=1;return a;},{})));
  var ddm=ISSL.map(function(x){var on=(x==='전체'&&!prodIssF)||x===prodIssF;return '<button data-iss="'+(x==='전체'?'':x)+'"'+(on?' class="on"':'')+'>'+x+'</button>';}).join('');
  var _pm=document.getElementById('prodIssMenu');if(_pm)_pm.innerHTML=ddm;var _pb=document.getElementById('prodIssBtn');if(_pb)_pb.firstChild.textContent='카드사 · '+(prodIssF||'전체')+' ';
  var head='<div class="ptr hd" style="grid-template-columns:'+gc+'"><div>카드 ('+rows.length+')</div>'+VL.map(function(pk){return '<div>'+_pdk(pk,true)+'</div>';}).join('')+'</div>';
  var body=rows.map(function(c){
   var vals=VL.map(function(pk){return mval(c.o[pk],cashMode);});var mx=Math.max.apply(null,vals);
   var cells=VL.map(function(pk){var o=c.o[pk];var v=mval(o,cashMode);if(!v)return '<span class="cell"><span class="chip no">–</span></span>';var top=(v===mx);return '<a class="cell" href="events.html?platform='+pk+'&n='+encodeURIComponent(c.name||'')+'"><span class="chip'+(top?' mx':'')+'">'+(top?HEART:'')+_chipW(v)+'</span>'+(cashMode==='t'?_capBD(o):'')+'</a>';}).join('');
   var plate='<div class="pcimg">'+imgTag(c.img)+'</div>';
   return '<div class="ptr" style="grid-template-columns:'+gc+'"><a class="pc" href="carddetail.html?n='+encodeURIComponent(c.name||'')+'" data-track="cmp" data-label="'+(c.name||'')+'">'+plate+'<div><div class="pcn">'+c.name+'</div><div class="pci">'+c.issuer+'</div></div></a>'+cells+'</div>';}).join('');
  var note='<div class="pcmpnote"><span class="dot"></span><svg viewBox="0 0 24 24" width="13" height="13" style="color:#000"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> = 이 카드의 최고 궁합(커플) 플랫폼 · 행 최대값 · 셀을 누르면 이번달 캐시백 상세로 · 캐시백 기준: 전체=주요+부가, 주요=발급·결제 기본 · 금액은 수집 시점 기준이에요.</div>';
  // 모바일 시안: 카드별 스택 카드(플레이트+이름+최대+사이트별 캐시백 칩, 최대=검은칩)
  var pcards='<div class="pcardlist">'+rows.map(function(c){return _pbar('carddetail.html?n='+encodeURIComponent(c.name||''),c.name,c.issuer,c.o);}).join('')+'</div>';
  document.getElementById('cmp-prod').innerHTML=rows.length?('<div class="ptblwrap"><div class="ptbl">'+head+body+'</div></div>'+pcards+note):'<div class="empty">교차비교 카드가 없어요.</div>';
  if(window.repairImages)repairImages();};
 renderProd();renderPlatToggle();
}).catch(function(){document.getElementById('cmp-iss').innerHTML='<div class="empty">데이터 준비 중</div>';document.getElementById('cmp-prod').innerHTML='<div class="empty">교차비교 데이터 준비 중이에요.</div>';});
/* ===== 통합 검색필터(UF) 컨트롤러 — 플랫폼사·카드사(다중)·캐시백유형(단일)+정렬4 · PC 팝오버 / 모바일 바텀시트 · URL 동기화 ===== */
function _ufEl(id){return document.getElementById(id);}
function _ufIss(){return ORD||[];}
var _UFCK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 6.5"/></svg>';
var _UFX='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';
function ufOptList(kind){
 if(kind==='plat')return PORD.map(function(pk){return '<div class="uf-opt'+(evVis[pk]?' on':'')+'" data-uf-k="'+pk+'"><span class="uf-cb">'+_UFCK+'</span><span class="dot" style="background:'+(PBC[pk]||"#888")+'"></span><span class="nm">'+(PN[pk]||pk)+'</span></div>';}).join('');
 return _ufIss().map(function(n){return '<div class="uf-opt'+(evIssF[n]?' on':'')+'" data-uf-k="'+n+'"><span class="uf-cb">'+_UFCK+'</span><span class="nm">'+n+'</span></div>';}).join('');}
function ufSeg(kind){var arr=kind==='type'?UFTYPES:UFSORTS,cur=kind==='type'?evType:evSortK;return '<div class="uf-seg" data-uf-seg="'+kind+'"'+(kind==='sort'?' style="flex-wrap:wrap"':'')+'>'+arr.map(function(t){return '<button type="button" data-v="'+t[0]+'" class="'+(cur===t[0]?'on':'')+'">'+t[1]+'</button>';}).join('')+'</div>';}
function ufSortRows(){return UFSORTS.map(function(s){return '<div class="uf-srow'+(evSortK===s[0]?' on':'')+'" data-uf-s="'+s[0]+'"><span class="sl">'+s[1]+'</span>'+_UFCK+'</div>';}).join('');}
function ufFillPop(which){
 if(which==='plat')_ufEl('ufPopplat').innerHTML='<div class="uf-poph"><span class="pt">플랫폼사</span><span class="pm">다중 선택</span></div>'+ufOptList('plat')+'<div class="uf-popft"><button type="button" class="r" data-uf-clr="plat">초기화</button><button type="button" class="a" data-uf-close="1">적용</button></div>';
 else if(which==='iss')_ufEl('ufPopiss').innerHTML='<div class="uf-poph"><span class="pt">카드사</span><span class="pm">다중 선택</span></div>'+ufOptList('iss')+'<div class="uf-popft"><button type="button" class="r" data-uf-clr="iss">초기화</button><button type="button" class="a" data-uf-close="1">적용</button></div>';
 else if(which==='type')_ufEl('ufPoptype').innerHTML='<div class="uf-poph"><span class="pt">캐시백 유형</span><span class="pm">단일</span></div><div style="margin-top:4px">'+ufSeg('type')+'</div>';
 else if(which==='sort')_ufEl('ufPopsort').innerHTML='<div class="uf-poph" style="padding:0 4px 4px;margin-bottom:2px"><span class="pt" style="font-size:12px;color:rgba(0,0,0,.45)">정렬</span></div>'+ufSortRows();}
function ufCloseAllPops(){['plat','iss','type','sort'].forEach(function(w){var p=_ufEl('ufPop'+w);if(p)p.classList.remove('open');});var dq=document.querySelectorAll('.uf-ddl[aria-expanded="true"]');for(var i=0;i<dq.length;i++)dq[i].setAttribute('aria-expanded','false');}
function ufOpenPop(which,trigger){var p=_ufEl('ufPop'+which);if(!p)return;var wasOpen=p.classList.contains('open');ufCloseAllPops();if(wasOpen)return;ufFillPop(which);
 var uf=_ufEl('uf');p.style.left=Math.max(0,trigger.offsetLeft)+'px';p.style.top=(trigger.offsetTop+trigger.offsetHeight+8)+'px';p.classList.add('open');
 if(uf&&p.offsetLeft+p.offsetWidth>uf.clientWidth)p.style.left=Math.max(0,uf.clientWidth-p.offsetWidth)+'px';
 if(trigger.hasAttribute('aria-expanded'))trigger.setAttribute('aria-expanded','true');}
function ufFillSheet(){_ufEl('ufSheetBody').innerHTML=
 '<div class="uf-sg"><div class="uf-sg-t">플랫폼사 <span>다중</span></div><div class="uf-sg-opts" data-uf-tags="plat">'+PORD.map(function(pk){return '<button type="button" class="uf-tag'+(evVis[pk]?' on':'')+'" data-uf-k="'+pk+'"><span class="dot" style="background:'+(PBC[pk]||"#888")+'"></span>'+(PN[pk]||pk)+'</button>';}).join('')+'</div></div>'
 +'<div class="uf-sg"><div class="uf-sg-t">카드사 <span>다중</span></div><div class="uf-sg-opts" data-uf-tags="iss">'+_ufIss().map(function(n){return '<button type="button" class="uf-tag'+(evIssF[n]?' on':'')+'" data-uf-k="'+n+'">'+n+'</button>';}).join('')+'</div></div>'
 +'<div class="uf-sg"><div class="uf-sg-t">캐시백 유형 <span>단일</span></div><div style="margin-top:11px">'+ufSeg('type')+'</div></div>'
 +'<div class="uf-sg"><div class="uf-sg-t">정렬</div><div style="margin-top:11px">'+ufSeg('sort')+'</div></div>';}
function ufOpenSheet(){ufFillSheet();_ufEl('ufSheetBg').classList.add('open');document.body.style.overflow='hidden';}
function ufCloseSheet(){var b=_ufEl('ufSheetBg');if(b)b.classList.remove('open');document.body.style.overflow='';}
function ufRender(count){
 var chips=PORD.filter(function(k){return evVis[k];}).map(function(pk){return '<span class="uf-chip"><span class="dot" style="background:'+(PBC[pk]||"#888")+'"></span>'+(PN[pk]||pk)+'<span class="x" data-uf-rm-plat="'+pk+'">'+_UFX+'</span></span>';})
  .concat(_ufIss().filter(function(n){return evIssF[n];}).map(function(n){return '<span class="uf-chip">'+n+'<span class="x" data-uf-rm-iss="'+n+'">'+_UFX+'</span></span>';})).join('');
 var ch=_ufEl('ufChips');if(ch)ch.innerHTML=chips;
 var np=PORD.filter(function(k){return evVis[k];}).length,ni=_ufIss().filter(function(n){return evIssF[n];}).length,tot=np+ni;
 var cp=_ufEl('ufCplat');if(cp)cp.textContent=np?String(np):'';var ci=_ufEl('ufCiss');if(ci)ci.textContent=ni?String(ni):'';
 var fn=_ufEl('ufFn');if(fn){fn.textContent=tot?String(tot):'';fn.className='uf-fn'+(tot?'':' zero');}
 var tt=_ufEl('ufTtype');if(tt)tt.textContent=ufTypeLabel();
 ['ufSortPc','ufSortMo'].forEach(function(id){var b=_ufEl(id);if(b&&b.firstChild)b.firstChild.textContent=ufSortLabel()+' ';});
 var rs=_ufEl('ufReset');if(rs)rs.style.display=tot?'':'none';
 var fa=_ufEl('ufFtApply');if(fa&&count!=null)fa.textContent=count+'건 결과 보기';}
function ufWriteURL(){var sp=new URLSearchParams(location.search);
 var pl=PORD.filter(function(k){return evVis[k];});pl.length?sp.set('plat',pl.join(',')):sp.delete('plat');sp.delete('issuer');
 var is=_ufIss().filter(function(n){return evIssF[n];});is.length?sp.set('iss',is.join(',')):sp.delete('iss');
 evType!=='main'?sp.set('type',evType):sp.delete('type');evSortK!=='cash'?sp.set('sort',evSortK):sp.delete('sort');
 var q=sp.toString();try{history.replaceState(null,'',location.pathname+(q?'?'+q:''));}catch(_){}}
function ufApply(){render();ufWriteURL();}
function ufResetAll(){evVis={};evIssF={};evType='main';evSortK='cash';ufCloseAllPops();ufApply();var sb=_ufEl('ufSheetBg');if(sb&&sb.classList.contains('open'))ufFillSheet();}
function ufInit(){var uf=_ufEl('uf');if(!uf||uf._b)return;uf._b=1;
 uf.addEventListener('click',function(e){
  var dd=e.target.closest('.uf-ddl');if(dd){e.stopPropagation();ufOpenPop(dd.getAttribute('data-uf'),dd);return;}
  var spc=e.target.closest('#ufSortPc');if(spc){e.stopPropagation();ufOpenPop('sort',spc);return;}
  var opt=e.target.closest('.uf-opt[data-uf-k]');if(opt){var pop=opt.closest('.uf-pop');var k=opt.getAttribute('data-uf-k');if(pop&&pop.id==='ufPopplat')evVis[k]=evVis[k]?0:1;else evIssF[k]=evIssF[k]?0:1;opt.classList.toggle('on');ufApply();return;}
  var seg=e.target.closest('.uf-seg[data-uf-seg] button[data-v]');if(seg){var sg=seg.closest('.uf-seg').getAttribute('data-uf-seg');if(sg==='type')evType=seg.getAttribute('data-v');else evSortK=seg.getAttribute('data-v');var bb=seg.closest('.uf-seg').querySelectorAll('button');for(var j=0;j<bb.length;j++)bb[j].classList.toggle('on',bb[j]===seg);ufApply();return;}
  var sr=e.target.closest('.uf-srow[data-uf-s]');if(sr){evSortK=sr.getAttribute('data-uf-s');ufCloseAllPops();ufApply();return;}
  var clr=e.target.closest('[data-uf-clr]');if(clr){var g=clr.getAttribute('data-uf-clr');if(g==='plat')evVis={};else evIssF={};ufFillPop(g);ufApply();return;}
  if(e.target.closest('[data-uf-close]')){ufCloseAllPops();return;}
  var rmp=e.target.closest('[data-uf-rm-plat]');if(rmp){evVis[rmp.getAttribute('data-uf-rm-plat')]=0;ufApply();return;}
  var rmi=e.target.closest('[data-uf-rm-iss]');if(rmi){evIssF[rmi.getAttribute('data-uf-rm-iss')]=0;ufApply();return;}
  if(e.target.closest('#ufReset')){ufResetAll();return;}});
 var fb=_ufEl('ufFbtn');if(fb)fb.onclick=function(){ufOpenSheet();};
 var sm=_ufEl('ufSortMo');if(sm)sm.onclick=function(){ufOpenSheet();};
 var sheet=_ufEl('ufSheet');if(sheet)sheet.addEventListener('click',function(e){
  var tag=e.target.closest('.uf-tag[data-uf-k]');if(tag){var box=tag.closest('[data-uf-tags]').getAttribute('data-uf-tags');var k=tag.getAttribute('data-uf-k');if(box==='plat')evVis[k]=evVis[k]?0:1;else evIssF[k]=evIssF[k]?0:1;tag.classList.toggle('on');render();ufWriteURL();return;}
  var seg=e.target.closest('.uf-seg[data-uf-seg] button[data-v]');if(seg){var sg=seg.closest('.uf-seg').getAttribute('data-uf-seg');if(sg==='type')evType=seg.getAttribute('data-v');else evSortK=seg.getAttribute('data-v');var bb=seg.closest('.uf-seg').querySelectorAll('button');for(var j=0;j<bb.length;j++)bb[j].classList.toggle('on',bb[j]===seg);render();ufWriteURL();return;}});
 var sx=_ufEl('ufSheetX');if(sx)sx.onclick=ufCloseSheet;
 var bg=_ufEl('ufSheetBg');if(bg)bg.addEventListener('click',function(e){if(e.target===bg)ufCloseSheet();});
 var fr=_ufEl('ufFtReset');if(fr)fr.onclick=function(){evVis={};evIssF={};evType='main';evSortK='cash';ufFillSheet();render();ufWriteURL();};
 var fa=_ufEl('ufFtApply');if(fa)fa.onclick=ufCloseSheet;
 document.addEventListener('click',function(e){if(!e.target.closest('#uf'))ufCloseAllPops();});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'){ufCloseAllPops();ufCloseSheet();}});
 ufRender();}
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
 # 강조 컴카드(이달의 PICK)
 '.tip-pick{display:grid;grid-template-columns:300px 1fr;background:var(--block-lime);border-radius:22px;overflow:hidden;text-decoration:none;color:#000;box-shadow:0 12px 30px rgba(0,0,0,.1);margin:24px 0 0}'
 '.tip-pick-img{position:relative;display:flex;align-items:center;justify-content:center;background:var(--block-navy);min-height:158px}.tip-pick-img svg{width:104px;height:80px;color:#fff;opacity:.92}'
 '.tip-pick-badge{position:absolute;left:16px;top:16px;font-family:var(--font-mono,monospace);font-size:9px;background:var(--accent-magenta);color:#fff;padding:5px 11px;border-radius:50px}'
 '.tip-pick-body{padding:30px 32px;display:flex;flex-direction:column;justify-content:center}'
 '.tip-pick-eb{font-family:var(--font-mono,monospace);font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:rgba(0,0,0,.55)}'
 '.tip-pick-t{font-weight:700;font-size:26px;letter-spacing:-.7px;line-height:1.25;margin-top:10px}'
 '.tip-pick-d{font-weight:400;font-size:14.5px;line-height:1.5;color:rgba(0,0,0,.62);margin-top:10px}'
 '.tip-pick-cta{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:50px;background:#000;color:#fff;font-weight:600;font-size:15px;margin-top:20px;align-self:flex-start}.tip-pick-cta svg{width:16px;height:16px}'
 # 가로 탭
 '.tip-tabs{display:flex;gap:28px;border-bottom:1px solid var(--hairline);margin:26px 0 0;overflow-x:auto;-webkit-overflow-scrolling:touch}.tip-tabs::-webkit-scrollbar{display:none}'
 '.tip-tab{background:0;border:0;padding:0 0 13px;font-family:inherit;font-weight:480;font-size:15px;letter-spacing:-.2px;white-space:nowrap;color:rgba(0,0,0,.5);border-bottom:2px solid transparent;margin-bottom:-1px;cursor:pointer;flex:0 0 auto}'
 '.tip-tab.on{font-weight:700;color:#000;border-bottom-color:#000}'
 # 썸네일 리스트 (데스크탑 2열)
 '.tip-list{display:grid;grid-template-columns:1fr 1fr;gap:14px 24px;margin-top:10px}'
 '.tip-row{display:flex;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--hairline-soft);text-decoration:none;color:#000}'
 '.tip-row:hover .tip-rt{color:var(--accent,#000);text-decoration:underline}'
 '.tip-thumb{width:96px;height:64px;border-radius:12px;flex:0 0 auto;display:flex;align-items:center;justify-content:center;overflow:hidden}.tip-thumb svg{width:34px;height:26px;color:#33402a;opacity:.85}'
 '.tip-rcat{font-family:var(--font-mono,monospace);font-size:9px;color:rgba(0,0,0,.45)}'
 '.tip-rt{font-weight:700;font-size:15px;letter-spacing:-.3px;line-height:1.35;margin-top:4px}'
 # 상세(detail) — 기존 유지 클래스
 '.adt .ghero{border-radius:16px;overflow:hidden;margin-bottom:18px}.adt .ghero img{width:100%;display:block}'
 '.adt .ah{font-weight:340;font-size:32px;letter-spacing:-1px;line-height:1.2;margin:14px 0 0}.adt .asum{font-size:16px;color:rgba(0,0,0,.6);margin:12px 0 0;line-height:1.5}'
 '.adt p{font-size:15.5px;line-height:1.75;margin:16px 0 0;color:rgba(0,0,0,.82)}.adt .bk2{display:inline-block;margin-top:30px;font-weight:600;font-size:14px}'
 '@media(max-width:760px){'
 '.tip-pick{grid-template-columns:1fr}.tip-pick-img img{height:158px;min-height:0}.tip-pick-body{padding:18px 18px 20px}.tip-pick-t{font-size:20px}.tip-pick-d{font-size:13px}.tip-pick-cta{width:100%;justify-content:center;font-size:15px}'
 '.tip-list{grid-template-columns:1fr;gap:0}'
 '.tip-thumb{width:74px;height:56px}.tip-thumb svg{width:28px;height:22px}.tip-rt{font-size:14px}'
 '.adt .ah{font-size:24px}'
 '}'
 '</style>'
 '<div class="wrap"><section id="listwrap">'
 '<div style="padding:24px 0 0"><span class="pg-eb">CARD GUIDE</span><h1 style="font-weight:340;font-size:32px;letter-spacing:-.8px;line-height:1.05;margin:6px 0 0">티라노 TIP</h1><p style="font-weight:400;font-size:14px;color:rgba(0,0,0,.6);margin:5px 0 0">전문가가 매달 직접 뜯어본 카드 전략.</p></div>'
 '<div id="tipPick"></div>'
 '<div class="tip-tabs" id="tipTabs"></div>'
 '<div class="tip-list" id="list"><div class="empty" style="grid-column:1/-1"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></section>'
 '<div id="detail" style="display:none"></div></div>')
CONTENT_JS=r"""
var C=[],cur='발급 팁';
var TYPES=[{k:'발급 팁',h:'이달의 캐시백 전략',cats:['발급 팁']},{k:'기초 상식',h:'카드 지식',cats:['기초 상식','여행']},{k:'할인 활용',h:'신용카드 해부',cats:['할인 활용']}];
var CATIMG={'발급 팁':'img/guide/issue.svg','할인 활용':'img/guide/discount.svg','기초 상식':'img/guide/basic.svg','여행':'img/guide/travel.svg'};
var CATBG={'발급 팁':'var(--block-lime)','기초 상식':'var(--block-cream)','할인 활용':'var(--block-mint)','여행':'var(--block-mint)'};
function _thumb(x){return x.img||CATIMG[x.cat]||'img/guide/reco.svg';}
function _catsOf(k){for(var i=0;i<TYPES.length;i++)if(TYPES[i].k===k)return TYPES[i].cats;return [k];}
function rowHtml(x){return '<a class="tip-row" href="content.html?id='+x.id+'"><span class="tip-thumb" style="background:'+(CATBG[x.cat]||'var(--block-lime)')+'"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg></span><div style="min-width:0"><div class="tip-rcat">'+(x.cat||'')+'</div><div class="tip-rt">'+x.title+'</div></div></a>';}
function renderList(){var cats=_catsOf(cur);var items=C.filter(function(x){return cats.indexOf(x.cat)>=0;});document.getElementById('list').innerHTML=items.length?items.map(rowHtml).join(''):'<div class="empty" style="grid-column:1/-1;padding:30px 0">글이 없어요.</div>';}
function tabs(){var t=document.getElementById('tipTabs');t.innerHTML=TYPES.map(function(ty){return '<button class="tip-tab'+(cur===ty.k?' on':'')+'" data-k="'+ty.k+'">'+ty.h+'</button>';}).join('');
 t.querySelectorAll('.tip-tab').forEach(function(b){b.onclick=function(){cur=b.dataset.k;tabs();renderList();};});}
function pick(){var st=C.filter(function(x){return x.cat==='발급 팁';})[0]||C[0];var el=document.getElementById('tipPick');if(!st||!el)return;
 el.innerHTML='<a class="tip-pick" href="content.html?id='+st.id+'"><div class="tip-pick-img"><svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg><span class="tip-pick-badge">이달의 PICK</span></div>'
  +'<div class="tip-pick-body"><div class="tip-pick-eb">이달의 캐시백 전략 · 2026.06</div><div class="tip-pick-t">'+st.title+'</div>'+(st.summary?'<div class="tip-pick-d">'+st.summary+'</div>':'')+'<span class="tip-pick-cta">전략 보러가기 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></span></div></a>';}
function detail(d){document.getElementById('listwrap').style.display='none';var el=document.getElementById('detail');el.style.display='';
 if(d.html){el.innerHTML='<div class="adt">'+d.html+'<a class="bk2" href="content.html" style="display:inline-block;margin-top:32px">← 티라노 TIP</a></div>';ctSeo(d.title+' | 카드티라노',(d.summary||d.title),'content.html?id='+d.id);return;}
 var hero=d.img?'<div class="ghero"><img src="'+d.img+'" alt="'+d.cat+'" loading="eager"/></div>':'';
 el.innerHTML='<div class="adt">'+hero+'<div class="acat" style="display:inline-block;background:'+(CATBG[d.cat]||'var(--block-lime)')+';color:#000;padding:6px 14px;border-radius:50px;font-size:12px;font-weight:700">'+d.cat+'</div><div class="ah">'+d.title+'</div>'+(d.summary?'<div class="asum">'+d.summary+'</div>':'')+(d.body||[]).map(function(p){return '<p>'+p+'</p>';}).join("")+'<a class="bk2" href="content.html">← 티라노 TIP</a></div>';ctSeo(d.title+' | 카드티라노',(d.summary||d.title),'content.html?id='+d.id);}
var id=new URLSearchParams(location.search).get('id');
fetch('content.json').then(function(r){return r.json();}).then(function(j){C=j.items;if(id!==null){var d=C.find(function(x){return String(x.id)===String(id);});if(d){detail(d);return;}}
 pick();tabs();renderList();});
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
 ctSeo(card.name+' 혜택·발급 캐시백 | 카드티라노',(card.issuer?card.issuer+' ':'')+card.name+'의 영역별 카드 혜택·연회비·전월실적과 토스·카드고릴라·아정당 등 플랫폼별 발급 캐시백을 한눈에 비교.',(card.id!=null?'carddetail.html?id='+card.id:'carddetail.html?n='+encodeURIComponent(card.name)));
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
 '.rg-only-mo{display:none}'
 '.rg-wrap{max-width:1080px;margin:0 auto;padding:0 20px 96px}'
 '.rg-back{display:inline-flex;align-items:center;gap:7px;color:rgba(0,0,0,.55);font-weight:480;font-size:14px;padding:18px 0 0}.rg-back svg{width:16px;height:16px}'
 # 헤더
 '.rg-head{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;padding:14px 0 6px}'
 '.rg-pchip{display:inline-flex;align-items:center;gap:10px;background:var(--surface-soft);padding:8px 16px 8px 12px;border-radius:50px}.rg-pchip i{width:14px;height:14px;border-radius:50%;flex:0 0 auto}.rg-pchip b{font-weight:700;font-size:26px;letter-spacing:-.6px;line-height:1}.rg-pchip .pl{font-family:var(--font-mono,monospace);font-size:10px;color:rgba(0,0,0,.45);margin-left:2px}'
 '.rg-h{font-weight:340;font-size:40px;line-height:1.02;letter-spacing:-1.3px;margin:14px 0 0}'
 '.rg-hsub{font-weight:400;font-size:15px;color:rgba(0,0,0,.62);margin:10px 0 0;word-break:keep-all}.rg-hsub b{font-weight:700}'
 '.rg-cta{display:inline-flex;align-items:center;gap:8px;padding:13px 24px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none;margin-top:20px}.rg-cta svg{width:17px;height:17px}'
 '.rg-deco{width:230px;flex-shrink:0;display:flex;align-items:center;justify-content:center}.rg-deco svg{width:100%;height:auto;display:block;overflow:visible}'
 # 상품 리스트
 '.rg-sec{padding:24px 0 0}'
 '.rg-listhd{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap}'
 '.rg-listhd h2{font-weight:340;font-size:24px;letter-spacing:-.6px;margin:0}.rg-listhd .hint{font-weight:400;font-size:13px;color:rgba(0,0,0,.5)}'
 '.rg-plist{display:flex;flex-direction:column;gap:8px;margin-top:14px}'
 '.rg-prow{display:grid;grid-template-columns:auto 1fr auto auto;gap:16px;align-items:center;border:1px solid var(--hairline);background:#fff;border-radius:14px;padding:12px 16px;cursor:pointer;text-align:left;width:100%;font:inherit;color:inherit}'
 '.rg-prow.sel{border:2px solid #000;background:var(--surface-soft)}'
 '.rg-pl{width:62px;flex-shrink:0;aspect-ratio:1.586/1;border-radius:8px;overflow:hidden;background:var(--surface-soft)}.rg-pl img{width:100%;height:100%;object-fit:cover;display:block}'
 '.rg-pn{display:flex;align-items:center;gap:7px}.rg-pn b{font-weight:700;font-size:16px}'
 '.rg-pi{font-family:var(--font-mono,monospace);font-size:10px;opacity:.5;margin-top:3px}'
 '.rg-tag{font-family:var(--font-mono,monospace);font-size:9px;padding:3px 8px;border-radius:50px;white-space:nowrap}.rg-tag.mx{background:#000;color:#fff}.rg-tag.se{background:var(--accent-magenta);color:#fff}'
 '.rg-pcash{text-align:right}.rg-pcash .l{font-family:var(--font-mono,monospace);font-size:9px;opacity:.45}.rg-pcash .v{font-weight:700;font-size:20px;letter-spacing:-.4px;white-space:nowrap}'
 '.rg-parr{width:18px;height:18px;color:rgba(0,0,0,.35)}'
 # 차트
 '.rg-chart{background:var(--block-lime);border-radius:22px;padding:30px 34px;margin-top:24px}'
 '.rg-chart-h{display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:10px}'
 '.rg-ceb{font-family:var(--font-mono,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.55)}'
 '.rg-ct{font-weight:340;font-size:26px;letter-spacing:-.7px;margin:6px 0 0}'
 '.rg-sums{display:flex;gap:18px}.rg-sums>div{text-align:right}.rg-sums .l{font-family:var(--font-mono,monospace);font-size:9px;opacity:.5}.rg-sums .v{font-weight:700;font-size:22px}'
 '.rg-bars{display:flex;align-items:flex-end;gap:18px;height:200px;margin-top:24px}.rg-bars.empty{position:relative}'
 '.rg-col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px}'
 '.rg-col .lbl{font-weight:700;font-size:14px}.rg-col .mm{font-family:var(--font-mono,monospace);font-size:11px;color:rgba(0,0,0,.55)}'
 '.rg-bar{width:54%;max-width:62px;border-radius:8px 8px 0 0;background:var(--block-navy);transition:height .4s}'
 '.rg-bar.miss{background:repeating-linear-gradient(135deg,transparent,transparent 5px,rgba(0,0,0,.05) 5px,rgba(0,0,0,.05) 6px);border:1.5px dashed rgba(0,0,0,.22);border-bottom:none}'
 '.rg-curbar{width:54%;max-width:62px;border-radius:8px 8px 0 0;overflow:hidden;display:flex;flex-direction:column;transition:height .4s}.rg-curbar .sub{background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.55)),var(--accent-magenta)}.rg-curbar .main{flex:1;background:var(--accent-magenta)}'
 '.rg-note-c{position:absolute;left:0;right:0;top:42%;text-align:center}.rg-note-c span{font-weight:540;font-size:13px;color:rgba(0,0,0,.55);background:rgba(220,238,177,.9);padding:6px 14px;border-radius:50px}'
 '.rg-legend{display:flex;align-items:center;gap:18px;margin-top:18px;flex-wrap:wrap}.rg-legend span.lg{display:inline-flex;align-items:center;gap:7px;font-size:13px;color:rgba(0,0,0,.6)}.rg-legend i{width:12px;height:12px;border-radius:3px;display:inline-block;flex:0 0 auto}.rg-lg-mag{background:var(--accent-magenta)}.rg-lg-sub{background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.55)),var(--accent-magenta)}.rg-lg-navy{background:var(--block-navy)}'
 # 구성
 '.rg-comp{padding:30px 0 0}'
 '.rg-comp-eb{font-family:var(--font-mono,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.5)}'
 '.rg-comp-t{font-weight:340;font-size:26px;letter-spacing:-.7px;margin:6px 0 4px}'
 '.rg-comp-p{font-weight:400;font-size:13px;color:rgba(0,0,0,.55);margin:0 0 16px}.rg-comp-p b{font-weight:700;color:#000}'
 '.rg-main{background:var(--block-navy);color:#fff;border-radius:18px;padding:24px 28px}.rg-main .l{font-family:var(--font-mono,monospace);font-size:10px;opacity:.6;margin-bottom:14px}.rg-main .row{display:flex;align-items:center;justify-content:space-between;gap:16px}.rg-main .row .t{font-weight:540;font-size:16px;opacity:.92}.rg-main .row .v{font-weight:700;font-size:26px;letter-spacing:-.6px;white-space:nowrap}'
 '.rg-subh{font-family:var(--font-mono,monospace);font-size:10px;color:rgba(0,0,0,.5);margin:14px 0 12px}'
 '.rg-subs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}'
 '.rg-sub{border:1px solid var(--hairline);border-radius:14px;padding:16px;display:flex;align-items:center;gap:13px}.rg-sub .ic{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}.rg-sub .ic svg{width:21px;height:21px;color:#000}.rg-sub .t{font-weight:700;font-size:14px}.rg-sub .c{font-weight:400;font-size:12px;color:rgba(0,0,0,.55);margin-top:2px}.rg-sub .v{font-weight:700;font-size:15px;margin-left:auto;white-space:nowrap}'
 '.rg-subnone{color:rgba(0,0,0,.5);font-size:13px;padding:4px 0}'
 # 티라노 코칭
 '.rg-coach{background:var(--surface-soft);border-radius:20px;padding:26px 28px;margin-top:30px;display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center}'
 '.rg-coach-badge{text-align:center}.rg-coach-ring{width:84px;height:84px;border-radius:50%;border:3px solid currentColor;color:var(--success);display:flex;align-items:center;justify-content:center;margin:0 auto}.rg-coach-ring.hold{color:#cf9220}.rg-coach-ring.no{color:rgba(0,0,0,.35)}.rg-coach-ring span{width:46px;height:46px;border-radius:50%;border:3px solid currentColor;display:block}'
 '.rg-coach-badge .lab{font-weight:700;font-size:16px;margin-top:10px}.rg-coach-badge .mono{font-family:var(--font-mono,monospace);font-size:9px;opacity:.5;margin-top:2px}'
 '.rg-coach-head{display:flex;align-items:center;gap:9px;margin-bottom:10px}.rg-coach-head svg{width:20px;height:20px}.rg-coach-head .eb{font-family:var(--font-mono,monospace);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:rgba(0,0,0,.5)}'
 '.rg-coach-molab{font-weight:700;font-size:14px;color:var(--success);margin-bottom:4px}.rg-coach-molab.hold{color:#cf9220}.rg-coach-molab.no{color:rgba(0,0,0,.55)}'
 '.rg-coach-t{font-weight:540;font-size:19px;letter-spacing:-.4px;line-height:1.35}'
 '.rg-coach-leg{display:flex;gap:18px;margin-top:16px;flex-wrap:wrap}.rg-coach-leg span{display:inline-flex;align-items:center;gap:7px;font-weight:480;font-size:13px;color:rgba(0,0,0,.65)}.rg-coach-leg .dot{width:20px;height:20px;flex:0 0 auto}.rg-coach-leg .dot.o{border:2px solid var(--success);border-radius:50%}'
 # 이런 이벤트도
 '.rg-others-sec{padding:30px 0 0}.rg-others-sec h2{font-weight:340;font-size:24px;letter-spacing:-.6px;margin:0 0 14px}'
 '.rg-others{display:flex;flex-direction:column;gap:10px}'
 '.rg-orow{display:grid;grid-template-columns:auto 1fr auto auto;gap:16px;align-items:center;border:1px solid var(--hairline);border-radius:16px;padding:14px 18px;text-decoration:none;color:#000}.rg-orow .rg-pl{width:54px}'
 '.rg-otag{display:inline-block;padding:4px 10px;border-radius:50px;font-family:var(--font-mono,monospace);font-size:9px;text-transform:uppercase;margin-bottom:6px}'
 # 방어 문구
 '.rg-foot{font-weight:400;font-size:12px;line-height:1.6;color:rgba(0,0,0,.45);padding:28px 0 0}.rg-foot b{font-weight:600;color:rgba(0,0,0,.6)}'
 # 하단 고정 CTA
 '.rg-float{position:fixed;left:0;right:0;bottom:0;z-index:55;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--hairline);padding:14px 0}.rg-float .in{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;gap:14px}.rg-float .lab{font-weight:540;font-size:14px;color:rgba(0,0,0,.62)}.rg-float .lab b{color:#000;font-weight:700}.rg-float .go{display:inline-flex;align-items:center;gap:8px;padding:14px 26px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none;white-space:nowrap}.rg-float .go svg{width:17px;height:17px}'
 # ===== 모바일 시안 (≤680) — PC와 분리 =====
 '@media(max-width:680px){'
 '.rg-only-pc{display:none!important}.rg-only-mo{display:inline}'
 '.rg-head{grid-template-columns:1fr auto;gap:10px;align-items:center}'
 '.rg-pchip{padding:6px 13px 6px 9px}.rg-pchip i{width:11px;height:11px}.rg-pchip b{font-size:19px}'
 '.rg-h{font-size:25px;margin-top:10px}.rg-hsub{font-size:12px;margin-top:7px}'
 '.rg-deco{width:110px}'
 '.rg-listhd h2{font-size:16px}.rg-listhd .hint{font-size:11px}'
 '.rg-prow{grid-template-columns:auto 1fr auto;gap:12px;padding:9px 12px}.rg-pl{width:48px}.rg-pn b{font-size:14px}.rg-pcash .v{font-size:16px}'
 '.rg-chart{padding:18px}.rg-ct{font-size:11px;font-family:var(--font-mono,monospace);text-transform:uppercase;letter-spacing:.4px;color:rgba(0,0,0,.55);margin:0}'
 '.rg-bars{height:120px;gap:10px;margin-top:14px}.rg-bar,.rg-curbar{max-width:34px}.rg-col .lbl{font-size:11px}.rg-col .mm{font-size:8px}'
 '.rg-legend{gap:12px;margin-top:12px}.rg-legend span.lg{font-size:10px;gap:5px}.rg-legend i{width:9px;height:9px;border-radius:2px}'
 '.rg-comp-t{font-size:16px;margin:0 0 2px}.rg-comp-p{font-size:11px;margin-bottom:10px}'
 '.rg-main{border-radius:14px;padding:16px 18px}.rg-main .row .t{font-size:13px}.rg-main .row .v{font-size:18px}.rg-main .l{margin-bottom:0;display:none}'
 '.rg-subs{grid-template-columns:1fr;gap:7px}.rg-sub{padding:11px 13px;gap:11px}.rg-sub .ic{width:34px;height:34px}.rg-sub .ic svg{width:18px;height:18px}.rg-sub .t{font-size:13px}.rg-sub .v{font-size:14px}'
 '.rg-coach{grid-template-columns:auto 1fr;gap:14px;padding:18px;border-radius:16px}.rg-coach-ring{width:56px;height:56px}.rg-coach-ring span{width:30px;height:30px}.rg-coach-t{font-size:12px;font-weight:400;color:rgba(0,0,0,.65);line-height:1.45;margin-top:4px}'
 '.rg-float .go{flex:1;justify-content:center}'
 '.mtab{display:none}'
 '}'
 '</style>'
 '<div class="rg-wrap"><a class="rg-back" href="issue.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12H5"/><path d="M11 6l-6 6 6 6"/></svg>이번달 캐시백<span class="rg-only-pc">으로</span></a>'
 '<div id="edroot"><div class="empty" style="padding:60px 0"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '<div id="rgFloat"></div>')
EVENTDETAIL_JS=r"""
var EGG='<svg viewBox="0 0 250 210" aria-hidden="true"><ellipse cx="128" cy="174" rx="104" ry="26" fill="#e7d9b6"/><ellipse cx="128" cy="170" rx="96" ry="22" fill="#f1e6c8"/><g stroke="rgba(0,0,0,.22)" stroke-width="1.6"><ellipse cx="70" cy="150" rx="15" ry="20" fill="#fbf6ea" transform="rotate(-14 70 150)"/><ellipse cx="186" cy="150" rx="15" ry="20" fill="#fbf6ea" transform="rotate(14 186 150)"/><ellipse cx="103" cy="142" rx="15" ry="20" fill="#fff9ee" transform="rotate(-7 103 142)"/><ellipse cx="153" cy="142" rx="15" ry="20" fill="#fff9ee" transform="rotate(7 153 142)"/></g><g transform="translate(64,8) scale(5)" fill="#1f1d3d"><path d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill-rule="evenodd" d="M15.8 4.6 h2.6 a2.6 2.6 0 0 1 2.6 2.6 v1.7 a2.6 2.6 0 0 1 -2.6 2.6 h-2.6 a2.6 2.6 0 0 1 -2.6 -2.6 v-1.7 a2.6 2.6 0 0 1 2.6 -2.6 z M17.75 7.4 a0.85 0.85 0 1 0 1.7 0 a0.85 0.85 0 1 0 -1.7 0 z M18.4 9.5 h2.6 v1 h-2.6 z"/></g><g stroke="rgba(0,0,0,.24)" stroke-width="1.6"><ellipse cx="92" cy="166" rx="16" ry="21" fill="#ffffff" transform="rotate(-9 92 166)"/><ellipse cx="128" cy="170" rx="17" ry="22" fill="#fffdf7" transform="rotate(2 128 170)"/><ellipse cx="164" cy="166" rx="16" ry="21" fill="#ffffff" transform="rotate(11 164 166)"/></g></svg>';
var TYR='<svg viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>';
var PBC={cardgorilla:'#FF6A13',banksalad:'#19C37D',toss:'#3182F6',ajungdang:'#1B64DA',naver:'#03C75A',kakaopay:'#FEE500'};
var PNM={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
function _nk(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _wm(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function _man(n){return n?Math.round(n/10000):0;}
function _mlabel(m){var mm=(''+m).split('-')[1];return mm?(parseInt(mm,10)+'월'):m;}
function _esc(s){return (''+(s||'')).replace(/"/g,'&quot;').replace(/</g,'&lt;');}
// 부가 유형 → 아웃라인 글리프 + 파스텔 배경 + 짧은 조건문 (이모지 금지·DS)
var CATSVG={'해외':'<circle cx="12" cy="12" r="8"/><path d="M4 12h16"/><path d="M12 4c2.5 2.3 3.8 5 3.8 8s-1.3 5.7-3.8 8c-2.5-2.3-3.8-5-3.8-8s1.3-5.7 3.8-8z"/>','자동납부':'<rect x="4" y="5.5" width="16" height="15" rx="2.5"/><path d="M4 10h16M8.5 3v4M15.5 3v4"/>','리볼빙':'<path d="M20 11a8 8 0 1 0-1.6 5"/><path d="M20 5.5V11h-5.5"/>','멤버십':'<rect x="3" y="5" width="18" height="12" rx="2.5"/><path d="M9 21h6M12 17v4"/>','여행':'<path d="M21 4L3 11l6 2.2L11 20l3-5 5-11z"/><path d="M9 13.2L14 8"/>','마케팅동의':'<path d="M5 12.5l4.2 4.2L19 6.8"/>','쿠폰':'<path d="M4 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H6a2 2 0 0 1-2-2 2 2 0 0 0 0-4z"/><path d="M14 6v12"/>','추가이용':'<path d="M12 5v14M5 12h14"/>','오프라인':'<path d="M4 9l1.2-4h13.6L20 9"/><path d="M5 9v10h14V9"/><path d="M4 9h16"/><path d="M9.5 19v-5h5v5"/>','연회비':'<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M3 10h18"/>','간편결제':'<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>','신규':'<path d="M12 3.5l1.7 5.8 5.8 1.7-5.8 1.7-1.7 5.8-1.7-5.8-5.8-1.7 5.8-1.7z"/>'};
var CATBG={'해외':'var(--block-mint)','자동납부':'var(--block-lime)','멤버십':'var(--block-lilac)','여행':'var(--block-coral)','마케팅동의':'var(--block-cream)','쿠폰':'var(--block-pink)','리볼빙':'var(--surface-soft)','추가이용':'var(--surface-soft)','오프라인':'var(--block-mint)','연회비':'var(--block-cream)','간편결제':'var(--block-lilac)','신규':'var(--block-lime)'};
var CATCOND={'해외':'해외 결제 시','자동납부':'자동납부 등록 시','멤버십':'OTT·멤버십 결제 시','여행':'여행 결제 시','마케팅동의':'마케팅 수신 동의 시','쿠폰':'쿠폰 사용 시','리볼빙':'리볼빙 약정 시','추가이용':'추가 이용 시','오프라인':'오프라인 결제 시','연회비':'연회비 캐시백','간편결제':'간편결제 이용 시','신규':'신규 발급 시'};
function catIcon(cat){return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+(CATSVG[cat]||'<path d="M12 5v14M5 12h14"/>')+'</svg>';}
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
 var CARDMAP={},ID2={};for(var _k in cj){(cj[_k]||[]).forEach(function(c){var n=_nk(c.name);if(!CARDMAP[n])CARDMAP[n]=c;if(c.id!=null)ID2[String(c.id)]=n;});}
 var root=document.getElementById('edroot');
 var focusNk=qn?_nk(qn):(qid&&ID2[String(qid)]?ID2[String(qid)]:'');
 var P=qPlat;
 if(!P&&focusNk){var fp=PE.filter(function(p){return _nk(p.name)===focusNk;})[0];if(fp){var mx=0;(fp.events||[]).forEach(function(e){if((e.reward_won||0)>mx){mx=e.reward_won;P=e.platform;}});}}
 if(!P){root.innerHTML='<div class="empty" style="padding:60px 0">플랫폼 정보가 없어요. <a class="accent" href="issue.html">이번달 캐시백</a></div>';return;}
 function evOf(p){return (p.events||[]).filter(function(e){return e.platform===P&&e.reward_won;}).sort(function(a,b){return b.reward_won-a.reward_won;})[0];}
 var platGroup=PE.map(function(p){var e=evOf(p);return e?{p:p,e:e}:null;}).filter(Boolean).sort(function(a,b){return b.e.reward_won-a.e.reward_won;});
 if(!platGroup.length){root.innerHTML='<div class="empty" style="padding:60px 0">이 플랫폼의 발급 캐시백이 없어요. <a class="accent" href="issue.html">이번달 캐시백</a></div>';return;}
 var anchor=(focusNk?platGroup.filter(function(g){return _nk(g.p.name)===focusNk;})[0]:null)||platGroup[0];
 var aIss=(anchor.p.issuer||''),aR=anchor.e.reward_won;
 function _rgk(g){return g.e.reward_group||(P+'|'+(g.p.issuer||'')+'|'+g.e.reward_won);}
 var aKey=_rgk(anchor);
 var group=platGroup.filter(function(g){return _rgk(g)===aKey;}).sort(function(a,b){return (a.p.name||'').localeCompare(b.p.name||'','ko');});
 var focusIdx=0;for(var gi=0;gi<group.length;gi++){if(group[gi]===anchor){focusIdx=gi;break;}}
 var col=PBC[P]||'#888',pnm=PNM[P]||P,N=group.length;
 var ARW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg>';
 var UR='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M9 7h8v8"/></svg>';
 Promise.all(months.map(function(m){return m===_cm?Promise.resolve(null):fetch('history/'+m+'.json').then(function(r){return r.json();}).catch(function(){return null;});})).then(function(MS){
  // ── 헤더 (PC: 칩+제목+부제+CTA+알일러스트 / 모바일: 칩(플랫폼라벨X)+제목+부제+작은알, CTA는 하단 플로팅만) ──
  var subFull=pnm+'에서 지금 발급하면 받는 캐시백 묶음이에요. <b>'+N+'개 카드</b>가 이 캐시백에 들어 있어요.';
  var subMo='<b>'+N+'개 카드</b>가 들어 있어요.';
  var sub=(N>1)?('<span class="rg-only-pc">'+subFull+'</span><span class="rg-only-mo">'+subMo+'</span>'):('<b>'+anchor.p.name+'</b> 발급 캐시백');
  var head='<div class="rg-head"><div>'
   +'<div class="rg-pchip"><i style="background:'+col+'"></i><b>'+pnm+'</b><span class="pl rg-only-pc">플랫폼</span></div>'
   +'<h1 class="rg-h">이번달 발급 캐시백</h1>'
   +'<p class="rg-hsub">'+sub+'</p>'
   +'<a class="rg-cta rg-only-pc" id="rgHeadCta" href="#" target="_blank" rel="sponsored nofollow noopener">'+pnm+'에서 자세히보기 '+UR+'</a>'
   +'</div><div class="rg-deco">'+EGG+'</div></div>';
  // ── 상품 리스트 (그룹 2개 이상일 때만) ──
  var listSec='';
  if(N>1){
   var rows=group.map(function(g,i){var p=g.p;var top=(i===0);
    return '<button type="button" class="rg-prow'+(i===focusIdx?' sel':'')+'" data-i="'+i+'">'
     +'<div class="rg-pl">'+imgTag(p.img)+'</div>'
     +'<div><div class="rg-pn"><b>'+p.name+'</b>'+(top?'<span class="rg-tag mx rg-only-pc">최대</span>':'')+'<span class="rg-tag se" data-sel hidden><span class="rg-only-pc">선택됨</span><span class="rg-only-mo">선택</span></span></div><div class="rg-pi">'+(p.issuer||'')+'</div></div>'
     +'<div class="rg-pcash"><div class="l rg-only-pc">최대 캐시백</div><div class="v">'+_wm(g.e.reward_won)+'</div></div>'
     +'<svg class="rg-parr rg-only-pc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></button>';
   }).join('');
   listSec='<div class="rg-sec"><div class="rg-listhd"><h2>이 캐시백을 받는 카드</h2><span class="hint">상품을 누르면 아래 차트·구성이 바뀌어요</span></div><div class="rg-plist" id="rgList">'+rows+'</div></div>';
  }
  root.innerHTML=head+listSec+'<div id="rgDyn"></div>';
  function buildSeries(p,e){var nk=_nk(p.name);var total=e.reward_won||0,bonus=e.bonus_won||0;if(bonus>=total)bonus=0;var main=Math.max(total-bonus,0);
   var series=months.map(function(m,i){if(m===_cm)return {m:m,v:total,sub:bonus,cur:true};
    var snap=MS[i],v=null;if(snap){var c=(snap.cards||[]).filter(function(x){return _nk(x.name)===nk;})[0];if(c&&c.max)v=c.max;
     if(v==null&&snap.issuers&&p.issuer&&snap.issuers[p.issuer]){var im=snap.issuers[p.issuer];var vv=Object.keys(im).map(function(kk){return im[kk];});if(vv.length)v=Math.max.apply(null,vv);}}
    return {m:m,v:v};});
   return {series:series,total:total,main:main,sub:bonus};}
  function renderDyn(i){var g=group[i],p=g.p,e=g.e;var S=buildSeries(p,e);
   // 차트
   var vals=S.series.filter(function(s){return s.v!=null&&s.v>0;}).map(function(s){return s.v;});
   var peak=vals.length?Math.max.apply(null,vals):S.total;var scale=Math.max(peak*1.12,10000);
   var bars=S.series.map(function(s){
    if(s.cur){var hp=Math.max(s.v/scale*100,4);var subH=s.v?(s.sub/s.v*100):0;
     return '<div class="rg-col"><div class="lbl" style="color:var(--accent-magenta)">'+_man(s.v)+'만</div><div class="rg-curbar" style="height:'+hp+'%">'+(s.sub>0?'<div class="sub" style="height:'+subH+'%"></div>':'')+'<div class="main"></div></div><div class="mm" style="color:var(--accent-magenta);font-weight:700">이번달('+_mlabel(s.m)+')</div></div>';}
    if(s.v==null||s.v<=0)return '<div class="rg-col"><div class="lbl" style="opacity:.4">—</div><div class="rg-bar miss" style="height:24px"></div><div class="mm">'+_mlabel(s.m)+'</div></div>';
    var hp2=Math.max(s.v/scale*100,4);
    return '<div class="rg-col"><div class="lbl">'+_man(s.v)+'만</div><div class="rg-bar" style="height:'+hp2+'%"></div><div class="mm">'+_mlabel(s.m)+'</div></div>';
   }).join('');
   var emptyNote=(S.total>0)?'':'<div class="rg-note-c"><span>이번 달 집계된 캐시백이 아직 없어요</span></div>';
   var chart='<div class="rg-chart"><div class="rg-chart-h"><div><div class="rg-ceb rg-only-pc">티라노차트 · 캐시백 추이</div><h2 class="rg-ct">'+p.name+' · 최근 4개월</h2></div>'
    +'<div class="rg-sums rg-only-pc"><div><div class="l">당월 전체</div><div class="v">'+(S.total?_wm(S.total):'—')+'</div></div><div><div class="l">주요</div><div class="v" style="color:var(--block-navy)">'+(S.main?_wm(S.main):'—')+'</div></div><div><div class="l">부가</div><div class="v" style="color:rgba(31,29,61,.55)">'+(S.sub?_wm(S.sub):'—')+'</div></div></div></div>'
    +'<div class="rg-bars'+(S.total>0?'':' empty')+'">'+bars+emptyNote+'</div>'
    +'<div class="rg-legend"><span class="lg"><i class="rg-lg-mag"></i><span class="rg-only-pc">이번달 · 주요 캐시백</span><span class="rg-only-mo">주요</span></span><span class="lg"><i class="rg-lg-sub"></i><span class="rg-only-pc">이번달 · 부가 캐시백</span><span class="rg-only-mo">부가</span></span><span class="lg"><i class="rg-lg-navy"></i><span class="rg-only-pc">직전 3개월 합계</span><span class="rg-only-mo">직전 합계</span></span></div></div>';
   // 구성 (cards.json main_tier·sub_tiers)
   var cd=CARDMAP[_nk(p.name)]||{};var mt=cd.main_tier,st=(cd.sub_tiers||[]);
   var mainReward=(mt&&mt.reward)?mt.reward:S.main;
   var subItems='';
   if(st.length){subItems=st.map(function(s){return '<div class="rg-sub" title="'+_esc(s.text)+'"><span class="ic" style="background:'+(CATBG[s.cat]||'var(--surface-soft)')+'">'+catIcon(s.cat)+'</span><div><div class="t">'+(s.cat||'부가')+'</div><div class="c">'+(CATCOND[s.cat]||'조건 충족 시')+'</div></div><span class="v">+'+_wm(s.reward)+'</span></div>';}).join('');}
   else if(S.sub>0){subItems='<div class="rg-sub"><span class="ic" style="background:var(--surface-soft)">'+catIcon('')+'</span><div><div class="t">부가 캐시백</div><div class="c">조건 충족 시</div></div><span class="v">+'+_wm(S.sub)+'</span></div>';}
   var comp='<div class="rg-comp"><div class="rg-comp-eb rg-only-pc">캐시백 구성</div><h2 class="rg-comp-t">전체 캐시백 구성</h2><p class="rg-comp-p"><b>'+p.name+'</b> 기준<span class="rg-only-pc"> · 주요(조건 금액 이상 이용 시) + 부가(조건별)</span></p>'
    +'<div class="rg-main"><div class="l">주요 캐시백</div><div class="row"><span class="t">조건 금액 이상 이용 시</span><span class="v">'+(mainReward?_wm(mainReward):'—')+'</span></div></div>'
    +(subItems?('<div class="rg-subh">부가 캐시백<span class="rg-only-pc"> · 조건 카테고리별</span></div><div class="rg-subs">'+subItems+'</div>'):'<div class="rg-subh">부가 캐시백</div><div class="rg-subnone">이 상품은 부가 캐시백 없이 주요 캐시백으로 구성돼요.</div>')+'</div>';
   // 티라노 코칭
   // 같은 카드 상품의 플랫폼 간 비교(주요혜택 main_won · 전체혜택 reward_won)
   function _mainOf(x){var t=x.reward_won||0,b=x.bonus_won||0;if(x.main_won!=null)return Math.min(x.main_won,t);if(b>=t)b=0;return Math.max(t-b,0);}
   var myMain=_mainOf(e),myTotal=S.total;
   var oMainMax=0,oTotalMax=0,oMainPlat='';
   (p.events||[]).forEach(function(x){if(x.platform===P||x.platform==='issuer')return;var xm=_mainOf(x),xt=x.reward_won||0;if(xm>oMainMax){oMainMax=xm;oMainPlat=x.platform;}if(xt>oTotalMax)oTotalMax=xt;});
   // O: 주요혜택이 다른 플랫폼보다 높거나 같음 / △: 전체는 높은데 주요가 더 높은 플랫폼 존재 / X: 전체·주요 모두 열위
   var baseRec=(myMain>=oMainMax)?'rec':(myTotal>=oTotalMax?'hold':'no');
   // 예외: 같은 카드사 내 주요혜택 5만원+ 더 큰 다른 카드가 있으면 보류 + 안내
   var _cnk=_nk(p.name),sibBest=null,sibMain=0;
   PE.forEach(function(q){if((q.issuer||'')!==(p.issuer||'')||_nk(q.name)===_cnk)return;var ee=evOf(q);if(!ee)return;var qm=_mainOf(ee);if(qm>sibMain){sibMain=qm;sibBest=q;}});
   var sibTriggered=!!(sibBest&&(sibMain-myMain)>=50000&&baseRec==='rec');
   var rec=sibTriggered?'hold':baseRec;
   var recLab=rec==='rec'?'추천':(rec==='hold'?'보류':'비추천');var recCls=rec==='rec'?'':(rec==='hold'?'hold':'no');
   var isPeak=vals.length?(S.total>=Math.max.apply(null,vals)):true;
   var recMsg;
   if(rec==='rec'){recMsg='지금 '+pnm+'에서 발급하기 좋아요. 주요 캐시백 '+_wm(myMain)+'으로 다른 플랫폼과 같거나 더 높아요'+(isPeak?' · 최근 4개월 중 가장 커요.':'.');}
   else if(rec==='hold'){if(sibTriggered){recMsg='같은 '+(p.issuer||'카드사')+'의 <b>'+sibBest.name+'</b>이(가) 주요 캐시백 '+_wm(sibMain)+'으로 '+_wm(sibMain-myMain)+' 더 커요. '+p.name+'과(와) 함께 비교해 보세요.';}else{recMsg='전체 캐시백은 '+pnm+'이(가) 가장 크지만, 주요 캐시백은 '+(PNM[oMainPlat]||oMainPlat||'다른 플랫폼')+'이(가) '+_wm(Math.max(oMainMax-myMain,0))+' 더 커요. 조건을 비교해 보세요.';}}
   else{recMsg='주요·전체 캐시백 모두 다른 채널이 더 커요. 비교 후 결정하세요.';}
   var coach='<div class="rg-coach"><div class="rg-coach-badge"><span class="rg-coach-ring '+recCls+'"><span></span></span><div class="lab rg-only-pc" style="color:'+(rec==='rec'?'var(--success)':(rec==='hold'?'#cf9220':'rgba(0,0,0,.55)'))+'">'+recLab+'</div><div class="mono rg-only-pc">티라노 코칭</div></div>'
    +'<div><div class="rg-coach-head rg-only-pc">'+TYR+'<span class="eb">티라노 코칭</span></div><div class="rg-coach-molab rg-only-mo '+recCls+'">'+recLab+' · 티라노 코칭</div><div class="rg-coach-t">'+recMsg+'</div>'
    +'<div class="rg-coach-leg rg-only-pc"><span><span class="dot o"></span>추천 — 지금 발급</span><span><svg class="dot" viewBox="0 0 24 24" style="color:rgba(0,0,0,.6)"><path d="M12 5l8 14H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>보류 — 추이 지켜보기</span><span><svg class="dot" viewBox="0 0 24 24" style="color:rgba(0,0,0,.6)"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>비추천 — 다음 달 권장</span></div></div></div>';
   // 이런 이벤트도 있어요 (PC만 — 모바일 시안에 없음)
   var nk=_nk(p.name);var orows=[];
   var op=null,opw=0;(p.events||[]).forEach(function(x){if(x.platform!==P&&(x.reward_won||0)>opw){opw=x.reward_won;op=x;}});
   if(op&&opw>S.total)orows.push({tag:'다른 플랫폼 · 더 큼',tagBg:'var(--block-lime)',tagFg:'#000',name:p.name,issuer:p.issuer,plat:op.platform,amt:opw,img:p.img,href:'events.html?platform='+op.platform+'&n='+encodeURIComponent(p.name)});
   var si=PE.filter(function(q){return q.issuer===p.issuer&&_nk(q.name)!==nk;}).map(function(q){var ee=evOf(q);return ee?{q:q,w:ee.reward_won}:null;}).filter(Boolean).sort(function(a,b){return b.w-a.w;})[0];
   if(si)orows.push({tag:'같은 카드사 · '+pnm,tagBg:'var(--surface-soft)',tagFg:'rgba(0,0,0,.7)',name:si.q.name,issuer:si.q.issuer,plat:P,amt:si.w,img:si.q.img,href:'events.html?platform='+P+'&n='+encodeURIComponent(si.q.name)});
   var pmax=platGroup[0];if(pmax&&pmax.e.reward_won>S.total&&_nk(pmax.p.name)!==nk)orows.push({tag:'이번달 최대 혜택',tagBg:'#000',tagFg:'#fff',name:pmax.p.name,issuer:pmax.p.issuer,plat:P,amt:pmax.e.reward_won,img:pmax.p.img,href:'events.html?platform='+P+'&n='+encodeURIComponent(pmax.p.name)});
   var others=orows.length?('<div class="rg-others-sec rg-only-pc"><h2>이런 이벤트도 있어요</h2><div class="rg-others">'+orows.map(function(o){var oc=PBC[o.plat]||'#888';return '<a class="rg-orow" href="'+o.href+'"><div class="rg-pl">'+imgTag(o.img)+'</div><div><span class="rg-otag" style="background:'+o.tagBg+';color:'+o.tagFg+'">'+o.tag+'</span><div class="rg-pn"><b style="font-size:15px">'+o.name+'</b></div><div class="rg-pi"><i style="display:inline-block;width:6px;height:6px;border-radius:50%;background:'+oc+';margin-right:5px"></i>'+(o.issuer||'')+' · '+(PNM[o.plat]||o.plat)+'</div></div><div class="rg-pcash"><div class="l">캐시백</div><div class="v">'+_wm(o.amt)+'</div></div><svg class="rg-parr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a>';}).join('')+'</div></div>'):'';
   var foot='<p class="rg-foot"><span class="rg-only-pc">· 표기된 캐시백·조건·효율은 공개 데이터 수집 시점 기준이며 실제 적용 금액·조건은 달라질 수 있어요. </span>· <b>상세한 캐시백 정보는 각 플랫폼사에서 최종 확인하세요.</b> 카드티라노는 발급을 중개·접수하지 않는 광고·정보제공 매체입니다.</p>';
   document.getElementById('rgDyn').innerHTML=chart+comp+coach+others+foot;
   var _ppd=(p.platforms||{})[P]||{};var edUrl=_best(P,e.url||_ppd.url,_ppd.id);if(P==='cardgorilla'){var _cg=_cgUrl(p.issuer,_ppd.id);if(_cg)edUrl=_cg;}if(!edUrl)edUrl=e.url||'#';
   var hc=document.getElementById('rgHeadCta');if(hc)hc.setAttribute('href',edUrl);
   document.getElementById('rgFloat').innerHTML='<div class="rg-float"><div class="in"><div class="lab rg-only-pc"><b>'+pnm+'</b> 발급 캐시백 · 최대 '+_wm(S.total)+'</div><a class="go" href="'+edUrl+'" target="_blank" rel="sponsored nofollow noopener">'+pnm+'에서 자세히보기 '+UR+'</a></div></div>';
   ctSeo(p.name+' '+pnm+' 발급 캐시백 | 카드티라노',p.name+'의 '+pnm+' 신규 발급 캐시백 금액·조건·마감과 최근 캐시백 추이를 확인하세요.','events.html?platform='+P+'&n='+encodeURIComponent(p.name));
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
 '.ch-wrap{max-width:880px;margin:0 auto}'
 '.ch-top{padding:20px 0 0}.ch-h1{font-weight:340;font-size:32px;letter-spacing:-.8px;line-height:1.05;margin:6px 0 0}.ch-sub{font-weight:400;font-size:13px;color:rgba(0,0,0,.6);margin:5px 0 0}'
 # 히어로 롤링 캐러셀
 '.ch-hero{margin-top:16px}.ch-vp{overflow:hidden;border-radius:20px}'
 '.ch-track{display:flex;width:200%;transition:transform .6s cubic-bezier(.4,0,.2,1)}'
 '.ch-slide{width:50%;flex-shrink:0;position:relative;overflow:hidden;padding:20px 18px}'
 '.ch-s1{background:var(--block-lime)}.ch-s2{background:var(--block-lilac);min-height:198px}'
 '.ch-face{position:absolute;opacity:.12;color:#000;pointer-events:none}'
 '.ch-eb{font-family:var(--font-mono,monospace);font-size:10px;letter-spacing:.5px;text-transform:uppercase;color:rgba(0,0,0,.6)}'
 '.ch-idxrow{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-top:8px}.ch-idx{font-weight:330;font-size:34px;letter-spacing:-1.2px;white-space:nowrap}'
 '.ch-up{display:inline-flex;align-items:center;gap:2px;font-weight:700;font-size:12px}.ch-up svg{width:12px;height:12px}'
 '.ch-s1 .cap{font-weight:400;font-size:12px;color:rgba(0,0,0,.65);margin-top:3px}'
 '.ch-spark{display:flex;align-items:flex-end;gap:7px;height:62px;margin-top:14px}.ch-spark .col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}.ch-spark .b{width:64%;max-width:22px;border-radius:4px 4px 0 0;min-height:2px}'
 '.ch-s2 h2{font-weight:330;font-size:24px;letter-spacing:-.8px;margin:8px 0 0}.ch-s2 .amt{font-weight:700;font-size:21px;letter-spacing:-.5px;margin-top:5px}'
 '.ch-s2 .who{font-weight:400;font-size:12px;color:rgba(0,0,0,.7);margin:7px 0 0}.ch-s2 .who b{font-weight:700}'
 '.ch-s2 .cta{display:inline-flex;align-items:center;gap:6px;padding:10px 15px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:13px;margin-top:13px;cursor:pointer;border:0;font-family:inherit}.ch-s2 .cta svg{width:14px;height:14px}'
 '.ch-plate{position:absolute;right:-14px;bottom:14px;width:108px;transform:rotate(-9deg);border-radius:9px;overflow:hidden;box-shadow:0 12px 24px rgba(0,0,0,.2);aspect-ratio:1.586/1;background:var(--block-cream)}.ch-plate img{width:100%;height:100%;object-fit:cover;display:block}'
 '.ch-dots{display:flex;justify-content:center;gap:7px;margin-top:12px}.ch-dot{height:7px;width:7px;border-radius:50px;cursor:pointer;transition:all .3s;background:rgba(0,0,0,.22);border:0;padding:0}.ch-dot.on{width:22px;background:#000}'
 # 카드 패널
 '.ch-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 18px;margin-top:18px}'
 '.ch-cardh{display:flex;align-items:flex-end;justify-content:space-between;gap:10px}.ch-ct{font-weight:330;font-size:23px;letter-spacing:-.7px;margin:5px 0 0}'
 # 추이
 '.ch-bars{display:flex;align-items:flex-end;gap:10px;height:150px;margin-top:22px}.ch-bars .col{flex:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:7px}'
 '.ch-bars .v{font-weight:700;font-size:12px;white-space:nowrap}.ch-bars .bar{width:62%;max-width:34px;border-radius:6px 6px 0 0;min-height:2px}.ch-bars .bar.empty{background:transparent;border:1.5px dashed var(--hairline);min-height:18px}'
 '.ch-bars .ml{font-family:var(--font-mono,monospace);font-size:9px;color:rgba(0,0,0,.5)}'
 '.ch-sum{display:flex;gap:8px;margin-top:18px}.ch-sum .box{flex:1;background:var(--surface-soft);border-radius:13px;padding:13px 14px}.ch-sum .l{font-family:var(--font-mono,monospace);font-size:8px;color:rgba(0,0,0,.45)}.ch-sum .bb{font-weight:700;font-size:17px;margin-top:3px}'
 # 플랫폼 드롭다운
 '.ch-dd{position:relative}.ch-ddbtn{display:inline-flex;align-items:center;gap:5px;padding:7px 13px;border-radius:50px;background:var(--surface-soft);font-weight:540;font-size:12px;cursor:pointer;border:0;font-family:inherit}.ch-ddbtn svg{width:12px;height:12px}'
 '.ch-ddmenu{position:absolute;right:0;top:calc(100% + 6px);background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.1);padding:6px;z-index:9;min-width:148px;display:none}.ch-ddmenu.open{display:block}'
 '.ch-ddmenu button{display:flex;align-items:center;gap:8px;width:100%;text-align:left;padding:9px 11px;border-radius:8px;background:0;border:0;font-family:inherit;font-size:13px;font-weight:540;cursor:pointer;color:#000}.ch-ddmenu button:hover{background:var(--surface-soft)}.ch-ddmenu button.on{font-weight:700}.ch-ddmenu button .dot{width:8px;height:8px;border-radius:50%;flex:0 0 auto}'
 # 랭킹
 '.ch-chips{display:flex;gap:7px;white-space:nowrap}.ch-chip{padding:7px 14px;border-radius:50px;background:var(--surface-soft);font-weight:540;font-size:12.5px;color:rgba(0,0,0,.65);cursor:pointer;border:0;font-family:inherit}.ch-chip.on{background:#000;color:#fff}'
 '.ch-rows{display:flex;flex-direction:column;margin-top:12px}'
 '.ch-rrow{display:flex;align-items:center;gap:12px;padding:13px 4px;border-top:1px solid var(--hairline-soft);text-decoration:none;color:#000;min-height:44px}.ch-rrow:first-child{border-top:0}'
 '.ch-rk{width:24px;flex:0 0 auto;text-align:center;font-weight:700;font-size:17px}'
 '.ch-rmid{flex:1;min-width:0}.ch-rname{font-weight:700;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.ch-rmeta{font-weight:400;font-size:11.5px;color:rgba(0,0,0,.5);margin-top:3px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}'
 '.ch-iss{font-family:var(--font-mono,monospace);font-size:9px;color:rgba(0,0,0,.45);text-transform:uppercase}'
 '.ch-hchip{display:inline-flex;align-items:center;gap:4px;cursor:pointer}.ch-hchip svg{width:10px;height:10px;color:#000}.ch-hchip .dot{width:6px;height:6px;border-radius:50%}.ch-hchip .pn{font-weight:540;font-size:10.5px;color:#000}'
 '.ch-rright{text-align:right;flex:0 0 auto}.ch-rrl{font-family:var(--font-mono,monospace);font-size:8px;color:rgba(0,0,0,.42)}.ch-rrv{font-weight:700;font-size:16px;letter-spacing:-.4px;white-space:nowrap}.ch-rd{font-family:var(--font-mono,monospace);font-size:8px;white-space:nowrap;margin-top:1px}'
 # PC 보정
 '@media(min-width:761px){'
 '.ch-h1{font-size:34px}'
 '.ch-slide{padding:32px 34px;display:flex;align-items:center;gap:24px}.ch-s2{min-height:0}'
 '.ch-s1 .left{flex:1}.ch-idx{font-size:46px}'
 '.ch-spark{height:96px;width:240px;margin-top:0;flex:0 0 auto}.ch-spark .b{max-width:30px}'
 '.ch-s2 .body{flex:1}.ch-s2 h2{font-size:32px}.ch-s2 .amt{font-size:24px}'
 '.ch-plate{position:static;width:170px;flex:0 0 auto}'
 '.ch-ct{font-size:26px}'
 '.ch-bars{height:200px;gap:16px}.ch-bars .bar{max-width:56px;width:56%}.ch-bars .v{font-size:15px}.ch-bars .ml{font-size:11px}'
 '.ch-rname{font-size:16px}'
 '}'
 '</style>'
 '<div class="wrap"><div class="ch-wrap">'
 '<div class="ch-top"><span class="pg-eb">CASHBACK DATA</span><h1 class="ch-h1">티라노 차트</h1><p class="ch-sub">캐시백이 어떻게 움직이는지, 데이터로.</p></div>'
 '<div class="ch-hero"><div class="ch-vp"><div class="ch-track" id="chTrack">'
 '<div class="ch-slide ch-s1"><svg class="ch-face" viewBox="2 3.6 20 16.4" style="right:-12px;top:-16px;width:84px"><use href="#mk"/></svg>'
 '<div class="left"><div class="ch-eb">이번 달 캐시백 지수</div><div class="ch-idxrow"><div class="ch-idx" id="chIdx">–</div><span class="ch-up" id="chDelta"></span></div><div class="cap">전 플랫폼 통합 최고 캐시백 · 전월 대비</div></div>'
 '<div class="ch-spark" id="chSpark"></div></div>'
 '<div class="ch-slide ch-s2"><svg class="ch-face" viewBox="2 3.6 20 16.4" style="left:-12px;bottom:-18px;width:90px"><use href="#mk"/></svg>'
 '<div class="body"><div class="ch-eb">이번 달 캐시백 1위</div><h2 id="chTopName">–</h2><div class="amt" id="chTopAmt"></div><p class="who" id="chTopWho"></p>'
 '<button class="cta" id="chTopCta">차트 보기 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></button></div>'
 '<div class="ch-plate" id="chTopPlate"></div></div>'
 '</div></div>'
 '<div class="ch-dots"><button class="ch-dot on" id="chDot0"></button><button class="ch-dot" id="chDot1"></button></div></div>'
 '<div class="ch-card"><div class="ch-cardh"><div><div class="ch-eb" style="font-size:10px">최근 6개월</div><h2 class="ch-ct">통합 캐시백 추이</h2></div>'
 '<div class="ch-dd"><button class="ch-ddbtn" id="chPfBtn">전체 플랫폼 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></button><div class="ch-ddmenu" id="chPfMenu"></div></div></div>'
 '<div class="ch-bars" id="chTrend"></div>'
 '<div class="ch-sum"><div class="box"><div class="l">6개월 최고</div><div class="bb" id="chHi">–</div></div><div class="box"><div class="l">평균</div><div class="bb" id="chAvg">–</div></div></div></div>'
 '<div class="ch-card"><div class="ch-cardh" style="align-items:center"><h2 class="ch-ct" style="margin:0">티라노 랭킹</h2>'
 '<div class="ch-chips"><button class="ch-chip on" id="chChipPop">인기 차트</button><button class="ch-chip" id="chChipCash">캐시백 차트</button></div></div>'
 '<div class="ch-rows" id="chRank"><div class="empty"><span class="tload"><svg class="tmk" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>불러오는 중</span></div></div></div>'
 '</div></div>')
CHART_JS=r"""
var PKO={toss:'토스',cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};
var PCO={toss:'#3182F6',cardgorilla:'#FF6A13',banksalad:'#19C37D',ajungdang:'#1B64DA',naver:'#03C75A',kakaopay:'#FEE500'};
var PORDK=['toss','naver','kakaopay','ajungdang','cardgorilla','banksalad'];
var MD=[],NAME2={},CUR=null,PREV=null,platFilter='all',chMode='pop',POP=[],CASH=[],slide=0,slideIv=null;
function _nk(s){return (s||'').replace(/[\s()（）·\-_/+]+/g,'').toLowerCase();}
function wman(v){if(v==null||v===0)return '0';var m=v/10000;return (m>=10?Math.round(m):Math.round(m*10)/10)+'만원';}
function wmm(v){return wman(v).replace('만원','만');}
function mlabel(ym){var p=(ym||'').split('-');return p.length>1?parseInt(p[1],10)+'월':ym;}
function idImg(name){return NAME2[_nk(name)]||NAME2[_nk((name||'').replace(/^토스\s*/,''))]||{};}
function chx(n){n=(n||'').toLowerCase();return n.indexOf('토스')>=0||n.indexOf('toss')>=0;}
function platsOf(c){return Object.keys(c.platforms||{}).filter(function(k){return c.platforms[k]!=null;});}
function bestPlat(c){var bk=null,bv=-1;PORDK.forEach(function(k){var v=(c.platforms||{})[k];if(v!=null&&v>bv){bv=v;bk=k;}});return {key:bk,val:bv};}
function monthMax(md,f){var mx=0;((md||{}).cards||[]).forEach(function(c){var v=f==='all'?c.max:(c.platforms||{})[f];if(v!=null&&v>mx)mx=v;});return mx;}
function avgList(md){var cs=((md||{}).cards||[]).filter(function(c){return platsOf(c).length>=2&&!chx(c.name);});var rk={};
 PORDK.forEach(function(k){var arr=cs.filter(function(c){return (c.platforms||{})[k]!=null;}).sort(function(a,b){return b.platforms[k]-a.platforms[k];});arr.forEach(function(c,i){(rk[c.name]=rk[c.name]||[]).push(i+1);});});
 return cs.map(function(c){var rs=rk[c.name]||[];var a=rs.reduce(function(s,x){return s+x;},0)/(rs.length||1);return {name:c.name,issuer:c.issuer,avg:a,n:rs.length};}).sort(function(a,b){return a.avg-b.avg;});}
function posMap(list){var m={};list.forEach(function(x,i){m[x.name]=i+1;});return m;}
function deltaHtml(prev,cur){var t,c;if(prev==null){t='NEW';c='var(--success)';}else{var d=prev-cur;if(d>0){t='▲ '+d;c='var(--success)';}else if(d<0){t='▼ '+(-d);c='var(--accent-magenta)';}else{t='— 0';c='rgba(0,0,0,.4)';}}return '<div class="ch-rd" style="color:'+c+'">'+t+'</div>';}
function rkColor(i){return i===0?'var(--accent-magenta)':(i<3?'#000':'rgba(0,0,0,.35)');}
function renderHero(){
 var cm=monthMax(CUR,'all'),pm=PREV?monthMax(PREV,'all'):0;
 document.getElementById('chIdx').textContent=wman(cm);
 var de=document.getElementById('chDelta');
 if(pm>0){var pct=Math.round((cm-pm)/pm*100);var up=pct>=0;de.style.color=up?'var(--success)':'var(--accent-magenta)';
  de.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="transform:'+(up?'none':'rotate(180deg)')+'"><path d="M5 15l7-7 7 7"/></svg>'+Math.abs(pct)+'%';}else de.textContent='';
 var sv=MD.map(function(md){return monthMax(md,'all');});var smax=Math.max.apply(null,sv)||1;
 document.getElementById('chSpark').innerHTML=sv.map(function(v,i){var last=i===sv.length-1;return '<div class="col"><div class="b" style="height:'+(v/smax*100)+'%;background:'+(last?'#000':'rgba(0,0,0,.28)')+'"></div></div>';}).join('');
 var t=CASH[0];if(t){document.getElementById('chTopName').textContent=t.name;document.getElementById('chTopAmt').textContent='최대 '+t.cash;
  document.getElementById('chTopWho').innerHTML='<b>'+t.issuer+'</b> · '+t.platform+'에서 최고';
  var pl=document.getElementById('chTopPlate');pl.innerHTML=t.img?imgTag(t.img):'';
  document.getElementById('chTopCta').onclick=function(){if(t.id!=null)location.href='carddetail.html?id='+t.id;else document.getElementById('chRank').scrollIntoView({behavior:'smooth'});};}
}
function setSlide(i,manual){slide=i;document.getElementById('chTrack').style.transform='translateX(-'+(i*50)+'%)';
 document.getElementById('chDot0').className='ch-dot'+(i===0?' on':'');document.getElementById('chDot1').className='ch-dot'+(i===1?' on':'');
 if(manual&&slideIv){clearInterval(slideIv);slideIv=null;}}
function renderTrend(){
 var vals=MD.map(function(md){return {m:mlabel(md.month),v:monthMax(md,platFilter)};});
 var mx=Math.max.apply(null,vals.map(function(x){return x.v;}))||1;
 document.getElementById('chTrend').innerHTML=vals.map(function(x,i){var last=i===vals.length-1;var empty=!x.v;
  return '<div class="col"><div class="v" style="color:'+(last?'var(--accent-magenta)':'#000')+'">'+(empty?'–':wmm(x.v))+'</div>'
   +(empty?'<div class="bar empty"></div>':'<div class="bar" style="height:'+(x.v/mx*100)+'%;background:'+(last?'var(--accent-magenta)':'var(--block-navy)')+'"></div>')
   +'<div class="ml">'+x.m+'</div></div>';}).join('');
 var nz=vals.map(function(x){return x.v;}).filter(function(v){return v;});
 document.getElementById('chHi').textContent=nz.length?wman(Math.max.apply(null,nz)):'–';
 document.getElementById('chAvg').textContent=nz.length?wman(Math.round(nz.reduce(function(s,v){return s+v;},0)/nz.length)):'–';
}
function renderPfMenu(){
 var opts=[['all','전체 플랫폼','#000']].concat(PORDK.map(function(k){return [k,PKO[k],PCO[k]];}));
 document.getElementById('chPfMenu').innerHTML=opts.map(function(o){return '<button data-f="'+o[0]+'" class="'+(platFilter===o[0]?'on':'')+'"><span class="dot" style="background:'+o[2]+'"></span>'+o[1]+'</button>';}).join('');
}
function renderRank(){
 var box=document.getElementById('chRank');
 if(chMode==='pop'){
  box.innerHTML=POP.length?POP.map(function(r,i){return '<a class="ch-rrow" href="'+(r.id!=null?'carddetail.html?id='+r.id:'cards.html')+'"><span class="ch-rk" style="color:'+rkColor(i)+'">'+(i+1)+'</span>'
   +'<div class="ch-rmid"><div class="ch-rname">'+r.name+'</div><div class="ch-rmeta">'+r.issuer+' · '+r.n+'개 플랫폼 평균</div></div>'
   +'<div class="ch-rright"><div class="ch-rrl">평균 순위</div><div class="ch-rrv">'+r.avg+'</div>'+r.deltaHtml+'</div></a>';}).join(''):'<div class="empty" style="padding:24px 0">데이터가 없어요.</div>';
 }else{
  box.innerHTML=CASH.length?CASH.map(function(r,i){return '<a class="ch-rrow" href="'+(r.id!=null?'carddetail.html?id='+r.id:'cards.html')+'"><span class="ch-rk" style="color:'+rkColor(i)+'">'+(i+1)+'</span>'
   +'<div class="ch-rmid"><div class="ch-rname">'+r.name+'</div><div class="ch-rmeta"><span class="ch-iss">'+r.issuer+'</span>'
   +'<span class="ch-hchip" data-ev="events.html?platform='+r.pkey+'&n='+encodeURIComponent(r.name)+'"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg><span class="dot" style="background:'+r.pColor+'"></span><span class="pn">'+r.platform+'</span></span></div></div>'
   +'<div class="ch-rright"><div class="ch-rrl">최고 캐시백</div><div class="ch-rrv">'+r.cash+'</div>'+r.deltaHtml+'</div></a>';}).join(''):'<div class="empty" style="padding:24px 0">데이터가 없어요.</div>';
 }
}
function initUI(){
 document.getElementById('chDot0').onclick=function(){setSlide(0,true);};
 document.getElementById('chDot1').onclick=function(){setSlide(1,true);};
 var cp=document.getElementById('chChipPop'),cc=document.getElementById('chChipCash');
 cp.onclick=function(){chMode='pop';cp.className='ch-chip on';cc.className='ch-chip';renderRank();};
 cc.onclick=function(){chMode='cash';cc.className='ch-chip on';cp.className='ch-chip';renderRank();};
 var btn=document.getElementById('chPfBtn'),menu=document.getElementById('chPfMenu');
 btn.onclick=function(e){e.stopPropagation();menu.classList.toggle('open');};
 menu.onclick=function(e){var b=e.target.closest('button[data-f]');if(!b)return;platFilter=b.getAttribute('data-f');btn.firstChild.textContent=(platFilter==='all'?'전체 플랫폼':PKO[platFilter])+' ';renderTrend();renderPfMenu();menu.classList.remove('open');};
 document.addEventListener('click',function(){menu.classList.remove('open');});
 document.getElementById('chRank').addEventListener('click',function(e){var h=e.target.closest('.ch-hchip');if(h&&h.dataset.ev){e.preventDefault();e.stopPropagation();location.href=h.dataset.ev;}});
 var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 if(!reduce)slideIv=setInterval(function(){setSlide((slide+1)%2);},4200);
}
Promise.all([fetch('cards.json').then(function(r){return r.json();}),fetch('platform_events.json').then(function(r){return r.json();}).catch(function(){return {products:[]};})]).then(function(A){
 var cj=A[0],PEIMG={};((A[1].products)||[]).forEach(function(p){if(p.img&&!PEIMG[_nk(p.name)])PEIMG[_nk(p.name)]=p.img;});
 for(var k in cj.cards){(cj.cards[k]||[]).forEach(function(c){NAME2[_nk(c.name)]={id:c.id,img:c.img||PEIMG[_nk(c.name)]||''};});}
 var months=['2026-01','2026-02','2026-03','2026-04','2026-05','2026-06'];
 return fetch('history/index.json').then(function(r){return r.json();}).then(function(idx){if(idx&&idx.months&&idx.months.length)months=idx.months.slice(-6);return months;}).catch(function(){return months;});
}).then(function(months){
 return Promise.all(months.map(function(m){return fetch('history/'+m+'.json').then(function(r){return r.json();}).catch(function(){return {month:m,cards:[]};});}));
}).then(function(arr){
 MD=arr;CUR=MD[MD.length-1]||{cards:[]};PREV=MD.length>1?MD[MD.length-2]:null;
 var curMaxList=((CUR.cards)||[]).slice().sort(function(a,b){return (b.max||0)-(a.max||0);});
 var prevMaxPos=PREV?posMap(((PREV.cards)||[]).slice().sort(function(a,b){return (b.max||0)-(a.max||0);})):{};
 CASH=curMaxList.map(function(c,i){var bp=bestPlat(c);var im=idImg(c.name);return {name:c.name,issuer:c.issuer,cash:wman(c.max),pkey:bp.key,platform:PKO[bp.key]||bp.key,pColor:PCO[bp.key]||'#888',id:im.id,img:im.img,deltaHtml:deltaHtml(prevMaxPos[c.name],i+1)};});
 var curAvg=avgList(CUR);var prevAvgPos=PREV?posMap(avgList(PREV)):{};var curAvgPos=posMap(curAvg);
 POP=curAvg.map(function(x){var im=idImg(x.name);return {name:x.name,issuer:x.issuer,avg:(Math.round(x.avg*10)/10)+'위',n:x.n,id:im.id,deltaHtml:deltaHtml(prevAvgPos[x.name],curAvgPos[x.name])};});
 renderHero();renderTrend();renderPfMenu();renderRank();initUI();
});
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
 '<div class="pushbox" id="pushbox"><div class="pb-l"><div class="pb-t"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:5px"><path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10.5 20a2 2 0 0 0 3 0"/></svg>새 이벤트 알림</div>'
 '<div class="pb-d" id="pbDesc">관심 카드에 다음 달 새 캐시백 이벤트가 등록되면 알려드려요.</div></div>'
 '<label class="pb-sw"><input type="checkbox" id="pushTg"><span class="pb-track"><span class="pb-thumb"></span></span></label></div>'
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
 '<div class="dnote"><b>스크래핑 헬스</b>는 콜렉터 산출물(platform_events.json)을 실시간 분석해 플랫폼·카드사별 수집 상태를 보여줍니다.<br>아래 <b>방문 지표(시간/일/월별)</b>는 <b>이 브라우저</b> 로컬 집계예요. <b>전체 방문자</b>는 개인정보(IP) 미저장 <b>Cloudflare Web Analytics</b>(자동 연동됨)에서 집계됩니다.</div>'
 '<div class="dsec"><h3>Cloudflare 실측 방문 (전체 방문자)</h3>'
 '<div class="kpis"><div class="kpi"><div class="n" id="cfPV">225</div><div class="l">페이지뷰 · 최근 24h</div></div>'
 '<div class="kpi"><div class="n" id="cfVisit">100</div><div class="l">방문(Visits) · 최근 24h</div></div>'
 '<div class="kpi"><div class="n">자동</div><div class="l">수집 방식(Automatic)</div></div>'
 '<div class="kpi"><div class="n" id="cfAsOf">06/27</div><div class="l">스냅샷 기준일</div></div></div>'
 '<div style="margin-top:4px"><a href="https://dash.cloudflare.com/?to=/:account/web-analytics" target="_blank" rel="noopener" style="display:inline-block;background:#f6821f;color:#fff;font-weight:800;font-size:13px;padding:11px 17px;border-radius:10px;text-decoration:none">Cloudflare에서 실시간 방문자 보기 ↗</a></div>'
 '<div class="dnote" style="margin-top:10px">위 수치는 Cloudflare Web Analytics <b>스냅샷</b>입니다(IP 미저장). <b>시간/일/월별 실시간 추세·국가·인기 페이지</b>는 위 버튼의 Cloudflare 대시보드에서 기간 필터로 확인하세요. (페이지 내 자동 실시간 표시는 토큰 기반 프록시 연동 시 가능 — 원하면 설정해 드립니다.)</div></div>'
 '<div class="dsec"><h3>플랫폼별 스크래핑 상태</h3><div class="hgrid" id="hplat"></div><div id="hfresh" class="empty2"></div></div>'
 '<div class="dsec"><h3>카드사별 커버리지</h3><div id="hiss"></div></div>'
 '<div class="sec-h" style="margin-top:8px"><h2 style="font-size:18px">방문 지표 (이 브라우저)</h2></div>'
 '<div class="dbtns"><button id="rf">새로고침</button><button id="csv">CSV 내보내기</button><button id="rs">이 브라우저 초기화</button></div>'
 '<div class="kpis" id="kpis"></div><div id="secs"></div>'
 '<div class="dsec"><h3>최근 활동</h3><div id="log"></div></div></div>')
DASHBOARD_JS=r"""
// === 스크래핑 헬스 — 콜렉터 산출물(platform_events.json) 실시간 분석 ===
(function(){var PN={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이'};var PORD=['toss','naver','kakaopay','ajungdang','cardgorilla','banksalad'];var PC={cardgorilla:'#ff4d4f',banksalad:'#2f6bff',toss:'#3182f6',ajungdang:'#3b5bdb',naver:'#03c75a',kakaopay:'#e8b800'};
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
  ['월별 방문(페이지뷰)', tbars(tagg(ev,'month'))],
  ['일별 방문 (최근 14일)', tbars(tagg(ev,'day'))],
  ['시간대별 방문', tbars(tagg(ev,'hour'))],
  ['페이지별 조회', bars(agg(ev,'pageview',function(e){return PG(e.l||e.p);}))],
  ['메뉴 클릭', bars(agg(ev,'menu',function(e){return e.l;}))],
  ['카드 클릭(상품)', bars(agg(ev,'card',function(e){return e.l;}))],
  ['필터·카드사 탭', bars(agg(ev,'filter',function(e){return e.l;}))],
  ['업종 카테고리 클릭', bars(agg(ev,'category',function(e){return e.l;}))],
  ['플랫폼 상세 클릭', bars(agg(ev,'plat',function(e){return e.l;}))],
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
var TPORD=['toss','naver','kakaopay','ajungdang','cardgorilla','banksalad'];
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
    return ('<section class="seo-static">'+style+'<div class="wrap"><h2>카드 캐시백·카드 혜택·카드 발급 혜택, 한눈에 비교</h2>'
      +intro+'<div class="seo-tbl-wrap">'+table+'</div>'+rank+links+'</div></section>')
SEO_STATIC_INDEX=_seo_static_index()

# 데이터 바인딩 페이지(JS 렌더)에 서버 정적 SEO 텍스트 보강 — 색인 강도/핵심 검색어 반영
_SEO_BLK_STYLE=('<style>.seo-static{border-top:1px solid var(--line);background:var(--surface-soft);padding:30px 0 8px;margin-top:34px}'
 '.seo-static .wrap{max-width:880px}.seo-static h2{font-size:19px;font-weight:900;letter-spacing:-.5px;margin-bottom:10px}'
 '.seo-static p{font-size:13.5px;color:var(--sub);line-height:1.75;margin:0 0 12px}.seo-static p b{color:var(--text)}'
 '.seo-static h3{font-size:14px;font-weight:800;margin:18px 0 9px}'
 '.seo-static .seo-links ul{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}'
 '.seo-static .seo-links a{display:inline-block;font-size:13px;font-weight:700;color:var(--text);background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;text-decoration:none}'
 '.seo-static .seo-links a:hover{border-color:var(--accent)}</style>')
def _seo_block(h2,paras,links):
    ps="".join('<p>%s</p>'%p for p in paras)
    ls=('<nav class="seo-links" aria-label="관련 메뉴"><h3>관련 메뉴</h3><ul>'
      +"".join('<li><a href="%s">%s</a></li>'%(u,t) for u,t in links)+'</ul></nav>') if links else ''
    return ('<section class="seo-static">'+_SEO_BLK_STYLE+'<div class="wrap"><h2>'+h2+'</h2>'+ps+ls+'</div></section>')
SEO_STATIC_ISSUE=_seo_block(
 "이번 달 카드 캐시백·발급 혜택, 플랫폼별로 비교",
 ["<b>카드 캐시백</b>은 같은 카드라도 발급 채널(토스 카드라운지·카드고릴라·아정당·카카오페이·뱅크샐러드)에 따라 금액이 크게 달라집니다. 카드티라노는 매달 각 플랫폼의 <b>신규 발급 캐시백(카드 발급 혜택)</b>을 자동 집계해, 같은 카드를 <b>어디서 발급하면 가장 많이 받는지</b> 한 표로 비교해 드립니다.",
  "캐시백 금액은 전월실적·결제기간·마케팅 동의 등 조건 충족 시 받을 수 있는 <b>최대 금액 기준</b>이며, 직전 6개월 내 동일 카드사 발급 이력이 있으면 제외될 수 있습니다. 발급 전 각 플랫폼·카드사에서 최종 조건을 확인하세요."],
 [("issue.html?v=cmp","한눈에 비교 (카드사·카드별)"),("cards.html","카드 찾기"),("diagnose.html","카드 진단으로 내 카드 찾기"),("content.html","카드 발급 혜택 가이드"),("chart.html","카드 캐시백 랭킹")])
SEO_STATIC_CARDS=_seo_block(
 "카드사별 신용카드 혜택·연회비 한눈에 비교",
 ["삼성·현대·신한·KB국민·롯데·우리·하나·NH농협·BC·IBK 등 <b>카드사별 대표 신용카드의 카드 혜택</b>을 영역별 적립·할인, 연회비, 전월실적, 그리고 이번 달 <b>발급 캐시백</b>까지 한곳에서 비교할 수 있습니다.",
  "여행·쇼핑·교통·구독·생활요금 등 <b>소비 카테고리별로 카드 혜택</b>을 좁혀 보고, 카드별 <b>최고 궁합 플랫폼</b>과 최대 캐시백을 함께 확인하세요. 어떤 카드가 맞을지 모르겠다면 <b>카드 진단</b>으로 2지선다 추천을 받아볼 수 있습니다."],
 [("diagnose.html","카드 진단 (2지선다 추천)"),("issue.html","이번 달 카드 캐시백"),("discount.html","가맹점별 카드 할인 혜택"),("content.html","카드 가이드")])

# ===== ABOUT (카드티라노란?) =====
ABOUT_BODY=(r'''<style>
.ab{font-family:'Pretendard','Pretendard Variable',-apple-system,sans-serif}
.ab .eb{font-family:var(--font-mono,monospace);font-size:12px;letter-spacing:.7px;text-transform:uppercase}
.ab .sec{padding:0 0 84px}
.ab .block{border-radius:24px;position:relative;overflow:hidden}
.ab-hero{background:var(--block-lilac);padding:72px 64px}
.ab-hero h1{font-weight:340;font-size:64px;line-height:1.02;letter-spacing:-2.2px;margin:18px 0 0;max-width:760px}
.ab-hero p{font-weight:400;font-size:18px;line-height:1.5;margin:26px 0 0;max-width:560px;color:rgba(0,0,0,.72)}
.ab-wm{position:absolute;right:-40px;bottom:-56px;width:300px;opacity:.16;color:#000}
.ab-cta{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;background:#000;color:#fff;font-weight:540;font-size:15px;text-decoration:none}.ab-cta svg{width:17px;height:17px}
.ab-cta2{display:inline-flex;align-items:center;padding:14px 24px;border-radius:50px;background:rgba(255,255,255,.7);font-weight:540;font-size:15px;text-decoration:none;color:#000}
.ab-g2{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.ab-h2{font-weight:340;font-size:46px;line-height:1.04;letter-spacing:-1.5px;margin:14px 0 0}
.ab-card{border:1px solid var(--hairline);border-radius:20px;padding:30px 32px;background:#fff}
.ab-bar{flex:1;height:12px;border-radius:50px;background:var(--surface-soft);overflow:hidden}.ab-bar i{display:block;height:100%;border-radius:50px}
.ab-lime{background:var(--block-lime);padding:64px}
.ab-navy{background:var(--block-navy);color:#fff;padding:72px 64px}
.ab-navy h2{font-weight:340;font-size:50px;line-height:1.04;letter-spacing:-1.7px;margin:16px 0 0;max-width:780px}
.ab-navy p{font-weight:400;font-size:17px;line-height:1.55;margin:16px 0 0;max-width:620px;color:rgba(255,255,255,.78)}.ab-navy p b{color:#fff;font-weight:700}
.ab-stats{display:flex;gap:40px;margin-top:44px;flex-wrap:wrap}.ab-stats .v{font-weight:700;font-size:38px;letter-spacing:-1.2px}.ab-stats .l{font-weight:400;font-size:13.5px;color:rgba(255,255,255,.62);margin-top:4px}
.ab-eg{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
.ab-ec{border-radius:20px;padding:28px 26px;display:flex;gap:22px;overflow:hidden;position:relative}
.ab-ec .gl{flex-shrink:0;display:flex;align-items:center;justify-content:center}.ab-ec .gl svg{width:100%;height:auto;color:#000}
.ab-ec .role{font-family:var(--font-mono,monospace);font-size:10px;color:rgba(0,0,0,.5)}
.ab-ec .nm{font-weight:700;font-size:22px;letter-spacing:-.5px;margin-top:6px}
.ab-ec .tag{font-weight:540;font-size:14px;margin-top:10px;color:rgba(0,0,0,.85)}
.ab-ec .ds{font-weight:400;font-size:13.5px;line-height:1.5;margin-top:6px;color:rgba(0,0,0,.62)}
.ab-cream{background:var(--block-cream);border-radius:24px;padding:80px 64px;text-align:center}
.ab-cream h2{font-weight:340;font-size:52px;line-height:1.08;letter-spacing:-1.8px;margin:18px auto 0;max-width:820px}
.ab-co-card{background:#000;color:#fff;border-radius:24px;padding:48px 44px}
.ab-co-card h3{font-weight:340;font-size:30px;letter-spacing:-.9px;line-height:1.15;margin:0}
@media(max-width:760px){
 .ab-hero{padding:36px 24px}.ab-hero h1{font-size:34px;letter-spacing:-1.2px}.ab-hero p{font-size:15px}
 .ab .sec{padding:0 0 48px}
 .ab-g2{grid-template-columns:1fr;gap:28px}
 .ab-h2{font-size:28px}
 .ab-lime{padding:32px 24px}.ab-lime .ab-g2{gap:28px}
 .ab-navy{padding:40px 24px}.ab-navy h2{font-size:30px;letter-spacing:-1px}.ab-navy p{font-size:15px}
 .ab-stats{gap:24px}.ab-stats .v{font-size:30px}
 .ab-eg{grid-template-columns:1fr;gap:12px}.ab-ec{grid-column:auto!important;flex-direction:row!important;align-items:center!important}.ab-ec .gl{width:96px!important}.ab-eg>:nth-child(1){order:1}.ab-eg>:nth-child(4){order:2}.ab-eg>:nth-child(3){order:3}.ab-eg>:nth-child(2){order:4}
 .ab-cream{padding:40px 24px}.ab-cream h2{font-size:30px;letter-spacing:-1px}
 .ab-card{padding:22px 20px}
 .ab-hero-ctas{flex-wrap:wrap}
}
</style>'''
 # 공룡 5종 글리프(이 페이지 전용)
 '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
 '<symbol id="d-brachio" viewBox="0 0 120 100"><g fill="currentColor"><rect x="36" y="62" width="9" height="30" rx="4"/><rect x="50" y="64" width="9" height="28" rx="4"/><rect x="68" y="64" width="9" height="28" rx="4"/><rect x="80" y="62" width="9" height="30" rx="4"/><ellipse cx="64" cy="58" rx="30" ry="18"/><path d="M90 56 Q110 52 118 64 Q104 60 90 66 Z"/><path d="M46 60 Q30 50 30 30 Q30 13 41 9 Q34 22 43 35 Q49 49 58 55 Z"/><ellipse cx="36" cy="11" rx="9.5" ry="7.5"/><path d="M28 9 q-6 -1 -8 3 q5 1 8 -1 z"/></g></symbol>'
 '<symbol id="d-ptera" viewBox="0 0 120 100"><g fill="currentColor"><polygon points="60,52 6,28 16,40 34,54"/><polygon points="60,52 114,28 104,40 86,54"/><ellipse cx="60" cy="56" rx="12" ry="17"/><path d="M56 42 Q50 31 36 30 Q52 24 60 33 L78 26 Q74 37 65 42 Z"/><rect x="52" y="70" width="7" height="20" rx="3"/><rect x="61" y="70" width="7" height="20" rx="3"/></g></symbol>'
 '<symbol id="d-eoraptor" viewBox="0 0 120 100"><g fill="currentColor"><path d="M58 56 Q88 56 116 68 Q90 62 60 65 Z"/><path d="M48 58 l9 0 -3 32 -8 0 z"/><path d="M60 58 l9 0 -2 32 -8 0 z"/><path d="M38 54 Q31 39 43 31 Q52 22 61 29 Q68 34 65 49 L63 60 L43 60 Q38 59 38 54 Z"/><path d="M47 33 Q43 20 32 16 Q27 12 21 15 Q28 18 28 25 Q32 31 45 38 Z"/><ellipse cx="24" cy="14" rx="8.5" ry="6.5"/><path d="M16 13 q-7 0 -9 3 q6 1 9 -1 z"/><path d="M45 42 Q52 47 52 54 Q47 49 42 49 Z"/></g></symbol>'
 '<symbol id="d-quetzal" viewBox="0 0 140 92"><g fill="currentColor"><path d="M70 40 Q40 15 7 33 Q34 33 51 46 Q30 46 17 59 Q44 50 68 50 Z"/><path d="M70 40 Q100 15 133 33 Q106 33 89 46 Q110 46 123 59 Q96 50 72 50 Z"/><ellipse cx="70" cy="46" rx="8" ry="14"/><path d="M68 35 Q66 22 76 16 Q70 15 65 21 Q62 29 64 38 Z"/><path d="M74 17 L106 9 L77 23 Z"/><polygon points="76,16 72,3 84,15"/></g></symbol>'
 '<symbol id="d-maia" viewBox="0 0 120 100"><g><path fill="currentColor" d="M44 70 Q40 38 66 34 Q92 32 96 60 Q97 68 92 73 Z"/><path fill="currentColor" d="M92 62 Q106 62 113 72 Q100 66 90 68 Z"/><path fill="currentColor" d="M52 44 Q40 25 23 26 Q33 17 46 23 Q58 29 62 42 Z"/><ellipse cx="21" cy="27" rx="9" ry="7" fill="currentColor"/><path fill="currentColor" d="M13 29 q-9 1 -11 5 q8 2 13 -1 z"/><polygon points="25,21 29,10 34,21" fill="currentColor"/><ellipse cx="52" cy="80" rx="40" ry="11" fill="currentColor"/><g fill="#fff" stroke="currentColor" stroke-width="2.2"><ellipse cx="36" cy="75" rx="7.5" ry="10"/><ellipse cx="52" cy="77" rx="8" ry="10.5"/><ellipse cx="68" cy="75" rx="7.5" ry="10"/></g></g></symbol>'
 '</defs></svg>'
 '<div class="ab"><div class="wrap">'
 # HERO
 '<section class="sec" style="padding-top:40px"><div class="block ab-hero"><svg class="ab-wm" viewBox="2 3.6 20 16.4"><use href="#mk"/></svg>'
 '<div class="eb" style="color:rgba(0,0,0,.55)">카드티라노란?</div>'
 '<h1>받을 수 있는 혜택을,<br>다 받게.</h1>'
 '<p>카드 혜택은 분명히 거기 있습니다. 다만 너무 흩어져 있고, 너무 자주 바뀝니다. 그 손해를 끝내려고 — 카드티라노가 나섰습니다.</p>'
 '<div class="ab-hero-ctas" style="display:flex;gap:12px;margin-top:34px;flex-wrap:wrap">'
 '<a class="ab-cta" href="issue.html?v=cmp">한눈에 비교 시작하기 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a>'
 '<a class="ab-cta2" href="issue.html">이번 달 캐시백 보기</a></div></div></section>'
 # PROBLEM
 '<section class="sec"><div class="ab-g2">'
 '<div><div class="eb" style="color:var(--accent-magenta)">정보의 비대칭</div>'
 '<h2 class="ab-h2">같은 카드인데,<br>받는 혜택이 다릅니다</h2>'
 '<p style="font-weight:400;font-size:16px;line-height:1.55;margin:22px 0 0;color:rgba(0,0,0,.72)">토스·카드고릴라·아정당·카카오페이·뱅크샐러드. 같은 카드를 발급해도 <b style="font-weight:700">어디서 받느냐에 따라 캐시백이 수십만 원씩</b> 차이 납니다. 그리고 그 금액은 매달 바뀝니다.</p>'
 '<p style="font-weight:400;font-size:16px;line-height:1.55;margin:16px 0 0;color:rgba(0,0,0,.72)">혜택 정보는 카드사와 플랫폼만 훤히 알고, 정작 받아야 할 사용자는 모릅니다. 우리는 이 정보의 비대칭이 카드 시장에서 <b style="font-weight:700">가장 불공평한 지점</b>이라고 생각했습니다.</p></div>'
 '<div class="ab-card"><div class="mono" style="font-size:10px;color:rgba(0,0,0,.45);margin-bottom:6px">같은 카드 · 같은 달 · 플랫폼별 캐시백</div>'
 '<div style="font-weight:700;font-size:17px;letter-spacing:-.3px;margin-bottom:20px">트래블 캐시백 카드</div>'
 '<div style="display:flex;flex-direction:column;gap:13px">'
 + "".join('<div style="display:flex;align-items:center;gap:12px"><span style="width:64px;font-weight:540;font-size:13px;white-space:nowrap">%s</span><div class="ab-bar"><i style="width:%s;background:%s"></i></div><span style="width:52px;text-align:right;font-weight:700;font-size:14px;white-space:nowrap;color:%s">%s</span></div>'%(n,w,f,t,v) for n,v,w,f,t in [
   ("토스","14만","100%","#000","#000"),("아정당","11만","78%","#cfcfcf","rgba(0,0,0,.55)"),("고릴라","9만","64%","#cfcfcf","rgba(0,0,0,.55)"),("카카오","8만","57%","#cfcfcf","rgba(0,0,0,.55)"),("뱅샐","7만","50%","#cfcfcf","rgba(0,0,0,.55)")])
 + '</div><div style="font-weight:400;font-size:12.5px;color:rgba(0,0,0,.5);margin-top:18px;line-height:1.5">같은 카드인데 최대 <b style="font-weight:700;color:#000">2배 차이</b>. 어디가 가장 많이 주는지, 직접 비교는 사실상 불가능합니다.</div></div>'
 '</div></section>'
 # SOLUTION 한눈에 비교
 '<section class="sec"><div class="block ab-lime"><div class="ab-g2">'
 '<div><div class="eb" style="color:rgba(0,0,0,.55)">한눈에 비교</div>'
 '<h2 class="ab-h2">흩어진 혜택을,<br>한곳에 모았습니다</h2>'
 '<p style="font-weight:400;font-size:16px;line-height:1.55;margin:22px 0 0;color:rgba(0,0,0,.74)">6개 발급 플랫폼의 신규 발급 캐시백, 가맹점 결제 할인, 무이자 할부까지 — 매달 수집하고 분석해, <b style="font-weight:700">\'가장 많이 주는 곳\'을 골라 한눈에</b> 보여드립니다.</p>'
 '<p style="font-weight:540;font-size:16px;line-height:1.5;margin:16px 0 0">"이 카드, 어디서 받아야 제일 이득이지?"에 대한 답을, 검색 없이.</p>'
 '<p style="font-weight:400;font-size:15px;line-height:1.5;margin:18px 0 0;color:rgba(0,0,0,.66)">복잡한 건 우리가 할게요. 당신은 가장 이득인 결과만 보면 됩니다.</p></div>'
 '<div style="background:#fff;border-radius:20px;padding:28px 30px;box-shadow:0 4px 16px rgba(0,0,0,.06)">'
 '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px"><span class="mono" style="font-size:10px;color:rgba(0,0,0,.45)">6개 플랫폼 → 가장 이득인 1곳</span><span style="width:26px;height:26px;border-radius:50%;background:var(--block-lime);display:flex;align-items:center;justify-content:center"><svg viewBox="2 3.6 20 16.4" style="width:16px;height:16px"><use href="#mk"/></svg></span></div>'
 '<div style="display:flex;flex-direction:column;gap:10px">'
 + "".join('<div style="display:flex;align-items:center;gap:11px;padding:11px 14px;border-radius:12px;background:%s;border:%s"><span style="width:8px;height:8px;border-radius:50%%;background:%s;flex-shrink:0"></span><span style="font-weight:540;font-size:13.5px;flex:1;color:%s">%s</span>%s<span style="font-weight:700;font-size:15px;white-space:nowrap;color:%s">%s</span></div>'%(bg,bd,dot,nc,nm,('<span class="mono" style="font-size:8px;background:#000;color:#fff;padding:3px 8px;border-radius:50px">최고</span>' if win else ''),vc,v) for nm,v,dot,win,bg,bd,nc,vc in [
   ("토스","14만원","#3182F6",True,"var(--block-lime)","1px solid #000","#000","#000"),
   ("아정당","11만원","#1B64DA",False,"var(--surface-soft)","1px solid transparent","rgba(0,0,0,.7)","rgba(0,0,0,.55)"),
   ("카드고릴라","9만원","#FF6A13",False,"var(--surface-soft)","1px solid transparent","rgba(0,0,0,.7)","rgba(0,0,0,.55)"),
   ("카카오페이","8만원","#FEE500",False,"var(--surface-soft)","1px solid transparent","rgba(0,0,0,.7)","rgba(0,0,0,.55)"),
   ("뱅크샐러드","7만원","#19C37D",False,"var(--surface-soft)","1px solid transparent","rgba(0,0,0,.7)","rgba(0,0,0,.55)"),
   ("네이버페이","6만원","#03C75A",False,"var(--surface-soft)","1px solid transparent","rgba(0,0,0,.7)","rgba(0,0,0,.55)")])
 + '</div></div></div></div></section>'
 # SKYSCANNER VISION
 '<section class="sec"><div class="block ab-navy"><svg viewBox="0 0 140 92" style="position:absolute;right:34px;top:40px;width:170px;opacity:.16;color:#fff"><use href="#d-quetzal"/></svg>'
 '<div class="eb" style="color:rgba(255,255,255,.6)">우리가 꿈꾸는 것</div>'
 '<h2>카드 시장의<br>스카이스캐너를&nbsp;꿈꿉니다</h2>'
 '<p>항공권을 살 때 우리는 더 이상 항공사 사이트를 일일이 돌지 않습니다. 한 곳에서 <b>모든 항공사를 비교</b>하고, 가장 싼 항공권을 찾으니까요.</p>'
 '<p>카드도 그래야 한다고 믿습니다. <b>모든 발급 플랫폼의 혜택을 한 화면에서 비교</b>해, 가장 이득인 곳을 찾는 곳. 카드티라노가 그 자리를 만들고 있습니다.</p>'
 '<div class="ab-stats">'
 + "".join('<div><div class="v">%s</div><div class="l">%s</div></div>'%(v,l) for v,l in [("6개","발급 플랫폼 통합 비교"),("매달","전수 수집·재분석"),("4인","사이트·사업·마케팅·분석 전문")])
 + '</div></div></section>'
 # EXPERTS 공룡
 '<section class="sec"><div style="max-width:680px"><div class="eb" style="color:var(--accent-magenta)">곁의 전문가</div>'
 '<h2 class="ab-h2">데이터를 읽는 공룡 넷</h2>'
 '<p style="font-weight:400;font-size:16px;line-height:1.55;margin:20px 0 0;color:rgba(0,0,0,.72)">자동화만으로는 \'진짜 좋은 카드\'를 가려낼 수 없습니다. 조건의 함정, 실적의 무게, 갱신 시점의 미묘한 차이는 결국 사람이 읽어야 하니까요. 그래서 카드티라노의 중심에는 <b style="font-weight:700">방향을 정하고 직접 만든 두 창업자 — 코파운더 듀오</b>가 있고, 그 곁에서 캐시백·마케팅·분석을 맡은 전문가들이 함께합니다.</p></div>'
 '<div class="ab-eg">'
 + "".join('<div class="ab-ec" style="background:%s;%s;%s"><div class="gl" style="width:%s"><svg viewBox="%s"><use href="%s"/></svg></div><div style="min-width:0"><div class="role">%s</div><div class="nm">%s</div><div class="tag">%s</div><div class="ds">%s</div></div></div>'%(bg,span,flex,gw,vb,ic,role,nm,tag,desc) for ic,vb,nm,role,tag,desc,bg,span,flex,gw in [
   ("#d-eoraptor","0 0 120 100","에오랍토르","공동창업자 · CEO (CTO/CPO 겸)","비전을 세우고, 직접 만듭니다","카드티라노가 어디로 갈지 — 전략과 비전을 세우고, 프로덕트·기술·디자인(CPO·CTO)을 직접 이끕니다. 가장 먼저 나타난 공룡처럼, 이 모든 것의 시작이자 중심.","var(--block-lilac)","grid-column:span 2","flex-direction:row;align-items:center","140px"),
   ("#d-maia","0 0 120 100","마이아사우라","공동창업자 · 캐시백·이벤트 분석","좋은 건 놓치지 않습니다","매달 바뀌는 캐시백과 발급 이벤트를 꼼꼼히 살펴, 가장 이득인 것을 골라냅니다.","var(--block-mint)","","flex-direction:column;align-items:flex-start","104px"),
   ("#d-ptera","0 0 120 100","프테라노돈","공동창업자 · 마케팅 총괄","멀리, 빠르게 알립니다","카드티라노가 찾은 가장 이득인 선택을, 필요한 사람에게 가장 빠르게 전합니다.","var(--block-pink)","","flex-direction:column;align-items:flex-start","104px"),
   ("#d-brachio","0 0 120 100","브라키오","공동창업자 · CSO · 전략 총괄","크게, 멀리 내다봅니다","에오랍토르와 함께 카드티라노를 세운 공동창업자이자 전략 총괄(CSO). 시장과 데이터를 읽어 사업 전략·방향을 설계하고, 카드사·플랫폼 파트너십으로 서비스가 더 크고 멀리 나아갈 길을 엽니다.","var(--block-cream)","grid-column:span 2","flex-direction:row;align-items:center","140px")])
 + '</div>'
 '<p style="font-weight:400;font-size:14px;line-height:1.55;margin:26px auto 0;max-width:680px;color:rgba(0,0,0,.6);text-align:center">데이터가 숫자를 모으고, 전문가가 그 숫자에 맥락을 입힙니다. 그래서 카드티라노의 추천에는 늘 <b style="font-weight:700;color:#000">근거</b>가 있습니다.</p></section>'
 # BELIEF
 '<section class="sec"><div class="ab-cream"><div class="eb" style="color:rgba(0,0,0,.5)">우리의 믿음</div>'
 '<h2>혜택은 부지런한 사람만의<br>것이 아니어야 합니다</h2>'
 '<p style="font-weight:400;font-size:17px;line-height:1.55;margin:24px auto 0;max-width:560px;color:rgba(0,0,0,.7)">정보를 더 가졌다는 이유로 누군가는 더 받고, 모른다는 이유로 누군가는 덜 받는 일. 카드티라노는 그 격차를 메우려 합니다.</p>'
 '<p style="font-weight:540;font-size:22px;letter-spacing:-.5px;margin:28px auto 0;max-width:560px">누구나, 받을 수 있는 혜택을 다 받는 것. 그게 우리가 만들고 싶은 카드 시장입니다.</p></div></section>'
 # COMPANY
 '<section class="sec"><div class="ab-g2">'
 '<div><div style="display:flex;align-items:center;gap:11px;margin-bottom:20px"><svg viewBox="2 3.6 20 16.4" style="width:34px;height:34px"><use href="#mk"/></svg><span style="font-weight:700;font-size:22px;letter-spacing:-.5px">CARD<span style="font-weight:340">TYRANNO</span></span></div>'
 '<p style="font-weight:400;font-size:17px;line-height:1.55;color:rgba(0,0,0,.74)"><b style="font-weight:700">데이터로 카드 혜택을 큐레이션하는 핀테크 스타트업</b>입니다. (운영: 쥬라기랩스) 오직 사용자 편에서, 흩어진 혜택을 모으고 분석해 가장 유리한 선택을 안내합니다.</p>'
 '<p style="font-weight:400;font-size:16px;line-height:1.55;margin:18px 0 0;color:rgba(0,0,0,.66)">가장 강한 포식자가 먹잇감을 놓치지 않듯 — 당신이 받아야 할 혜택도, 카드티라노가 놓치지 않겠습니다.</p></div>'
 '<div class="ab-co-card"><h3>이번 달, 당신에게<br>가장 유리한 선택은?</h3>'
 '<p style="font-weight:400;font-size:15px;line-height:1.5;margin:16px 0 0;color:rgba(255,255,255,.7)">매달 쌓이는 데이터와 전문가의 시선으로 카드티라노가 안내합니다.</p>'
 '<a class="sans" style="display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:50px;background:#fff;color:#000;font-weight:540;font-size:15px;margin-top:26px;text-decoration:none" href="issue.html?v=cmp">한눈에 비교 시작하기 <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></div>'
 '</div></section>'
 '</div></div>')

# ===== BUILD =====
page("index.html",BRAND+" | 카드 발급 캐시백·할인 혜택 비교","같은 카드도 채널 따라 혜택이 달라요. 토스·카드고릴라·아정당·카카오페이의 발급 캐시백·할인을 카드티라노가 매달 비교해 드려요.","/index.html",INDEX_BODY+SEO_STATIC_INDEX,INDEX_JS,faq_jsonld(),searchbar=False,catstrip=False,active="")
page("about.html",BRAND+" | 카드티라노란? · 서비스 소개","흩어진 카드 혜택을 모아 가장 이득인 발급처를 한눈에 비교해 드리는 카드티라노 소개 — 정보의 비대칭을 줄이는 카드 비교 핀테크(쥬라기랩스).","/about.html",ABOUT_BODY,"",active="about")

# ===== DIAGNOSE (카드 진단 · 60초 2지선다) =====
DIAG_BODY=(r'''<style>
.dg-wrap{max-width:780px;margin:0 auto;padding:8px 0 0}
.dg-screen{display:none}.dg-screen.on{display:block}
.dg-tcircle{position:relative;border-radius:50%;display:flex;align-items:center;justify-content:center}
.dg-tcircle .prop{position:absolute;right:4px;top:6px;border-radius:50%;background:#fff;box-shadow:0 3px 10px rgba(0,0,0,.14);display:flex;align-items:center;justify-content:center;color:#1a1714}
.dg-eb{font-family:var(--font-mono,monospace);font-size:10px;letter-spacing:.6px;text-transform:uppercase;color:rgba(0,0,0,.5)}
/* intro */
.dg-intro-hero{background:var(--block-lilac);border-radius:26px;padding:34px 26px 30px;text-align:center;position:relative;overflow:hidden}
.dg-intro-hero h1{font-weight:330;font-size:30px;letter-spacing:-1.1px;line-height:1.18;margin:16px 0 0}
.dg-intro-hero p{font-weight:400;font-size:14px;line-height:1.55;color:rgba(0,0,0,.66);margin:11px 8px 0}
.dg-cta{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:16px;border:none;border-radius:50px;background:#000;color:#fff;font-weight:600;font-size:15.5px;cursor:pointer;font-family:inherit}.dg-cta svg{width:17px;height:17px}
.dg-cta:active{transform:scale(.97)}
.dg-note{text-align:center;font-weight:400;font-size:12px;color:rgba(0,0,0,.5);margin:12px 0 0}
/* question */
.dg-top{display:flex;align-items:center;justify-content:space-between;padding:4px 2px 12px}
.dg-icnbtn{width:34px;height:34px;border-radius:50%;background:var(--surface-soft);display:flex;align-items:center;justify-content:center;color:#000;border:0;cursor:pointer}.dg-icnbtn svg{width:16px;height:16px}
.dg-step{font-family:var(--font-mono,monospace);font-size:11px;color:rgba(0,0,0,.55)}
.dg-prog{height:5px;border-radius:50px;background:var(--hairline);overflow:hidden}.dg-prog i{display:block;height:100%;border-radius:50px;background:#000;transition:width .3s}
.dg-qhead{text-align:center;padding:8px 12px 0}
.dg-qhead h2{font-weight:330;font-size:25px;letter-spacing:-.9px;line-height:1.25;margin:9px 0 0}
.dg-choices{padding:22px 0 8px;display:flex;flex-direction:column;gap:12px}
.choice{display:flex;align-items:center;gap:13px;width:100%;padding:17px 18px;border:1.5px solid var(--hairline);border-radius:18px;background:#fff;text-align:left;cursor:pointer;font-family:inherit;min-height:56px;transition:transform .12s ease}
.choice:active{transform:scale(.97)}
.choice .k{flex-shrink:0;width:30px;height:30px;border-radius:50%;border:1.5px solid rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;font-family:var(--font-mono,monospace);font-size:13px;font-weight:600;color:rgba(0,0,0,.55)}.choice .k svg{width:16px;height:16px}
.choice .cl{display:block;font-weight:700;font-size:15.5px;letter-spacing:-.3px}.choice .cs{display:block;font-weight:400;font-size:12.5px;color:rgba(0,0,0,.58);margin-top:2px}
.choice.sel{border-color:#000;background:#000;color:#fff}.choice.sel .k{border-color:#fff;background:#fff;color:#000}.choice.sel .cs{color:rgba(255,255,255,.66)}
/* 4~8지선다 아이콘 2열 그리드 */
.dg-grid{padding:18px 0 8px;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.dg-gopt{display:flex;flex-direction:column;align-items:flex-start;gap:8px;padding:14px 14px;border-radius:14px;border:1.5px solid var(--hairline);background:#fff;color:#111;text-align:left;cursor:pointer;font-family:inherit;min-height:56px;transition:transform .12s ease}
.dg-gopt:active{transform:scale(.97)}
.dg-gopt .gi{width:32px;height:32px;border-radius:9px;background:var(--surface-soft);color:#1a1714;display:flex;align-items:center;justify-content:center}.dg-gopt .gi svg{width:18px;height:18px}
.dg-gopt .gt{font-weight:700;font-size:13px;letter-spacing:-.3px}
.dg-gopt.sel{border-color:#000;background:#000;color:#fff}.dg-gopt.sel .gi{background:rgba(255,255,255,.16);color:#fff}
/* 결과 · 내 진단 유형 비중 */
.dg-dist .bar{display:flex;height:18px;border-radius:50px;overflow:hidden;margin-top:11px}
.dg-dist .bar span{display:block;height:100%}
.dg-dist .lg{display:flex;flex-wrap:wrap;gap:10px 16px;margin-top:12px}
.dg-dist .lg .it{display:flex;align-items:center;gap:7px}
.dg-dist .lg .dt{width:8px;height:8px;border-radius:50%}
.dg-dist .lg .nm{font-size:12px}.dg-dist .lg .pc{font-weight:700;font-size:12px}
.dg-dist .lg .me{font-family:var(--font-mono,monospace);font-size:8px;background:var(--accent-magenta);color:#fff;padding:2px 6px;border-radius:50px;text-transform:uppercase}
/* result */
.dg-rhero{background:var(--block-lime);border-radius:26px;padding:22px 22px 24px;text-align:center;position:relative;overflow:hidden}
.dg-badge{display:inline-block;font-family:var(--font-mono,monospace);font-size:9px;background:var(--accent-magenta);color:#fff;padding:5px 11px;border-radius:50px}
.dg-plate{position:relative;margin:14px auto 0;width:210px;height:132px}
.dg-plate .pl{position:absolute;left:18px;top:12px;width:176px;height:108px;border-radius:14px;overflow:hidden;transform:rotate(-7deg);box-shadow:0 10px 22px rgba(0,0,0,.18);background:#9a86e8}
.dg-plate .pl img{width:100%;height:100%;object-fit:cover;display:block}
.dg-plate .tyr{position:absolute;left:-6px;bottom:-8px;color:#1a1714}
.dg-rhero h2{font-weight:700;font-size:22px;letter-spacing:-.6px;line-height:1.25;margin:16px 0 0}
.dg-rhero .rd{font-weight:400;font-size:13px;line-height:1.5;color:rgba(0,0,0,.66);margin:7px 12px 0}
.dg-sec{padding:18px 2px 0}
.dg-chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px}
.dg-chips span{font-weight:540;font-size:12px;padding:6px 11px;border:1px solid var(--hairline);border-radius:50px}
.dg-bars{margin-top:12px;display:flex;flex-direction:column;gap:11px}
.dg-bar{display:flex;align-items:center;gap:10px}
.dg-bar .bn{width:62px;flex-shrink:0;font-size:12px;letter-spacing:-.2px}
.dg-bar .bt{flex:1;height:18px;border-radius:50px;background:var(--surface-soft);overflow:hidden}.dg-bar .bt i{display:block;height:100%;border-radius:50px}
.dg-bar .ba{width:58px;flex-shrink:0;text-align:right;font-size:12.5px;letter-spacing:-.3px}
.dg-evrow{display:flex;align-items:center;gap:11px;padding:12px 0;border-bottom:1px solid var(--hairline-soft);text-decoration:none;color:#000}
.dg-evrow .dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.dg-evrow .et{font-weight:700;font-size:13px;letter-spacing:-.3px;line-height:1.35}.dg-evrow .ep{font-family:var(--font-mono,monospace);font-size:8.5px;color:rgba(0,0,0,.5);margin-top:3px;text-transform:uppercase}
.dg-evrow .dd{flex-shrink:0;font-weight:700;font-size:11px;color:#b01060;background:#fff0f6;padding:4px 9px;border-radius:50px;white-space:nowrap}
.dg-rcta{padding:16px 0 26px}
.dg-redo{display:flex;align-items:center;justify-content:center;gap:7px;width:100%;padding:13px;border:none;background:none;color:rgba(0,0,0,.6);font-weight:540;font-size:13.5px;margin-top:4px;cursor:pointer;font-family:inherit}.dg-redo svg{width:15px;height:15px}
.dg-foot{font-size:11px;color:rgba(0,0,0,.4);text-align:center;margin-top:6px;line-height:1.5}
/* desktop */
@media(min-width:761px){
 .dg-wrap{max-width:880px}
 .dg-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:#fff}
 .dg-qgrid{display:grid;grid-template-columns:300px 1fr}
 .dg-qgrid .qleft{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 24px;text-align:center}
 .dg-qgrid .qright{padding:44px 40px;display:flex;flex-direction:column;justify-content:center}
 .dg-qgrid .qright h2{font-size:32px;letter-spacing:-1.2px}
 .dg-qhead.mo{display:none}
 .dg-rgrid{display:grid;grid-template-columns:330px 1fr}
 .dg-rgrid .rleft{background:var(--block-lime);padding:34px 28px;display:flex;flex-direction:column;align-items:center;text-align:center}
 .dg-rgrid .rright{padding:30px 32px}
 .dg-rhero{display:none}
 .dg-intro-hero{padding:46px 40px 40px}.dg-intro-hero h1{font-size:36px}
}
@media(max-width:760px){.dg-qgrid,.dg-rgrid{display:block}.dg-qgrid .qleft,.dg-rgrid .rleft{display:none}.dg-card{border:0}.dg-qhead.pc{display:none}}
/* === 시나리오 선택 스와이프 === */
.dg-swipe{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:12px 2px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.dg-swipe::-webkit-scrollbar{display:none}
.dg-scard{scroll-snap-align:center;flex:0 0 84%;max-width:430px;border-radius:24px;padding:26px 22px 22px;display:flex;flex-direction:column;min-height:340px}
.dg-scard .sc-ic{width:62px;height:62px;border-radius:50%;background:rgba(255,255,255,.55);display:flex;align-items:center;justify-content:center;color:#1a1714}.dg-scard .sc-ic svg{width:32px;height:32px}
.dg-scard .sc-eb{font-family:var(--font-mono,monospace);font-size:10px;letter-spacing:.6px;text-transform:uppercase;color:rgba(0,0,0,.5);margin-top:16px}
.dg-scard h3{font-weight:330;font-size:23px;letter-spacing:-.8px;line-height:1.22;margin:7px 0 0;word-break:keep-all}
.dg-scard .sc-d{font-weight:400;font-size:13px;line-height:1.55;color:rgba(0,0,0,.62);margin:9px 0 0;word-break:keep-all}
.dg-scard ul{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-direction:column;gap:7px}
.dg-scard li{display:flex;align-items:center;gap:8px;font-size:12.5px;color:rgba(0,0,0,.72);word-break:keep-all}
.dg-scard li svg{width:15px;height:15px;flex-shrink:0;color:#1a1714}
.dg-scard .sc-sp{flex:1}
.sc-a{background:var(--block-lilac)}.sc-b{background:var(--block-lime)}
.dg-dots{display:flex;justify-content:center;gap:7px;margin-top:4px}
.dg-dots span{width:7px;height:7px;border-radius:50%;background:rgba(0,0,0,.18);transition:all .25s}
.dg-dots span.on{background:#000;width:20px;border-radius:50px}
@media(min-width:761px){.dg-scard{flex:0 0 47%}}
/* === 시나리오2 카드사 선택 === */
.s2-iss-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;padding:16px 0 4px}
.s2-iss{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;padding:15px 4px;border:1.5px solid var(--hairline);border-radius:16px;background:#fff;cursor:pointer;font-family:inherit;min-height:76px;transition:transform .12s}
.s2-iss:active{transform:scale(.95)}
.s2-iss .nm{font-weight:700;font-size:13px;letter-spacing:-.3px}
.s2-iss .ck{width:18px;height:18px;border-radius:50%;border:1.5px solid rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center}
.s2-iss .ck svg{width:11px;height:11px;opacity:0}
.s2-iss.sel{border-color:#000;background:#000;color:#fff}
.s2-iss.sel .ck{border-color:#fff;background:#fff}.s2-iss.sel .ck svg{opacity:1;color:#000}
.dg-cta:disabled{opacity:.38;pointer-events:none}
/* === 시나리오2 결과 === */
.s2-total .amt{font-weight:700;font-size:34px;letter-spacing:-1.4px;line-height:1}.s2-total .amt small{font-size:15px;font-weight:540;letter-spacing:0}
.s2-brk{margin-top:10px;display:flex;flex-direction:column;gap:8px}
.s2-brow{display:flex;align-items:center;gap:11px;padding:11px 13px;border:1px solid var(--hairline);border-radius:14px}
.s2-brow.off{opacity:.55}
.s2-brow .bi{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}.s2-brow .bi svg{width:14px;height:14px}
.s2-brow .bl{flex:1;font-weight:600;font-size:13px;letter-spacing:-.2px}.s2-brow .bl small{display:block;font-weight:400;font-size:11px;color:rgba(0,0,0,.5);margin-top:1px}
.s2-brow .bv{font-weight:700;font-size:13.5px;letter-spacing:-.3px;white-space:nowrap}
.s2-pf{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:12.5px;padding:6px 13px;border-radius:50px}
/* === 공룡알 부화 일러스트 === */
.egg-wrap,.egg-shake,.egg-hatch-wrap{display:inline-block;line-height:0}
.egg-wrap{transform-origin:50% 88%;animation:dgEggWob 1.9s ease-in-out infinite}
.egg-shake{transform-origin:50% 88%;animation:dgEggShake 2.6s ease-in-out infinite}
.egg-hatch-wrap{animation:dgEggPop .62s cubic-bezier(.2,.9,.3,1.35) both}
@keyframes dgEggWob{0%,100%{transform:rotate(-3.5deg)}50%{transform:rotate(3.5deg)}}
@keyframes dgEggShake{0%,100%{transform:rotate(0)}20%{transform:rotate(-3.5deg)}40%{transform:rotate(2.5deg)}60%{transform:rotate(-2deg)}80%{transform:rotate(3deg)}}
@keyframes dgEggPop{0%{transform:scale(.4) translateY(8px);opacity:0}55%{transform:scale(1.14) translateY(-2px)}100%{transform:scale(1) translateY(0);opacity:1}}
@media(prefers-reduced-motion:reduce){.egg-wrap,.egg-shake,.egg-hatch-wrap{animation:none}}
</style>'''
 r'''<svg style="display:none" aria-hidden="true">
 <symbol id="tyr" viewBox="0 0 100 86"><path fill="currentColor" d="M6 64 C 26 56 36 53 46 53 C 50 44 56 38 66 38 L 62 22 L 74 22 L 72 40 C 78 46 80 54 80 60 C 80 68 74 72 64 72 L 30 72 C 18 72 10 70 6 64 Z"/><rect x="30" y="68" width="9" height="15" rx="3" fill="currentColor"/><rect x="56" y="68" width="9" height="15" rx="3" fill="currentColor"/><path fill="currentColor" d="M58 52 c5 0 9 2 11 5 c-3 -1 -6 -1 -9 0 z"/><rect x="58" y="6" width="26" height="24" rx="6" fill="currentColor"/><circle cx="66" cy="14" r="2.4" fill="#fff"/><rect x="70" y="17" width="9" height="8" rx="1.4" fill="none" stroke="#fff" stroke-width="1.4"/><path d="M70 21h9" stroke="#fff" stroke-width="1.4"/><path d="M74.5 17v8" stroke="#fff" stroke-width="1.4"/></symbol>
 <symbol id="p-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.3 3.6 5.3 3.6 8.5s-1.2 6.2-3.6 8.5c-2.4-2.3-3.6-5.3-3.6-8.5S9.6 5.8 12 3.5Z"/></symbol>
 <symbol id="p-receipt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3.5h12v17l-2.2-1.4-2 1.4-1.8-1.4-1.8 1.4-2-1.4L6 20.5z"/><path d="M9 8h6M9 11.5h6M9 15h3.5"/></symbol>
 <symbol id="p-coins" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="9" cy="9" r="5.5"/><path d="M14.2 5.4A5.5 5.5 0 1 1 9 18.4"/><path d="M9 6.6v4.8M7.2 8.2h2.8a1.2 1.2 0 0 1 0 2.4H7.6"/></symbol>
 <symbol id="p-spark" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2.5l1.9 5.6 5.6 1.9-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.9z"/><path d="M19 15l.9 2.6 2.6.9-2.6.9-.9 2.6-.9-2.6-2.6-.9 2.6-.9z"/></symbol>
 <symbol id="p-bag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 8h13l-1 11.5a1.5 1.5 0 0 1-1.5 1.4H8a1.5 1.5 0 0 1-1.5-1.4z"/><path d="M8.5 8V6.5a3.5 3.5 0 0 1 7 0V8"/></symbol>
 <symbol id="p-crown" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7.5l3.5 3 4.5-6 4.5 6 3.5-3-1.5 11h-13z"/><path d="M5.5 21h13"/></symbol>
 <symbol id="c-cart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h2l2 11h11"/><path d="M5.5 7h15l-1.6 6H7"/><circle cx="9" cy="19" r="1.3"/><circle cx="17" cy="19" r="1.3"/></symbol>
 <symbol id="c-store" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9.5V20h16V9.5"/><path d="M3 9.5L4.5 4h15L21 9.5a2.5 2.5 0 0 1-4.5 1.5 2.5 2.5 0 0 1-4.5 0 2.5 2.5 0 0 1-4.5 0A2.5 2.5 0 0 1 3 9.5z"/><path d="M9.5 20v-5h5v5"/></symbol>
 <symbol id="c-cup" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 8h12v4a6 6 0 0 1-12 0z"/><path d="M17 9h2a2 2 0 0 1 0 4h-2"/><path d="M6 21h10"/></symbol>
 <symbol id="c-car" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v-3l2-5h12l2 5v3"/><path d="M3 16h18v2h-2v1.5h-2V18H7v1.5H5V18H3z"/><circle cx="7.5" cy="14" r="1"/><circle cx="16.5" cy="14" r="1"/></symbol>
 <symbol id="c-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/></symbol>
 <symbol id="c-plane" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 13.5L3 11l2-3 4 1 5-5.5c.8-.8 2.2-.8 2.8 0s.8 2 0 2.8L13 11l1 4-2 2-2.5-3.5z"/></symbol>
 <symbol id="c-cross" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8.5v7M8.5 12h7"/></symbol>
 <symbol id="c-bill" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3.5h12v17l-2.2-1.4-2 1.4-1.8-1.4-1.8 1.4-2-1.4L6 20.5z"/><path d="M9 8h6M9 11.5h6M9 15h3.5"/></symbol>
 <symbol id="dg-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></symbol>
 <symbol id="dg-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></symbol>
 <symbol id="dg-back" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 6l-6 6 6 6"/></symbol>
 <symbol id="dg-redo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M19 5v5h-5"/><path d="M18.4 10A7.5 7.5 0 1 0 20 13.5"/></symbol>
 <symbol id="dg-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 6.5"/></symbol>
 <symbol id="egg-whole" viewBox="0 0 100 120"><path d="M50 8 C68 8 82 40 82 68 C82 97 68 113 50 113 C32 113 18 97 18 68 C18 40 32 8 50 8 Z" fill="#F7E8CF"/><path d="M50 113 C32 113 18 97 18 68 C18 60 19 53 21 46 C26 71 41 87 64 92 C58 105 54 113 50 113 Z" fill="#E9CFA3" opacity=".55"/><ellipse cx="37" cy="50" rx="6" ry="7" fill="#E6A765" opacity=".85"/><ellipse cx="61" cy="38" rx="4.5" ry="5.5" fill="#E6A765" opacity=".85"/><ellipse cx="63" cy="74" rx="7" ry="8" fill="#E6A765" opacity=".85"/><ellipse cx="42" cy="88" rx="4" ry="5" fill="#E6A765" opacity=".85"/><path d="M39 25 C44 21 51 21 56 25" stroke="#fff" stroke-width="3.4" stroke-linecap="round" fill="none" opacity=".6"/></symbol>
 <symbol id="egg-crack1" viewBox="0 0 100 120"><path d="M50 8 C68 8 82 40 82 68 C82 97 68 113 50 113 C32 113 18 97 18 68 C18 40 32 8 50 8 Z" fill="#F7E8CF"/><path d="M50 113 C32 113 18 97 18 68 C18 60 19 53 21 46 C26 71 41 87 64 92 C58 105 54 113 50 113 Z" fill="#E9CFA3" opacity=".55"/><ellipse cx="37" cy="52" rx="6" ry="7" fill="#E6A765" opacity=".85"/><ellipse cx="63" cy="76" rx="7" ry="8" fill="#E6A765" opacity=".85"/><ellipse cx="42" cy="88" rx="4" ry="5" fill="#E6A765" opacity=".85"/><path d="M47 15 L53 27 L45 35 L52 45" fill="none" stroke="#9C6B2E" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M39 25 C44 21 51 21 56 25" stroke="#fff" stroke-width="3.4" stroke-linecap="round" fill="none" opacity=".55"/></symbol>
 <symbol id="egg-crack2" viewBox="0 0 100 120"><path d="M50 8 C68 8 82 40 82 68 C82 97 68 113 50 113 C32 113 18 97 18 68 C18 40 32 8 50 8 Z" fill="#F7E8CF"/><path d="M50 113 C32 113 18 97 18 68 C18 60 19 53 21 46 C26 71 41 87 64 92 C58 105 54 113 50 113 Z" fill="#E9CFA3" opacity=".55"/><ellipse cx="37" cy="54" rx="5.5" ry="6.5" fill="#E6A765" opacity=".85"/><ellipse cx="64" cy="78" rx="6.5" ry="7.5" fill="#E6A765" opacity=".85"/><path d="M46 14 L54 26 L44 34 L53 44 L43 53 L51 63" fill="none" stroke="#9C6B2E" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M44 34 L34 38 M53 44 L63 47" fill="none" stroke="#9C6B2E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
 <symbol id="egg-crack3" viewBox="0 0 100 120"><path d="M50 8 C68 8 82 40 82 68 C82 97 68 113 50 113 C32 113 18 97 18 68 C18 40 32 8 50 8 Z" fill="#F7E8CF"/><path d="M50 113 C32 113 18 97 18 68 C18 60 19 53 21 46 C26 71 41 87 64 92 C58 105 54 113 50 113 Z" fill="#E9CFA3" opacity=".55"/><path d="M20 60 L30 54 L37 61 L45 52 L52 60 L60 51 L68 60 L76 55 L81 62" fill="none" stroke="#9C6B2E" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M45 14 L53 25 L43 33 L52 42 L42 50 L50 60" fill="none" stroke="#9C6B2E" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M43 33 L33 36 M52 42 L62 44 M50 60 L57 70" fill="none" stroke="#9C6B2E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
 <symbol id="egg-hatch" viewBox="0 0 100 120"><g transform="rotate(20 72 18)"><path d="M56 16 L64 9 L78 13 L88 22 L75 25 L63 23 Z" fill="#F7E8CF"/><path d="M63 23 L75 25 L70 21 L65 22 Z" fill="#E9CFA3" opacity=".7"/></g><path d="M33 64 C29 46 36 28 50 28 C64 28 71 46 67 64 Z" fill="#FF7A1A"/><path d="M41 30 l3 -7 l4 7 Z M50 28 l3.5 -7 l3.5 7 Z M59 30 l4 -7 l3 7 Z" fill="#E85D00"/><path d="M42 64 C40 50 44 42 50 42 C56 42 60 50 58 64 Z" fill="#FFC182"/><circle cx="44" cy="46" r="2.8" fill="#2A1C0E"/><circle cx="56" cy="46" r="2.8" fill="#2A1C0E"/><circle cx="45.1" cy="45" r=".9" fill="#fff"/><circle cx="57.1" cy="45" r=".9" fill="#fff"/><path d="M45 55 q5 4 10 0" fill="none" stroke="#2A1C0E" stroke-width="2" stroke-linecap="round"/><path d="M22 65 L30 55 L37 63 L45 53 L52 62 L60 52 L68 62 L76 56 L80 65 C82 92 68 113 50 113 C33 113 18 95 22 65 Z" fill="#F7E8CF"/><path d="M50 113 C33 113 18 95 22 65 C28 84 41 96 64 100 C60 109 54 113 50 113 Z" fill="#E9CFA3" opacity=".5"/><ellipse cx="38" cy="86" rx="5" ry="6" fill="#E6A765" opacity=".8"/><ellipse cx="62" cy="90" rx="6" ry="7" fill="#E6A765" opacity=".8"/></symbol>
 </svg>'''
 r'''<div class="wrap"><div class="dg-wrap">
 <section class="dg-screen on" id="dgChooser">
  <div style="text-align:center;padding:10px 0 2px">
   <div class="dg-eb">CARD DIAGNOSIS</div>
   <h1 style="font-weight:330;font-size:27px;letter-spacing:-1px;line-height:1.2;margin:11px 0 0">어떤 진단을<br>받아볼까요?</h1>
   <p style="font-weight:400;font-size:13px;color:rgba(0,0,0,.58);margin:9px 0 0">좌우로 넘겨 보고 골라주세요</p>
  </div>
  <div class="dg-swipe" id="dgSwipe">
   <article class="dg-scard sc-b">
    <div class="sc-ic"><svg><use href="#p-coins"/></svg></div>
    <div class="sc-eb">NEW · 캐시백 진단</div>
    <h3>캐시백 최적 카드사 진단</h3>
    <div class="sc-d">관심 카드사를 고르고 소비 유형을 답하면, 받을 수 있는 예상 캐시백을 카드사·플랫폼별로 추정해 드려요.</div>
    <ul><li><svg><use href="#dg-check"/></svg> 카드사 복수 선택 · 질문 7개</li><li><svg><use href="#dg-check"/></svg> 예상 캐시백 금액 + 최적 플랫폼</li></ul>
    <div class="sc-sp"></div>
    <button class="dg-cta" data-scn="2" style="margin-top:18px">캐시백 진단 시작 <svg><use href="#dg-right"/></svg></button>
   </article>
   <article class="dg-scard sc-a">
    <div class="sc-ic"><svg><use href="#tyr"/></svg></div>
    <div class="sc-eb">카드 성향 진단 · 60초</div>
    <h3>카드 성향 진단</h3>
    <div class="sc-d">6개 질문으로 내 소비 성향에 맞는 카드 1종과 지금 가장 큰 발급 캐시백 플랫폼을 찾아드려요.</div>
    <ul><li><svg><use href="#dg-check"/></svg> 질문 6개 · 약 1분</li><li><svg><use href="#dg-check"/></svg> 맞춤 카드 + 마감 임박 이벤트</li></ul>
    <div class="sc-sp"></div>
    <button class="dg-cta" data-scn="1" style="margin-top:18px">성향 진단 시작 <svg><use href="#dg-right"/></svg></button>
   </article>
  </div>
  <div class="dg-dots" id="dgDots"><span class="on"></span><span></span></div>
 </section>
 <section class="dg-screen" id="dgIntro">
  <div class="dg-top" style="justify-content:flex-start;gap:8px"><button class="dg-icnbtn" id="dgIntroBack"><svg><use href="#dg-back"/></svg></button><span class="dg-step">카드 성향 진단</span></div>
  <div class="dg-intro-hero">
   <div class="dg-eb">CARD DIAGNOSIS · 60초</div>
   <div class="dg-tcircle" style="margin:14px auto 4px;width:118px;height:118px;background:rgba(255,255,255,.55)"><span class="egg-wrap"><svg width="72" height="90" viewBox="0 0 100 120"><use href="#egg-whole"/></svg></span></div>
   <h1>6개 질문이면<br>내 카드가 보여요</h1>
   <p>2지선다만 누르면 끝. 당신께 맞는 카드와 지금 가장 큰 캐시백 플랫폼·마감 임박 이벤트까지 찾아드려요.</p>
  </div>
  <div style="padding:18px 0 0"><button class="dg-cta" id="dgStart">진단 시작하기 <svg><use href="#dg-right"/></svg></button>
   <p class="dg-note">약 1분 소요 · 가입 없이 바로</p><div style="text-align:center;margin-top:14px"><button id="dgShareIntro" style="display:inline-flex;align-items:center;gap:7px;background:none;border:1px solid var(--line,#e6e6e6);border-radius:50px;padding:10px 18px;font-weight:600;font-size:13px;color:var(--sub,#666);cursor:pointer"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg> 친구에게 공유</button></div></div>
 </section>
 <section class="dg-screen" id="dgQuestion">
  <div class="dg-top"><button class="dg-icnbtn" id="dgBack"><svg><use href="#dg-back"/></svg></button><span class="dg-step" id="dgStepN">01 / 06</span><button class="dg-icnbtn" id="dgClose"><svg><use href="#dg-x"/></svg></button></div>
  <div class="dg-prog"><i id="dgProg" style="width:16.6%"></i></div>
  <div class="dg-card"><div class="dg-qgrid">
   <div class="qleft"><div class="dg-tcircle" id="dgTcPc" style="width:150px;height:150px;background:var(--block-lime)"><span class="egg-shake"><svg width="86" height="106" viewBox="0 0 100 120"><use id="dgEggPc" href="#egg-crack1"/></svg></span><span class="prop" id="dgPropPc" style="width:48px;height:48px"><svg width="26" height="26"><use href="#p-globe"/></svg></span></div><div class="dg-eb" id="dgThemePc" style="margin-top:20px">STEP 01 · 소비처</div></div>
   <div class="qright">
    <div class="dg-qhead mo" style="padding:18px 0 0"><div class="dg-tcircle" id="dgTcMo" style="width:128px;height:128px;margin:0 auto;background:var(--block-lime)"><span class="egg-shake"><svg width="74" height="92" viewBox="0 0 100 120"><use id="dgEggMo" href="#egg-crack1"/></svg></span><span class="prop" id="dgPropMo" style="width:42px;height:42px"><svg width="23" height="23"><use href="#p-globe"/></svg></span></div><div class="dg-eb" id="dgThemeMo" style="margin-top:10px">STEP 01 · 소비처</div></div>
    <h2 id="dgQ">질문</h2>
    <div class="dg-choices" id="dgChoices"></div>
   </div>
  </div></div>
 </section>
 <section class="dg-screen" id="dgResult">
  <div class="dg-top"><div style="display:flex;align-items:center;gap:7px"><svg width="20" height="20"><use href="#mk"/></svg><span style="font-weight:700;font-size:13.5px;letter-spacing:-.3px">진단 완료</span></div><button class="dg-icnbtn" id="dgClose2"><svg><use href="#dg-x"/></svg></button></div>
  <div class="dg-card"><div class="dg-rgrid">
   <div class="rleft" id="dgRleft"></div>
   <div class="rright">
    <div class="dg-rhero" id="dgRhero"></div>
    <div class="dg-sec"><div class="dg-eb">왜 이 카드?</div><div class="dg-chips" id="dgWhy"></div></div>
    <div class="dg-sec"><div style="display:flex;align-items:baseline;justify-content:space-between"><div class="dg-eb">지금 발급 캐시백</div><div style="font-weight:400;font-size:11px;color:rgba(0,0,0,.5)" id="dgBarsCap">플랫폼 비교</div></div><div class="dg-bars" id="dgBars"></div></div>
    <div class="dg-sec"><div class="dg-eb">마감 임박 이벤트</div><div id="dgEvents" style="margin-top:8px"></div></div>
    <div class="dg-sec dg-dist"><div style="display:flex;align-items:baseline;justify-content:space-between"><div class="dg-eb">내 진단 유형 비중</div><div style="font-weight:400;font-size:11px;color:rgba(0,0,0,.5)" id="dgDistCap">최근 30일</div></div><div class="bar" id="dgDistBar"></div><div class="lg" id="dgDistLg"></div></div>
    <div class="dg-rcta"><a class="dg-cta" id="dgGo" href="#">발급 이벤트 전체 보기 <svg><use href="#dg-right"/></svg></a><button class="dg-redo" id="dgRedo"><svg><use href="#dg-redo"/></svg> 다시 진단하기</button><button class="dg-redo" id="dgShareResult"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg> 결과 공유</button>
     <div class="dg-foot">추천은 입력한 응답 + 공개 캐시백 데이터 기준이에요. 금액은 최대 금액 기준(조건 충족 시)이며 수집 시점에 따라 달라질 수 있어요.</div></div>
   </div>
  </div></div>
 </section>
 <section class="dg-screen" id="dgS2Issuers">
  <div class="dg-top"><button class="dg-icnbtn" id="s2BackI"><svg><use href="#dg-back"/></svg></button><span class="dg-step">카드사 선택</span><button class="dg-icnbtn" id="s2CloseI"><svg><use href="#dg-x"/></svg></button></div>
  <div class="dg-qhead" style="padding:6px 12px 0"><div class="dg-tcircle" style="width:96px;height:96px;margin:2px auto 0;background:var(--block-lime)"><span class="egg-wrap"><svg width="58" height="72" viewBox="0 0 100 120"><use href="#egg-whole"/></svg></span></div><h2 style="font-weight:330;font-size:25px;letter-spacing:-.9px;line-height:1.25;margin:14px 0 0">관심 있는 카드사를<br>모두 골라주세요</h2><p style="font-weight:400;font-size:13px;color:rgba(0,0,0,.58);margin:9px 0 0">복수 선택할 수 있어요 · 고른 카드사끼리 비교해요</p></div>
  <div class="s2-iss-grid" id="s2IssGrid"></div>
  <div style="padding:18px 0 26px"><button class="dg-cta" id="s2IssNext" disabled>다음 <svg><use href="#dg-right"/></svg></button></div>
 </section>
 <section class="dg-screen" id="dgS2Question">
  <div class="dg-top"><button class="dg-icnbtn" id="s2Back"><svg><use href="#dg-back"/></svg></button><span class="dg-step" id="s2StepN">01 / 07</span><button class="dg-icnbtn" id="s2CloseQ"><svg><use href="#dg-x"/></svg></button></div>
  <div class="dg-prog"><i id="s2Prog" style="width:14.2%"></i></div>
  <div class="dg-card"><div class="dg-qgrid">
   <div class="qleft"><div class="dg-tcircle" id="s2TcPc" style="width:150px;height:150px;background:var(--block-lime)"><span class="egg-shake"><svg width="86" height="106" viewBox="0 0 100 120"><use id="s2EggPc" href="#egg-crack1"/></svg></span><span class="prop" id="s2PropPc" style="width:48px;height:48px"><svg width="26" height="26"><use href="#p-globe"/></svg></span></div><div class="dg-eb" id="s2ThemePc" style="margin-top:20px">STEP 01</div></div>
   <div class="qright">
    <div class="dg-qhead mo" style="padding:18px 0 0"><div class="dg-tcircle" id="s2TcMo" style="width:128px;height:128px;margin:0 auto;background:var(--block-lime)"><span class="egg-shake"><svg width="74" height="92" viewBox="0 0 100 120"><use id="s2EggMo" href="#egg-crack1"/></svg></span><span class="prop" id="s2PropMo" style="width:42px;height:42px"><svg width="23" height="23"><use href="#p-globe"/></svg></span></div><div class="dg-eb" id="s2ThemeMo" style="margin-top:10px">STEP 01</div></div>
    <h2 id="s2Q">질문</h2>
    <div class="dg-choices" id="s2Choices"></div>
   </div>
  </div></div>
 </section>
 <section class="dg-screen" id="dgS2Result">
  <div class="dg-top"><div style="display:flex;align-items:center;gap:7px"><svg width="20" height="20"><use href="#mk"/></svg><span style="font-weight:700;font-size:13.5px;letter-spacing:-.3px">캐시백 진단 완료</span></div><button class="dg-icnbtn" id="s2Close2"><svg><use href="#dg-x"/></svg></button></div>
  <div class="dg-card"><div class="dg-rgrid">
   <div class="rleft" id="s2Rleft"></div>
   <div class="rright">
    <div class="dg-rhero" id="s2Rhero"></div>
    <div class="dg-sec"><div class="dg-eb">예상 캐시백 분해</div><div class="s2-brk" id="s2Brk"></div></div>
    <div class="dg-sec"><div class="dg-eb">카드사별 예상 캐시백</div><div class="dg-bars" id="s2Bars" style="margin-top:11px"></div></div>
    <div class="dg-rcta"><a class="dg-cta" id="s2Go" href="#">이 카드 발급 이벤트 보기 <svg><use href="#dg-right"/></svg></a><button class="dg-redo" id="s2Redo"><svg><use href="#dg-redo"/></svg> 다른 진단하기</button>
     <div class="dg-foot">예상 금액은 선택한 소비 유형 + 공개 캐시백 데이터 기반 추정치예요. 실제 지급은 카드사·플랫폼별 조건·수집 시점에 따라 달라질 수 있어요.</div></div>
   </div>
  </div></div>
 </section>
 </div></div>''')
DIAG_JS=r"""
var PORD=['toss','naver','kakaopay','ajungdang','cardgorilla','banksalad'];
var PN={toss:'토스',cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',ajungdang:'아정당',naver:'네이버페이',kakaopay:'카카오페이',issuer:'카드사 직접'};
var PC={toss:'#3182F6',cardgorilla:'#FF6A13',banksalad:'#19C37D',ajungdang:'#1B64DA',naver:'#03C75A',kakaopay:'#FEE500'};
var QS=[
 {theme:'소비처',q:'어디서 결제가 더 잦나요?',prop:'#p-globe',bg:'var(--block-lime)',opts:[
   {l:'해외·여행',s:'출장·여행·직구가 많아요',tk:'overseas'},{l:'국내 일상',s:'국내 생활 결제 위주예요',tk:'domestic'}]},
 {theme:'카드 실적',q:'월 카드값, 보통 얼마쯤 쓰세요?',prop:'#p-receipt',bg:'var(--block-lilac)',opts:[
   {l:'30만원 미만',s:'가볍게 쓰는 편',tk:'nospend'},{l:'30~80만원',s:'딱 생활비만큼',tk:'nospend'},{l:'80만원 이상',s:'메인카드로 몰아서',tk:'spend'}]},
 {theme:'혜택 취향',q:'더 끌리는 혜택은 어느 쪽인가요?',prop:'#p-spark',bg:'var(--block-mint)',opts:[
   {l:'포인트·마일리지 적립',s:'쌓아서 크게 쓰는 맛',tk:'point'},{l:'즉시 캐시백·할인',s:'결제할 때 바로 돌려받기',tk:'cash'}]},
 {theme:'연회비',q:'연회비는 어느 정도가 좋아요?',prop:'#p-coins',bg:'var(--block-pink)',opts:[
   {l:'프리미엄도 OK',s:'혜택 크면 연회비 감수',tk:'premium'},{l:'실속·저연회비',s:'부담 없는 쪽이 좋아요',tk:'value'}]},
 {theme:'주력 소비',q:'어디에 가장 많이 쓰세요?',prop:'#p-bag',bg:'var(--block-cream)',hint:'최대 8개 중 하나를 골라주세요',opts:[
   {l:'온라인 쇼핑',icon:'#c-cart',tk:'shopping'},{l:'마트·편의점',icon:'#c-store',tk:'shopping'},{l:'카페·외식',icon:'#c-cup',tk:'transit'},{l:'교통·주유',icon:'#c-car',tk:'transit'},
   {l:'통신·구독',icon:'#c-phone',tk:'shopping'},{l:'해외·여행',icon:'#c-plane',tk:'overseas'},{l:'병원·약국',icon:'#c-cross',tk:'value'},{l:'공과금·기타',icon:'#c-bill',tk:'transit'}]},
 {theme:'사용 스타일',q:'카드는 어떻게 쓰는 편이에요?',prop:'#p-crown',bg:'var(--block-coral)',opts:[
   {l:'한 장에 몰아쓰기',s:'주력 카드 하나면 충분',tk:'single'},{l:'여러 장 가볍게',s:'상황 따라 나눠 써요',tk:'multi'}]}
];
var ARCH=[
 {iss:'삼성카드',type:'트래블·해외형',chips:['해외 결제','무실적','즉시 캐시백'],likes:['overseas','nospend','cash','value','single']},
 {iss:'현대카드',type:'프리미엄형',chips:['마일 적립','프리미엄','여행'],likes:['overseas','spend','point','premium','single']},
 {iss:'KB국민카드',type:'캐시백·실속형',chips:['일상 캐시백','무실적','생활'],likes:['domestic','nospend','cash','value','single']},
 {iss:'신한카드',type:'온라인쇼핑형',chips:['구독 할인','즉시 캐시백','일상'],likes:['domestic','cash','shopping','value','multi']},
 {iss:'롯데카드',type:'온라인쇼핑형',chips:['온라인 쇼핑','적립','생활'],likes:['domestic','shopping','cash','single']},
 {iss:'우리카드',type:'교통·생활형',chips:['교통·통신','실속','생활'],likes:['domestic','transit','value','multi']},
 {iss:'하나카드',type:'교통·생활형',chips:['주유','즉시 캐시백','생활'],likes:['domestic','transit','cash','value']},
 {iss:'BC카드',type:'교통·생활형',chips:['배달·외식','즉시 캐시백','생활'],likes:['domestic','transit','cash','multi']}
];
// 진단 유형 비중(최근 30일 누적, 예시) — 결과에서 내 유형만 강조
var DIST=[{type:'트래블·해외형',pct:32,color:'#9a86e8'},{type:'캐시백·실속형',pct:24,color:'#3182F6'},{type:'온라인쇼핑형',pct:21,color:'#19C37D'},{type:'교통·생활형',pct:14,color:'#FF6A13'},{type:'프리미엄형',pct:9,color:'#1a1714'}];
function issAlias(s){s=s||'';if(/국민/.test(s))return 'KB국민카드';if(/^bc|비씨|바로/i.test(s))return 'BC카드';if(/신한/.test(s))return '신한카드';if(/현대/.test(s))return '현대카드';if(/삼성/.test(s))return '삼성카드';if(/롯데/.test(s))return '롯데카드';if(/우리/.test(s))return '우리카드';if(/하나/.test(s))return '하나카드';return s;}
function _wm(n){if(!n)return'0원';if(n>=10000){var m=n/10000;return (m>=10?Math.round(m):Math.round(m*10)/10)+'만원';}return n.toLocaleString()+'원';}
function platMap(p){var o={};(p.events||[]).forEach(function(e){if(e.platform==='issuer')return;var w=e.reward_won||0;if(w>(o[e.platform]||0))o[e.platform]=w;});return o;}
function maxRw(p){var m=0;(p.events||[]).forEach(function(e){if(e.platform!=='issuer'&&(e.reward_won||0)>m)m=e.reward_won;});return m;}
var PRODS=[],IMGN={};
var state={screen:'intro',step:0,answers:[]};
var LS='ct_diag_v2';
function save(){try{localStorage.setItem(LS,JSON.stringify({step:state.step,answers:state.answers}));}catch(e){}}
function load(){try{var j=JSON.parse(localStorage.getItem(LS)||'null');if(j&&j.answers)return j;}catch(e){}return null;}
function clearLS(){try{localStorage.removeItem(LS);}catch(e){}}
var REDUCE=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function show(id){var ss=document.querySelectorAll('.dg-screen');for(var i=0;i<ss.length;i++)ss[i].classList.toggle('on',ss[i].id===id);window.scrollTo(0,0);}
function eggStage(n,N){var p=n/N;if(p<=0.34)return'#egg-crack1';if(p<=0.7)return'#egg-crack2';return'#egg-crack3';}
function setEgg(ids,n,N){var h=eggStage(n,N);ids.forEach(function(id){var el=document.getElementById(id);if(el)el.setAttribute('href',h);});}
function setTheme(){var Q=QS[state.step];var n=state.step+1;
 document.getElementById('dgStepN').textContent=(n<10?'0'+n:n)+' / 06';
 document.getElementById('dgProg').style.width=(n/6*100)+'%';
 document.getElementById('dgQ').textContent=Q.q;
 var th='STEP '+(n<10?'0'+n:n)+' · '+Q.theme;
 ['dgThemePc','dgThemeMo'].forEach(function(id){document.getElementById(id).textContent=th;});
 ['dgTcPc','dgTcMo'].forEach(function(id){document.getElementById(id).style.background=Q.bg;});
 ['dgPropPc','dgPropMo'].forEach(function(id){document.getElementById(id).querySelector('use').setAttribute('href',Q.prop);});
 setEgg(['dgEggPc','dgEggMo'],n,6);
 var sel=state.answers[state.step];var C=document.getElementById('dgChoices');
 if(Q.opts.length<=3){C.className='dg-choices';
  C.innerHTML=Q.opts.map(function(o,i){var on=sel===i;var key=String.fromCharCode(65+i);
   return '<button class="choice'+(on?' sel':'')+'" data-opt="'+i+'"><span class="k">'+(on?'<svg><use href="#dg-check"/></svg>':key)+'</span><span style="flex:1"><span class="cl">'+o.l+'</span>'+(o.s?'<span class="cs">'+o.s+'</span>':'')+'</span></button>';}).join('');
 }else{C.className='dg-grid';
  C.innerHTML=(Q.hint?'<div style="grid-column:1/-1;font-weight:400;font-size:11.5px;color:rgba(0,0,0,.5);margin:-2px 0 2px">'+Q.hint+'</div>':'')
   +Q.opts.map(function(o,i){var on=sel===i;return '<button class="dg-gopt'+(on?' sel':'')+'" data-opt="'+i+'"><span class="gi"><svg><use href="'+(o.icon||'#c-cart')+'"/></svg></span><span class="gt">'+o.l+'</span></button>';}).join('');
 }
}
function gotoStep(i){state.step=i;state.screen='q';show('dgQuestion');setTheme();save();}
function choose(idx){idx=parseInt(idx);if(isNaN(idx))return;var Q=QS[state.step];if(idx<0||idx>=Q.opts.length)return;state.answers[state.step]=idx;
 var btns=document.getElementById('dgChoices').querySelectorAll('[data-opt]');btns.forEach(function(b){var on=parseInt(b.getAttribute('data-opt'))===idx;b.classList.toggle('sel',on);if(on&&b.classList.contains('choice')){var k=b.querySelector('.k');if(k)k.innerHTML='<svg><use href="#dg-check"/></svg>';}});
 save();
 var next=function(){if(state.step>=QS.length-1){finish();}else{gotoStep(state.step+1);}};
 if(REDUCE)next();else setTimeout(next,220);
}
function pickArch(){var toks=state.answers.map(function(idx,i){return (QS[i].opts[idx]||{}).tk;}).filter(Boolean);
 var scored=ARCH.map(function(a){var sc=toks.filter(function(t){return a.likes.indexOf(t)>=0;}).length;var card=pickCard(a);return {a:a,sc:sc,card:card,cmax:card?maxRw(card):-1};});
 scored=scored.filter(function(x){return x.card;});
 scored.sort(function(x,y){return (y.sc-x.sc)||(y.cmax-x.cmax);});
 return scored[0]||null;}
function pickCard(a){var ps=PRODS.filter(function(p){return issAlias(p.issuer)===a.iss&&maxRw(p)>0;});if(!ps.length)return null;
 ps.sort(function(x,y){return maxRw(y)-maxRw(x);});return ps[0];}
function _norm(d){return (d||'').replace(/\./g,'-').slice(0,10);}
function dday(pe){if(!pe)return null;var t=_norm(pe);var end=new Date(t+'T23:59:59');if(isNaN(end))return null;var now=new Date();var ms=end-now;var d=Math.ceil(ms/86400000);return d;}
function finish(){var r=pickArch();if(!r){show('dgResult');document.getElementById('dgRhero').innerHTML='<p style="padding:30px">추천 데이터를 불러오지 못했어요. 다시 시도해 주세요.</p>';return;}
 var a=r.a,card=r.card;var img=card.img||IMGN[(card.name||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'')]||'';
 var desc=({'삼성카드':'해외·여행에 강하고 무실적 캐시백까지 — 당신의 응답에 가장 잘 맞았어요.','현대카드':'마일·포인트 적립과 프리미엄 혜택 — 6개 응답에 가장 잘 맞았어요.','KB국민카드':'조건 없이 일상에서 즉시 캐시백 — 당신의 응답에 가장 잘 맞았어요.','신한카드':'구독·온라인 결제에서 즉시 돌려받기 — 응답에 가장 잘 맞았어요.','롯데카드':'온라인 쇼핑 적립에 강한 한 장 — 응답에 가장 잘 맞았어요.','우리카드':'교통·통신 등 생활 고정비를 알뜰하게 — 응답에 잘 맞았어요.','하나카드':'주유·생활 결제에서 즉시 캐시백 — 응답에 가장 잘 맞았어요.','BC카드':'배달·외식 등 일상 결제 캐시백 — 응답에 잘 맞았어요.'})[a.iss]||'당신의 응답에 가장 잘 맞는 카드예요.';
 var plateImg=img?'<img src="'+encodeURI(img)+'" alt="" onerror="this.style.display=\'none\'">':'';
 var heroInner='<span class="dg-badge">당신의 카드</span><div class="dg-plate"><div class="pl">'+plateImg+'</div><span class="tyr egg-hatch-wrap"><svg width="64" height="76" viewBox="0 0 100 120"><use href="#egg-hatch"/></svg></span></div><h2>'+card.name+'</h2><div class="rd">'+desc+'</div>';
 document.getElementById('dgRhero').innerHTML=heroInner;
 // desktop left (mirror hero)
 document.getElementById('dgRleft').innerHTML='<span class="dg-badge">당신의 카드</span><div class="dg-plate" style="margin-top:20px"><div class="pl">'+plateImg+'</div><span class="tyr egg-hatch-wrap"><svg width="70" height="84" viewBox="0 0 100 120"><use href="#egg-hatch"/></svg></span></div><h2 style="font-weight:700;font-size:24px;letter-spacing:-.7px;line-height:1.22;margin:20px 0 0">'+card.name+'</h2><div class="rd" style="font-size:13.5px;color:rgba(0,0,0,.66);margin:9px 4px 0">'+desc+'</div><div class="dg-chips" style="justify-content:center;margin-top:16px">'+a.chips.map(function(c){return '<span style="background:rgba(255,255,255,.6);border:0">'+c+'</span>';}).join('')+'</div>';
 document.getElementById('dgWhy').innerHTML=a.chips.map(function(c){return '<span>'+c+'</span>';}).join('');
 // platform bars
 var pm=platMap(card);var ks=PORD.filter(function(p){return pm[p];}).sort(function(x,y){return pm[y]-pm[x];});var mx=ks.length?pm[ks[0]]:0;
 document.getElementById('dgBarsCap').textContent='플랫폼 '+ks.length+'곳 비교';
 document.getElementById('dgBars').innerHTML=ks.length?ks.map(function(p,i){var best=i===0;return '<div class="dg-bar"><span class="bn" style="font-weight:'+(best?700:400)+'">'+PN[p]+'</span><span class="bt"><i style="width:'+Math.max(8,Math.round(pm[p]/mx*100))+'%;background:'+(best?PC[p]:'rgba(0,0,0,.16)')+'"></i></span><span class="ba" style="font-weight:'+(best?700:400)+'">'+_wm(pm[p])+'</span></div>';}).join(''):'<div style="font-size:13px;color:rgba(0,0,0,.45);padding:6px 0">이 카드의 플랫폼 캐시백 데이터를 준비 중이에요.</div>';
 // events (마감임박)
 var evs=(card.events||[]).filter(function(e){return e.platform!=='issuer'&&e.reward_won;}).map(function(e){var d=dday(e.period_end);return {e:e,d:d};}).filter(function(x){return x.d===null||x.d>=0;});
 evs.sort(function(x,y){var dx=x.d===null?9999:x.d,dy=y.d===null?9999:y.d;return dx-dy;});
 evs=evs.slice(0,4);
 var cgUrl=function(e,pl){return e.url||((card.platforms||{})[e.platform]||{}).url||('events.html?platform='+e.platform+'&n='+encodeURIComponent(card.name));};
 document.getElementById('dgEvents').innerHTML=evs.length?evs.map(function(x){var e=x.e;var dl=x.d===null?'진행중':(x.d<=0?'오늘 마감':'D-'+x.d);var title=(e.reward_text&&e.reward_text.length<40)?e.reward_text:('최대 '+_wm(e.reward_won)+' 캐시백');
  return '<a class="dg-evrow" href="'+cgUrl(e)+'" rel="sponsored nofollow noopener" target="_blank"><span class="dot" style="background:'+(PC[e.platform]||'#888')+'"></span><div style="flex:1;min-width:0"><div class="et">'+title+'</div><div class="ep">'+(PN[e.platform]||e.platform)+' · 외부 광고 링크</div></div><span class="dd">'+dl+'</span></a>';
 }).join(''):'<div style="font-size:13px;color:rgba(0,0,0,.45);padding:10px 0">마감 임박 이벤트가 없어요. 카드 상세에서 전체 이벤트를 확인하세요.</div>';
 document.getElementById('dgGo').setAttribute('href','carddetail.html?n='+encodeURIComponent(card.name));
 renderDist(a.type);
 state.screen='result';show('dgResult');clearLS();
}
// 내 진단 유형 비중(스택바+범례, 내 유형만 강조) — 최근 30일 누적(예시)
function renderDist(myType){var bar=document.getElementById('dgDistBar'),lg=document.getElementById('dgDistLg');if(!bar||!lg)return;
 bar.innerHTML=DIST.map(function(d){return '<span style="width:'+d.pct+'%;background:'+d.color+';opacity:'+(d.type===myType?'1':'.4')+'"></span>';}).join('');
 lg.innerHTML=DIST.map(function(d){var me=d.type===myType;return '<span class="it" style="opacity:'+(me?'1':'.4')+'"><span class="dt" style="background:'+d.color+'"></span><span class="nm" style="font-weight:'+(me?700:540)+'">'+d.type+'</span><span class="pc">'+d.pct+'%</span>'+(me?'<span class="me">내 유형</span>':'')+'</span>';}).join('');
}
function startFresh(){state.step=0;state.answers=[];gotoStep(0);}
function dgToast(m){var t=document.createElement("div");t.textContent=m;t.style.cssText="position:fixed;left:50%;bottom:40px;transform:translateX(-50%);background:#000;color:#fff;padding:11px 18px;border-radius:50px;font-size:13px;font-weight:600;z-index:9999;opacity:0;transition:opacity .2s";document.body.appendChild(t);requestAnimationFrame(function(){t.style.opacity="1";});setTimeout(function(){t.style.opacity="0";setTimeout(function(){t.remove();},300);},1800);}
function dgShare(isResult){var url=location.origin+"/diagnose.html";var text=isResult?"내 카드, 60초 만에 진단받았어요 — 카드티라노":"60초 2지선다로 내게 맞는 카드 찾기 — 카드티라노";if(navigator.share){navigator.share({title:"카드티라노 카드 진단",text:text,url:url}).catch(function(){});return;}var sx=text+" "+url;if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(sx).then(function(){dgToast("링크를 복사했어요");},function(){window.prompt("아래 링크를 복사하세요",sx);});}else{window.prompt("아래 링크를 복사하세요",sx);}}
/* ===== 시나리오 2 · 캐시백 최적 카드사 진단 ===== */
var S2ISS=[
 {k:'samsung',label:'삼성'},{k:'hyundai',label:'현대'},{k:'kb',label:'KB국민'},{k:'shinhan',label:'신한'},
 {k:'lotte',label:'롯데'},{k:'woori',label:'우리'},{k:'hana',label:'하나'},{k:'nh',label:'NH농협'}
];
function s2match(raw,k){raw=raw||'';switch(k){
 case 'samsung':return /삼성/.test(raw);
 case 'hyundai':return /현대/.test(raw)&&!/백화점/.test(raw);
 case 'kb':return /KB|국민/.test(raw);
 case 'shinhan':return /신한/.test(raw);
 case 'lotte':return /롯데/.test(raw);
 case 'woori':return /우리/.test(raw);
 case 'hana':return /하나/.test(raw);
 case 'nh':return /NH|농협/.test(raw);}return false;}
var S2Q=[
 {key:'overseas',theme:'해외 결제',prop:'#p-globe',bg:'var(--block-lime)',q:'해외 결제, 자주 하시나요?',a:{l:'자주 해요',s:'출장·여행·직구가 많아요'},b:{l:'거의 안 해요',s:'국내 결제 위주예요'}},
 {key:'channel',theme:'쇼핑 채널',prop:'#p-bag',bg:'var(--block-lilac)',q:'쇼핑은 주로 어디서 하세요?',a:{l:'대형마트·오프라인',s:'이마트·홈플러스 등'},b:{l:'온라인 쇼핑',s:'쿠팡·네이버·11번가 등'}},
 {key:'transit',theme:'교통·주유',prop:'#p-coins',bg:'var(--block-mint)',q:'교통·주유, 월 10만원 이상 쓰세요?',a:{l:'네, 많이 써요',s:'대중교통·주유가 잦아요'},b:{l:'적은 편이에요',s:'이동이 많지 않아요'}},
 {key:'autopay',theme:'자동납부',prop:'#p-receipt',bg:'var(--block-pink)',q:'통신·공과금을 카드 자동납부 하세요?',a:{l:'자동납부 해요',s:'통신·공과금을 카드로'},b:{l:'안 해요',s:'따로 납부해요'}},
 {key:'pay',theme:'간편결제',prop:'#p-spark',bg:'var(--block-cream)',q:'카카오·네이버페이 등 간편결제 자주 쓰세요?',a:{l:'자주 써요',s:'간편결제가 익숙해요'},b:{l:'잘 안 써요',s:'실물 카드를 주로'}},
 {key:'highspend',theme:'월 사용액',prop:'#p-crown',bg:'var(--block-coral)',q:'월 카드 사용액이 50만원 이상인가요?',a:{l:'네, 50만+',s:'실적 채울 수 있어요'},b:{l:'그보다 적어요',s:'가볍게 쓰는 편이에요'}},
 {key:'subscribe',theme:'구독',prop:'#p-spark',bg:'var(--block-lime)',q:'넷플릭스·유튜브 등 구독 서비스 쓰세요?',a:{l:'이용해요',s:'OTT·멤버십 구독 중'},b:{l:'안 써요',s:'구독은 없어요'}}
];
var s2={iss:[],step:0,ans:{}};
function s2Flags(){return{overseas:s2.ans.overseas==='a',shopping:!!s2.ans.channel,transit:s2.ans.transit==='a',autopay:s2.ans.autopay==='a',pay:s2.ans.pay==='a',highspend:s2.ans.highspend==='a',subscribe:s2.ans.subscribe==='a'};}
function s2Tok(t){if(/해외/.test(t))return'overseas';if(/자동납부|생활요금|공과금|통신/.test(t))return'autopay';if(/간편결제|페이/.test(t))return'pay';if(/구독|넷플릭스|ott/i.test(t))return'subscribe';if(/마케팅/.test(t))return'marketing';if(/추가/.test(t))return'extra';return null;}
function s2Parse(e){var bd=(e.breakdown||[]).map(function(b){return b.text||'';}).join(' ');var t=bd||(e.reward_text||'');var re=/(해외|자동납부|생활요금|공과금|통신|간편결제|페이|구독|넷플릭스|마케팅|추가)\s*(?:최대\s*)?(\d+(?:\.\d+)?)\s*만/g;var cats={},m;while((m=re.exec(t))){var c=s2Tok(m[1]);if(!c)continue;cats[c]=(cats[c]||0)+Math.round(parseFloat(m[2])*10000);}return cats;}
var S2LAB={overseas:'해외 결제',autopay:'통신·공과금 자동납부',pay:'간편결제',subscribe:'구독 서비스',marketing:'마케팅 동의',extra:'추가 이용 실적',bonus:'부가 캐시백'};
function s2Est(e,f){
 var bonusMax=e.bonus_won||0;var main=e.main_won||Math.max(0,(e.reward_won||0)-bonusMax);
 var cats=s2Parse(e);var enable={overseas:f.overseas,autopay:f.autopay,pay:f.pay,subscribe:f.subscribe,marketing:true,extra:f.highspend};
 var got=0,detail=[];
 for(var c in cats){var on=!!enable[c];if(on)got+=cats[c];detail.push({cat:c,label:S2LAB[c]||c,won:cats[c],on:on});}
 if(bonusMax>0&&got>bonusMax)got=bonusMax;
 if(!detail.length&&bonusMax>0){var ks=['overseas','autopay','pay','subscribe'];var oc=ks.filter(function(k){return f[k];}).length;got=Math.round(bonusMax*(0.4+0.15*oc));detail.push({cat:'bonus',label:S2LAB.bonus,won:got,on:oc>0});}
 var spendF=f.highspend?1:0.6;var mainGot=Math.round(main*spendF);
 var total=mainGot+got;var cap=e.reward_won||0;if(cap>0&&total>cap)total=cap;
 return{total:total,main:main,mainGot:mainGot,bonusGot:got,detail:detail,highspend:f.highspend};
}
function s2BestForIss(k,f){var best=null;PRODS.forEach(function(p){if(!s2match(p.issuer,k))return;(p.events||[]).forEach(function(e){if(e.platform==='issuer')return;var r=s2Est(e,f);if(r.total<=0)return;if(!best||r.total>best.total)best={total:r.total,est:r,product:p,event:e,platform:e.platform};});});return best;}
function s2PfStyle(pl){var bg=PC[pl]||'#000';var fg=(pl==='kakaopay')?'#1a1714':'#fff';return'background:'+bg+';color:'+fg;}
function s2Finish(){var f=s2Flags();
 var rows=s2.iss.map(function(k){var b=s2BestForIss(k,f);return{k:k,label:(S2ISS.filter(function(x){return x.k===k;})[0]||{}).label||k,best:b};}).filter(function(r){return r.best;});
 rows.sort(function(a,b){return b.best.total-a.best.total;});
 show('dgS2Result');
 if(!rows.length){document.getElementById('s2Rhero').innerHTML='<p style="padding:30px">선택한 카드사의 캐시백 데이터를 불러오지 못했어요. 다른 카드사로 다시 진단해 주세요.</p>';document.getElementById('s2Rleft').innerHTML='';document.getElementById('s2Brk').innerHTML='';document.getElementById('s2Bars').innerHTML='';return;}
 var top=rows[0],rec=top.best,ev=rec.event,p=rec.product,pl=rec.platform;
 var img=p.img||IMGN[(p.name||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'')]||'';
 var plateImg=img?'<img src="'+encodeURI(img)+'" alt="" onerror="this.style.display=\'none\'">':'';
 var pill='<span class="s2-pf" style="'+s2PfStyle(pl)+'">'+(PN[pl]||pl)+' 발급 기준</span>';
 var heroInner='<span class="dg-badge">추천 카드</span><div class="dg-plate"><div class="pl">'+plateImg+'</div><span class="tyr egg-hatch-wrap"><svg width="64" height="76" viewBox="0 0 100 120"><use href="#egg-hatch"/></svg></span></div><h2>'+p.name+'</h2>'
  +'<div class="rd">'+top.label+'카드 · 입력하신 소비 유형 기준 예상 캐시백이 가장 컸어요.</div>'
  +'<div class="s2-total" style="margin-top:14px"><div class="amt"><small>예상 </small>'+_wm(rec.total)+'</div></div>'
  +'<div style="margin-top:12px">'+pill+'</div>';
 document.getElementById('s2Rhero').innerHTML=heroInner;
 document.getElementById('s2Rleft').innerHTML='<span class="dg-badge">추천 카드</span><div class="dg-plate" style="margin-top:20px"><div class="pl">'+plateImg+'</div><span class="tyr egg-hatch-wrap"><svg width="70" height="84" viewBox="0 0 100 120"><use href="#egg-hatch"/></svg></span></div><h2 style="font-weight:700;font-size:22px;letter-spacing:-.6px;line-height:1.22;margin:20px 0 0">'+p.name+'</h2><div class="s2-total" style="margin-top:14px"><div class="amt"><small>예상 </small>'+_wm(rec.total)+'</div></div><div style="margin-top:14px">'+pill+'</div>';
 // 분해
 var brk=[{label:'주요 캐시백',sub:rec.est.highspend?'월 50만원+ 실적 충족 기준':'실적 미달 가정 — 60%만 반영',won:rec.est.mainGot,on:true}];
 rec.est.detail.forEach(function(d){brk.push({label:d.label,sub:d.on?'해당 소비에 적용':'해당 소비 없음 — 미반영',won:d.won,on:d.on});});
 document.getElementById('s2Brk').innerHTML=brk.map(function(b){var ic=b.on?'<span class="bi" style="background:#e7f8ec;color:#1a8f3a"><svg><use href="#dg-check"/></svg></span>':'<span class="bi" style="background:var(--surface-soft);color:rgba(0,0,0,.4)"><svg><use href="#dg-x"/></svg></span>';
  return '<div class="s2-brow'+(b.on?'':' off')+'">'+ic+'<span class="bl">'+b.label+'<small>'+b.sub+'</small></span><span class="bv" style="color:'+(b.on?'#000':'rgba(0,0,0,.4)')+'">'+(b.on?'+'+_wm(b.won):_wm(b.won))+'</span></div>';
 }).join('');
 // 카드사별 비교
 var mx=rows[0].best.total;
 document.getElementById('s2Bars').innerHTML=rows.map(function(r,i){var best=i===0;var pl2=r.best.platform;return '<div class="dg-bar"><span class="bn" style="font-weight:'+(best?700:400)+'">'+r.label+'</span><span class="bt"><i style="width:'+Math.max(8,Math.round(r.best.total/mx*100))+'%;background:'+(best?(PC[pl2]||'#000'):'rgba(0,0,0,.16)')+'"></i></span><span class="ba" style="font-weight:'+(best?700:400)+'">'+_wm(r.best.total)+'</span></div>';}).join('');
 document.getElementById('s2Go').setAttribute('href','carddetail.html?n='+encodeURIComponent(p.name));
}
function s2Start(){s2={iss:[],step:0,ans:{}};s2RenderIss();show('dgS2Issuers');}
function s2RenderIss(){var g=document.getElementById('s2IssGrid');g.innerHTML=S2ISS.map(function(x){var on=s2.iss.indexOf(x.k)>=0;return '<button class="s2-iss'+(on?' sel':'')+'" data-k="'+x.k+'"><span class="ck"><svg><use href="#dg-check"/></svg></span><span class="nm">'+x.label+'</span></button>';}).join('');document.getElementById('s2IssNext').disabled=s2.iss.length===0;}
function s2ToggleIss(k){var i=s2.iss.indexOf(k);if(i>=0)s2.iss.splice(i,1);else s2.iss.push(k);s2RenderIss();}
function s2SetQ(){var Q=S2Q[s2.step];var n=s2.step+1,N=S2Q.length;
 document.getElementById('s2StepN').textContent=(n<10?'0'+n:n)+' / '+(N<10?'0'+N:N);
 document.getElementById('s2Prog').style.width=(n/N*100)+'%';
 document.getElementById('s2Q').textContent=Q.q;
 var th='STEP '+(n<10?'0'+n:n)+' · '+Q.theme;
 ['s2ThemePc','s2ThemeMo'].forEach(function(id){document.getElementById(id).textContent=th;});
 ['s2TcPc','s2TcMo'].forEach(function(id){document.getElementById(id).style.background=Q.bg;});
 ['s2PropPc','s2PropMo'].forEach(function(id){document.getElementById(id).querySelector('use').setAttribute('href',Q.prop);});
 setEgg(['s2EggPc','s2EggMo'],n,N);
 var sel=s2.ans[Q.key];
 document.getElementById('s2Choices').innerHTML=[['A','a'],['B','b']].map(function(pp){var o=Q[pp[1]];var on=sel===pp[1];return '<button class="choice'+(on?' sel':'')+'" data-opt="'+pp[1]+'"><span class="k">'+(on?'<svg><use href="#dg-check"/></svg>':pp[0])+'</span><span style="flex:1"><span class="cl">'+o.l+'</span><span class="cs">'+o.s+'</span></span></button>';}).join('');
}
function s2GotoStep(i){s2.step=i;show('dgS2Question');s2SetQ();}
function s2Choose(opt){var Q=S2Q[s2.step];s2.ans[Q.key]=opt;
 var btns=document.getElementById('s2Choices').querySelectorAll('.choice');btns.forEach(function(b){var on=b.getAttribute('data-opt')===opt;b.classList.toggle('sel',on);if(on)b.querySelector('.k').innerHTML='<svg><use href="#dg-check"/></svg>';});
 var next=function(){if(s2.step>=S2Q.length-1)s2Finish();else s2GotoStep(s2.step+1);};
 if(REDUCE)next();else setTimeout(next,200);
}
function s2Dots(){var sw=document.getElementById('dgSwipe'),dots=document.getElementById('dgDots');if(!sw||!dots)return;var cs=sw.querySelectorAll('.dg-scard'),mid=sw.scrollLeft+sw.clientWidth/2,idx=0;for(var i=0;i<cs.length;i++){if(cs[i].offsetLeft<=mid)idx=i;}var ds=dots.children;for(var j=0;j<ds.length;j++)ds[j].classList.toggle('on',j===idx);}
function bind(){
 document.getElementById('dgStart').onclick=startFresh;
 var _si=document.getElementById('dgShareIntro');if(_si)_si.onclick=function(){dgShare(false);};
 var _sr=document.getElementById('dgShareResult');if(_sr)_sr.onclick=function(){dgShare(true);};
 document.getElementById('dgRedo').onclick=function(){clearLS();state.screen='intro';show('dgIntro');};
 document.getElementById('dgBack').onclick=function(){if(state.step<=0){state.screen='intro';show('dgIntro');}else gotoStep(state.step-1);};
 function close(){if(confirm('진단을 종료할까요? 진행 내용이 초기화됩니다.')){clearLS();state.step=0;state.answers=[];state.screen='intro';show('dgIntro');}}
 document.getElementById('dgClose').onclick=close;document.getElementById('dgClose2').onclick=function(){location.href='index.html';};
 document.getElementById('dgChoices').addEventListener('click',function(e){var b=e.target.closest('[data-opt]');if(b)choose(b.getAttribute('data-opt'));});
 document.addEventListener('keydown',function(e){if(state.screen!=='q')return;if(/^[1-8]$/.test(e.key))choose(parseInt(e.key)-1);else if(e.key==='ArrowLeft'){if(state.step>0)gotoStep(state.step-1);}});
 // 시나리오 선택(스와이프)
 var sw=document.getElementById('dgSwipe');if(sw){sw.addEventListener('scroll',s2Dots);s2Dots();sw.querySelectorAll('[data-scn]').forEach(function(btn){btn.onclick=function(){if(btn.getAttribute('data-scn')==='2')s2Start();else{clearLS();state.step=0;state.answers=[];state.screen='intro';show('dgIntro');}};});}
 var _ib=document.getElementById('dgIntroBack');if(_ib)_ib.onclick=function(){show('dgChooser');s2Dots();};
 // 시나리오2 바인딩
 document.getElementById('s2BackI').onclick=function(){show('dgChooser');s2Dots();};
 document.getElementById('s2CloseI').onclick=function(){show('dgChooser');s2Dots();};
 document.getElementById('s2IssGrid').addEventListener('click',function(e){var b=e.target.closest('.s2-iss[data-k]');if(b)s2ToggleIss(b.getAttribute('data-k'));});
 document.getElementById('s2IssNext').onclick=function(){if(!s2.iss.length)return;s2.step=0;s2.ans={};s2GotoStep(0);};
 document.getElementById('s2Back').onclick=function(){if(s2.step<=0)show('dgS2Issuers');else s2GotoStep(s2.step-1);};
 document.getElementById('s2CloseQ').onclick=function(){show('dgChooser');s2Dots();};
 document.getElementById('s2Choices').addEventListener('click',function(e){var b=e.target.closest('.choice[data-opt]');if(b)s2Choose(b.getAttribute('data-opt'));});
 document.getElementById('s2Close2').onclick=function(){show('dgChooser');s2Dots();};
 document.getElementById('s2Redo').onclick=function(){show('dgChooser');s2Dots();};
 document.addEventListener('keydown',function(e){if(!document.getElementById('dgS2Question').classList.contains('on'))return;if(e.key==='a'||e.key==='A')s2Choose('a');else if(e.key==='b'||e.key==='B')s2Choose('b');else if(e.key==='ArrowLeft'){if(s2.step>0)s2GotoStep(s2.step-1);else show('dgS2Issuers');}});
}
Promise.all([fetch('platform_events.json').then(function(r){return r.json();}),fetch('cards.json').then(function(r){return r.json();}).catch(function(){return {cards:{}};})]).then(function(A){
 PRODS=(A[0].products||[]);
 for(var k in (A[1].cards||{})){(A[1].cards[k]||[]).forEach(function(c){if(c.img)IMGN[(c.name||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'')]=c.img;});}
 // 카드 이미지 폴백: products img → cards.json IMGN 우선, 없으면 product.img
 PRODS.forEach(function(p){if(!p.img){var n=(p.name||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');if(IMGN[n])p.img=IMGN[n];}});
 bind();
 var saved=load();
 if(saved&&saved.answers&&saved.answers.length&&saved.answers.length<6){state.answers=saved.answers;gotoStep(Math.min(saved.answers.length,5));}
}).catch(function(){bind();});
"""
page("diagnose.html",BRAND+" | 카드 진단 · 성향/캐시백 2가지","2지선다 카드 성향 진단과 카드사·소비 유형 기반 예상 캐시백 진단 — 원하는 진단을 골라 내게 맞는 카드와 최적 플랫폼을 찾아드려요.","/diagnose.html",DIAG_BODY,DIAG_JS,active="diagnose")
page("discount.html",BRAND+" | 카드 할인 혜택 (가맹점·업종별)","네이버·쿠팡·무신사·이마트·GS25 등 가맹점의 카드 즉시할인·청구할인·캐시백·무이자할부를 업종·카드사별로.","/discount.html",DISC_BODY,DISC_JS,searchbar=True,catstrip=True,active="discount")
page("cards.html",BRAND+" | 카드 찾기 (카드사별 신용카드)","삼성·현대·신한·KB국민·롯데·우리·하나·NH농협·BC·IBK 카드사별 대표 신용카드를 플레이트 이미지·연회비·혜택으로 비교.","/cards.html",CARDS_BODY+SEO_STATIC_CARDS,CARDS_JS,active="cards")
page("issue.html",BRAND+" | 이번달 캐시백 (플랫폼별 비교)","카드사별 신규 발급 캐시백을 아정당·카드고릴라·토스·카카오페이 등 플랫폼별로 비교. 이번달 캐시백 리스트와 최대 혜택 비교표.","/issue.html",ISSUE_BODY+SEO_STATIC_ISSUE,ISSUE_JS,active="issue")
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
function rowHtml(p){var img=p.image||p.img||'';return '<a class="cm-row" href="community.html?id='+p.id+'" data-id="'+p.id+'">'+tag(p.category)+'<div class="cm-rb"><div class="cm-rt">'+esc(p.title)+(p.comment_count?' <span style="color:var(--accent-magenta);font-weight:800">['+p.comment_count+']</span>':'')+'</div><div class="cm-rm">'+esc(p.author_nickname||'익명')+' · '+ago(p.created_at)+' · 조회 '+(p.views||0)+'</div></div><div class="cm-rs"><b><svg viewBox="0 0 24 24" width="11" height="11" style="vertical-align:-1px" fill="currentColor" aria-hidden="true"><path d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> '+(p.likes||0)+'</b><br>댓글 '+(p.comment_count||0)+'</div>'+(img?'<span class="cm-th"><img src="'+esc(img)+'" alt=""></span>':'')+'</a>';}
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
 C.innerHTML=cs.map(function(c){var liked=lks('c'+c.id);var rep=c.parent_id?' reply':'';return '<div class="cm-cmt'+rep+'"><div class="cm-cmt-h"><span class="cm-cmt-n">'+ava(BMAP[c.category]?c.category:'자유게시판').replace('cm-ava','cm-ava" style="width:20px;height:20px')+esc(c.author_nickname||'익명')+' <span class="cm-cmt-t">'+ago(c.created_at)+'</span></span><span><button class="cm-cmt-a lk'+(liked?' on':'')+'" data-lc="'+c.id+'"><svg viewBox="0 0 24 24" width="11" height="11" style="vertical-align:-1px" fill="currentColor" aria-hidden="true"><path d="M12 20.3S3.8 15.3 3.8 9.4A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.2 2.4c0 5.9-8.2 10.9-8.2 10.9z"/></svg> <span>'+(c.likes||0)+'</span></button> <button class="cm-cmt-a" data-dc="'+c.id+'">삭제</button></span></div><div class="cm-cmt-c">'+esc(c.content)+'</div></div>';}).join('');
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
# ===== HTML 사이트맵 (전체 메뉴 · 크롤러/접근성용, 푸터에서 진입) =====
_SMAP=[
 ("카드 캐시백·혜택 비교",[
   ("issue.html","이번달 카드 캐시백 — 플랫폼별 최대 발급 캐시백 비교"),
   ("issue.html?v=cmp","한눈에 비교 — 카드사·카드별 캐시백 한 표"),
   ("discount.html","카드 할인 혜택 — 가맹점·업종별 즉시할인·청구할인·캐시백"),
   ("installment.html","무이자·부분무이자 할부 — 카드사·업종별"),
   ("events.html","발급 이벤트 상세 — 캐시백 추이·발급 적기")]),
 ("카드 찾기·추천",[
   ("cards.html","카드 찾기 — 카드사별 신용카드 혜택·연회비 비교"),
   ("diagnose.html","카드 진단 — 2지선다로 내게 맞는 카드·캐시백 추천"),
   ("chart.html","티라노차트 — 카드 인기·캐시백 랭킹"),
   ("trends.html","월별 캐시백 추이 — 발급 캐시백 변화 차트")]),
 ("가이드·커뮤니티",[
   ("content.html","카드 가이드 — 연회비 캐시백·전월실적·해외카드 꿀팁"),
   ("community.html","커뮤니티 — 카드 발급 후기·정보 공유")]),
 ("서비스 정보",[
   ("about.html","카드티라노란? — 서비스 소개"),
   ("business.html","사업자정보"),
   ("terms.html","이용약관"),
   ("privacy.html","개인정보처리방침")]),
]
SITEMAP_BODY=('<style>.smap{max-width:880px;margin:0 auto;padding:14px 0 8px}.smap h1{font-weight:330;font-size:30px;letter-spacing:-1.1px;margin:6px 0 0}'
 '.smap .sub{font-weight:400;font-size:13.5px;color:var(--sub);margin:8px 0 0;line-height:1.6}'
 '.smap section{margin-top:30px}.smap h2{font-size:16px;font-weight:800;letter-spacing:-.3px;margin:0 0 12px;padding-bottom:9px;border-bottom:1px solid var(--line)}'
 '.smap ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:9px 22px}'
 '.smap li a{display:block;font-size:14px;font-weight:600;color:var(--text);text-decoration:none;padding:4px 0}.smap li a:hover{color:var(--accent);text-decoration:underline}'
 '@media(max-width:620px){.smap ul{grid-template-columns:1fr}}'
 '</style>'
 '<div class="wrap"><div class="smap">'
 '<h1>사이트맵</h1><p class="sub">카드티라노의 카드 캐시백·카드 혜택·카드 발급 혜택 비교 메뉴를 한곳에 모았어요. 원하는 카테고리로 바로 이동하세요.</p>'
 +"".join('<section><h2>'+g+'</h2><ul>'+"".join('<li><a href="'+u+'">'+t+'</a></li>' for u,t in items)+'</ul></section>' for g,items in _SMAP)
 +'</div></div>')
page("sitemap.html",BRAND+" | 사이트맵 (전체 메뉴)","카드 캐시백·카드 혜택·카드 발급 혜택 비교 등 카드티라노 전체 메뉴를 한곳에. 이번달 캐시백, 카드 할인 혜택, 카드 찾기, 카드 진단, 무이자 할부까지.","/sitemap.html",SITEMAP_BODY,"",active="")

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
 ("/cards.html","daily","0.8"),("/diagnose.html","weekly","0.8"),("/content.html","weekly","0.8"),
 ("/chart.html","daily","0.7"),("/events.html","daily","0.7"),("/cashback.html","weekly","0.6"),
 ("/installment.html","weekly","0.6"),("/trends.html","weekly","0.6"),("/community.html","daily","0.6"),
 ("/about.html","monthly","0.5"),("/business.html","monthly","0.4"),("/search.html","weekly","0.4"),
 ("/sitemap.html","monthly","0.3"),("/terms.html","yearly","0.2"),("/privacy.html","yearly","0.2"),
]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p,cf,pr in SITEMAP_PAGES:
    fn=(p[1:] or "index.html")
    fp=os.path.join(SITE,fn)
    lm=datetime.date.fromtimestamp(os.path.getmtime(fp)).isoformat() if os.path.exists(fp) else _today
    sm+='<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n'%(BASE,p,lm,cf,pr)
# 인기 카드상세(carddetail?id=) URL을 사이트맵에 포함 — 카드별 색인 유도(JS가 카드별 canonical=?id= 로 갱신)
try:
    _cj=json.load(open(os.path.join(SITE,"cards.json"),encoding="utf-8"))
    _n2id={};_n2rk={}
    for _iss,_lst in (_cj.get("cards") or {}).items():
        for _c in _lst:
            _nm=re.sub(r"[^0-9a-z가-힣]","",(_c.get("name") or "").lower())
            if _c.get("id") is not None:_n2id[_nm]=_c["id"]
    try:_rkj=json.load(open(os.path.join(SITE,"rank.json"),encoding="utf-8"))
    except Exception:_rkj={"items":[]}
    _seen=set();_cardlm=datetime.date.fromtimestamp(os.path.getmtime(os.path.join(SITE,"carddetail.html"))).isoformat() if os.path.exists(os.path.join(SITE,"carddetail.html")) else _today
    for _it in (_rkj.get("items") or [])[:60]:
        _nm=re.sub(r"[^0-9a-z가-힣]","",(_it.get("name") or "").lower())
        _id=_n2id.get(_nm)
        if _id is None or _id in _seen:continue
        _seen.add(_id)
        sm+='<url><loc>%s/carddetail.html?id=%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.5</priority></url>\n'%(BASE,_id,_cardlm)
except Exception as _e:
    pass
# 카드 가이드 글(content?id=) — 정보성 검색 유입용
try:
    _ctj=json.load(open(os.path.join(SITE,"content.json"),encoding="utf-8"))
    _ctlm=datetime.date.fromtimestamp(os.path.getmtime(os.path.join(SITE,"content.html"))).isoformat() if os.path.exists(os.path.join(SITE,"content.html")) else _today
    for _it in (_ctj.get("items") or []):
        if _it.get("id") is None:continue
        sm+='<url><loc>%s/content.html?id=%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.5</priority></url>\n'%(BASE,_it["id"],_ctlm)
except Exception as _e:
    pass
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
