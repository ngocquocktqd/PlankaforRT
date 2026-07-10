#!/usr/bin/env python3
"""Máy tính chứng quyền có bảo đảm (CW) — phục vụ lướt sóng CW.

Đại số tiền tệ (điểm hòa vốn, giá trị nội tại/thời gian, đòn bẩy) dùng `Decimal`
cho chính xác. Các đại lượng Black-Scholes (delta, theta, vega, IV ngụ ý) bản chất
cần hàm mũ/log nên tính bằng float và GẮN NHÃN "[BS xấp xỉ]" — đây là MÔ HÌNH, không
phải số chắc; IV thực tế do nhà tạo lập (issuer) quyết định và có thể lệch.

Bối cảnh VN: hiện chỉ có **chứng quyền MUA (call)**, thanh toán tiền mặt khi đáo hạn,
kiểu châu Âu nhưng giao dịch tự do trên sàn. Bạn gần như luôn BÁN CW trên sàn chứ
không giữ tới đáo hạn.

Dùng:
  # Đủ chỉ số (tự suy IV từ giá CW thị trường):
  python3 cw_calc.py metrics --underlying 130000 --strike 120000 --ratio 5 \
      --price 3000 --days 90
  # Hoặc tự nhập IV:
  python3 cw_calc.py metrics --underlying 130000 --strike 120000 --ratio 5 \
      --price 3000 --days 90 --iv 0.35
  # Chỉ back-out IV ngụ ý:
  python3 cw_calc.py iv --underlying 130000 --strike 120000 --ratio 5 \
      --price 3000 --days 90
  # Điểm hòa vốn thuần Decimal (không cần mô hình):
  python3 cw_calc.py breakeven --strike 120000 --ratio 5 --price 3000 \
      --underlying 130000

Quy ước: giá cơ sở & giá thực hiện cùng đơn vị VND; `ratio` = tỷ lệ chuyển đổi
(vd 5 = 5 CW đổi 1 cổ phiếu); `price` = giá CW thị trường (VND/CW); `days` = số ngày
lịch tới đáo hạn; `iv` = biến động ngụ ý (thập phân, 0.35 = 35%); `rf` = lãi suất phi
rủi ro/năm (mặc định 0.04).

Đây là công cụ HỖ TRỢ — số CW sống (mã, IV, bid/ask) phải lấy từ bảng giá chứng quyền
của công ty chứng khoán; kết quả gắn nhãn tin cậy theo chất lượng đầu vào.
"""

import argparse
import math
import sys
from decimal import Decimal, getcontext

getcontext().prec = 28

# ---------- Đại số tiền tệ (Decimal — chính xác) ----------


def d(x) -> Decimal:
    return Decimal(str(x))


def breakeven_price(strike: Decimal, ratio: Decimal, price: Decimal) -> Decimal:
    """Giá cơ sở tại đáo hạn để HÒA VỐN nếu giữ CW tới đáo hạn.
    payoff/CW = max(0, S-K)/ratio; hòa vốn khi (S-K)/ratio = premium.
    """
    return strike + price * ratio


def intrinsic_per_cw(underlying: Decimal, strike: Decimal, ratio: Decimal) -> Decimal:
    """Giá trị nội tại trên mỗi CW = max(0, S-K)/ratio."""
    return max(Decimal(0), underlying - strike) / ratio


# ---------- Black-Scholes (float — GẮN NHÃN xấp xỉ) ----------


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _bs_call(S: float, K: float, T: float, r: float, sigma: float) -> dict:
    """Giá & greeks call Black-Scholes (cho 1 cổ phiếu, chưa chia ratio)."""
    if T <= 0 or sigma <= 0:
        price = max(0.0, S - K)
        return {"price": price, "delta": 1.0 if S > K else 0.0,
                "gamma": 0.0, "theta_year": 0.0, "vega": 0.0}
    srt = sigma * math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / srt
    d2 = d1 - srt
    price = S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    delta = _norm_cdf(d1)
    gamma = _norm_pdf(d1) / (S * srt)
    theta_year = (-(S * _norm_pdf(d1) * sigma) / (2.0 * math.sqrt(T))
                  - r * K * math.exp(-r * T) * _norm_cdf(d2))
    vega = S * _norm_pdf(d1) * math.sqrt(T)
    return {"price": price, "delta": delta, "gamma": gamma,
            "theta_year": theta_year, "vega": vega}


