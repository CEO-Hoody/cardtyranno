# -*- coding: utf-8 -*-
"""카드티라노 프론트엔드 v2 — 다크테마(무신사 감성·카드고릴라 구조) + SEO/AEO 최적화.
데이터는 site/*.json(DB export) 런타임 fetch. AEO: JSON-LD, llms.txt, FAQ, AI 크롤러 허용.
"""
import os, json
OUT="/sessions/busy-charming-mayer/mnt/제휴마케팅 콜렉터"; SITE=os.path.join(OUT,"site")
BASE="https://cardtyranno.com"; BRAND="카드티라노"; BRAND_EN="CardTyranno"
DESC_SITE="여러 카드 중개 플랫폼(토스 카드라운지·카드고릴라·아정당·뱅크샐러드)의 카드 발급 혜택과 결제 할인 이벤트를 한곳에서 비교·분석하는 카드 비교 플랫폼."

CSS = r"""
:root{--bg:#f6f5f1;--surface:#ffffff;--surface2:#edebe4;--line:#e6e3da;--text:#16161b;--sub:#54545f;--dim:#8a8780;--accent:#ef5226;--accent-d:#d6420f;--blue:#2f6bff;--plate:#eceef2;--radius:18px}
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
.logo .rx{width:23px;height:23px;color:var(--accent);display:block;flex:0 0 auto}.logo b{color:var(--accent)}
.gnb{display:flex;gap:22px;font-size:15px;font-weight:700}
.gnb a{color:#55555e;padding:6px 0;position:relative}.gnb a:hover,.gnb a.on{color:var(--accent)}
.gnb a.on::after{content:"";position:absolute;left:0;right:0;bottom:-21px;height:3px;background:var(--accent)}
.hd .right{margin-left:auto;display:flex;align-items:center;gap:14px}
.icbtn{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#55555e;border:1px solid var(--line);cursor:pointer}
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
.item .body{flex:1;min-width:0}.item .l1{display:flex;align-items:center;gap:6px;margin-bottom:3px}
.item .store{font-size:13px;color:#6a6a72;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:60%}
.item .tag{font-size:10px;font-weight:800;background:#fbf0df;color:#e8a33c;padding:2px 7px;border-radius:6px}.item .tag.off{background:#ececf0;color:#9a9aa2}
.item .l2{font-size:16px;font-weight:800;letter-spacing:-.3px}.item .l2 .hl{color:var(--accent)}
.item .l3{font-size:12.5px;color:var(--sub);margin-top:4px;line-height:1.5;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.item .chev{color:#46464d;font-size:20px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:18px 14px;padding:16px 0}
.ctile{position:relative;border-radius:16px;padding:6px 8px 12px;background:var(--surface);border:1px solid var(--line);display:flex;flex-direction:column;transition:.15s}
.favbtn{position:absolute;top:9px;right:11px;font-size:17px;cursor:pointer;z-index:3;line-height:1}
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
.ev .eb{flex:1;min-width:0}.ev .ec{font-size:14px;font-weight:800}.ev .ei{font-size:11.5px;color:var(--sub);margin-top:3px}
.ev .ebn{font-size:14.5px;font-weight:900;color:var(--accent);text-align:right;max-width:42%}.ev .chev{color:#46464d;font-size:19px}
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
footer{border-top:1px solid var(--line);margin-top:40px;background:#f5f5f7}
.foot{display:flex;gap:50px;padding:42px 0 10px;flex-wrap:wrap}
.foot .col h4{font-size:12px;color:var(--dim);font-weight:800;margin-bottom:13px}.foot .col a{display:block;font-size:13.5px;color:#55555e;margin-bottom:9px}.foot .col a:hover{color:var(--accent)}
.foot .brand{flex:1;min-width:220px}.foot .brand .lg{font-size:20px;font-weight:900;letter-spacing:-1px}.foot .brand .lg b{color:var(--accent)}.foot .brand p{font-size:12px;color:var(--sub);margin-top:12px;line-height:1.7;max-width:400px}
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
/* 티라노 브랜드 플레이트 배너(특정 카드 아님·서비스 대표 장식) */
.tybnr{display:flex;align-items:center;gap:20px;background:#c5b0f4;border-radius:20px;padding:24px 26px;margin:18px 0 22px;overflow:hidden;position:relative;color:#16161b;text-decoration:none;transition:box-shadow .18s,transform .18s}
.tybnr:hover{transform:translateY(-2px);box-shadow:0 16px 36px rgba(123,90,210,.28)}
.tybnr .tyb-txt{flex:1;min-width:0;position:relative;z-index:1}
.tybnr .tyb-eb{font-size:11.5px;font-weight:900;letter-spacing:.6px;color:#5b3fb0;text-transform:uppercase}
.tybnr .tyb-h{font-size:21px;font-weight:900;letter-spacing:-.03em;line-height:1.25;margin-top:8px}
.tybnr .tyb-sub{font-size:13px;color:#3a2d5e;margin-top:7px;line-height:1.55}
.tybnr .tyb-plate{position:relative;width:172px;aspect-ratio:1.586/1;border-radius:13px;background:linear-gradient(135deg,#ffffff 0%,#efe7ff 100%);box-shadow:0 16px 34px rgba(70,40,120,.30);transform:rotate(-6deg);flex:0 0 auto;overflow:hidden}
.tybnr .tyb-plate .tyb-mk{position:absolute;top:13px;left:15px;font-size:12px;font-weight:900;letter-spacing:-.3px;color:#16161b}.tybnr .tyb-plate .tyb-mk b{color:#ef5226}
.tybnr .tyb-plate .tyb-dino{position:absolute;right:-7%;bottom:-12%;width:62%;height:62%;color:#ef5226;opacity:.92}
.tybnr .tyb-plate .tyb-dino.bg{right:auto;left:-14%;bottom:auto;top:36%;width:44%;height:44%;color:#c9b6f0;opacity:.5}
.tybnr::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.35),transparent 70%)}
@media(max-width:560px){.tybnr{padding:18px;gap:14px}.tybnr .tyb-h{font-size:17px}.tybnr .tyb-plate{width:120px}}
@media(max-width:900px){.grid,.posts{grid-template-columns:1fr 1fr}.cur{grid-template-columns:1fr}.rank{grid-template-columns:1fr}.gnb,.util{display:none}.menu{display:flex}.wrap{padding:0 16px}.icbtn{width:42px;height:42px}}
@media(max-width:480px){.wrap{padding:0 13px}.grid,.posts{grid-template-columns:1fr}.sec-h h2{font-size:19px}.chip,.ctlb,.ctlf{padding:9px 13px}.cat{width:62px}.cat .ico{width:40px;height:40px}.hd .row{height:56px}.logo{font-size:18px}.searchbar .wrap{padding:11px 13px}.sb{padding:11px 13px}.sb .go{padding:10px 14px}.sec-h{margin-bottom:12px}section{padding:22px 0}}
"""

HELPERS = r"""
function _purl(plat,id){id=String(id||'').trim();if(!id)return '';return ({cardgorilla:'https://www.card-gorilla.com/card/detail/'+id,banksalad:'https://www.banksalad.com/product/cards/'+id,toss:'https://card-lounge.toss.im/card/'+id,ajungdang:'https://www.ajd.co.kr/card/event/detail/'+id}[plat])||'';}
function thumbOf(p){var m=[["마트","🛒","#fff3d6"],["하이마트","📺","#e9f0ff"],["편의|GS25|CU|세븐|이마트24","🏪","#e7f6ee"],["백화점","🏬","#f1ecff"],["면세","🛍️","#ffeef0"],["주유|칼텍스|에너지|OIL|오일","⛽","#e9f7f1"],["CGV|시네마|메가박스","🎬","#ececf3"],["스타벅스","☕","#eaf6ee"],["무신사|W컨셉|한섬|패션","👕","#fff0e6"],["알라딘|교보|도서","📚","#eaf2ff"],["홈쇼핑|CJ|GS샵|NS","📺","#fdeef0"],["야놀자|여행|네이버 패키지","✈️","#e8f3ff"],["쿠팡|11번가|G마켓|옥션|SSG|롯데온|올리브영","🛍️","#fff3d6"]];for(var i=0;i<m.length;i++){if(new RegExp(m[i][0]).test(p))return{e:m[i][1],bg:m[i][2]};}return{e:"",bg:"#eef1f5"};}
function favico(dom,e,bg){return dom?'<img src="https://www.google.com/s2/favicons?domain='+dom+'&sz=128" alt="" onerror="this.parentNode.style.background=\''+bg+'\';this.parentNode.textContent=\''+e+'\'">':e;}
var DEFCARD="data:image/svg+xml,"+encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 202'><rect width='320' height='202' rx='14' fill='#eef0f3'/><rect x='26' y='40' width='44' height='32' rx='6' fill='#d6d6dd'/><circle cx='280' cy='36' r='13' fill='#33333b'/><rect x='26' y='150' width='150' height='11' rx='5' fill='#d6d6dd'/><rect x='26' y='170' width='96' height='9' rx='4' fill='#33333b'/></svg>");
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
function toggleFav(id){var a=getFav();var i=a.indexOf(id);if(i>=0)a.splice(i,1);else a.push(id);setFav(a);updateFavCount();return i<0;}
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
  if(g.scope==='통합') cap='<div class="lcap">🔗 통합한도'+(g.amount?(' · '+g.unit+' '+g.amount.toLocaleString()+'원'):'')+'</div>';
  else if(g.amount) cap='<div class="lcap">개별한도 · '+g.unit+' '+g.amount.toLocaleString()+'원</div>';
  return '<div class="bgrp">'+cap+groups[gid].map(function(it){
   return '<div class="bitem"><div class="bareas">'+it.areas.map(function(a){return '<span class="ba">'+a+'</span>';}).join('')+'</div><div class="bval"><span class="bv">'+it.value+'</span> <span class="bm">'+(it.method||'')+(it.type||'')+'</span>'+(it.tier&&it.tier!=='기본'?'<span class="btier">'+it.tier+'</span>':'')+'</div></div>';
  }).join('')+'</div>';
 }).join('');
 var head='<div class="bhead">'+(d.prev_spend?('전월실적 '+d.prev_spend):'전월실적 없음')+(d.max_benefit?(' · '+d.max_benefit):'')+'</div>';
 return head+html;
}
"""

