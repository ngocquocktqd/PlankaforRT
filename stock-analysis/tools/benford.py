#!/usr/bin/env python3
"""Kiểm tra Định luật Benford trên chuỗi số liệu tài chính.

Số liệu tài chính tự nhiên (doanh thu, chi phí, số dư... qua nhiều kỳ) có phân bố
chữ số đầu tiên tuân theo Benford: P(d) = log10(1 + 1/d). Lệch mạnh khỏi phân bố
này là DẤU HIỆU (không phải bằng chứng) số liệu bị can thiệp — cần đối chiếu thêm.

Cần tối thiểu ~50 con số để kết quả có ý nghĩa; dưới 100 số nên diễn giải thận trọng.

Dùng:
    python3 benford.py --values 1234,5678,910,...          # truyền trực tiếp
    python3 benford.py --file numbers.txt                  # mỗi dòng 1 số, hoặc CSV
    cat report_numbers.txt | python3 benford.py            # qua stdin
"""

import argparse
import math
import re
import sys


BENFORD = {d: math.log10(1 + 1 / d) for d in range(1, 10)}


def first_digit(x: str) -> int | None:
    m = re.search(r"[1-9]", x.lstrip("-").lstrip("0").replace(".", "").replace(",", ""))
    return int(m.group()) if m else None


def extract_numbers(text: str) -> list[str]:
    # Dấu phẩy chỉ là phân tách hàng nghìn khi theo đúng nhóm 3 chữ số (1,234,567);
    # còn lại coi là phân tách giữa các số (CSV).
    return re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?", text)


def analyze(values: list[str]) -> None:
    digits = [d for d in (first_digit(v) for v in values) if d]
    n = len(digits)
    if n < 20:
        sys.exit(f"LỖI: chỉ có {n} số hợp lệ — cần tối thiểu 20 (khuyến nghị ≥50).")

    counts = {d: digits.count(d) for d in range(1, 10)}
    chi2 = 0.0
    print(f"Số mẫu: {n}\n")
    print(f"{'Chữ số':>7} {'Quan sát':>10} {'Benford':>10} {'Lệch':>8}")
    for d in range(1, 10):
        obs = counts[d] / n
        exp = BENFORD[d]
        expected_count = exp * n
        chi2 += (counts[d] - expected_count) ** 2 / expected_count
        bar = "█" * round(obs * 50)
        print(f"{d:>7} {obs:>9.1%} {exp:>9.1%} {obs - exp:>+7.1%}  {bar}")

    # Chi-square, 8 bậc tự do: 15.51 (p=0.05), 20.09 (p=0.01)
    print(f"\nChi-square = {chi2:.2f} (df=8)")
    if chi2 <= 15.51:
        print("✅ Phù hợp Benford (p>0.05) — không thấy dấu hiệu bất thường.")
    elif chi2 <= 20.09:
        print("🟡 Lệch nhẹ (0.01<p<0.05) — nên soi thêm các khoản mục lớn, nhưng chưa kết luận được.")
    else:
        print("🚩 Lệch mạnh (p<0.01) — DẤU HIỆU số liệu bất thường. Lưu ý: mẫu nhỏ, "
              "số liệu bị làm tròn mạnh, hoặc dải giá trị hẹp cũng gây lệch. "
              "Đối chiếu thêm: CFO/LNST, phải thu, giao dịch bên liên quan.")
    if n < 100:
        print(f"\n⚠️  Mẫu {n} < 100 — kết quả chỉ mang tính tham khảo.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--values", help="Danh sách số phân cách bằng dấu phẩy hoặc khoảng trắng")
    p.add_argument("--file", help="File chứa số liệu (mỗi dòng một số, hoặc văn bản/CSV bất kỳ)")
    a = p.parse_args()

    if a.values:
        values = re.split(r"[\s;]+", a.values.strip())
        values = [v for chunk in values for v in chunk.split(",") if v]
    elif a.file:
        with open(a.file, encoding="utf-8") as f:
            values = extract_numbers(f.read())
    elif not sys.stdin.isatty():
        values = extract_numbers(sys.stdin.read())
    else:
        p.error("cần --values, --file hoặc dữ liệu qua stdin")
    analyze(values)


if __name__ == "__main__":
    main()
