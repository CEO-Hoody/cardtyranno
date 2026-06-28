# -*- coding: utf-8 -*-
"""카드티라노 데이터 빌더 v2 — 카드메타(연회비 포함)·발급이벤트·플랫폼비교를 SQLite에 적재 후 site/*.json export."""
import os, json, sqlite3, shutil
OUT="/sessions/busy-charming-mayer/mnt/제휴마케팅 콜렉터"; SITE=os.path.join(OUT,"site")
DBL="/tmp/cardtyrano.db"; DBF=os.path.join(OUT,"cardtyrano.db")
# 카드 콘텐츠(자체 작성) export
try:
    from content_data import CONTENT
    _ct=[{**c,"id":i} for i,c in enumerate(CONTENT)]
    json.dump({"updated":"2026-06-20","items":_ct},open(os.path.join(SITE,"content.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
except Exception as _e:
    print("content skip:",_e)
T="https://static.toss.im/assets/credit-card/"
def c(name,img,fee,ben,cid): return {"name":name,"img":img,"fee":fee,"benefit":ben,"url":"https://card-lounge.toss.im/card/"+cid}

CARDS={
"삼성카드":[
 c("토스 삼성카드",T+"toss_samsung.png","15,000원","토스페이·토스쇼핑 15%·온라인 10% 결제일할인","10279"),
 c("삼성카드 taptap O",T+"2936.png","10,000원","대중교통·통신 10% 결제일할인·연 최대 36만원","17"),
 c("Toss taptap S",T+"samsung-taptap-s.png","10,000원","국내외 1% 빅포인트 적립","16"),
 c("삼성 iD 달달할인 카드",T+"samsung-id-monthly-discount-bubble.png","29,000원","생활요금 정기결제 10% 결제일할인","1366"),
 c("삼성 iD EV 카드",T+"1797.png","15,000원","전기차 충전요금 최대 70% 결제일할인","5461"),
 c("삼성 iD PLUG-IN 카드",T+"samsung_iDPLUG-IN.png","20,000원","전기차·주차·보험·해외 맞춤 할인","10275"),
 c("AI 구독 클럽 삼성카드",T+"credit-card-new/samsung_AI_구독_클럽_삼성카드.png","20,000원","삼성전자 AI 구독 클럽 특화 혜택","11045"),
 c("신세계이마트 삼성카드 SFC 7",T+"1958.png","18,000원","빅포인트 0.5~3% 적립·신세계·이마트","5936"),
 c("신세계이마트 삼성카드 SFC 2",T+"2025070121.png","18,000원","음식점 1% 빅포인트 적립","5331"),
 c("신세계이마트 삼성카드 SFC 4",T+"2025070130.png","10,000원","0.7% 빅포인트 적립","6216"),
 c("신세계이마트 삼성카드 5",T+"2025090103.png","12,000원","생활쇼핑·아이교육 혜택","5299"),
 c("네이버페이 taptap BY SAMSUNG",T+"1676.png","15,000원","라이프스타일 옵션 패키지","5085"),
 c("모니모카드",T+"1915.png","10,000원","커피 50% 할인","5838"),
 c("T나는혜택 삼성카드",T+"1912.png","20,000원","통신비 최대 16,000원 할인","5854"),
 c("삼성 SFC & MILEAGE PLATINUM",T+"2025080801.png","47,000원","1,000원당 스카이패스 1마일 적립","6320")],
"현대카드":[
 c("현대카드 M",T+"wood.png","30,000원","국내외 1.5% M포인트 적립","1827"),
 c("현대카드 ZERO Edition3(포인트형)",T+"2266.png","15,000원","국내외 1.2% M포인트 적립","1822"),
 c("현대카드 ZERO Edition3(할인형)",T+"2266.png","15,000원","국내외 0.8% 청구할인","1820"),
 c("현대카드 MX Black Edition2",T+"2803.png","200,000원","국내외 1% M포인트 + 5개영역 10% 청구할인","1900"),
 c("현대카드 Z family Edition2",T+"10192.png","20,000원","온라인몰·병원·약국·학원·주유 10% 청구할인","1833"),
 c("현대카드 Z work Edition2",T+"10194.png","20,000원","온라인·편의점·커피·교통·도서 10% 청구할인","1835"),
 c("현대카드 Z play",T+"10188.png","20,000원","온라인쇼핑·음식점·영화·해외 10% 청구할인","1831"),
 c("NOL 카드",T+"2078.png","20,000원","NOL·인터파크·트리플 10% 적립","6172"),
 c("배민현대카드",T+"1683.png","10,000원","배민페이 결제 3% 포인트 적립","5049"),
 c("네이버 현대카드",T+"2025070111.png","10,000원","네이버플러스 무료·네이버페이 최대 5% 적립","5735"),
 c("네이버 현대카드 Edition2",T+"hyundai-naver-edition2.png","20,000원","네이버페이 포인트 적립","10211"),
 c("Hyundai EV카드",T+"2133.png","30,000원","전기·수소차 충전 적립·블루멤버스 3%","6288"),
 c("이마트 e카드 Edition2",T+"1664.png","20,000원","당월 0.1~5% 신세계포인트 적립","5131"),
 c("Hyundai Mobility Platinum",T+"2050.png","70,000원","블루멤버스 적립·차량정비 2만원 할인","6118"),
 c("Kia Members 전기차 카드",T+"2259.png","30,000원","전기차 충전 30~70% 할인·M포인트","6522"),
 c("Kia Members 카드 Edition2",T+"3045.png","30,000원","기아멤버스·M포인트 적립","7224")],
"신한카드":[
 c("토스 신한카드 Mr.Life",T+"3480.png","15,000원","전기·도시가스·통신 및 생활영역 10% 할인","1259"),
 c("토스 신한카드 YOLO",T+"credit-card-new/sh_toss_yolo.png","15,000원","커피·편의점·택시·영화 할인율 선택","1261"),
 c("신한카드 Deep Oil",T+"2025070113.png","10,000원","주유소 10%·정비·주차 10% 할인","34"),
 c("신한카드 Deep Dream Platinum+",T+"993.png","30,000원","전월실적 없는 포인트 적립·해외 10% 캐시백","993"),
 c("신한카드 Deep Dream",T+"shinhan_deepdream.png","","속 깊은 디지털 라이프 적립","989"),
 c("신한카드 EV",T+"1937.png","","전기차 LIFE 특화 혜택","1937"),
 c("신한카드 EVerywhere",T+"2025090105.png","","전기차 충전 혜택","2025090105"),
 c("신한카드 Simple Plan+",T+"credit-card-new/sh_simple_plan_plus_core.png","","주유 3만원↑ 시 3만원 웰컴 캐시백","8594"),
 c("LG전자 The 구독케어 신한카드",T+"8322.png","","LG전자 구독료 케어 혜택","8322")],
"KB국민카드":[
 c("KB국민 굿데이카드",T+"1121.png","10,000원","주유·통신·교통·음식점 10% 청구할인","1121"),
 c("KB국민 굿데이올림카드",T+"kb_goodday_olim.png","20,000원","주유·대형마트·통신·교통 10% 청구할인","50"),
 c("KB국민 다담카드",T+"kb_dadam.png","20,000원","기본할인 + 선택팩(생활·교육·쇼핑 등)","701"),
 c("KB국민 WE:SH Travel",T+"2801.png","25,000원","해외 수수료 1.25% 면제·공항 라운지 무료","1906"),
 c("KB 청춘대로 톡톡카드",T+"55.png","","간편결제 10% 할인","55"),
 c("KB국민 My WE:SH 카드",T+"1468.png","","간편결제 10% 할인","1467"),
 c("KB국민 Easy on카드",T+"1097.png","","제과점·카페 5% 할인","1097")],
"롯데카드":[
 c("토스 LIKIT ALL",T+"1418.png","14,000원","국내외 1% 결제일 할인","1418"),
 c("LOCA LIKIT 1.2 카드",T+"1677.png","10,000원","국내외 1.2%·온라인 1.5% 할인","5083"),
 c("LOCA 365",T+"1477.png","20,000원","생활업종 월 최대 36,500원 결제일 할인","1477"),
 c("LG구독엔로카",T+"lottecard-lg-subscribe.png","20,000원","LG전자 구독료 최대 26,000원 할인","10207"),
 c("DIGILOCA SKYPASS",T+"2025090102.png","20,000원","실적조건 없이 마일리지 적립","10343"),
 c("Mobile x LOCA SE",T+"25090301.png","","이동통신비 최대 2만원 할인","10365"),
 c("LOCA LIKIT",T+"1305.png","","버스·지하철 10% 할인","1583"),
 c("LOCA LIKIT Eat",T+"1770.png","","음식점 60% 할인","1699"),
 c("LOCA LIKIT Shop",T+"1810.png","","온라인 쇼핑 60% 할인","1731"),
 c("롯데하이마트 Hi-Plan 롤라카드",T+"1987.png","","하이마트 5% 할인","1987"),
 c("디지로카 Link",T+"new/lotte_DiGiLOCA_LINK.png","","커피 5% 결제일할인","10489"),
 c("LOCA Biz",T+"new/lotte_LOCA_Biz.JPG","","주유 3% 할인","10491"),
 c("보험엔로카",T+"credit-card-new/lotte_보험엔로카.png","","보험료 할인 특화","2098")],
"하나카드":[
 c("하나 클럽SK카드(CLUB SK)",T+"credit-card-new/%ED%95%98%EB%82%98%20%ED%81%B4%EB%9F%BDSK%EC%B9%B4%EB%93%9C%28CLUB%20SK%29.png","6,000원","통신·주유·영화·외식·커피 할인","5"),
 c("하나 스카이패스 아멕스 플래티늄",T+"1420.png","45,000원","1천원당 최대 2마일·인천공항 라운지 무료","1420"),
 c("원더카드2.0 FREE+",T+"20030.png","19,000원","국내외 0.8%·배달·온라인·택시 4% 청구할인","10209"),
 c("JADE Classic",T+"2182.png","120,000원","공항라운지·면세점 1.5% 적립","1818"),
 c("JADE Prime",T+"2817.png","300,000원","공항라운지 무료·면세점 3% 적립","1932"),
 c("트래블로그 신용카드",T+"1878.png","20,000원","외화 하나머니 적립 트래블 카드","1793"),
 c("HD현대 패밀리카드",T+"2132.png","100,000원","현대오일뱅크 리터당 150원 청구할인","6286"),
 c("BIGPOT(빅팟) 카드",T+"1629.png","4,000원","SK주유·외식·커피 10%·영화 할인","5235"),
 c("SMART ANY 카드",T+"1669.png","5,000원","전가맹점 0.8%·온라인 1.3% 청구할인","5115"),
 c("더 심플 하나카드",T+"2025070108.png","25,000원","월납요금 1만/1.5만원 청구할인","6420"),
 c("하나 MULTI Living",T+"1340.png","12,000원","온라인·마트·주유·백화점 청구할인","1340"),
 c("하나 MULTI Oil",T+"1338.png","15,000원","주유 10% 할인·생활 할인","1338"),
 c("Any PLUS 카드",T+"1984.png","15,000원","국내 0.7%·온라인·해외 1.7% 할인","5988")],
"우리카드":[
 c("카드의정석 2",T+"10550.png","22,000원","국내외 1.2% 할인","10175"),
 c("카드의정석 SHOPPING+",T+"2856.png","10,000원","온오프 쇼핑 10%·간편결제 5% 추가할인","1959"),
 c("카드의정석 EVERY MILE SKYPASS",T+"10168.png","39,000원","1천원당 1마일·라운지 연2회·해외수수료 면제","1761"),
 c("DA카드의정석Ⅱ",T+"2812.png","12,000원","국내외 최대 1.3% 청구할인·공항라운지","1924"),
 c("카드의정석 NEW우리V카드",T+"1668.png","2,000원","커피·통신·영화 6천원·놀이공원 할인","5117"),
 c("카드의정석 EVERY DISCOUNT",T+"10170.png","12,000원","국내외 0.8%·간편결제 2% 추가할인","10127"),
 c("카드의정석 EVERY POINT",T+"10172.png","12,000원","국내외 0.8% 적립·간편결제 2% 추가적립","10129"),
 c("SKT 우리카드+",T+"credit-card-new/woori_SKT_%EC%9A%B0%EB%A6%AC%EC%B9%B4%EB%93%9C.png","10,000원","SKT 통신요금 최대 23,000원 할인","17011"),
 c("카드의정석2 SIMPLE",T+"credit-card-new/woori_%EC%B9%B4%EB%93%9C%EC%9D%98%EC%A0%95%EC%84%9D2_SIMPLE.png","7,000원","국내외 0.8% 청구할인","11699"),
 c("DA@카드의정석 DISCOUNT",T+"credit-card-new/woori_DA_%EC%B9%B4%EB%93%9C%EC%9D%98%EC%A0%95%EC%84%9D_DISCOUNT.png","5,000원","생활쇼핑 2.0% 적립","17335"),
 c("로얄블루1000",T+"credit-card-new/woori_%EB%A1%9C%EC%96%84%EB%B8%94%EB%A3%A81000.png","1,000,000원","프리미엄 바우처·마일리지","17237"),
 c("LG전자 우리카드",T+"7093.png","15,000원","LG전자 구독요금 최대 2만원 청구할인","10217")],
"NH농협카드":[
 c("올바른 FLEX 카드",T+"1236.png","10,000원","스타벅스 50%·스트리밍·영화 할인·라운지","1236"),
 c("농협 별다줄카드",T+"1356.png","12,000원","온라인 7%·FLEX 14% 할인·라운지 연2회","1356"),
 c("zgm.play카드",T+"1821.png","12,000원","영화 5천원 청구할인·간편결제","10173"),
 c("zgm.streaming카드",T+"1814.png","12,000원","간편결제 5% 할인·스트리밍 구독","1739"),
 c("올바른하나로(Hanaro) 카드",T+"2980.png","13,000원","범농협 우대·공항 라운지 무료","10055"),
 c("NH20 해봄카드",T+"1218.png","8,000원","20대 특화 선택형 할인","1218"),
 c("올바른 NEW HAVE카드",T+"10152.png","12,000원","스마트한 적립 혜택","5097"),
 c("NH올원 LGU+카드",T+"1210.png","15,000원","LGU+ 통신료 자동이체 할인","1210"),
 c("NH올원 Rental&코웨이",T+"2196.png","10,000원","렌탈·코웨이 실속 할인","6400"),
 c("T라이트카드",T+"1212.png","15,000원","SKT 통신·커피·영화 1천원 청구할인","1212"),
 c("채움 스카이패스카드",T+"credit-card-new/%EC%B1%84%EC%9B%80%20%EC%8A%A4%EC%B9%B4%EC%9D%B4%ED%8C%A8%EC%8A%A4%EC%B9%B4%EB%93%9C.png","15,000원","1,500원당 1~3 마일리지 적립","6626"),
 c("NH올원 All100카드",T+"1981.png","8,000원","생활 가맹점 NH포인트 10% 적립","5982"),
 c("채움 BAZIC",T+"5169.png","8,000원","기본 생활 할인형","5169")],
"BC카드":[
 c("BC 바로 ZONE 카드",T+"BC_104520_a.png","19,000원","ZONE별 7% 할인·해외 1%","10467"),
 c("BC 바로 MACAO카드",T+"2854.png","12,000원","주유·마트 최대 10%·해외 2% 할인","1953"),
 c("BC 바로 에어 마스터",T+"BC_104452_a.png","29,000원","스카이패스 마일리지 적립","10469"),
 c("BC 바로 에어 맥스",T+"BC_airmax_236774-F.png","43,000원","1,500원당 최대 2마일 적립","10471"),
 c("BC 바로 클리어 플러스",T+"1824.png","5,000원","편의점·온라인·통신·스트리밍 10% 청구할인","1579"),
 c("KT SUPER DC BC 바로카드",T+"credit-card-new/bc_KT_SUPER_DC_BC_%EB%B0%94%EB%A1%9C%EC%B9%B4%EB%93%9C.png","25,000원","KT 통신요금 월 최대 9천원 할인","10503"),
 c("케이뱅크 SIMPLE 카드",T+"1807.png","10,000원","국내외 0.8%·생활 1.5% 청구할인","5659"),
 c("신세계 BC 바로 콰트로 플러스",T+"2408.png","5,000원","신세계·이마트 5%·SSG·쿠팡 7% 할인","6827"),
 c("신세계 푸빌라 BC 바로카드",T+"2479.png","10,000원","신세계백화점·SSGPAY·해외 1.7% 할인","6971"),
 c("컬리카드",T+"1996.png","12,000원","컬리 5%·해외 2% 적립","6012"),
 c("BC 바로 에어 플러스 스카이패스",T+"1825.png","19,000원","1천원당 1마일·보너스 마일리지","1559"),
 c("세븐캐쉬백카드",T+"6314.png","10,000원","월 최대 40,000원 캐시백","6314")],
"IBK기업":[
 c("IBK 포인트3.8 토스 제휴카드",T+"10184.png","37,000원","국내외 1.5%·해외 최대 5% 적립","10097"),
 c("IBK 일상의 기쁨카드",T+"ibk_happy.png","10,000원","온라인몰 20%·영화 1만원·마트 5% 할인","43"),
 c("IBK 포인트 카드",T+"10130.png","21,000원","구간별 0.6~3.3% 포인트 적립","10045"),
 c("참! 좋은 kt wiz 카드",T+"1777.png","2,000원","주유·쇼핑·영화 8천원·외식 할인","1709"),
 c("IBK 국민행복카드(신용)",T+"2908.png","없음","국가 바우처 통합·월 최대 6만원","6885"),
 c("IBK K-패스(신용)",T+"2802.png","2,000원","대중교통 K-패스 환급·택시 5% 할인","1875"),
 c("Daily With 카드",T+"1226-master.png","10,000원","버스·지하철 1% 적립 등 일상 혜택","1226"),
 c("IBK I-Mileage(대한항공)",T+"2892.png","41,000원","1천원당 1마일·공항 라운지 연2회 무료","10017"),
 c("코웨이 IBK 카드",T+"1775.png","12,000원","코웨이 렌탈료 최대 23,000원 청구할인","1705"),
 c("IBK-Hybrid카드",T+"48.png","10,000원","하이브리드 신용·체크·월 최대 6천원","48"),
 c("IBK I ALL",T+"1495.png","14,000원","전방위 생활 할인형","1495")],
}
# 확장 수집분 병합 (이름 정규화 dedup, 기존 무이미지면 새 이미지로 보강)
try:
    from extra_cards import EXTRA
except Exception:
    EXTRA={}
import re as _re
def _nk(n): return _re.sub(r"[\s()（）·\-_/+]+","",n).lower()
for _iss,_lst in EXTRA.items():
    _base=CARDS.setdefault(_iss,[])
    _seen={_nk(b["name"]):b for b in _base}
    for _cd in _lst:
        _k=_nk(_cd["name"])
        if _k in _seen:
            _b=_seen[_k]
            if not _b.get("img") and _cd.get("img"): _b["img"]=_cd["img"]
            continue
        _base.append(_cd); _seen[_k]=_cd

# 풀 스크래핑 병합 (scrape/cards_p1.json, p2.json) — 이미지·연회비 보강 + 신규 카드 추가
def _shortfee(s):
    if not s: return ""
    if "없음" in s: return "없음"
    m=_re.search(r"([\d,]+)\s*원",s); return (m.group(1)+"원") if m else ""
for _f in ["scrape/cards_p1.json","scrape/cards_p2.json"]:
    try: _sc=json.load(open(os.path.join(OUT,_f),encoding="utf-8"))
    except Exception as _e2:
        print("scrape skip",_f,_e2); continue
    for _iss,_lst in _sc.items():
        _base=CARDS.setdefault(_iss,[]); _idx={_nk(b["name"]):b for b in _base}
        for _cd in _lst:
            _k=_nk(_cd["name"]); _img=_cd.get("img",""); _fee=_shortfee(_cd.get("fee",""))
            if _k in _idx:
                _b=_idx[_k]
                if _img and not _b.get("img"): _b["img"]=_img
                if _fee and not _b.get("fee"): _b["fee"]=_fee
            else:
                _new={"name":_cd["name"],"img":_img,"fee":_fee,"benefit":"","url":_cd.get("url","")}
                _base.append(_new); _idx[_k]=_new

# 토스 ID 기반 연회비 병합 (collector.scrape_toss_fees → scrape/toss_fees.json)
# 우선순위: 카드의 toss source id(byId) → 정규화 이름(byName). 빈 fee만 채움(기존 값 보존).
try:
    _tf=json.load(open(os.path.join(OUT,"scrape/toss_fees.json"),encoding="utf-8"))
    _byId=_tf.get("byId",{}); _byName=_tf.get("byName",{}); _nfill=0
    for _iss,_lst in CARDS.items():
        for _c in _lst:
            _cur=str(_c.get("fee") or "").strip()
            if _cur and _cur not in ("","없음","-","0"): continue   # 금액 있으면 건너뜀
            _fee=""
            _src=(_c.get("source") or "")+" "+(_c.get("url") or "")
            _m=_re.search(r"/card/(\d+)", _src)               # toss 카드 id 보유 시 id 기준(정확)
            if _m and _m.group(1) in _byId: _fee=_byId[_m.group(1)].get("fee","")
            if not _fee: _fee=_byName.get(_nk(_c["name"]),"")  # 폴백: 정규화 이름
            if _fee and _fee!=_cur:
                _c["fee"]=_fee; _nfill+=1
    print(f"toss_fees 병합: {_nfill}건 연회비 보강 (byId {len(_byId)}, byName {len(_byName)})")
except FileNotFoundError:
    print("toss_fees.json 없음 — 토스 연회비 병합 스킵")
except Exception as _e3:
    print("toss_fees 병합 오류:", _e3)

# 카드 메타정보(연회비·혜택·전월실적) 병합 — collector가 수집한 card_meta.json
def _nk(n): return _re2.sub(r"[\s()（）·\-_/+.]+", "", (n or "")).lower()
try:
    _cm=json.load(open(os.path.join(OUT,"scrape","card_meta.json"),encoding="utf-8")).get("cards",{})
    _cmn=0
    for _iss, _clist in CARDS.items():
        for _c in _clist:
            _cnk=_nk(_c["name"])
            _m=_cm.get(_cnk)
            if not _m: continue
            if _m.get("annual_fee") and not _c.get("fee"):
                _c["fee"]=_m["annual_fee"]; _cmn+=1
            if _m.get("spending_req") and not (_c.get("detail") or {}).get("prev_spend"):
                _c.setdefault("detail",{})["prev_spend"]=_m["spending_req"]; _cmn+=1
            if _m.get("benefits") and not _c.get("benefit"):
                _c["benefit"]=" / ".join(_m["benefits"][:3]); _cmn+=1
    if _cmn: print(f"card_meta.json 병합 {_cmn}건")
except FileNotFoundError: pass
except Exception as _e4: print("card_meta 병합 오류:", _e4)

# 저작권 햇징: 플랫폼 소개문구 미사용 — 카드명/유형 기반으로 자체 작성한 독창적 설명으로 통일
def _gendesc(name):
    rules=[
     (r"EV|전기차|볼트업|e카드|충전","전기차 충전·친환경 소비 혜택 중심"),
     (r"트래블|트립|SKYPASS|스카이패스|마일리지|항공|여행|NOL|아시아나|대한항공|글로벌|해외","항공 마일리지·해외여행 특화"),
     (r"Oil|주유|칼텍스|S-OIL|에너지|오일|RPM|드라이브|모빌리티|Mobility|쏘카|렌터카|에너지플러스","주유·드라이브 영역 할인 중심"),
     (r"스타벅스|커피|카페|투썸","카페·디저트 할인 중심"),
     (r"쇼핑|SHOPPING|이마트|신세계|쿠팡|11번가|G마켓|옥션|SSG|올리브영|무신사|컬리|마트|백화점|아울렛|트레이더스|코스트코|하이마트|전자랜드|알라딘|교보|W컨셉|오아시스|롯데마트|MAXX","쇼핑·마트 적립/할인 특화"),
     (r"통신|SKT|KT|U\+|LGU|알뜰폰|모바일|T라이트|헬로|브로드밴드|LGE","통신비 할인 특화"),
     (r"구독|케어|렌탈|코웨이|청호|SK매직|프레딧|Z:IN|인테리어|LG구독|LG전자","구독·렌탈료 할인 중심"),
     (r"K-패스|교통|기후동행|대중교통|버스|지하철|wiz","대중교통·교통비 혜택"),
     (r"게임|넥슨|위버스|웹툰|라이온즈|트윈스|BTS|EDU|교육|학원|단비|엘리하이|쏘카|TXT|SEVENTEEN|ENHYPEN|배민|요기|문화|영화|CGV","취미·문화·생활 특화"),
     (r"Black|Purple|the Red|the Green|the Pink|the First|PRESTIGE|RAUME|JADE|BLISS|CLASSIC|PLATINUM|MX|프레스티지|플래티늄|아멕스|Amex|Diamond|Gold","프리미엄 바우처·공항 라운지 혜택"),
     (r"포인트|적립|리워드|POINT|빅포인트|더블포인트|Hi-Point|HI-POINT|3.8|All100|하나로|TOP포인트","포인트 적립 중심"),
     (r"행복|햇살|국민행복|나라사랑","정부 지원·바우처 연계"),
     (r"Deep|굿데이|다담|YOLO|Mr\.Life|Simple|정석|LIKIT|LOCA|원더|tag1|MULTI|ZERO|ANY|SMART|FLEX|별다줄|처음|디지로카|365|HAVE|클럽SK|CLUB|일상","생활 영역 할인·적립 밸런스"),
    ]
    for pat,desc in rules:
        if _re.search(pat,name,_re.I): return desc+" 카드"
    return "국내외 가맹점 적립·할인 밸런스 카드"
for _iss,_lst in CARDS.items():
    for _c in _lst: _c["benefit"]=_gendesc(_c["name"])

APPLY={"KB국민카드":"https://card.kbcard.com/CRD/DVIEW/HCAMCXPRICAC0076","신한카드":"https://www.shinhancard.com/pconts/html/card/main.html",
"삼성카드":"https://www.samsungcard.com/home/card/cardinfo/PGHPPDCCardCardinfoRecommendPC001","현대카드":"https://www.hyundaicard.com/cpc/cr/CPCCR0101_01.hc",
"하나카드":"https://www.hanacard.co.kr/OPI41000000D.web","롯데카드":"https://www.lottecard.co.kr/app/LPCDAACR_V100.lc",
"우리카드":"https://pc.wooricard.com/dcpc/yh1/crd/crd01/H1CRD101S00.do","NH농협카드":"https://card.nonghyup.com/IDDCB0001.act",
"BC카드":"https://www.bccard.com/app/card/CreditCardMain.do","IBK기업":"https://card.ibk.co.kr/"}
ORDER=["삼성카드","현대카드","신한카드","KB국민카드","롯데카드","우리카드","하나카드","NH농협카드","BC카드","IBK기업"]

# 발급혜택 비교 (4개 플랫폼)
PLATFORMS=[{"key":"ajungdang","name":"아정당","color":"#3b5bdb","url":"https://www.ajd.co.kr/card"},
 {"key":"cardgorilla","name":"카드고릴라","color":"#ff4d4f","url":"https://www.card-gorilla.com/event"},
 {"key":"toss","name":"토스","color":"#3182f6","url":"https://card-lounge.toss.im/event"},
 {"key":"kakaopay","name":"카카오페이","color":"#e8b800","url":"https://contents.kakaopay.com/contents/2296"}]
ISSUE=[
 {"issuer":"삼성카드","ajungdang":"최대 61.1만원","cardgorilla":"최대 117만원","toss":"-","kakaopay":"-"},
 {"issuer":"현대카드","ajungdang":"최대 72만원","cardgorilla":"최대 89만원","toss":"-","kakaopay":"최대 44만P"},
 {"issuer":"신한카드","ajungdang":"최대 54만원","cardgorilla":"최대 78.9만원","toss":"-","kakaopay":"최대 39만원"},
 {"issuer":"KB국민카드","ajungdang":"최대 85만원","cardgorilla":"최대 86만원","toss":"최대 81만원","kakaopay":"-"},
 {"issuer":"롯데카드","ajungdang":"최대 66만원","cardgorilla":"최대 67만원","toss":"최대 48만원","kakaopay":"-"},
 {"issuer":"우리카드","ajungdang":"최대 77만원","cardgorilla":"최대 78만원","toss":"-","kakaopay":"-"},
 {"issuer":"하나카드","ajungdang":"-","cardgorilla":"최대 57만원","toss":"-","kakaopay":"-"},
 {"issuer":"NH농협카드","ajungdang":"최대 20.5만원","cardgorilla":"최대 17.5만원","toss":"-","kakaopay":"-"},
]
def e(iss,card,plat,ben,period,url): return {"issuer":iss,"card":card,"platform":plat,"benefit":ben,"period":period,"url":url}
CG="https://www.card-gorilla.com/event"; BS="https://www.banksalad.com/chart/cards?tab=event"; AJ="https://www.ajd.co.kr/card"; KP="https://contents.kakaopay.com/contents/2296"; TS="https://card-lounge.toss.im/event"
EVENTS=[
 e("삼성카드","연회비 캐시백 대상카드","카드고릴라","최대 119만원 캐시백","2026.06","https://www.card-gorilla.com/team/detail/1"),
 e("현대카드","연회비 캐시백 대상카드","카드고릴라","최대 89만원 캐시백","2026.06",CG),
 e("KB국민카드","연회비 캐시백 대상카드","카드고릴라","최대 86만원 캐시백","2026.06",CG),
 e("신한카드","연회비 캐시백 대상카드","카드고릴라","최대 78.9만원 캐시백","2026.06",CG),
 e("우리카드","연회비 캐시백 대상카드","카드고릴라","최대 78만원 캐시백","2026.06","https://www.card-gorilla.com/team/detail/5"),
 e("롯데카드","연회비 캐시백 대상카드","카드고릴라","최대 67만원 캐시백","2026.06",CG),
 e("하나카드","연회비 캐시백 대상카드","카드고릴라","최대 57만원 캐시백","2026.06",CG),
 e("NH농협카드","연회비 캐시백 대상카드","카드고릴라","최대 17.5만원 캐시백","2026.06","https://www.card-gorilla.com/team/detail/9"),
 e("삼성카드","연회비 캐시백 대상카드","뱅크샐러드","최대 119만원 캐시백","2026.06",BS),
 e("현대카드","연회비 캐시백 대상카드","뱅크샐러드","최대 89만원 캐시백","2026.06",BS),
 e("KB국민카드","연회비 캐시백 대상카드","뱅크샐러드","최대 86만원 캐시백","2026.06",BS),
 e("신한카드","연회비 캐시백 대상카드","뱅크샐러드","최대 78.9만원 캐시백","2026.06",BS),
 e("우리카드","연회비 캐시백 대상카드","뱅크샐러드","최대 78만원 캐시백","2026.06",BS),
 e("롯데카드","연회비 캐시백 대상카드","뱅크샐러드","최대 67만원 캐시백","2026.06",BS),
 e("하나카드","연회비 캐시백 대상카드","뱅크샐러드","최대 57만원 캐시백","2026.06",BS),
 e("KB국민카드","KB국민카드 발급","아정당","최대 85만원","2026.06","https://www.ajd.co.kr/card/event/detail/243"),
 e("우리카드","우리카드 발급","아정당","최대 77만원","2026.06","https://www.ajd.co.kr/card/event/detail/267"),
 e("현대카드","현대카드 발급","아정당","최대 72만원","2026.06","https://www.ajd.co.kr/card/event/detail/86"),
 e("롯데카드","롯데카드 발급","아정당","최대 66만원","2026.06","https://www.ajd.co.kr/card/event/detail/158"),
 e("삼성카드","삼성카드 발급","아정당","최대 63.1만원","2026.06","https://www.ajd.co.kr/card/event/detail/260"),
 e("신한카드","신한카드 발급","아정당","최대 54만원","2026.06","https://www.ajd.co.kr/card/event/detail/75"),
 e("NH농협카드","NH농협카드 발급","아정당","최대 20.5만원","2026.06","https://www.ajd.co.kr/card/event/list"),
 e("신한카드","Deep Oil / KaPick","카카오페이","최대 39만원(기본 27만)","2026.06",KP),
 e("현대카드","현대카드M / ZERO Edition3","카카오페이","최대 44만 포인트","2026.06",KP),
 e("KB국민카드","굿데이/굿데이올림","토스","최대 81만원 이벤트","2026.06",TS),
 e("롯데카드","LOCA 365 / LIKIT","토스","최대 48만원 이벤트","2026.06",TS),
 e("하나카드","클럽SK카드","토스","80만원 이벤트","2026.06","https://card-lounge.toss.im/card/5"),
 e("삼성카드","삼성카드 taptap O","삼성카드","연회비 100% 캐시백(신규)","상시","https://www.samsungcard.com/home/card/cardinfo/PGHPPCCCardCardinfoDetails001?code=AAP1483"),
 e("신한카드","신한카드 첫만남","신한카드","연회비 100% 캐시백(7천~5.1만)","회차별","https://www.shinhancard.com/pconts/html/benefit/event/1196240_2239.html"),
 e("우리카드","카드의정석2","우리카드","최대 39만원 캐시백","2026 진행","https://pc.wooricard.com/dcpc/yh1/bnf/bnf02/prgevnt/movePrgEvntDtl.do?evntSrno=30004533"),
 e("롯데카드","트래블월렛 하이브리드 롯데","롯데카드","20만원 캐시백","2026 진행","https://www.lottecard.co.kr/app/LPBNFDA_V300.lc?evnBultSeq=8271"),
 e("KB국민카드","트래블러스 체크","KB국민카드","최대 5.5만원+30달러","~2026.07.31","https://card.kbcard.com/CRD/DVIEW/HCAMCXPRICAC0076"),
 e("BC카드","BC바로 발급","카드고릴라","국내 20만원↑ 시 페이북머니 10만원","2026 진행","https://www.card-gorilla.com/team/detail/32"),
]

# ===== 이번 달 리워드 높은 카드 (메인 히어로) =====
def h(rank,iss,card,reward,img,cid): return {"rank":rank,"issuer":iss,"card":card,"reward":reward,"img":T+img,"url":"https://card-lounge.toss.im/card/"+cid}
HERO=[
 h(1,"삼성카드","삼성카드 taptap O","최대 119만원","2936.png","17"),
 h(2,"현대카드","현대카드 M","최대 89만원","wood.png","1827"),
 h(3,"KB국민카드","KB국민 굿데이카드","최대 86만원","1121.png","1121"),
 h(4,"우리카드","카드의정석 2","최대 78만원","10550.png","10175"),
 h(5,"신한카드","토스 신한카드 Mr.Life","최대 78.9만원","3480.png","1259"),
 h(6,"롯데카드","LOCA 365","최대 67만원","1477.png","1477"),
 h(7,"하나카드","하나 클럽SK카드","최대 57만원","credit-card-new/%ED%95%98%EB%82%98%20%ED%81%B4%EB%9F%BDSK%EC%B9%B4%EB%93%9C%28CLUB%20SK%29.png","5"),
 h(8,"NH농협카드","농협 별다줄카드","최대 20.5만원","1356.png","1356"),
]
json.dump({"month":"2026-06","items":HERO},open(os.path.join(SITE,"hero.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)

# ===== 이벤트 카드 메타 병합 (카드고릴라 TOP100/뱅크샐러드/아정당 → 카드별 발급이벤트 + 신규카드 + 인기순위) =====
_ISSMAP={"농협카드":"NH농협카드","IBK기업은행":"IBK기업","BC 바로카드":"BC카드"}
_cardidx={}
for _iss,_lst in CARDS.items():
    for _c in _lst: _cardidx.setdefault(_nk(_c["name"]),(_iss,_c))
_RANKMAP={}
def _ev(cardname,issuer,platform,amount,is_event):
    issuer=_ISSMAP.get(issuer,issuer); k=_nk(cardname)
    if k in _cardidx: _iss,_c=_cardidx[k]
    else:
        _c={"name":cardname,"img":"","fee":"","benefit":_gendesc(cardname),"url":APPLY.get(issuer,""),"events":[]}
        CARDS.setdefault(issuer,[]).append(_c); _cardidx[k]=(issuer,_c)
    if is_event and amount:
        _c.setdefault("events",[])
        if not any(e["platform"]==platform for e in _c["events"]): _c["events"].append({"platform":platform,"amount":amount})
def _ld(p):
    try: return json.load(open(os.path.join(OUT,p),encoding="utf-8"))
    except Exception as _e: print("scrape load fail",p,_e); return None
_cg=_ld("scrape/ranking_cardgorilla.json")
if _cg:
    for _it in _cg["items"]:
        _amt=_it.get("amount",""); _isev=("캐시백" in _amt or "연회비" in _amt)
        _ev(_it["name"],_it["issuer"],"카드고릴라",_amt,_isev); _RANKMAP[_nk(_it["name"])]=_it["rank"]
_bs=_ld("scrape/banksalad_chart.json")
if _bs:
    for _it in _bs["items"]:
        if _it.get("event"): _ev(_it["name"],_it["issuer"],"뱅크샐러드",_it["event"],True)
_aj=_ld("scrape/ajungdang_events.json")
if _aj:
    for _it in _aj.get("fuel_cards",[]): _ev(_it["name"],_it["issuer"],"아정당",_it["amount"],True)
_EVMAP={_nk(c["name"]):c.get("events",[]) for lst in CARDS.values() for c in lst}
print("event merge → total cards:",sum(len(v) for v in CARDS.values()),"| cards with event:",sum(1 for lst in CARDS.values() for c in lst if c.get("events")))

# 상세 혜택(benefit_detail) 로드 (사실 데이터·우리 스키마)
_bd=_ld("scrape/benefit_detail.json") or {}
_DETMAP={_nk(k):v for k,v in _bd.items() if not k.startswith("_")}

# 플랫폼별 상품상세 딥링크(product_id) 매핑
_pl=_ld("scrape/plat_links.json") or {}
_PLATMAP={_nk(k):v for k,v in _pl.items() if not k.startswith("_")}

# 독자 인기순위 (순위/차트를 제공하는 모든 플랫폼 동일가중 평균: 토스·카드고릴라·뱅크샐러드)
_toss=_ld("scrape/ranking_toss.json"); _rk={}
if _toss:
    for _it in _toss["items"]: _rk.setdefault(_nk(_it["name"]),{"name":_it["name"]})["t"]=_it["rank"]
if _cg:
    for _it in _cg["items"]: _rk.setdefault(_nk(_it["name"]),{"name":_it["name"]})["c"]=_it["rank"]
if _bs:    # 뱅크샐러드 차트: items 순서를 순위로 사용
    for _i2,_it in enumerate(_bs.get("items",[]),1): _rk.setdefault(_nk(_it["name"]),{"name":_it["name"]})["b"]=_i2
_our=[]
for _k,_v in _rk.items():
    _rs=[r for r in (_v.get("t"),_v.get("c"),_v.get("b")) if r]; _avg=sum(_rs)/len(_rs)
    _iss=_cardidx[_k][0] if _k in _cardidx else ""; _img=_cardidx[_k][1].get("img","") if _k in _cardidx else ""
    _our.append({"name":_v["name"],"issuer":_iss,"img":_img,"avg":round(_avg,1),"toss":_v.get("t"),"cg":_v.get("c"),"bs":_v.get("b"),"n":len(_rs)})
_our.sort(key=lambda x:(x["avg"], -x["n"]))   # 평균 동률이면 표본 많은 카드 우선
for _i,_r in enumerate(_our,1): _r["rank"]=_i
json.dump({"month":"2026-06","note":"토스·카드고릴라·뱅크샐러드 순위 동일가중 평균","items":_our},open(os.path.join(SITE,"rank.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("독자 순위 items:",len(_our),"| 상세혜택 cards:",len(_DETMAP))

# ===== DB =====
data=json.load(open(os.path.join(SITE,"data.json"),encoding="utf-8"))  # 할인(도메인 포함) 유지(수기 베이스)
# 프테라노돈(결제처 카드할인 거주지 수집) 병합: discount_seed.json 의 신규 항목을 합친다.
#   - 중복키(결제처+카드+할인액+유형) 동일하면 자동수집(conf 보존)으로 갱신, 없으면 추가.
try:
    _ds=json.load(open(os.path.join(OUT,"collector","discount_seed.json"),encoding="utf-8")).get("items",[])
    _seen={(d["plat"],d.get("card"),d.get("disc"),d.get("type")) for d in data["items"]}
    _add=0
    for _it in _ds:
        _k=(_it["plat"],_it.get("card"),_it.get("disc"),_it.get("type"))
        if _k not in _seen:
            data["items"].append(_it); _seen.add(_k); _add+=1
    for _i,_d in enumerate(data["items"]): _d["id"]=_i   # id 재부여
    if _add: print(f"프테라노돈 결제처할인 병합 +{_add}건 (총 {len(data['items'])}건)")
except FileNotFoundError:
    pass
except Exception as _e:
    print("discount_seed 병합 err", _e)

# 이번 달 할인 많이 주는 가맹점 랭킹 (메인 배너용)
import re as _re2
from collections import defaultdict as _dd
def _won(s):
    s=s or ""
    m=_re2.search(r"([\d,]+)\s*원",s)
    if m: return int(m.group(1).replace(",",""))
    m=_re2.search(r"(\d+)\s*%",s)
    if m: return int(m.group(1))*2000
    return 0
_mg=_dd(list)
for _d in data["items"]: _mg[_d["plat"]].append(_d)
_merch=[]
for _plat,_items in _mg.items():
    _b=max(_items,key=lambda d:_won(d["disc"]))
    _merch.append({"plat":_plat,"domain":_items[0].get("domain",""),"gubun":_items[0]["gubun"],
                   "count":len(_items),"top":(_b["disc"]+" "+_b["type"]).strip(),"_v":_won(_b["disc"])})
_merch.sort(key=lambda m:(-m["count"],-m["_v"]))
for m in _merch: m.pop("_v",None)
json.dump({"month":"2026-06","items":_merch[:10]},open(os.path.join(SITE,"merchants.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
con=sqlite3.connect(DBL); cur=con.cursor()
cur.executescript("""
DROP TABLE IF EXISTS merchant;DROP TABLE IF EXISTS discount;DROP TABLE IF EXISTS platform;
DROP TABLE IF EXISTS issue_benefit;DROP TABLE IF EXISTS issuer;DROP TABLE IF EXISTS card;DROP TABLE IF EXISTS event;
CREATE TABLE merchant(name TEXT PRIMARY KEY,domain TEXT,gubun TEXT);
CREATE TABLE discount(id INTEGER PRIMARY KEY,merchant TEXT,card TEXT,tab TEXT,type TEXT,min TEXT,disc TEXT,cond TEXT,period TEXT,conf TEXT,url TEXT,domain TEXT);
CREATE TABLE platform(key TEXT PRIMARY KEY,name TEXT,color TEXT,url TEXT,ord INTEGER);
CREATE TABLE issue_benefit(issuer TEXT,platform_key TEXT,amount TEXT,PRIMARY KEY(issuer,platform_key));
CREATE TABLE issuer(name TEXT PRIMARY KEY,apply_url TEXT,ord INTEGER);
CREATE TABLE card(issuer TEXT,name TEXT,img TEXT,fee TEXT,benefit TEXT,source_url TEXT);
CREATE TABLE event(id INTEGER PRIMARY KEY AUTOINCREMENT,issuer TEXT,card TEXT,platform TEXT,benefit TEXT,period TEXT,url TEXT);
""")
seen=set()
for d in data["items"]:
    m=d["plat"]
    if m not in seen: cur.execute("INSERT OR REPLACE INTO merchant VALUES(?,?,?)",(m,d.get("domain",""),d["gubun"]));seen.add(m)
    cur.execute("INSERT INTO discount VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(d["id"],m,d["card"],d["tab"],d["type"],d["min"],d["disc"],d["cond"],d["period"],d.get("conf",""),d["url"],d.get("domain","")))
for i,p in enumerate(PLATFORMS): cur.execute("INSERT INTO platform VALUES(?,?,?,?,?)",(p["key"],p["name"],p["color"],p["url"],i))
for row in ISSUE:
    for p in PLATFORMS: cur.execute("INSERT INTO issue_benefit VALUES(?,?,?)",(row["issuer"],p["key"],row.get(p["key"],"-")))
# 카드 dedup: 동일 카드명 중복 시 첫 등장(카드사 리소스 우선 — 현재 토스 단일소스라 카드사명 기준 정규화) 유지
namekey=set()
for i,iss in enumerate(ORDER):
    cur.execute("INSERT INTO issuer VALUES(?,?,?)",(iss,APPLY.get(iss,""),i))
    for cd in CARDS.get(iss,[]):
        k=(iss,cd["name"].strip())
        if k in namekey: continue
        namekey.add(k)
        cur.execute("INSERT INTO card VALUES(?,?,?,?,?,?)",(iss,cd["name"],cd["img"],cd["fee"],cd["benefit"],cd["url"]))
for ev in EVENTS:
    cur.execute("INSERT INTO event(issuer,card,platform,benefit,period,url) VALUES(?,?,?,?,?,?)",(ev["issuer"],ev["card"],ev["platform"],ev["benefit"],ev["period"],ev["url"]))
con.commit()

# ===== export =====
def export():
    plats=[{"key":k,"name":n,"color":c2,"url":u} for k,n,c2,u,_ in cur.execute("SELECT * FROM platform ORDER BY ord")]
    irows=[]
    for row in ISSUE:
        o={"issuer":row["issuer"]}
        for p in plats: o[p["key"]]=cur.execute("SELECT amount FROM issue_benefit WHERE issuer=? AND platform_key=?",(row["issuer"],p["key"])).fetchone()[0]
        irows.append(o)
    json.dump({"month":"2026-06","source":"db","platforms":plats,"items":irows},open(os.path.join(SITE,"issue.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    apply=dict(cur.execute("SELECT name,apply_url FROM issuer").fetchall())
    order=[r[0] for r in cur.execute("SELECT name FROM issuer ORDER BY ord")]
    out={}; _gid=[0]
    for iss in order:
        arr=[]
        for n,img,fee,b,src in cur.execute("SELECT name,img,fee,benefit,source_url FROM card WHERE issuer=?",(iss,)).fetchall():
            _gid[0]+=1
            _bn=_nk(_re.sub(r"^토스\s*","",n))
            _det=_DETMAP.get(_nk(n)) or _DETMAP.get(_bn)
            _plat=_PLATMAP.get(_nk(n)) or _PLATMAP.get(_bn) or {}
            arr.append({"id":_gid[0],"name":n,"img":img,"fee":fee,"benefit":b,"source":src,"url":apply.get(iss,""),
                        "events":_EVMAP.get(_nk(n),[]),"rank":_RANKMAP.get(_nk(n)),"detail":_det,"plat":_plat})
        out[iss]=arr
    json.dump({"month":"2026-06","source":"db","order":order,"apply":apply,"cards":out},open(os.path.join(SITE,"cards.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    # [2026-06-27] events.json은 이제 collector.py가 platform_events에서 생성(네이버 포함)한다.
    # build_data가 덮어쓰면 네이버 0건으로 회귀하므로 여기서는 더 이상 쓰지 않는다(소유권: collector).
    # (구버전) json.dump({...events...}, open(SITE/events.json)) — 비활성화
export(); con.close(); shutil.copy(DBL,DBF)
import collections
tot=sum(len(v) for v in CARDS.values())
print("cards:",tot,"| issue rows:",len(ISSUE),"| events:",len(EVENTS))