def header(active):
    L=[("cards","cards.html","카드찾기"),("compare","issue.html?v=cmp","플랫폼 비교"),("issue","issue.html","발급 이벤트"),
       ("charts","chart.html","티라노차트"),("curation","index.html#curation","큐레이션"),("content","content.html","가이드")]
    gnb="".join('<a href="%s" class="%s">%s</a>'%(u,("on" if k==active else ""),t) for k,u,t in L)
    drawer="".join('<a href="%s">%s</a>'%(u,t) for k,u,t in L)
    return ('<div class="scrim" id="scrim"></div><aside class="drawer" id="drawer">'
            '<div class="logo" style="margin-bottom:10px"><svg class="rx" viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.8 4.6 h2.6 a2.6 2.6 0 0 1 2.6 2.6 v1.7 a2.6 2.6 0 0 1 -2.6 2.6 h-2.6 a2.6 2.6 0 0 1 -2.6 -2.6 v-1.7 a2.6 2.6 0 0 1 2.6 -2.6 z M17.75 7.4 a0.85 0.85 0 1 0 1.7 0 a0.85 0.85 0 1 0 -1.7 0 z M18.4 9.5 h2.6 v1 h-2.6 z"/></svg>CARD<b>TYRANNO</b></div>'+drawer+'</aside>'
            '<div class="util"><div class="wrap"><a href="content.html">가이드</a><a href="mailto:partner@cardtyranno.com">제휴·광고 문의</a></div></div>'
            '<header class="hd"><div class="wrap row">'
            '<span class="icbtn menu" id="menuBtn">☰</span>'
            '<a class="logo" href="index.html"><svg class="rx" viewBox="0 0 24 24" width="23" height="23" aria-hidden="true"><path fill="currentColor" d="M3 11.6 L11 9.8 C13.2 9.8 14.4 11 14.4 13.2 L14.4 18.4 Q14.4 19 13.8 19 L12.8 19 Q12.2 19 12.2 18.4 L12.2 14.6 L10.4 14.6 L10.4 18.4 Q10.4 19 9.8 19 L8.8 19 Q8.2 19 8.2 18.4 L8.2 13.7 C6.3 13.5 4.7 13 3 11.6 Z M13.5 12.4 l2 1.1 -2 .9 z"/><path fill="currentColor" fill-rule="evenodd" d="M15.8 4.6 h2.6 a2.6 2.6 0 0 1 2.6 2.6 v1.7 a2.6 2.6 0 0 1 -2.6 2.6 h-2.6 a2.6 2.6 0 0 1 -2.6 -2.6 v-1.7 a2.6 2.6 0 0 1 2.6 -2.6 z M17.75 7.4 a0.85 0.85 0 1 0 1.7 0 a0.85 0.85 0 1 0 -1.7 0 z M18.4 9.5 h2.6 v1 h-2.6 z"/></svg>CARD<b>TYRANNO</b></a>'
            '<nav class="gnb">'+gnb+'</nav>'
            '<div class="right"><div class="icbtn" id="searchGo">🔎</div>'
            '<a class="icbtn" href="favorites.html" title="관심카드" style="position:relative">🤍<i id="favCount" style="position:absolute;top:-5px;right:-5px;background:var(--accent);color:#fff;font-size:9px;font-weight:800;border-radius:8px;padding:1px 5px;font-style:normal;display:none"></i></a></div>'
            '</div></header>')

SEARCHBAR=('<div class="searchbar"><div class="wrap">'
 '<div class="sb"><span>🔎</span><input id="siteSearch" placeholder="카드명 · 카드사 · 가맹점 · 혜택을 검색하세요"><button class="go" id="searchGo2">검색</button></div>'
 '<div class="sfilters"><span class="chip">즉시할인</span><span class="chip">청구할인</span><a class="chip" href="installment.html">무이자할부</a><span class="chip">캐시백</span><a class="chip" href="issue.html">발급 이벤트</a></div>'
 '</div></div>')

CATSTRIP=('<div class="catstrip"><div class="wrap">'
 +"".join('<a class="cat" href="discount.html?cat=%s"><span class="ico">%s</span>%s</a>'%(n,i,n) for i,n in
   [("🍽️","식음료"),("🛍️","쇼핑"),("⛽","주유"),("📱","통신"),("✈️","여행"),("🛒","마트"),("☕","카페"),("🎬","문화"),("🔁","구독"),("🚗","자동차"),("🏥","병원"),("","전체")])
 +'</div></div>')

FOOTER=('<footer><div class="wrap foot">'
 '<div class="brand"><div class="lg">CARD<b>TYRANNO</b></div>'
 '<p>카드티라노는 여러 카드 중개 플랫폼의 카드·이벤트 혜택을 한곳에서 비교·분석해 드리는 정보 서비스입니다. 실제 카드 발급·심사는 각 카드사에서 진행됩니다.</p></div>'
 '<div class="col"><h4>서비스</h4><a href="cards.html">카드찾기</a><a href="issue.html">발급 이벤트</a><a href="installment.html">무이자할부</a><a href="content.html">카드 가이드</a></div>'
 '<div class="col"><h4>회사</h4><a href="mailto:partner@cardtyranno.com">제휴·광고 문의</a><a href="index.html">서비스 소개</a></div>'
 '<div class="col"><h4>약관·정책</h4><a href="index.html">이용약관</a><a href="index.html">개인정보처리방침</a></div></div>'
 '<div class="wrap legal">본 사이트는 카드 상품의 비교·정보 제공 및 광고를 목적으로 하며, 카드 신청 시 각 제휴 플랫폼·카드사로 연결됩니다. 게시된 혜택·연회비·이벤트는 수집 시점 기준이며 실제와 다를 수 있으므로 신청 전 각 카드사·플랫폼에서 최종 확인이 필요합니다.'
 '<div class="biz muted">카드티라노(CardTyranno) · 쥬라기랩스 · 제휴/광고 partner@cardtyranno.com</div>'
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
      '<meta property="og:type" content="website"><meta property="og:site_name" content="'+BRAND+'"><meta property="og:title" content="'+title+'">'
      '<meta property="og:description" content="'+desc+'"><meta property="og:url" content="'+BASE+path+'"><meta property="og:image" content="'+BASE+'/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="'+BRAND+'"><meta property="og:locale" content="ko_KR">'
      '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+title+'"><meta name="twitter:description" content="'+desc+'"><meta name="twitter:image" content="'+BASE+'/og-image.png">'
      '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22></text></svg>">'
      +ld)

def page(fname,title,desc,path,body,script="",extra_jsonld=None,searchbar=False,catstrip=False,active="",noindex=False):
    html=('<!DOCTYPE html><html lang="ko"><head>'+head(title,desc,path,extra_jsonld,noindex)
      +'<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">'
      +'<style>'+CSS+'</style></head><body>'
      +header(active)+(SEARCHBAR if searchbar else "")+(CATSTRIP if catstrip else "")
      +body+FOOTER+'<script>'+HELPERS+script+'\nbindUI();</script></body></html>')
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
 '<a class="curc"><span class="em">🚗</span><div class="th">THEME</div><div class="ti">신차 구매자를 위한 카드</div><div class="ds">자동차 할부·주유·정비 혜택 모음</div></a>'
 '<a class="curc"><span class="em">✈️</span><div class="th">THEME</div><div class="ti">해외여행 필수 카드</div><div class="ds">수수료 면제·라운지·마일리지</div></a>'
 '<a class="curc"><span class="em">🎓</span><div class="th">THEME</div><div class="ti">사회초년생 첫 카드</div><div class="ds">연회비 낮고 실적 부담 적은 카드</div></a></div></section>')

# ===== INDEX (landing) =====
INDEX_BODY=('<div class="wrap">'
 '<div class="herowrap">'
 '<a class="vhero vh1" href="cashback.html" data-track="hero" data-label="max_card"><div class="vh-tag">이번 달 최대 할인 카드</div><div class="vh-iss" id="vh1iss"></div><div class="vh-name" id="vh1name">불러오는 중…</div><div class="vh-amt" id="vh1amt"></div><div class="vh-go">캐시백 비교 보기 ›</div></a>'
 '</div>'
 +tybnr("chart.html","CARDTYRANNO · 티라노차트","플랫폼 순위를 모아 한 번에","토스·카드고릴라·뱅크샐러드 순위를 평균낸 카드티라노 랭킹으로 이번 달 인기 카드를 확인하세요.")
 +'<section id="rank"><div class="sec-h"><h2>티라노차트</h2><a class="more" href="chart.html">전체보기 ›</a></div>'
 '<div class="rank" id="rk"><div class="empty">불러오는 중…</div></div></section>'
 '<a class="adbanner" href="mailto:partner@cardtyranno.com" data-track="ad" data-label="main_hero"><span class="adtag">AD · 샘플</span><img src="img/sample_ad.svg" alt="광고 문의 샘플 배너" loading="eager"/></a>'
 '<a class="cardad" id="cardad" href="issue.html?v=cmp" data-track="ad" data-label="card_promo"><span class="adtag">AD</span><div class="cadbody"><div class="cadplate" id="cadplate"></div><div class="cadinfo"><div class="cadev">이번 달 발급 이벤트 · 최대 혜택</div><div class="cadname" id="cadname">불러오는 중…</div><div class="cadiss" id="cadiss"></div><div class="cadamt" id="cadamt"></div><div class="cadplats" id="cadplats"></div><div class="cadcta" id="cadcta"></div></div></div></a>'
 '<section><div class="sec-h"><h2>6월 티라노 추천 카드</h2><a class="more" href="issue.html?v=cmp">플랫폼 비교 ›</a></div><div class="muted" style="font-size:12.5px;padding-bottom:12px">5개 플랫폼 교차 캐시백이 가장 크고 채널 선택지가 많은 카드예요.</div><div class="grid" id="reco"></div></section>'
 '<section><div class="sec-h"><h2>6월 추천 카드사</h2><a class="more" href="issue.html?v=cmp">플랫폼 비교 ›</a></div><div class="muted" style="font-size:12.5px;padding-bottom:12px">교차 발급 캐시백이 큰 카드를 많이 보유한 카드사 순이에요.</div><div class="grid" id="recoIss"></div></section>'
 '<section><div class="sec-h"><h2>지금 뜨는 발급 이벤트</h2><a class="more" href="issue.html">전체보기 ›</a></div><div class="grid" id="evs"></div></section>'
 +CUR_HTML+
 '<section><div class="sec-h"><h2>카드 가이드</h2><a class="more" href="content.html">전체보기 ›</a></div><div class="posts" id="posts"></div></section>'
 +FAQ_HTML+'</div>')