def implied_vol(S: float, K: float, T: float, r: float, ratio: float,
                cw_market: float) -> float | None:
    """Back-out IV: tìm sigma sao cho _bs_call(...).price/ratio = giá CW thị trường.
    Đơn điệu theo sigma → chia đôi (bisection), bền vững."""
    target = cw_market * ratio  # quy về giá call cho 1 cổ phiếu
    lo, hi = 0.001, 3.0
    plo = _bs_call(S, K, T, r, lo)["price"]
    phi = _bs_call(S, K, T, r, hi)["price"]
    if not (plo <= target <= phi):
        return None  # ngoài dải mô hình (vd CW dưới nội tại, hoặc IV > 300%)
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        pm = _bs_call(S, K, T, r, mid)["price"]
        if abs(pm - target) < 1e-6:
            return mid
        if pm < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------- Lệnh ----------


def cmd_breakeven(a) -> None:
    strike, ratio, price = d(a.strike), d(a.ratio), d(a.price)
    be = breakeven_price(strike, ratio, price)
    print(f"Điểm hòa vốn tại đáo hạn = giá TH + giá CW × tỷ lệ = {be:,.0f} đ")
    if a.underlying:
        S = d(a.underlying)
        move = (be - S) / S
        intr = intrinsic_per_cw(S, strike, ratio)
        tv = price - intr
        print(f"Giá cơ sở hiện tại        = {S:,.0f} đ")
        print(f"Cần cơ sở tăng            = {move:+.2%} để hòa vốn "
              f"({'⚠️ xa — coi chừng OTM sâu' if move > Decimal('0.10') else 'trong tầm'})")
        print(f"Giá trị nội tại/CW        = {intr:,.1f} đ")
        print(f"Giá trị thời gian/CW      = {tv:,.1f} đ "
              f"({tv / price:.0%} giá CW — phần này theta bào về 0 khi đáo hạn)")
        moneyness = ("ITM (nội tại dương)" if S > strike else
                     "ATM (~ngang giá TH)" if abs(S - strike) / strike < Decimal("0.03")
                     else "OTM (dưới giá TH — rủi ro cao)")
        print(f"Trạng thái                = {moneyness}")


def cmd_metrics(a) -> None:
    S, K, ratio, price = d(a.underlying), d(a.strike), d(a.ratio), d(a.price)
    days = int(a.days)
    T = days / 365.0
    rf = float(a.rf)

    # Đại số tiền tệ (chắc chắn)
    be = breakeven_price(K, ratio, price)
    move_be = (be - S) / S
    intr = intrinsic_per_cw(S, K, ratio)
    tv = price - intr
    gearing = S / (price * ratio)  # đòn bẩy đơn giản

    print("=== CHỨNG QUYỀN — CHỈ SỐ ===")
    print(f"Cơ sở {S:,.0f} · giá TH {K:,.0f} · tỷ lệ {ratio} · giá CW {price:,.0f} · "
          f"còn {days} ngày")
    moneyness = ("ITM" if S > K else "ATM" if abs(S - K) / K < Decimal("0.03") else "OTM")
    print(f"[Decimal] Trạng thái        : {moneyness} "
          f"({(S - K) / K:+.1%} so giá TH)")
    print(f"[Decimal] Điểm hòa vốn      : {be:,.0f} đ  (cơ sở cần {move_be:+.2%})")
    print(f"[Decimal] Nội tại / thời gian: {intr:,.1f} / {tv:,.1f} đ  "
          f"(thời gian = {tv / price:.0%} giá CW → theta bào)")
    print(f"[Decimal] Đòn bẩy đơn giản  : {gearing:,.1f}x")

    # Black-Scholes (xấp xỉ)
    sigma = float(a.iv) if a.iv else implied_vol(float(S), float(K), T, rf,
                                                 float(ratio), float(price))
    if sigma is None:
        print("[BS] Không suy được IV (giá CW ngoài dải mô hình — có thể dưới nội tại "
              "hoặc IV quá cao). Bỏ qua greeks.")
        _warn_maturity(days)
        return
    bs = _bs_call(float(S), float(K), T, rf, sigma)
    delta = bs["delta"]                          # delta cho 1 cổ phiếu = delta 1 CW
    eff_lev = delta * float(gearing)             # đòn bẩy hiệu dụng
    theta_day_cw = bs["theta_year"] / 365.0 / float(ratio)  # theta/ngày trên 1 CW
    src = "nhập tay" if a.iv else "suy từ giá CW"
    print(f"[BS xấp xỉ] IV ({src})     : {sigma:.1%}")
    print(f"[BS xấp xỉ] Delta           : {delta:.3f}")
    print(f"[BS xấp xỉ] Đòn bẩy HIỆU DỤNG: {eff_lev:,.1f}x  "
          f"(= delta × đòn bẩy đơn giản — đây mới là số thật cho lời/lỗ)")
    print(f"[BS xấp xỉ] Theta/ngày/CW   : {theta_day_cw:,.1f} đ "
          f"({theta_day_cw / float(price):+.2%} giá CW MỖI NGÀY khi các yếu tố khác đứng yên)")
    _rate_leverage(eff_lev)
    _warn_maturity(days)


