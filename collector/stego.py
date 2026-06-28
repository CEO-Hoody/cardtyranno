# -*- coding: utf-8 -*-
"""stego(스테고사우루스) — 카드 메타정보(연회비·혜택·전월실적) 범용 파서.
이벤트 파서(brachio/apato/diplo/bronto/mamenchi)와 동일 입력을 받아
카드 고유 메타만 추출. collect_platform()에서 응답을 이중 파싱할 때 사용.
"""
import re, json


def _clean(s):
    if not s: return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(s))).strip()


def extract_annual_fee(text):
    if not text: return None
    t = _clean(text)
    m = re.search(r'연회비[:\s]*((?:(?:국내전용|해외겸용|국내|해외|VISA|Master|AMEX|JCB|UnionPay)\s*[\d,만천백]+\s*원[\s/,·]*)+)', t, re.I)
    if m: return m.group(1).strip().rstrip("/,· ")
    m = re.search(r'연회비[:\s]*([\d,]+\s*원)', t)
    if m: return m.group(1).strip()
    m = re.search(r'연회비[:\s]*([\d]+(?:\.\d+)?\s*만\s*원)', t)
    if m: return m.group(1).strip()
    m = re.search(r'연회비[:\s]*(없음|무료)', t)
    if m: return m.group(1)
    m = re.search(r'(국내전용\s*[\d만천백,]+\s*원)', t)
    if m: return m.group(1).strip()
    return None


def extract_spending_req(text):
    if not text: return None
    t = _clean(text)
    m = re.search(r'전월\s*(?:이용)?실적\s*([\d,]+\s*(?:만원|원)(?:\s*이상)?)', t)
    if m: return "전월실적 " + m.group(1).strip()
    m = re.search(r'전월\s*(?:이용)?실적\s*(없음|없이|조건\s*없음|면제)', t)
    if m: return "전월실적 없음"
    return None


def extract_benefits(text):
    if not text: return []
    t = _clean(text)
    bens = []; seen = set()
    for m in re.finditer(r'([\w가-힣·()]+)\s+([\d.]+%\s*(?:할인|적립|캐시백|리워드|페이백|포인트\s*적립))', t):
        b = m.group(1)+" "+m.group(2)
        if b not in seen: bens.append(b); seen.add(b)
    for m in re.finditer(r'([\d,]+원당)\s*(?:최대\s*)?([\d]+)\s*(마일리지|포인트|원)', t):
        b = m.group(1)+" 최대 "+m.group(2)+" "+m.group(3)
        if b not in seen: bens.append(b); seen.add(b)
    for m in re.finditer(r'([\w가-힣]+)\s+(리터당\s*[\d,]+원\s*(?:할인|적립))', t):
        b = m.group(1)+" "+m.group(2)
        if b not in seen: bens.append(b); seen.add(b)
    return bens[:10]


def parse_meta_from_text(text):
    meta = {}
    fee = extract_annual_fee(text)
    if fee: meta["annual_fee"] = fee
    spend = extract_spending_req(text)
    if spend: meta["spending_req"] = spend
    bens = extract_benefits(text)
    if bens: meta["benefits"] = bens
    return meta


def parse_meta_from_json(data, text_fallback=""):
    meta = {}
    if not data or not isinstance(data, dict):
        return parse_meta_from_text(text_fallback) if text_fallback else {}
    cands = [data]
    for k in ("detail","card_detail","card_info","card","result","product","cardProduct"):
        v = data.get(k)
        if isinstance(v, dict): cands.append(v)
    pp = (data.get("props") or {}).get("pageProps") or {}
    for k in ("card","product","cardProduct"):
        v = pp.get(k)
        if isinstance(v, dict): cands.append(v)
    rc = data.get("result") or {}
    if isinstance(rc, dict):
        for k in ("card","product"):
            v = rc.get(k)
            if isinstance(v, dict): cands.append(v)
    for obj in cands:
        for k in ("annual_fee","annualFee","fee","annual_cost","annualCost"):
            v = obj.get(k)
            if not v: continue
            if isinstance(v, dict):
                parts = []
                for fk, label in [("domestic","국내전용"),("international","해외겸용"),("visa","VISA"),("master","MASTER"),("amex","AMEX")]:
                    if v.get(fk): parts.append(label+" "+str(v[fk]))
                if not parts:
                    for fk2, val2 in v.items():
                        if val2 and fk2 not in ("_id","id","type"): parts.append(str(fk2)+" "+str(val2))
                if parts: meta["annual_fee"] = " / ".join(parts)
                elif v.get("text"): meta["annual_fee"] = _clean(v["text"])
            elif isinstance(v, list):
                parts = []
                for f in v:
                    if isinstance(f, dict):
                        nm = f.get("name") or f.get("type") or ""
                        amt = f.get("amount") or f.get("fee") or ""
                        if amt: parts.append((nm+" "+str(amt)).strip() if nm else str(amt))
                if parts: meta["annual_fee"] = " / ".join(parts)
            else:
                fs = _clean(str(v))
                if fs: meta["annual_fee"] = fs
            if meta.get("annual_fee"): break
        if meta.get("annual_fee"): break
    for obj in cands:
        for k in ("benefits","mainBenefits","keyBenefits","benefit","card_benefits","topBenefits"):
            v = obj.get(k)
            if not v: continue
            if isinstance(v, list):
                bens = [_clean(b.get("title","") if isinstance(b,dict) else str(b)) for b in v[:10] if b]
                bens = [b for b in bens if b]
                if bens: meta["benefits"] = bens; break
            elif isinstance(v, str) and v.strip():
                meta["benefits"] = [_clean(v)]; break
        if meta.get("benefits"): break
    for obj in cands:
        for k in ("minSpending","previousMonthSpending","condition","spending_condition","spendingCondition","min_spending","prevMonthSpending"):
            v = obj.get(k)
            if v: meta["spending_req"] = _clean(str(v)); break
        if meta.get("spending_req"): break
    if text_fallback:
        fb = parse_meta_from_text(text_fallback)
        for k in ("annual_fee","spending_req","benefits"):
            if not meta.get(k) and fb.get(k): meta[k] = fb[k]
    return meta