INDEX_JS=r"""
var PCOL={"카드고릴라":"#ff4d4f","뱅크샐러드":"#2f6bff","아정당":"#3b5bdb","카카오페이":"#e8b800","토스":"#3182f6"};
// 카드명→상품 상세 id 매핑(슬롯 클릭이 실제 상품으로 가도록). cards.json 로드 후 랭킹·이벤트 렌더.
fetch('cards.json').then(r=>r.json()).then(function(cj){
 var NAME2ID={};for(var k in cj.cards){(cj.cards[k]||[]).forEach(function(c){if(NAME2ID[_nk2(c.name)]==null)NAME2ID[_nk2(c.name)]=c.id;});}
 function cardHref(name){var id=NAME2ID[_nk2(name||'')];if(id==null)id=NAME2ID[_nk2((name||'').replace(/^토스\s*/,''))];return id!=null?('carddetail.html?id='+id):null;}
 fetch('hero.json').then(r=>r.json()).then(function(j){document.getElementById('rk').innerHTML=j.items.map(function(d,i){
  var h=cardHref(d.card)||'chart.html';var rk=i+1;
  return '<a class="rk" href="'+h+'"><span class="no'+(rk<=3?' top':'')+'">'+rk+'</span><span class="pl">'+imgTag(d.img)+'</span><div class="ri"><div class="rn">'+d.card+'</div><div class="rs">'+d.issuer+'</div></div><span class="rw">'+d.reward+'</span></a>';}).join("");repairImages();});
 fetch('events.json').then(r=>r.json()).then(function(j){document.getElementById('evs').innerHTML=j.items.slice(0,4).map(function(x){
  var h=cardHref(x.card)||('issue.html?issuer='+encodeURIComponent(x.issuer||''));
  return '<a class="gcard" href="'+h+'"><span class="badge" style="background:'+(PCOL[x.platform]||'#ff5a2e')+'">'+x.platform+'</span><div class="ct">'+x.card+'</div><div class="cw accent">'+x.benefit+'</div><div class="cs">'+x.issuer+(x.period?' · '+x.period:'')+'</div></a>';}).join("");});
}).catch(function(){});
fetch('data.json').then(r=>r.json()).then(function(j){var _de=document.getElementById('discs');if(!_de)return;var pick=j.items.slice(0,4);_de.innerHTML=pick.map(function(d){
 return '<a class="gcard" href="detail.html?id='+d.id+'"><span class="badge gray">'+d.plat+'</span><div class="cw accent">'+d.disc+'</div><div class="cs">'+d.card+' · '+d.type+'</div></a>';}).join("");});
fetch('content.json').then(r=>r.json()).then(function(j){document.getElementById('posts').innerHTML=j.items.slice(0,4).map(function(x){
 return '<a class="post" href="content.html?id='+x.id+'"><div class="thumb">'+x.emoji+'</div><div class="pb"><div class="pc">'+x.cat+'</div><div class="pt">'+x.title+'</div></div></a>';}).join("");});
// 🦖 6월 티라노 추천 — reco.json(추천 테이블 기반): 교차 최대혜택·멀티플랫폼 우선
fetch('reco.json').then(r=>r.json()).then(function(j){function won(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
 var pick=(j.cards||[]).slice().sort(function(a,b){return (b.platformCount-a.platformCount)||(b.maxCashbackWon-a.maxCashbackWon);}).slice(0,6);
 var el=document.getElementById('reco');if(!el)return;
 el.innerHTML=pick.map(function(c){var dl=_deadln(c.periodEnd);return '<a class="gcard" href="issue.html?v=cmp"><span class="badge" style="background:#19c37d">'+c.platformCount+'개 플랫폼</span><div class="ct">'+c.name+'</div><div class="cw accent">최대 '+won(c.maxCashbackWon)+' 캐시백</div><div class="cs">'+(c.issuer||'')+(dl?' · '+dl:'')+'</div></a>';}).join("");}).catch(function(){});
// 플랫폼 메타(영문키→표기/브랜드색)
var PMETA={cardgorilla:{n:'카드고릴라',c:'#ff4d4f'},banksalad:{n:'뱅크샐러드',c:'#2f6bff'},toss:{n:'토스',c:'#3182f6'},ajungdang:{n:'아정당',c:'#3b5bdb'},naver:{n:'네이버페이',c:'#03c75a'},kakaopay:{n:'카카오페이',c:'#e8b800'}};
function _nk2(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function _deadln(pe){if(!pe)return'';var m=(''+pe).match(/20\d\d[.\-](\d\d?)[.\-](\d\d?)/);return m?('~'+(+m[1])+'/'+(+m[2])+' 마감'):'';}
function _wonM(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
// 💳 카드 광고 구좌 — 교차혜택 1위 카드를 플레이트 크게 + 당월 이벤트 + 대상 플랫폼
Promise.all([fetch('reco.json').then(r=>r.json()),fetch('cards.json').then(r=>r.json())]).then(function(A){
 var rc=(A[0].cards||[]).slice().sort(function(a,b){return (b.platformCount-a.platformCount)||(b.maxCashbackWon-a.maxCashbackWon);});
 var el=document.getElementById('cardad');if(!el||!rc.length)return;var c=rc[0];
 var IMG={},cj=A[1].cards||{};for(var ik in cj){(cj[ik]||[]).forEach(function(k){if(k.img&&!IMG[_nk2(k.name)])IMG[_nk2(k.name)]=k.img;});}
 var plats=(c.platforms||[]).map(function(p){var m=PMETA[p]||{n:p,c:'#33333b'};return '<span class="pb2" style="background:'+m.c+'">'+m.n+'</span>';}).join("");
 document.getElementById('cadplate').innerHTML=imgTag(c.img||IMG[_nk2(c.name)]);
 document.getElementById('cadname').textContent=c.name;
 document.getElementById('cadiss').textContent=c.issuer||'';
 document.getElementById('cadamt').innerHTML='이번 달 최대 <b>'+_wonM(c.maxCashbackWon)+'</b> 캐시백';
 document.getElementById('cadplats').innerHTML=plats;
 var dl=_deadln(c.periodEnd);document.getElementById('cadcta').innerHTML='대상 플랫폼 <b>'+c.platformCount+'곳</b>에서 발급 가능'+(dl?' · <b>'+dl+'</b>':'')+' · 비교 ›';
}).catch(function(){});
// 🏦 6월 추천 카드사 — reco.json을 카드사로 집계(최대 캐시백·보유 카드 수)
fetch('reco.json').then(r=>r.json()).then(function(j){var el=document.getElementById('recoIss');if(!el)return;
 var by={};(j.cards||[]).forEach(function(c){var i=c.issuer;if(!i)return;by[i]=by[i]||{iss:i,max:0,cnt:0,top:'',pl:{}};by[i].cnt++;if((c.maxCashbackWon||0)>by[i].max){by[i].max=c.maxCashbackWon;by[i].top=c.name;}(c.platforms||[]).forEach(function(p){by[i].pl[p]=1;});});
 var arr=Object.keys(by).map(function(k){return by[k];}).sort(function(a,b){return (b.max-a.max)||(b.cnt-a.cnt);}).slice(0,6);
 el.innerHTML=arr.map(function(d){var pc=Object.keys(d.pl).length;return '<a class="gcard" href="issue.html?v=cmp"><span class="badge" style="background:#5b3df2">카드 '+d.cnt+'종</span><div class="ct">'+d.iss+'</div><div class="cw accent">최대 '+_wonM(d.max)+' 캐시백</div><div class="cs">대표: '+d.top+' · '+pc+'개 플랫폼</div></a>';}).join("");}).catch(function(){});
// 세로형 히어로 ① 이번 달 최대 할인(캐시백) 카드 — 콜렉터 platform_events.json
(function(){function won(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
 fetch('platform_events.json').then(r=>r.json()).then(function(j){var best=null,bw=-1;(j.products||[]).forEach(function(p){(p.events||[]).forEach(function(e){if((e.reward_won||0)>bw){bw=e.reward_won;best=p;}});});
  if(best){document.getElementById('vh1iss').textContent=best.issuer||'';document.getElementById('vh1name').textContent=best.name;document.getElementById('vh1amt').innerHTML='최대 '+won(bw)+'<small>캐시백</small>';}}).catch(function(){});
})();
// 세로형 히어로 ② 이번 달 최고 결제 할인 — data.json
fetch('data.json').then(r=>r.json()).then(function(j){function num(s){var m=(s||'').match(/([0-9]+(?:\.[0-9]+)?)/);return m?parseFloat(m[1]):-1;}
 var its=(j.items||[]).slice();its.sort(function(a,b){return num(b.disc)-num(a.disc);});var t=its[0];
 var _vn=document.getElementById('vh2name');if(t&&_vn){document.getElementById('vh2iss').textContent=t.plat||'';_vn.textContent=t.card||t.type||'';document.getElementById('vh2amt').innerHTML=t.disc+'<small> '+(t.type||'')+'</small>';}}).catch(function(){});
"""

# ===== DISCOUNT =====
DISC_BODY=('<div class="wrap"><section><div class="sec-h"><h2>카드 할인 혜택</h2></div>'
 '<div class="filterbar"><div class="seg" id="seg"><button data-g="전체" class="on">전체</button><button data-g="온라인">온라인</button><button data-g="오프라인">오프라인</button></div>'
 '<select id="tabSel"></select><select id="platSel"></select></div>'
 '<div class="list" id="list"><div class="empty">불러오는 중…</div></div></section></div>')
DISC_JS=r"""
var DATA=[],cur="전체",curG="전체",curPlat="전체",Q=(new URLSearchParams(location.search).get('q')||'').trim();
function fmt(s){return (s&&s!=="-"&&s!=="없음")?s:"";}
function base(){return DATA.filter(function(d){var ok=(cur==="전체"||d.tab===cur)&&(curG==="전체"||d.gubun===curG);if(ok&&Q){var hay=(d.plat+d.card+d.type+d.disc+d.cond).toLowerCase();ok=hay.indexOf(Q.toLowerCase())>=0;}return ok;});}
function syncSel(){var t=document.getElementById('tabSel');var tabs=[...new Set(DATA.map(d=>d.tab))];t.innerHTML='<option value="전체">카드사 전체</option>'+tabs.map(x=>'<option'+(x===cur?' selected':'')+'>'+x+'</option>').join("");
 var p=document.getElementById('platSel');var ps=[...new Set(base().map(d=>d.plat))].sort((a,b)=>a.localeCompare(b,'ko'));if(!ps.includes(curPlat))curPlat="전체";p.innerHTML='<option value="전체">가맹점 전체 ('+base().length+')</option>'+ps.map(x=>'<option'+(x===curPlat?' selected':'')+'>'+x+'</option>').join("");}
function render(){var L=document.getElementById('list');var items=base().filter(d=>curPlat==="전체"||d.plat===curPlat);if(!items.length){L.innerHTML='<div class="empty">조건에 맞는 혜택이 없어요.</div>';return;}
 L.innerHTML=items.map(function(d){var t=thumbOf(d.plat);var sub=[fmt(d.card),fmt(d.min)?'최소 '+d.min:'',fmt(d.cond),'📅 '+d.period].filter(Boolean).join(' · ');
 return '<a class="item" href="detail.html?id='+d.id+'"><div class="th">'+favico(d.domain,t.e,t.bg)+'</div><div class="body"><div class="l1"><span class="store">'+d.plat+'</span><span class="tag '+(d.gubun==="오프라인"?"off":"")+'">'+d.gubun+'</span></div><div class="l2"><span class="hl">'+d.disc+'</span> '+d.type+'</div><div class="l3">'+sub+'</div></div><div class="chev">›</div></a>';}).join("");}
document.getElementById('seg').onclick=function(e){var b=e.target.closest('button');if(!b)return;curG=b.dataset.g;curPlat="전체";document.querySelectorAll('#seg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');syncSel();render();};
document.getElementById('tabSel').onchange=function(){cur=this.value;curPlat="전체";syncSel();render();};
document.getElementById('platSel').onchange=function(){curPlat=this.value;render();};
fetch('data.json').then(r=>r.json()).then(function(j){DATA=j.items;if(Q){var s=document.getElementById('siteSearch');if(s)s.value=Q;}syncSel();render();});
"""

# ===== CARDS =====
CARDS_BODY=('<div class="wrap"><section><div class="sec-h"><h2>카드 찾기</h2></div>'
 '<div class="tabs" id="tabs"></div><div class="cgrid" id="list"><div class="empty">불러오는 중…</div></div></section></div>')
