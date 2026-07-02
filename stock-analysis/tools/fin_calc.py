#!/usr/bin/env python3
"""Công cụ tính toán tài chính độ chính xác tuyệt đối (decimal.Decimal, cấm float).

Dùng dạng CLI:
    python3 fin_calc.py dcf --fcf 1200 --growth 0.08 --years 10 --terminal 0.03 --discount 0.11 --shares 500
    python3 fin_calc.py owner-earnings --net-income 1500 --depreciation 300 --maintenance-capex 250
    python3 fin_calc.py margin-of-safety --intrinsic 120000 --price 85000
    python3 fin_calc.py cagr --begin 1000 --end 2500 --years 5
    python3 fin_calc.py ratios --net-income 1500 --equity 8000 --revenue 12000 \
        --ebit 2000 --invested-capital 10000 --tax-rate 0.2
    python3 fin_calc.py verify-mcap --price 85000 --shares 5000000000 --reported-mcap 425e12

Mọi giá trị tiền tệ nhập cùng một đơn vị (vd: tỷ VND). Kết quả in kèm công thức
để người đọc kiểm tra lại được.
"""

import argparse
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 50

TWO = Decimal("0.01")


def D(x) -> Decimal:
    """Chuyển input về Decimal qua str để tránh nhiễm bẩn float."""
    return Decimal(str(x))


def money(x: Decimal) -> str:
    return str(x.quantize(TWO, rounding=ROUND_HALF_UP))


def pct(x: Decimal) -> str:
    return money(x * 100) + "%"


def dcf(fcf: Decimal, growth: Decimal, years: int, terminal: Decimal,
        discount: Decimal, shares: Decimal | None) -> None:
    if terminal >= discount:
        sys.exit("LỖI: tăng trưởng terminal phải nhỏ hơn tỷ suất chiết khấu.")
    pv_sum = Decimal(0)
    cf = fcf
    print(f"{'Năm':>4} {'FCF':>18} {'Hệ số CK':>12} {'PV':>18}")
    for t in range(1, years + 1):
        cf = cf * (1 + growth)
        factor = (1 + discount) ** t
        pv = cf / factor
        pv_sum += pv
        print(f"{t:>4} {money(cf):>18} {money(1 / factor):>12} {money(pv):>18}")
    terminal_value = cf * (1 + terminal) / (discount - terminal)
    terminal_pv = terminal_value / (1 + discount) ** years
    intrinsic = pv_sum + terminal_pv
    print(f"\nPV dòng tiền {years} năm : {money(pv_sum)}")
    print(f"Giá trị terminal (PV)  : {money(terminal_pv)}"
          f"  ({pct(terminal_pv / intrinsic)} tổng giá trị)")
    print(f"GIÁ TRỊ NỘI TẠI        : {money(intrinsic)}")
    if shares:
        print(f"Giá trị / cổ phiếu     : {money(intrinsic / shares)}")
        print(f"Vùng mua (biên an toàn 30%): ≤ {money(intrinsic / shares * D('0.7'))}")
    if terminal_pv / intrinsic > D("0.6"):
        print("⚠️  Terminal chiếm >60% giá trị — định giá phụ thuộc nặng vào giả định xa; hạ growth hoặc tăng discount để kiểm tra độ nhạy.")


def owner_earnings(net_income: Decimal, depreciation: Decimal,
                   maintenance_capex: Decimal) -> None:
    oe = net_income + depreciation - maintenance_capex
    print(f"Owner earnings = LNST {money(net_income)} + Khấu hao {money(depreciation)}"
          f" − Capex duy trì {money(maintenance_capex)} = {money(oe)}")
    if net_income != 0:
        print(f"Owner earnings / LNST = {pct(oe / net_income)}")


def margin_of_safety(intrinsic: Decimal, price: Decimal) -> None:
    mos = (intrinsic - price) / intrinsic
    print(f"Biên an toàn = (Nội tại {money(intrinsic)} − Giá {money(price)}) / Nội tại = {pct(mos)}")
    if mos >= D("0.3"):
        print("✅ Đạt ngưỡng biên an toàn ≥30%")
    elif mos > 0:
        print("🟡 Có chiết khấu nhưng chưa đạt 30%")
    else:
        print("🚩 Giá cao hơn giá trị nội tại — không có biên an toàn")


def cagr(begin: Decimal, end: Decimal, years: Decimal) -> None:
    if begin <= 0 or end <= 0:
        sys.exit("LỖI: CAGR cần giá trị đầu/cuối dương.")
    rate = (end / begin) ** (Decimal(1) / years) - 1
    print(f"CAGR {years} năm: {money(begin)} → {money(end)} = {pct(rate)}/năm")


