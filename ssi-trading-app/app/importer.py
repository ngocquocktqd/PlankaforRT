"""Import luận điểm từ file markdown của framework (reports/theses/*.md).

Format nguồn do skill /theo-doi-luan-diem sinh ra — ta kiểm soát format nên parse
heuristic là chấp nhận được. Trích: symbol, title, mode, hạng, trụ cột (🟢🟡🔴⚪),
điều kiện vô hiệu hoá, các mốc giá (tích luỹ/mua hời/entry/stop), khuyến nghị.

Nguyên tắc: parse KHÔNG chắc thì bỏ qua trường đó (để trống), không đoán bừa.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

_STATUS = {"🟢": "green", "🟡": "yellow", "🔴": "red", "⚪": "none"}


@dataclass
class ParsedThesis:
    symbol: str = ""
    title: str = ""
    mode: str = "value"          # value | momentum | cw
    conviction: str = "B"
    summary: str = ""
    pillars: list[dict] = field(default_factory=list)       # {text, status, is_invalidation}
    levels: list[dict] = field(default_factory=list)        # {kind, price, note}
    warnings: list[str] = field(default_factory=list)


def _vnd_to_decimal(s: str) -> Decimal | None:
    """'12.000đ' → 12000; '7.000' → 7000; '20,5k' → 20500. Không chắc → None."""
    s = s.strip().replace("đ", "").replace(" ", "")
    m = re.fullmatch(r"(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d))?(k)?", s)
    if not m:
        return None
    whole = m.group(1).replace(".", "")
    val = Decimal(whole)
    if m.group(3):  # hậu tố k
        val = val * 1000
        if m.group(2):
            val += Decimal(m.group(2)) * 100
    return val


def _find_price(line: str) -> Decimal | None:
    """Tìm mốc giá đầu tiên dạng '≤ 12.000đ' / '12.000' trong một dòng."""
    for m in re.finditer(r"(\d{1,3}(?:\.\d{3})+)\s*đ?", line):
        v = _vnd_to_decimal(m.group(1))
        if v and v >= 1000:  # bỏ số thứ tự/percent
            return v
    return None


def parse_thesis_markdown(text: str, symbol_hint: str = "") -> ParsedThesis:
    out = ParsedThesis()
    lines = text.splitlines()

    # --- symbol + title ---
    m = re.search(r"LUẬN ĐIỂM THEO DÕI:\s*([A-Z0-9]{2,5})\s*(?:\((.*?)\))?", text)
    if m:
        out.symbol = m.group(1)
        out.title = (m.group(2) or "").strip()
    if not out.symbol and symbol_hint:
        out.symbol = symbol_hint.upper()
    if not out.symbol:
        out.warnings.append("Không tìm thấy mã — cần symbol_hint")

    # --- mode ---
    low = text.lower()
    if "momentum" in low or "lướt sóng" in low and "chờ mua" not in low[:400]:
        # ưu tiên value nếu là luận điểm giá trị chờ đáy
        pass
    if re.search(r"mode.*momentum|hoi-dong-luot-song|trader momentum", low):
        out.mode = "momentum"
    if "chứng quyền" in low or re.search(r"\bcw\b", low):
        out.mode = "cw"

    # --- conviction (hạng / Nhãn) ---
    m = re.search(r"(?:hạng|Nhãn:?)\s*\**([ABC])\b", text)
    if m:
        out.conviction = m.group(1)

    # --- summary: dòng KHUYẾN NGHỊ ---
    m = re.search(r"KHUYẾN NGHỊ:?\s*(.+)", text)
    if m:
        out.summary = re.sub(r"[#*]", "", m.group(1)).strip()[:300]

    # --- pillars: hàng bảng có emoji trạng thái, hoặc bullet trong mục trụ cột ---
    in_invalidation = False
    for ln in lines:
        header = ln.strip().lower()
        if re.search(r"điều kiện vô hiệu|rủi ro nhị phân", header):
            in_invalidation = True
        elif ln.startswith("#") or re.match(r"^###", ln):
            # sang mục mới → thoát vùng vô hiệu hoá nếu không phải mục đó
            if not re.search(r"vô hiệu|nhị phân", header):
                in_invalidation = False

        emoji = next((e for e in _STATUS if e in ln), None)
        is_table_row = ln.strip().startswith("|") and emoji
        is_numbered_inv = in_invalidation and re.match(r"^\s*\d+\.\s+\S", ln)

        if is_table_row:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            # ưu tiên ô ĐẦU TIÊN đủ dài không chứa emoji trạng thái (= tên trụ cột),
            # tránh max-len vớ nhầm ô ghi chú
            text_cell = next(
                (c for c in cells
                 if len(re.sub(r"[*#]", "", c).strip()) > 8
                 and not any(e in c for e in _STATUS)),
                max(cells, key=len, default=""),
            )
            text_clean = re.sub(r"[*#]", "", text_cell).strip()
            if len(text_clean) > 8:
                out.pillars.append({
                    "text": text_clean[:250],
                    "status": _STATUS[emoji],
                    "is_invalidation": in_invalidation,
                })
        elif is_numbered_inv:
            t = re.sub(r"^\s*\d+\.\s+", "", ln)
            t = re.sub(r"[*#]", "", t).strip()
            if len(t) > 8:
                out.pillars.append({"text": t[:250], "status": "none", "is_invalidation": True})

    # --- levels ---
    for ln in lines:
        l = ln.lower()
        price = _find_price(ln)
        if price is None:
            continue
        note = re.sub(r"[*#|]", "", ln).strip()[:150]
        if "tích luỹ" in l or "tích lũy" in l:
            out.levels.append({"kind": "accumulate", "price": price, "note": note})
        elif "mua hời" in l or "mos" in l and "30" in l:
            out.levels.append({"kind": "buy_hoi", "price": price, "note": note})
        elif "stop" in l or "cắt lỗ" in l:
            out.levels.append({"kind": "stop", "price": price, "note": note})
        elif "pivot" in l or "điểm vào" in l or "reclaim" in l or "kích hoạt mua" in l:
            out.levels.append({"kind": "entry", "price": price, "note": note})
        elif "mục tiêu" in l or re.search(r"\bt[12]\b", l) or "target" in l:
            out.levels.append({"kind": "target", "price": price, "note": note})

    # khử trùng lặp level (cùng kind + price)
    seen: set[tuple] = set()
    uniq = []
    for lv in out.levels:
        key = (lv["kind"], str(lv["price"]))
        if key not in seen:
            seen.add(key)
            uniq.append(lv)
    out.levels = uniq

    if not out.pillars:
        out.warnings.append("Không parse được trụ cột nào — kiểm tra format")
    return out


def import_into_db(parsed: ParsedThesis, session) -> dict:
    """Ghi ParsedThesis vào DB. Trả snapshot. Trùng symbol đang WATCH/OPEN → từ chối."""
    from sqlmodel import select

    from .models import (Level, LevelKind, Pillar, PillarStatus, Thesis,
                         ThesisMode, ThesisState)

    dup = session.exec(
        select(Thesis).where(Thesis.symbol == parsed.symbol,
                             Thesis.state != ThesisState.CLOSED)
    ).first()
    if dup:
        return {"error": f"{parsed.symbol} đã có luận điểm đang mở (id={dup.id}). "
                         f"Đóng nó trước hoặc sửa tay."}

    th = Thesis(symbol=parsed.symbol, title=parsed.title or parsed.symbol,
                mode=ThesisMode(parsed.mode), conviction=parsed.conviction,
                summary=parsed.summary)
    session.add(th)
    session.commit()
    session.refresh(th)
    for i, p in enumerate(parsed.pillars):
        session.add(Pillar(thesis_id=th.id, text=p["text"],
                           status=PillarStatus(p["status"]),
                           is_invalidation=p["is_invalidation"], order=i))
    for lv in parsed.levels:
        session.add(Level(thesis_id=th.id, kind=LevelKind(lv["kind"]),
                          price=lv["price"], note=lv["note"]))
    session.commit()
    return {"id": th.id, "symbol": th.symbol, "pillars": len(parsed.pillars),
            "levels": len(parsed.levels), "warnings": parsed.warnings}


def scan_theses_dir() -> list[Path]:
    """Tìm file luận điểm trong repo (stock-analysis/reports/theses/*.md)."""
    roots = [
        Path(__file__).resolve().parent.parent.parent / "stock-analysis" / "reports" / "theses",
    ]
    files: list[Path] = []
    for r in roots:
        if r.exists():
            files.extend(sorted(r.glob("*.md")))
    return files