CARDS_JS=r"""
var C={},ORD=[],cur="",EVSET={},PEIMG={};
function _nkc(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function render(){var a=(C[cur]||[]).slice();
 a.sort(function(x,y){return (EVSET[_nkc(y.name)]||0)-(EVSET[_nkc(x.name)]||0);});   // 이벤트 있는 카드 우선(플랫폼 많은 순)
 document.getElementById('list').innerHTML=a.map(function(c){var fee=c.fee?('연회비 '+c.fee):'';
 var pc=EVSET[_nkc(c.name)]||((c.events&&c.events.length)?1:0);    // platform_events.json 매칭(상세페이지와 동일 정규화)
 var ev=pc?'<div class="cev">발급 이벤트'+(pc>1?' · '+pc+'곳':'')+'</div>':'';
 var img=c.img||PEIMG[_nkc(c.name)];                               // 메타 이미지 폴백(콜렉터 카드고릴라 플레이트)
 var hb='<span class="favbtn" onclick="event.preventDefault();event.stopPropagation();this.textContent=toggleFav('+c.id+')?String.fromCodePoint(10084):String.fromCodePoint(129293);">'+(isFav(c.id)?'❤️':'🤍')+'</span>';
 return '<a class="ctile" href="carddetail.html?id='+c.id+'">'+hb+'<div class="plate">'+imgTag(img)+'</div><div class="cn">'+c.name+'</div>'+(fee?'<div class="cfee">'+fee+'</div>':'')+'<div class="cd">'+c.benefit+'</div>'+ev+'<div class="apply">카드 자세히 보기 ›</div></a>';}).join("");if(window.repairImages)repairImages();}
function tabs(){var t=document.getElementById('tabs');t.innerHTML=ORD.map(function(o){return '<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'<span class="cnt">'+(C[o]||[]).length+'</span></div>';}).join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};});}
Promise.all([fetch('cards.json').then(r=>r.json()),fetch('platform_events.json').then(r=>r.json()).catch(function(){return {products:[]};})]).then(function(A){
 C=A[0].cards;ORD=A[0].order;cur=ORD[0];
 (A[1].products||[]).forEach(function(p){if((p.events||[]).length){EVSET[_nkc(p.name)]=new Set((p.events||[]).map(function(e){return e.platform;})).size;}if(p.img)PEIMG[_nkc(p.name)]=p.img;});
 tabs();render();});
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
 '.pcmp-hero h1{font-size:40px;font-weight:350;line-height:1.05;letter-spacing:-1.4px;margin:13px 0 0;color:#0c0b14}'
 '.pcmp-hero p{font-size:16px;color:rgba(0,0,0,.62);margin:13px 0 0;max-width:520px;font-weight:500;line-height:1.45}'
 '.pcmp-spread{background:#1f1d3d;color:#fff;border-radius:22px;padding:28px 30px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between;gap:20px;overflow:hidden}'
 '.pcmp-spread .sl{font:800 11px ui-monospace,Menlo,monospace;opacity:.72;letter-spacing:.4px}'
 '.pcmp-spread .st{font-size:25px;font-weight:800;letter-spacing:-.6px;margin-top:9px;line-height:1.16}'
 '.pcmp-spread .ss{font-size:14px;opacity:.76;margin-top:9px}'
 '.pcmp-spread .splate{width:168px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:11px;overflow:hidden;transform:rotate(-7deg);box-shadow:0 16px 36px rgba(0,0,0,.34);background:#c5b0f4;transition:.2s}'
 '.pcmp-spread:hover .splate{transform:rotate(-3deg) scale(1.03)}'
 '.pcmp-spread .splate img{width:100%;height:100%;object-fit:cover}'
 '.pbasis{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin:4px 0 12px}'
 '.pbasis .bl{font-size:11.5px;color:var(--sub);font-weight:700}.pbasis .bt{font-size:16px;font-weight:800;margin-top:3px;letter-spacing:-.2px}'
 '.pchips{display:flex;gap:5px;background:var(--surface2);border-radius:50px;padding:5px;flex-wrap:wrap}'
 '.pchips button{border:0;background:transparent;font-size:12.5px;font-weight:700;color:var(--sub);padding:8px 14px;border-radius:50px;cursor:pointer;transition:.12s}'
 '.pchips button.on{background:#fff;color:var(--text);box-shadow:0 1px 3px rgba(0,0,0,.13)}'
 '.ptbl{border:1px solid var(--line);border-radius:18px;overflow:hidden}'
 '.ptr{display:grid;grid-template-columns:1.7fr repeat(5,1fr);align-items:center;border-top:1px solid var(--line);text-decoration:none;color:var(--text);transition:.12s}'
 '.ptbl .ptr:first-child{border-top:0}'
 '.ptr.hd{background:var(--surface2);font:800 11px ui-monospace,Menlo,monospace;letter-spacing:.3px;color:var(--dim)}'
 '.ptr.hd>div{padding:14px 8px;text-align:center}.ptr.hd>div:first-child{text-align:left;padding-left:18px}'
 'a.ptr:hover{background:var(--surface2)}'
 '.ptr .pc{padding:12px 16px;display:flex;align-items:center;gap:12px;min-width:0}'
 '.ptr .pcimg{width:60px;flex:0 0 auto;aspect-ratio:1.586/1;border-radius:7px;overflow:hidden;background:#eef0f3;transition:.16s}'
 'a.ptr:hover .pcimg{transform:scale(1.07)}'
 '.ptr .pcimg img{width:100%;height:100%;object-fit:cover}'
 '.ptr .pc>div{min-width:0;overflow:hidden}'
 '.ptr .pcn{font-size:15px;font-weight:800;letter-spacing:-.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
 '.ptr .pci{font:10px ui-monospace,Menlo,monospace;color:var(--dim);margin-top:3px}'
 '.ptr .cell{padding:12px 5px;text-align:center}'
 '.ptr .chip{display:inline-block;min-width:50px;padding:7px 8px;border-radius:50px;font-size:13px;font-weight:700;background:var(--surface2);color:var(--sub)}'
 '.ptr .chip.mx{background:#000;color:#fff;font-weight:800}.ptr .chip.no{background:transparent;color:var(--dim);font-weight:600}'
 '.pcmpnote{font-size:12px;color:var(--sub);margin-top:13px;display:flex;align-items:center;gap:8px;line-height:1.5}.pcmpnote .dot{width:13px;height:13px;border-radius:50%;background:#000;flex:0 0 auto}'
 '.tybox{margin:12px 0 2px;background:#f3f0fb;border:1px solid #e4dcf6;border-radius:13px;padding:13px 15px}'
 '.tyhd{font-size:12.5px;font-weight:900;color:#5b3fb0;display:flex;align-items:center;gap:8px;flex-wrap:wrap}'
 '.tyai{font-size:10px;font-weight:800;color:#6f5bb0;background:#ece5fb;border-radius:999px;padding:3px 8px;letter-spacing:.2px}'
 '.tytxt{font-size:13px;color:var(--text);line-height:1.65;margin-top:8px}.tytxt b{color:#5b3fb0;font-weight:800}'
 '@media(max-width:680px){.pcmp-hero{padding:28px 22px}.pcmp-hero h1{font-size:29px}.pcmp-spread{flex-direction:column;align-items:flex-start}.pcmp-spread .splate{width:128px;align-self:flex-end;margin-top:-30px}.pbasis{flex-direction:column;align-items:stretch;gap:8px}.pchips{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch}.pchips::-webkit-scrollbar{display:none}.ptblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch}.ptbl{min-width:516px}.ptr{grid-template-columns:136px repeat(5,76px)}.ptr .pc{padding:11px 12px;gap:9px}.ptr .pcimg{width:42px}.ptr .pcn{font-size:12.5px}.ptr .chip{min-width:0;padding:6px 5px;font-size:11px}.ptr.hd>div:first-child{padding-left:12px}}'
 '</style>'
 '<div class="wrap"><section><div class="sec-h"><h2 id="issTitle">발급 이벤트</h2></div>'
 '<div id="view-ev">'
 '<div class="cmpctl"><div class="ctlrow"><span class="ctll">정렬</span><button class="ctlb on" data-esort="amt">금액순</button><button class="ctlb" data-esort="plat">플랫폼순</button><button class="ctlb" data-esort="iss">카드사순</button></div>'
 '<div class="ctlrow"><span class="ctll">플랫폼</span><button class="ctlf on" data-eplat="">전체</button><button class="ctlf" data-eplat="카드고릴라">카드고릴라</button><button class="ctlf" data-eplat="뱅크샐러드">뱅크샐러드</button><button class="ctlf" data-eplat="토스">토스</button><button class="ctlf" data-eplat="아정당">아정당</button><button class="ctlf" data-eplat="네이버페이">네이버페이</button></div></div>'
 '<div class="tabs" id="tabs"></div><div id="list"><div class="empty">불러오는 중…</div></div></div>'
 '<div id="view-cmp" style="display:none">'
 '<div class="pcmp-hero"><div class="eb">PLATFORM COMPARE · 플랫폼 비교</div><h1>같은 카드, 채널마다<br>다른 캐시백.</h1><p>토스·카드고릴라·아정당·네이버페이·뱅크샐러드의 발급 캐시백을 한 표로 모았어요.</p></div>'
 '<div id="pcmp-spread"></div>'
 '<div class="subnav2"><button data-c="iss" class="on">카드사 최대혜택 비교</button><button data-c="prod">카드상품별 플랫폼 비교</button></div>'
 '<div id="cmp-iss"><div class="empty">불러오는 중…</div></div>'
 '<div id="cmp-prod" style="display:none"><div class="empty">불러오는 중…</div></div>'
 '</div>'
 '</section></div>')
ISSUE_JS=r"""
var EV=[],ORD=[],cur="전체",evSort="amt",evPlat="";
var PRODALL=[],pSort="amt",pFilter="",basis="cardgorilla",renderProd=function(){};
var PCOL={"카드고릴라":"#ff4d4f","뱅크샐러드":"#2f6bff","아정당":"#3b5bdb","카카오페이":"#e8b800","토스":"#3182f6","네이버페이":"#03c75a","네이버":"#03c75a"};
function pcol(p){return PCOL[p]||"#7a8088";}
function render(){var items=(cur==="전체"?EV:EV.filter(x=>x.issuer===cur)).slice();
 if(evPlat)items=items.filter(x=>x.platform===evPlat);
 items.sort(function(a,b){return evSort==='plat'?(a.platform||'').localeCompare(b.platform||'','ko'):evSort==='iss'?(a.issuer||'').localeCompare(b.issuer||'','ko'):(num(b.benefit)-num(a.benefit));});
 var L=document.getElementById('list');if(!items.length){L.innerHTML='<div class="empty">조건에 맞는 이벤트가 없어요.</div>';return;}
 L.innerHTML=items.map(function(x){return '<a class="ev" href="'+x.url+'" target="_blank" rel="noopener"><span class="pf" style="background:'+pcol(x.platform)+'">'+x.platform+'</span><div class="eb"><div class="ec">'+x.card+'</div><div class="ei">'+x.issuer+(x.period?' · '+x.period:'')+'</div></div><div class="ebn">'+x.benefit+'</div><div class="chev">›</div></a>';}).join("");}