def ratios(args) -> None:
    if args.net_income is not None and args.equity:
        print(f"ROE  = LNST/VCSH = {pct(D(args.net_income) / D(args.equity))}")
    if args.net_income is not None and args.revenue:
        print(f"Biên ròng = LNST/Doanh thu = {pct(D(args.net_income) / D(args.revenue))}")
    if args.ebit is not None and args.invested_capital:
        nopat = D(args.ebit) * (1 - D(args.tax_rate))
        print(f"ROIC = EBIT×(1−thuế)/Vốn đầu tư = {money(nopat)}/{money(D(args.invested_capital))}"
              f" = {pct(nopat / D(args.invested_capital))}")
    if args.cfo is not None and args.net_income:
        print(f"CFO/LNST = {pct(D(args.cfo) / D(args.net_income))} (lành mạnh ≥ 80%)")
    if args.net_debt is not None and args.ebitda:
        print(f"Nợ ròng/EBITDA = {money(D(args.net_debt) / D(args.ebitda))}× (an toàn ≤ 2.5×)")


def verify_mcap(price: Decimal, shares: Decimal, reported: Decimal) -> None:
    calc = price * shares
    diff = abs(calc - reported) / reported
    print(f"Giá × Số CP = {money(calc)} | Vốn hoá công bố = {money(reported)} | Lệch = {pct(diff)}")
    print("✅ Khớp (≤3%)" if diff <= D("0.03")
          else "🚩 Lệch >3% — kiểm tra lại số CP lưu hành (pha loãng? cổ phiếu quỹ? dữ liệu cũ?)")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dcf", help="Chiết khấu dòng tiền 2 giai đoạn")
    d.add_argument("--fcf", required=True, help="FCF/owner earnings năm gần nhất")
    d.add_argument("--growth", required=True, help="Tăng trưởng giai đoạn 1 (vd 0.08)")
    d.add_argument("--years", type=int, default=10)
    d.add_argument("--terminal", default="0.03", help="Tăng trưởng terminal (mặc định 0.03)")
    d.add_argument("--discount", required=True, help="Tỷ suất chiết khấu (vd 0.11)")
    d.add_argument("--shares", help="Số CP lưu hành (để tính giá trị/CP)")

    oe = sub.add_parser("owner-earnings", help="LNST + khấu hao − capex duy trì")
    oe.add_argument("--net-income", required=True)
    oe.add_argument("--depreciation", required=True)
    oe.add_argument("--maintenance-capex", required=True)

    m = sub.add_parser("margin-of-safety", help="Biên an toàn so với giá trị nội tại")
    m.add_argument("--intrinsic", required=True)
    m.add_argument("--price", required=True)

    c = sub.add_parser("cagr", help="Tăng trưởng kép hằng năm")
    c.add_argument("--begin", required=True)
    c.add_argument("--end", required=True)
    c.add_argument("--years", required=True)

    r = sub.add_parser("ratios", help="ROE, ROIC, biên ròng, CFO/LNST, nợ ròng/EBITDA")
    r.add_argument("--net-income")
    r.add_argument("--equity")
    r.add_argument("--revenue")
    r.add_argument("--ebit")
    r.add_argument("--invested-capital")
    r.add_argument("--tax-rate", default="0.2")
    r.add_argument("--cfo")
    r.add_argument("--net-debt")
    r.add_argument("--ebitda")

    v = sub.add_parser("verify-mcap", help="Đối chiếu giá × số CP với vốn hoá công bố")
    v.add_argument("--price", required=True)
    v.add_argument("--shares", required=True)
    v.add_argument("--reported-mcap", required=True)

    a = p.parse_args()
    if a.cmd == "dcf":
        dcf(D(a.fcf), D(a.growth), a.years, D(a.terminal), D(a.discount),
            D(a.shares) if a.shares else None)
    elif a.cmd == "owner-earnings":
        owner_earnings(D(a.net_income), D(a.depreciation), D(a.maintenance_capex))
    elif a.cmd == "margin-of-safety":
        margin_of_safety(D(a.intrinsic), D(a.price))
    elif a.cmd == "cagr":
        cagr(D(a.begin), D(a.end), D(a.years))
    elif a.cmd == "ratios":
        ratios(a)
    elif a.cmd == "verify-mcap":
        verify_mcap(D(a.price), D(a.shares), D(a.reported_mcap))


if __name__ == "__main__":
    main()