def cmd_iv(a) -> None:
    S, K, ratio, price = float(a.underlying), float(a.strike), float(a.ratio), float(a.price)
    T = int(a.days) / 365.0
    sigma = implied_vol(S, K, T, float(a.rf), ratio, price)
    if sigma is None:
        sys.exit("Không suy được IV: giá CW ngoài dải mô hình (kiểm lại đầu vào).")
    print(f"[BS xấp xỉ] IV ngụ ý = {sigma:.2%}  "
          f"(so IV các CW khác cùng cơ sở — CAO hơn = đang trả đắt, dễ bị 'IV crush')")


def _rate_leverage(eff: float) -> None:
    if eff < 2:
        note = "thấp — CW này gần như đi cùng cổ phiếu, ít lý do dùng đòn bẩy"
    elif eff <= 6:
        note = "✅ vùng hợp lý cho lướt sóng (3–6x)"
    elif eff <= 8:
        note = "⚠️ cao — lời nhanh nhưng lỗ cũng nhanh, siết size"
    else:
        note = "🚩 rất cao (thường OTM sâu) — bom gamma/theta, dễ về 0"
    print(f"           → Đòn bẩy hiệu dụng: {note}")


def _warn_maturity(days: int) -> None:
    if days < 30:
        print("🚩 ĐÁO HẠN < 30 ngày: vách theta dốc đứng + gần ngày GD cuối cùng — "
              "TRÁNH trừ khi lướt cực ngắn có lý do rõ.")
    elif days < 45:
        print("⚠️ Đáo hạn < 45 ngày: theta bắt đầu tăng tốc, ưu tiên CW xa đáo hạn hơn.")
    else:
        print(f"✓ Còn {days} ngày tới đáo hạn: đủ dư địa cho luận điểm chạy "
              "(vẫn đặt time-stop trước đáo hạn).")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("metrics", help="đủ chỉ số CW (đại số + BS)")
    for name in ("--underlying", "--strike", "--ratio", "--price", "--days"):
        m.add_argument(name, required=True)
    m.add_argument("--iv", help="IV thập phân; bỏ trống = tự suy từ giá CW")
    m.add_argument("--rf", default="0.04")
    m.set_defaults(func=cmd_metrics)

    iv = sub.add_parser("iv", help="back-out IV ngụ ý từ giá CW")
    for name in ("--underlying", "--strike", "--ratio", "--price", "--days"):
        iv.add_argument(name, required=True)
    iv.add_argument("--rf", default="0.04")
    iv.set_defaults(func=cmd_iv)

    be = sub.add_parser("breakeven", help="điểm hòa vốn (thuần Decimal)")
    for name in ("--strike", "--ratio", "--price"):
        be.add_argument(name, required=True)
    be.add_argument("--underlying", help="để tính %% cơ sở cần tăng")
    be.set_defaults(func=cmd_breakeven)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