function tabs(){var T=["전체"].concat(ORD);var t=document.getElementById('tabs');t.innerHTML=T.map(function(o){var c=o==="전체"?EV.length:EV.filter(x=>x.issuer===o).length;return '<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'<span class="cnt">'+c+'</span></div>';}).join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};});}
// 발급이벤트 / 플랫폼비교는 별도 화면(서브탭 제거). ?v=cmp로 진입 화면 결정.
document.querySelector('.subnav2').onclick=function(e){var b=e.target.closest('button');if(!b)return;document.querySelectorAll('.subnav2 button').forEach(x=>x.classList.remove('on'));b.classList.add('on');var iss=b.dataset.c==='iss';document.getElementById('cmp-iss').style.display=iss?'':'none';document.getElementById('cmp-prod').style.display=iss?'none':'';var cn=document.getElementById('cmpnote-iss');if(cn)cn.style.display=iss?'':'none';};
// 기준 플랫폼 칩(테이블 정렬 기준 변경) — cmp-prod 내부에 렌더되므로 위임 처리
document.getElementById('cmp-prod').addEventListener('click',function(e){var b=e.target.closest('#pchips button');if(!b)return;e.preventDefault();basis=b.dataset.b;renderProd();});
// 발급이벤트 화면 정렬(금액/플랫폼/카드사)+플랫폼 필터
document.getElementById('view-ev').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 if(b.dataset.esort!==undefined){evSort=b.dataset.esort;document.querySelectorAll('[data-esort]').forEach(x=>x.classList.remove('on'));b.classList.add('on');render();}
 else if(b.dataset.eplat!==undefined){evPlat=b.dataset.eplat;document.querySelectorAll('[data-eplat]').forEach(x=>x.classList.remove('on'));b.classList.add('on');render();}});
// 진입 화면 결정: ?v=cmp면 플랫폼 비교, 아니면 발급 이벤트 (서브탭 없이 분리)
(function(){var isCmp=new URLSearchParams(location.search).get('v')==='cmp';
 document.getElementById('view-ev').style.display=isCmp?'none':'';
 document.getElementById('view-cmp').style.display=isCmp?'':'none';
 var t=document.getElementById('issTitle');if(t)t.textContent=isCmp?'플랫폼 비교':'발급 이벤트';
 document.title=(isCmp?'플랫폼 비교':'발급 이벤트')+' | 카드티라노';})();
function num(s){var m=(s||"").match(/([0-9]+(?:\.[0-9]+)?)\s*만/);return m?parseFloat(m[1]):-1;}
fetch('events.json').then(r=>r.json()).then(function(j){EV=j.items;ORD=j.order;
 var qi=new URLSearchParams(location.search).get('issuer');
 if(qi&&(qi==="전체"||ORD.indexOf(qi)>=0))cur=qi;
 tabs();render();
 var at=document.querySelector('#tabs .tab.active');if(at)at.scrollIntoView({inline:'center',block:'nearest'});});
// 카드사·카드상품 비교 모두 콜렉터 platform_events.json에서 집계(뱅샐·아정당 포함, 카카오페이 제외)
var PN={cardgorilla:"카드고릴라",banksalad:"뱅크샐러드",toss:"토스",naver:"네이버페이",ajungdang:"아정당"};
var PORD=["cardgorilla","banksalad","toss","ajungdang","naver"];
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
 // (1) 카드사 최대혜택 비교 — issuer×platform 최대 집계
 var byIss={};
 prods.forEach(function(p){if(!(p.events||[]).length)return;var iss=p.issuer||'기타';byIss[iss]=byIss[iss]||{};
  p.events.forEach(function(e){var c=byIss[iss][e.platform];var _pp=(p.platforms||{})[e.platform]||{};if(!c||(e.reward_won||0)>c.won)byIss[iss][e.platform]={won:e.reward_won||0,text:e.reward_text||'',url:e.url||_pp.url||_purl(e.platform,_pp.id),main:e.main_won,bonus:e.bonus_won};});});
 var issuers=Object.keys(byIss).map(function(iss){var mx=0;for(var k in byIss[iss])if(byIss[iss][k].won>mx)mx=byIss[iss][k].won;return {iss:iss,mx:mx,data:byIss[iss]};}).sort(function(a,b){return b.mx-a.mx;});
 var present=PORD.filter(function(pk){return issuers.some(function(x){return x.data[pk];});});
 function _tyrano(x,bk){
  if(!bk)return '';var d=x.data[bk]||{};var total=d.won||0;var main=(d.main!=null?d.main:total);var bonus=d.bonus||0;
  var others=present.filter(function(pk){return pk!==bk&&(x.data[pk]||{}).won;}).sort(function(a,b){return x.data[b].won-x.data[a].won;});
  var snd=others[0];var sndV=snd?x.data[snd].won:0;var ratio=sndV?total/sndV:0;
  var s=x.iss+'는 이번 달 <b>'+PN[bk]+'</b> 채널이 가장 유리해요. '+(bonus>0?('메인 캐시백 '+_wm(main)+' + 부가혜택 '+_wm(bonus)+' 합산 최대 <b>'+_wm(total)+'</b>'):('조건 없이 받는 기본 캐시백 최대 <b>'+_wm(total)+'</b>'));
  if(snd&&ratio>=1.15)s+='으로, '+PN[snd]+'('+_wm(sndV)+') 대비 약 '+(Math.round(ratio*10)/10)+'배';
  s+='.'+(bonus>0?' 해외결제·자동납부 등 조건부 부가혜택까지 챙기면 실속이 가장 큽니다.':'');
  return '<div class="tybox"><div class="tyhd">🦖 티라노 AI 추천<span class="tyai">AI 분석</span></div><div class="tytxt">'+s+'</div></div>';}
 document.getElementById('cmp-iss').innerHTML=issuers.length?issuers.map(function(x){
  var best=-1,bk=null;present.forEach(function(pk){var d=x.data[pk];if(!d||!d.won)return;var sc=_pick({main_won:d.main,bonus_won:d.bonus,reward_won:d.won});if(sc>best){best=sc;bk=pk;}});
  var withEv=present.filter(function(pk){return (x.data[pk]||{}).won;}).sort(function(a,b){return ((x.data[b]||{}).won||0)-((x.data[a]||{}).won||0);});  // 금액 높은 순
  var noEv=present.filter(function(pk){return !(x.data[pk]||{}).won;});
  var rows=withEv.map(function(pk,i){var d=x.data[pk];var isb=pk===bk&&best>0;var u=d.url||'';
   var rk=i+1;
   var cls='prow'+(i===0?' f':'')+(isb?' best':'')+(u?' lk':'');
   var inner='<span class="prank r'+rk+'">'+rk+'</span><span class="pf" style="background:'+pcol(PN[pk])+'">'+PN[pk]+'</span><span class="pv">'+_rwd(d.text,d.won)+'</span>'+(u?'<span class="go">›</span>':'');
   return (u?('<a class="'+cls+'" href="'+u+'" target="_blank" rel="noopener" data-track="cmp" data-label="'+pk+'">'+inner+'</a>'):('<div class="'+cls+'">'+inner+'</div>'))+_bd({main_won:d.main,bonus_won:d.bonus,reward_won:d.won});}).join("");
  var noEvHtml=noEv.length?'<div class="noevline">이번 달 이벤트 없음: <b>'+noEv.map(function(pk){return PN[pk];}).join(' · ')+'</b></div>':'';
  return '<div class="cmpcard"><div class="cmphd"><div class="ch">'+x.iss+'</div><div class="chmax">최대 '+_wm(x.mx)+'</div></div>'+rows+noEvHtml+_tyrano(x,bk)+'</div>';}).join(""):'<div class="empty">데이터 준비 중</div>';
 // (2) 카드상품별 플랫폼 비교 — 시안 테이블형(카드 × 플랫폼, 검은 칩=최대 채널)
 // 2개 이상 플랫폼에 이벤트가 있는 카드만(교차비교 의미). o={플랫폼:원}.
 var TBL=prods.filter(function(p){return new Set((p.events||[]).map(e=>e.platform)).size>1;}).map(function(p){
  var o={};(p.events||[]).forEach(function(e){var w=e.reward_won||0;if(w>(o[e.platform]||0))o[e.platform]=w;});
  return {id:p.id,name:p.name,issuer:p.issuer||'',img:p.img||IMG[_nk2(p.name)]||'',o:o};});
 PRODALL=TBL;
 // 기준 플랫폼 기본값 = 비표시 셀이 가장 적은(=커버리지 큰) 플랫폼
 (function(){var cnt={};PORD.forEach(function(pk){cnt[pk]=0;});TBL.forEach(function(c){PORD.forEach(function(pk){if(c.o[pk])cnt[pk]++;});});var bp=PORD[0],mx=-1;PORD.forEach(function(pk){if(cnt[pk]>mx){mx=cnt[pk];bp=pk;}});if(mx>0)basis=bp;})();
 // 이 달의 최대 격차(피처카드) — 플랫폼 간 max-min 차이가 가장 큰 카드
 (function(){var best=null,gap=-1,bp,wp,mxv,mnv;TBL.forEach(function(c){var ks=PORD.filter(function(pk){return c.o[pk];});if(ks.length<2)return;var mx=Math.max.apply(null,ks.map(function(pk){return c.o[pk];})),mn=Math.min.apply(null,ks.map(function(pk){return c.o[pk];}));if(mx-mn>gap){gap=mx-mn;best=c;mxv=mx;mnv=mn;bp=ks.reduce(function(a,b){return c.o[b]>c.o[a]?b:a;});wp=ks.reduce(function(a,b){return c.o[b]<c.o[a]?b:a;});}});
  var el=document.getElementById('pcmp-spread');if(!el)return;
  if(best&&gap>0){el.innerHTML='<div class="pcmp-spread"><div><div class="sl">⚡ 이 달의 최대 격차</div><div class="st">'+best.name+', 채널 따라<br>최대 '+_wm(gap)+' 차이</div><div class="ss">'+PN[bp]+' '+_wm(mxv)+' · '+PN[wp]+' '+_wm(mnv)+'</div></div><div class="splate">'+imgTag(best.img)+'</div></div>';}else{el.innerHTML='';}})();
 function _chipW(w){var s=_wm(w);return s.replace('만원','만').replace('원','');}
 renderProd=function(){
  var rows=TBL.slice().sort(function(a,b){return (b.o[basis]||0)-(a.o[basis]||0);});
  var head='<div class="ptr hd"><div>카드 ('+rows.length+')</div>'+PORD.map(function(pk){return '<div'+(pk===basis?' style="color:var(--text)"':'')+'>'+PN[pk]+'</div>';}).join('')+'</div>';
  var body=rows.map(function(c){
   var vals=PORD.map(function(pk){return c.o[pk]||0;});var mx=Math.max.apply(null,vals);
   var cells=PORD.map(function(pk){var w=c.o[pk]||0;if(!w)return '<div class="cell"><span class="chip no">–</span></div>';return '<div class="cell"><span class="chip'+(w===mx?' mx':'')+'">'+_chipW(w)+'</span></div>';}).join('');
   var plate='<div class="pcimg">'+imgTag(c.img)+'</div>';
   return '<a class="ptr" href="carddetail.html?n='+encodeURIComponent(c.name||'')+'" data-track="cmp" data-label="'+(c.name||'')+'"><div class="pc">'+plate+'<div><div class="pcn">'+c.name+'</div><div class="pci">'+c.issuer+'</div></div></div>'+cells+'</a>';}).join('');
  var chips='<div class="pbasis"><div><div class="bl">기준 플랫폼</div><div class="bt">'+PN[basis]+' 캐시백 순으로 정렬돼요</div></div><div class="pchips" id="pchips">'+PORD.map(function(pk){return '<button data-b="'+pk+'"'+(pk===basis?' class="on"':'')+'>'+PN[pk]+'</button>';}).join('')+'</div></div>';
  var note='<div class="pcmpnote"><span class="dot"></span>검은 칩 = 그 카드의 최대 캐시백 채널이에요 · 행을 누르면 카드 상세로 이동 · 금액은 수집 시점 기준이에요.</div>';
  document.getElementById('cmp-prod').innerHTML=rows.length?(chips+'<div class="ptblwrap"><div class="ptbl">'+head+body+'</div></div>'+note):'<div class="empty">교차비교 카드가 없어요.</div>';
  if(window.repairImages)repairImages();};
 renderProd();
}).catch(function(){document.getElementById('cmp-iss').innerHTML='<div class="empty">데이터 준비 중</div>';document.getElementById('cmp-prod').innerHTML='<div class="empty">교차비교 데이터 준비 중이에요.</div>';});
"""

# ===== DETAIL =====
DETAIL_BODY='<div style="padding:12px 0"><div class="wrap"><a class="bk" href="discount.html">‹</a></div></div><div id="root"><div class="empty">불러오는 중…</div></div>'
DETAIL_JS=r"""
function fmt(s){return (s&&s!=="-"&&s!=="없음")?s:"-";}
var id=Number(new URLSearchParams(location.search).get('id'));
fetch('data.json').then(r=>r.json()).then(function(j){var d=j.items.find(x=>x.id===id);if(!d){document.getElementById('root').innerHTML='<div class="empty">혜택을 찾을 수 없어요. <a class="accent" href="discount.html">목록</a></div>';return;}var t=thumbOf(d.plat);
 document.getElementById('root').innerHTML='<div class="wrap"><div class="hero-detail"><div class="th">'+favico(d.domain,t.e,t.bg)+'</div><div class="store">'+d.plat+'</div><div class="disc"><span class="hl">'+d.disc+'</span></div><div class="type">'+d.type+'</div></div>'+
 '<div class="rows"><div class="r"><div class="k">카드/페이</div><div class="v">'+fmt(d.card)+'</div></div><div class="r"><div class="k">할인유형</div><div class="v">'+fmt(d.type)+'</div></div><div class="r"><div class="k">최소결제</div><div class="v">'+fmt(d.min)+'</div></div><div class="r"><div class="k">조건/한도</div><div class="v">'+fmt(d.cond)+'</div></div><div class="r"><div class="k">행사기간</div><div class="v">'+fmt(d.period)+'</div></div></div>'+
 '<div class="cta"><a href="'+d.url+'" target="_blank" rel="noopener">혜택 받으러 가기 ›</a></div></div>';});
"""

# ===== CONTENT =====
CONTENT_BODY=('<div class="wrap"><section id="listwrap"><div class="sec-h"><h2>카드 가이드</h2></div>'
 '<div class="tabs" id="tabs"></div><div class="posts" id="list" style="padding:4px 0"><div class="empty">불러오는 중…</div></div></section>'
 '<div id="detail" style="display:none"></div></div>')
CONTENT_JS=r"""
var C=[],cur="전체";
function cats(){return ["전체"].concat([...new Set(C.map(x=>x.cat))]);}
function renderList(){var items=cur==="전체"?C:C.filter(x=>x.cat===cur);document.getElementById('list').innerHTML=items.map(function(x){
 return '<a class="post" href="content.html?id='+x.id+'"><div class="thumb">'+x.emoji+'</div><div class="pb"><div class="pc">'+x.cat+'</div><div class="pt">'+x.title+'</div></div></a>';}).join("");}
function tabs(){var t=document.getElementById('tabs');t.innerHTML=cats().map(o=>'<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'</div>').join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderList();};});}
function detail(d){document.getElementById('listwrap').style.display='none';var el=document.getElementById('detail');el.style.display='';
 var hero=d.img?'<div class="ghero"><img src="'+d.img+'" alt="'+d.cat+'" loading="eager"/></div>':'';
 el.innerHTML='<div class="adt">'+hero+'<div class="acat">'+d.emoji+' '+d.cat+'</div><div class="ah">'+d.title+'</div>'+(d.summary?'<div class="asum">'+d.summary+'</div>':'')+d.body.map(p=>'<p>'+p+'</p>').join("")+'<a class="bk2" href="content.html">← 다른 가이드</a></div>';document.title=d.title+' | 카드티라노';}
var id=new URLSearchParams(location.search).get('id');
fetch('content.json').then(r=>r.json()).then(function(j){C=j.items;if(id!==null){var d=C.find(x=>String(x.id)===String(id));if(d){detail(d);return;}}tabs();renderList();});
"""

# ===== CARD DETAIL =====
CARDDETAIL_BODY=('<style>'
 '.cdhero{padding:24px 16px 18px;text-align:center;border-bottom:1px solid var(--line)}'
 '.cdhero .pl{width:208px;height:131px;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:12px;background:#eef0f3;font-size:38px}'
 '.cdhero .pl img{width:100%;height:100%;object-fit:cover;border-radius:12px;filter:drop-shadow(0 8px 18px rgba(0,0,0,.16))}'
 '.cdhero .pl img.isdef{object-fit:cover}'
 '.cdhero .iss{font-size:13px;color:var(--sub);font-weight:700}.cdhero .nm{font-size:22px;font-weight:900;margin-top:6px;letter-spacing:-.5px}'
 '.cdhero .ds{font-size:13.5px;color:#55555e;margin-top:8px}.cdhero .fee{font-size:12.5px;color:var(--dim);margin-top:6px}'
 '.sec2{padding:22px 0 12px;font-size:17px;font-weight:900}'
 '.bhead{font-size:12.5px;color:var(--sub);font-weight:700;margin-bottom:10px}'
 '.bgrp{border:1px solid var(--line);border-radius:14px;padding:2px 14px;margin-bottom:12px}'
 '.lcap{font-size:12px;font-weight:800;color:var(--accent);padding:11px 0 2px}'
 '.bitem{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}.bitem:last-child{border-bottom:0}'
 '.bareas{flex:1;display:flex;flex-wrap:wrap;gap:5px}.ba{font-size:12px;font-weight:700;color:#55555e;background:var(--surface2);padding:3px 8px;border-radius:6px}'
 '.bval{flex:0 0 auto;text-align:right}.bv{font-size:15px;font-weight:900;color:var(--accent)}.bm{font-size:11px;color:var(--sub);margin-left:3px}'
 '.btier{font-size:10px;font-weight:800;color:#e8a33c;background:#fbf0df;padding:2px 6px;border-radius:5px;margin-left:6px}'
 '.bnone{color:var(--sub);font-size:13.5px;padding:6px 0 14px}'
 '.evlist{display:flex;flex-direction:column;gap:8px}'
 '.evrow{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:12px;padding:12px 14px}'
 '.evrow .pf{font-size:11px;font-weight:800;color:#fff;padding:4px 9px;border-radius:7px;flex:0 0 auto}.evrow .am{flex:1;font-size:14px;font-weight:800;color:var(--accent)}'
 '.evrow.off{opacity:.6}.evrow .am.none{color:var(--dim);font-weight:600;font-size:13px}'
 '.evrow .more{flex:0 0 auto;color:var(--blue);font-size:12.5px;font-weight:700;white-space:nowrap}'
 '.applybtns{display:flex;flex-direction:column;gap:10px;padding:18px 0 8px}'
 '.applybtns a{display:block;text-align:center;font-size:15px;font-weight:800;padding:15px;border-radius:13px}'
 '.applybtns a.primary{background:var(--accent);color:#fff}.applybtns a.sec{background:var(--surface2);color:var(--text);border:1px solid var(--line)}'
 '.rellink{display:block;text-align:center;font-size:13px;color:var(--blue);font-weight:700;padding:14px 0 40px}'
 '.platgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:4px 0 2px}'
 '.platgrid a{display:flex;align-items:center;gap:9px;border:1px solid var(--line);border-radius:13px;padding:14px 13px;font-weight:800;font-size:13.5px;background:var(--surface)}'
 '.platgrid a .dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}.platgrid a .pn{flex:1}.platgrid a .go{color:var(--sub);font-size:13px}'
 '.offnote{font-size:11.5px;color:var(--dim);padding:9px 2px 2px;line-height:1.5}'
 '</style>'
 '<div style="padding:12px 0"><div class="wrap"><a class="bk" href="cards.html">‹</a></div></div>'
 '<div class="wrap"><div id="root"><div class="empty">불러오는 중…</div></div></div>')
CARDDETAIL_JS=r"""
var PCOL={"카드고릴라":"#ff4d4f","뱅크샐러드":"#2f6bff","아정당":"#3b5bdb","카카오페이":"#e8b800","토스":"#3182f6"};
var _qp=new URLSearchParams(location.search);
var id=Number(_qp.get('id'));var nParam=_qp.get('n');
Promise.all([fetch('cards.json').then(r=>r.json()),fetch('events.json').then(r=>r.json()).catch(function(){return {items:[]};}),fetch('platform_events.json').then(r=>r.json()).catch(function(){return {products:[]};})]).then(function(A){
 var j=A[0],EVT=(A[1]&&A[1].items)||[],PE=(A[2]&&A[2].products)||[];
 function _nk(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
 function _wmc(n){if(!n)return'';if(n>=10000)return(Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
 function _rwdc(t,w){return (w&&w>0)?('최대 '+_wmc(w)+' 캐시백'):(t||'');}   // 이벤트명 통일(금액+캐시백)
 var PEMAP={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',naver:'네이버페이',ajungdang:'아정당'};
 var card=null,issuer='';
 // ?n=카드명 우선(비교표에서 넘어옴). 정확→퍼지 매칭. 없으면 ?id=cards.json id.
 if(nParam){var nk0=_nk(nParam);
  for(var k in j.cards){var f=(j.cards[k]||[]).filter(function(c){return _nk(c.name)===nk0;})[0];if(f){card=f;issuer=k;break;}}
  if(!card){for(var k2 in j.cards){var f2=(j.cards[k2]||[]).filter(function(c){var cn=_nk(c.name);return cn&&(cn.indexOf(nk0)>=0||nk0.indexOf(cn)>=0);})[0];if(f2){card=f2;issuer=k2;break;}}}
 }
 if(!card&&!isNaN(id)){for(var k3 in j.cards){var f3=(j.cards[k3]||[]).filter(function(c){return c.id===id;})[0];if(f3){card=f3;issuer=k3;break;}}}
 // platform_events 매칭(이름 기준 정확→퍼지) — 비교표↔상세 정합 핵심
 var matchName=card?card.name:(nParam||'');var ck=_nk(matchName);
 var pmatch=PE.filter(function(p){return _nk(p.name)===ck;})[0]||PE.filter(function(p){var pn=_nk(p.name);return pn&&ck&&(pn.indexOf(ck)>=0||ck.indexOf(pn)>=0);})[0];
 if(!card&&pmatch){card={name:pmatch.name,issuer:pmatch.issuer||'',benefit:'',fee:'',detail:null,plat:{},events:[]};issuer=pmatch.issuer||'';}
 if(!card){document.getElementById('root').innerHTML='<div class="empty">카드를 찾을 수 없어요. <a class="accent" href="cards.html">카드찾기</a></div>';return;}
 var _imgurl=card.img;
 function _rel(e){var cn=(card.name||'').toLowerCase();var ec=(e.card||'').toLowerCase();return ec&&cn&&(ec.indexOf(cn)>=0||cn.indexOf(ec)>=0);}
 var spec=EVT.filter(function(e){return e.issuer===issuer&&_rel(e);});
 var img=imgTag(_imgurl||(pmatch&&pmatch.img));   // 메타 이미지 폴백(콜렉터 카드고릴라 플레이트)
 var platBenefit={},platUrl={};
 if(pmatch){(pmatch.events||[]).forEach(function(e){var nm=PEMAP[e.platform]||e.platform;if(!platBenefit[nm]){platBenefit[nm]=_rwdc(e.reward_text,e.reward_won);var _pp=(pmatch.platforms||{})[e.platform]||{};platUrl[nm]=e.url||_pp.url||_purl(e.platform,_pp.id)||'';}});}
 (card.events||[]).forEach(function(e){if(e.platform&&!platBenefit[e.platform])platBenefit[e.platform]=e.amount;});       // 폴백(옛 데이터)
 spec.forEach(function(e){if(e.platform&&!platBenefit[e.platform])platBenefit[e.platform]=e.benefit;});
 var PL=card.plat||{};var src=card.source||'';
 function _won(s){var m=(s||'').replace(/,/g,'').match(/([0-9]+(?:\.[0-9]+)?)\s*(억|만)/);return m?parseFloat(m[1])*(m[2]==='억'?10000:1):0;}
 function _src(d){return src.indexOf(d)>=0;}
 var allP=[
  {k:'토스',c:'#3182f6',u:platUrl['토스']||PL['토스']||(_src('toss')?src:''),mapped:!!(PL['토스']||_src('toss')||platBenefit['토스'])},
  {k:'카드고릴라',c:'#ff4d4f',u:platUrl['카드고릴라']||PL['카드고릴라']||(_src('gorilla')?src:''),mapped:!!(PL['카드고릴라']||_src('gorilla')||platBenefit['카드고릴라'])},
  {k:'뱅크샐러드',c:'#2f6bff',u:platUrl['뱅크샐러드']||PL['뱅크샐러드']||(_src('banksalad')?src:''),mapped:!!(PL['뱅크샐러드']||_src('banksalad')||platBenefit['뱅크샐러드'])},
  {k:'아정당',c:'#3b5bdb',u:platUrl['아정당']||PL['아정당']||(_src('ajd')||_src('jungdang')?src:''),mapped:!!(PL['아정당']||_src('ajd')||_src('jungdang')||platBenefit['아정당'])},
  {k:'네이버페이',c:'#03c75a',u:platUrl['네이버페이']||'https://card.pay.naver.com/home/promotion/event',mapped:!!platBenefit['네이버페이']}
 ];
 var plats=allP.filter(function(p){return p.mapped||platBenefit[p.k];});           // 맵핑/이벤트 있는 플랫폼만
 plats.sort(function(a,b){return _won(platBenefit[b.k])-_won(platBenefit[a.k]);});  // 금액 높은 순
 var ev=plats.length?('<div class="sec2">플랫폼별 발급 이벤트</div><div class="evlist">'+plats.map(function(p){var b=platBenefit[p.k];var amt=b?('<span class="am">'+b+'</span>'):'<span class="am none">이벤트 없음</span>';return '<a class="evrow'+(b?'':' off')+'" href="'+(p.u||'#')+'" target="_blank" rel="noopener" data-track="plat" data-label="'+p.k+'"><span class="pf" style="background:'+p.c+'">'+p.k+'</span>'+amt+'<span class="more">자세히보기 ›</span></a>';}).join('')+'</div>'):'';
 var apply='<div class="sec2">🔗 카드사·이벤트 바로가기</div><div class="evlist">'+
  '<a class="evrow" href="issue.html?issuer='+encodeURIComponent(issuer)+'" data-track="issuer-events" data-label="'+issuer+'"><span class="pf" style="background:#e8843c">발급이벤트</span><span class="am" style="color:var(--text);font-weight:700">진행 중인 '+issuer+' 카드 이벤트</span><span class="more">보기 ›</span></a>'+
  (card.url?'<a class="evrow" href="'+card.url+'" target="_blank" rel="noopener" data-track="official" data-label="'+issuer+'"><span class="pf" style="background:#565d68">카드사</span><span class="am" style="color:var(--text);font-weight:700">'+issuer+' 공식 홈페이지 신청</span><span class="more">바로가기 ›</span></a>':'')+
  '</div><div class="offnote">※ 같은 카드라도 발급 채널(플랫폼)에 따라 캐시백·사은품이 달라질 수 있어요. 상세 혜택·한도는 각 플랫폼/카드사 페이지에서 최종 확인하세요.</div>';
 document.getElementById('root').innerHTML=
  '<div class="cdhero"><div class="pl">'+img+'</div><div class="iss">'+issuer+'</div><div class="nm">'+card.name+'</div><div class="ds">'+(card.benefit||'')+'</div>'+(card.fee?'<div class="fee">연회비 '+card.fee+'</div>':'')+'</div>'+
  '<div class="sec2">카드 혜택</div>'+renderBenefit(card.detail)+ev+apply;
 document.title=card.name+' | 카드티라노';
});
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
 +tybnr("chart.html","CARDTYRANNO · 티라노차트","시중 플랫폼 순위를 한 표로","토스·카드고릴라·뱅크샐러드의 카드 순위를 평균낸 카드티라노 랭킹이에요.")
 +'<section><div class="sec-h"><h2>티라노차트</h2></div>'
 '<div class="muted" style="font-size:12.5px;padding-bottom:10px">시중 플랫폼 순위 평균이에요.</div>'
 '<div class="tabs" id="tabs"></div><div id="list"><div class="empty">불러오는 중…</div></div></section></div>')
CHART_JS=r"""
var R=[],ORD=[],cur="전체";
function render(){var items=cur==="전체"?R:R.filter(function(x){return x.issuer===cur;});
 document.getElementById('list').innerHTML=items.map(function(x,i){var rs=[];if(x.toss)rs.push('토스 '+x.toss+'위');if(x.cg)rs.push('고릴라 '+x.cg+'위');if(x.bs)rs.push('뱅샐 '+x.bs+'위');
  var href=(x.id!=null)?('carddetail.html?id='+x.id):'cards.html';var rk=i+1;
  return '<a class="crow" href="'+href+'"><span class="no'+(rk<=3?' top':'')+'">'+rk+'</span><span class="pl">'+imgTag(x.img)+'</span><div class="ci"><div class="cn">'+x.name+'</div><div class="cs">'+(x.issuer||'')+' · <span class="src">'+rs.join(' / ')+'</span></div></div></a>';}).join("");}
function tabs(){var T=["전체"].concat(ORD);var t=document.getElementById('tabs');t.innerHTML=T.map(function(o){return '<div class="tab'+(o===cur?' active':'')+'" data-t="'+o+'">'+o+'</div>';}).join("");
 t.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){cur=b.dataset.t;t.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));b.classList.add('active');render();};});}
function _nk(s){return (s||'').replace(/[\s()（）·\-_/+]+/g,'').toLowerCase();}
Promise.all([fetch('rank.json').then(r=>r.json()),fetch('cards.json').then(r=>r.json())]).then(function(a){
 R=a[0].items;var m={};for(var k in a[1].cards){(a[1].cards[k]||[]).forEach(function(c){m[_nk(c.name)]=c.id;});}
 R.forEach(function(x){var k=_nk(x.name);if(m[k]!=null)x.id=m[k];else{var alt=_nk((x.name||'').replace(/^토스\s*/,''));if(m[alt]!=null)x.id=m[alt];}});
 ORD=[...new Set(R.map(function(x){return x.issuer;}).filter(Boolean))];tabs();render();});
"""

# ===== FAVORITES (관심카드) =====
FAV_BODY=('<div class="wrap"><section><div class="sec-h"><h2>관심 카드</h2></div>'
 '<div class="muted" style="font-size:12.5px;padding-bottom:8px">로그인 없이 이 브라우저에 저장돼요. 담은 카드를 한눈에 비교하세요.</div>'
 '<div class="cgrid" id="list"><div class="empty">불러오는 중…</div></div></section></div>')
FAV_JS=r"""
fetch('cards.json').then(r=>r.json()).then(function(j){
 var all=[];for(var k in j.cards){(j.cards[k]||[]).forEach(function(c){c._iss=k;all.push(c);});}
 function render(){var fav=getFav();var items=all.filter(function(c){return fav.indexOf(c.id)>=0;});var L=document.getElementById('list');
  if(!items.length){L.innerHTML='<div class="empty">아직 관심 카드가 없어요.<br><br><a class="accent" href="cards.html">카드찾기에서 🤍를 눌러 담아보세요 ›</a></div>';updateFavCount();return;}
  L.innerHTML=items.map(function(c){var fee=c.fee?('연회비 '+c.fee):'';
   var hb='<span class="favbtn" onclick="event.preventDefault();event.stopPropagation();toggleFav('+c.id+');window._fr();">❤️</span>';
   return '<a class="ctile" href="carddetail.html?id='+c.id+'">'+hb+'<div class="plate">'+imgTag(c.img)+'</div><div class="cn">'+c.name+'</div>'+(fee?'<div class="cfee">'+fee+'</div>':'')+'<div class="cd">'+c._iss+' · '+c.benefit+'</div></a>';}).join("");updateFavCount();}
 window._fr=render; render();
});
"""

# ===== SEARCH (통합검색) =====
SEARCH_BODY=('<div class="wrap"><div class="search" style="margin:16px 0"><span>🔎</span><input id="q2" placeholder="카드 · 카드사 · 가맹점 · 혜택 검색"><button class="go" id="q2go">검색</button></div>'
 '<div id="results"><div class="empty">검색어를 입력하세요.</div></div></div>')
SEARCH_JS=r"""
var Q=(new URLSearchParams(location.search).get('q')||'').trim();var CC=[],DD=[],EE=[];
function lc(s){return (s||'').toLowerCase();}
function run(q){q=(q||'').trim();var R=document.getElementById('results');if(!q){R.innerHTML='<div class="empty">검색어를 입력하세요.</div>';return;}
 var ql=q.toLowerCase();
 var c=CC.filter(function(x){return lc(x.name+x._iss+x.benefit).indexOf(ql)>=0;}).slice(0,40);
 var d=DD.filter(function(x){return lc(x.plat+x.card+x.type+x.disc+x.cond).indexOf(ql)>=0;}).slice(0,30);
 var e=EE.filter(function(x){return lc(x.card+x.issuer+x.platform+x.benefit).indexOf(ql)>=0;}).slice(0,30);
 var h='';
 if(c.length)h+='<section><div class="sec-h"><h2>카드 ('+c.length+')</h2></div><div class="list">'+c.map(function(x){return '<a class="item" href="carddetail.html?id='+x.id+'"><div class="th"></div><div class="body"><div class="l1"><span class="store">'+x._iss+'</span></div><div class="l2">'+x.name+'</div><div class="l3">'+(x.benefit||'')+'</div></div><div class="chev">›</div></a>';}).join('')+'</div></section>';
 if(d.length)h+='<section><div class="sec-h"><h2>카드 할인 ('+d.length+')</h2></div><div class="list">'+d.map(function(x){return '<a class="item" href="detail.html?id='+x.id+'"><div class="th"></div><div class="body"><div class="l1"><span class="store">'+x.plat+'</span></div><div class="l2"><span class="hl">'+x.disc+'</span> '+x.type+'</div><div class="l3">'+x.card+'</div></div><div class="chev">›</div></a>';}).join('')+'</div></section>';
 if(e.length)h+='<section><div class="sec-h"><h2>발급 이벤트 ('+e.length+')</h2></div><div class="list">'+e.map(function(x){return '<a class="item" href="issue.html"><div class="th"></div><div class="body"><div class="l1"><span class="store">'+x.issuer+' · '+x.platform+'</span></div><div class="l2">'+x.card+'</div><div class="l3">'+x.benefit+'</div></div><div class="chev">›</div></a>';}).join('')+'</div></section>';
 R.innerHTML=h||('<div class="empty">"'+q+'" 검색 결과가 없어요.</div>');}
Promise.all([fetch('cards.json').then(r=>r.json()),fetch('data.json').then(r=>r.json()),fetch('events.json').then(r=>r.json())]).then(function(a){
 var cj=a[0];for(var k in cj.cards){(cj.cards[k]||[]).forEach(function(c){c._iss=k;CC.push(c);});}
 DD=a[1].items;EE=a[2].items;
 var inp=document.getElementById('q2');inp.value=Q;inp.addEventListener('keydown',function(ev){if(ev.key==='Enter')run(inp.value);});
 document.getElementById('q2go').onclick=function(){run(inp.value);};
 if(Q)run(Q);});
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
 '<div class="dnote">📡 <b>스크래핑 헬스</b>는 콜렉터 산출물(platform_events.json)을 실시간 분석해 플랫폼·카드사별 수집 상태를 보여줍니다. 아래 <b>방문 지표</b>는 이 브라우저 로컬 집계예요(전체 통합은 Cloudflare Web Analytics 연결 시 제공).</div>'
 '<div class="dsec"><h3>📡 플랫폼별 스크래핑 상태</h3><div class="hgrid" id="hplat"></div><div id="hfresh" class="empty2"></div></div>'
 '<div class="dsec"><h3>🏦 카드사별 커버리지</h3><div id="hiss"></div></div>'
 '<div class="sec-h" style="margin-top:8px"><h2 style="font-size:18px">👣 방문 지표 (이 브라우저)</h2></div>'
 '<div class="dbtns"><button id="rf">↻ 새로고침</button><button id="csv">⬇ CSV 내보내기</button><button id="rs">🗑 이 브라우저 초기화</button></div>'
 '<div class="kpis" id="kpis"></div><div id="secs"></div>'
 '<div class="dsec"><h3>🕒 최근 활동</h3><div id="log"></div></div></div>')
DASHBOARD_JS=r"""
// === 스크래핑 헬스 — 콜렉터 산출물(platform_events.json) 실시간 분석 ===
(function(){var PN={cardgorilla:'카드고릴라',banksalad:'뱅크샐러드',toss:'토스',ajungdang:'아정당',naver:'네이버페이'};var PORD=['cardgorilla','banksalad','toss','ajungdang','naver'];var PC={cardgorilla:'#ff4d4f',banksalad:'#2f6bff',toss:'#3182f6',ajungdang:'#3b5bdb',naver:'#03c75a'};
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
function PG(p){var M={'index.html':'홈','discount.html':'카드 혜택','cards.html':'카드찾기','issue.html':'발급 이벤트','chart.html':'티라노차트','content.html':'가이드','carddetail.html':'카드 상세','detail.html':'혜택 상세','favorites.html':'관심카드','search.html':'검색','dashboard.html':'대시보드'};return M[p]||p;}
function agg(ev,type,keyfn){var m={};ev.forEach(function(e){if(type&&e.t!==type)return;var k=keyfn(e);if(!k)return;m[k]=(m[k]||0)+1;});return Object.keys(m).map(function(k){return [k,m[k]];}).sort(function(a,b){return b[1]-a[1];});}
function bars(rows,n){rows=rows.slice(0,n||8);if(!rows.length)return '<div class="empty2">아직 데이터가 없어요.</div>';var max=rows[0][1]||1;return rows.map(function(r){return '<div class="bar"><span class="bl">'+esc(r[0])+'</span><span class="bt"><span class="bf" style="width:'+Math.max(6,Math.round(r[1]/max*100))+'%"></span></span><span class="bn">'+r[1]+'</span></div>';}).join('');}
function kpi(n,l){return '<div class="kpi"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';}
function render(){
 var ev=[];try{ev=JSON.parse(localStorage.getItem('ct_evt')||'[]');}catch(_){}
 var pv=ev.filter(function(e){return e.t==='pageview';}).length;
 var first=Number(localStorage.getItem('ct_first')||0);var fd=first?new Date(first).toLocaleDateString('ko-KR'):'-';
 document.getElementById('kpis').innerHTML=kpi(pv,'페이지뷰')+kpi(ev.length,'총 이벤트')+kpi(new Set(ev.map(function(e){return e.p;})).size,'방문 페이지수')+kpi(fd,'첫 방문');
 var secs=[
  ['📄 페이지별 조회', bars(agg(ev,'pageview',function(e){return PG(e.l||e.p);}))],
  ['🧭 메뉴 클릭', bars(agg(ev,'menu',function(e){return e.l;}))],
  ['카드 클릭(상품)', bars(agg(ev,'card',function(e){return e.l;}))],
  ['필터·카드사 탭', bars(agg(ev,'filter',function(e){return e.l;}))],
  ['📂 업종 카테고리 클릭', bars(agg(ev,'category',function(e){return e.l;}))],
  ['🔗 플랫폼 상세 클릭', bars(agg(ev,'plat',function(e){return e.l;}))],
  ['카드사 공식 클릭', bars(agg(ev,'official',function(e){return e.l;}))],
  ['발급 이벤트 클릭', bars(agg(ev,'event',function(e){return e.l;}))],
  ['🔎 리스트/검색 클릭', bars(agg(ev,'item',function(e){return e.l;}))]
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
 '<div class="isec"><h3>🛫 업종별 할부 (항공·백화점·가전)</h3>'+_cat+'</div>'
 '<div class="muted" style="font-size:11.5px;line-height:1.6">※ 2026년 6월 기준 수집 정보로 실제와 다를 수 있어요. 무이자할부는 보통 건별 5만원 이상 결제 시 적용되며, 부분무이자는 일부 회차 수수료가 발생합니다.</div>'
 '</div>')

# ===== BUILD =====
page("index.html",BRAND+" | 이번 달 카드 혜택·발급 이벤트 비교","2026년 6월 카드 발급 혜택과 카드 할인 혜택을 토스·카드고릴라·아정당·뱅크샐러드 등 플랫폼별로 비교. 이번 달 리워드 높은 카드 랭킹과 카드 찾기까지.","/index.html",INDEX_BODY,INDEX_JS,faq_jsonld(),searchbar=True,catstrip=False,active="charts")
page("discount.html",BRAND+" | 카드 할인 혜택 (가맹점·업종별)","네이버·쿠팡·무신사·이마트·GS25 등 가맹점의 카드 즉시할인·청구할인·캐시백·무이자할부를 업종·카드사별로.","/discount.html",DISC_BODY,DISC_JS,searchbar=True,catstrip=True,active="discount")
page("cards.html",BRAND+" | 카드 찾기 (카드사별 신용카드)","삼성·현대·신한·KB국민·롯데·우리·하나·NH농협·BC·IBK 카드사별 대표 신용카드를 플레이트 이미지·연회비·혜택으로 비교.","/cards.html",CARDS_BODY,CARDS_JS,active="cards")
page("issue.html",BRAND+" | 카드 발급 혜택 (플랫폼별 비교)","카드사별 신규 발급 캐시백을 아정당·카드고릴라·토스·카카오페이 등 플랫폼별로 비교. 발급 이벤트 리스트와 최대 혜택 비교표.","/issue.html",ISSUE_BODY,ISSUE_JS,active="issue")
page("detail.html",BRAND+" | 혜택 상세","카드 할인 혜택 상세와 공식 안내 링크.","/detail.html",DETAIL_BODY,DETAIL_JS,active="discount")
page("content.html",BRAND+" | 카드 가이드","연회비 캐시백, 전월실적, 즉시할인 vs 청구할인, 해외카드까지 카드 똑똑하게 쓰는 법.","/content.html",CONTENT_BODY,CONTENT_JS,active="content")
page("carddetail.html",BRAND+" | 카드 상세 혜택","카드별 영역 혜택·연회비·전월실적·발급 이벤트를 한눈에. 플랫폼별 신청 링크 제공.","/carddetail.html",CARDDETAIL_BODY,CARDDETAIL_JS,active="cards")
page("chart.html",BRAND+" | 티라노차트","시중 플랫폼(토스·카드고릴라·뱅크샐러드) 순위를 평균낸 카드티라노 티라노차트.","/chart.html",CHART_BODY,CHART_JS,active="charts")
page("favorites.html",BRAND+" | 관심 카드","담아둔 관심 카드를 한눈에 비교. 로그인 없이 브라우저에 저장.","/favorites.html",FAV_BODY,FAV_JS,active="")
page("search.html",BRAND+" | 검색","카드·카드사·가맹점·혜택을 한 번에 검색.","/search.html",SEARCH_BODY,SEARCH_JS,active="")
page("installment.html",BRAND+" | 무이자·부분무이자 할부","카드사별·업종별(항공·백화점·가전) 무이자/부분무이자 할부를 2026년 6월 기준으로 정리.","/installment.html",INSTALLMENT_BODY,"",active="discount")
page("dashboard.html",BRAND+" | 통계 대시보드","방문·클릭 통계 (관리자 전용).","/dashboard.html",DASHBOARD_BODY,DASHBOARD_JS,active="",noindex=True)

# robots.txt — AI 크롤러 환영 (AEO)
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

# sitemap
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in ["/","/discount.html","/cards.html","/issue.html","/content.html","/chart.html","/search.html","/installment.html"]:
    sm+='<url><loc>%s%s</loc><lastmod>2026-06-21</lastmod><changefreq>daily</changefreq></url>\n'%(BASE,p)
sm+='</urlset>\n'
open(os.path.join(SITE,"sitemap.xml"),"w").write(sm)
print("dark site built:",[f for f in sorted(os.listdir(SITE)) if f.endswith(('.html','.txt','.xml'))])
"""
"""
