#!/usr/bin/env python3
"""Generate a clean HTML invoice from a JSON file. Zero dependencies."""
import argparse
import html
import json
import sys


def money(n):
    return f"${n:,.2f}"


def render(data):
    items = data["items"]
    subtotal = sum(i["qty"] * i["rate"] for i in items)
    tax_rate = data.get("tax_rate", 0)
    tax = subtotal * tax_rate / 100
    total = subtotal + tax

    rows = "\n".join(
        f"<tr><td>{html.escape(i['description'])}</td>"
        f"<td style='text-align:right'>{i['qty']}</td>"
        f"<td style='text-align:right'>{money(i['rate'])}</td>"
        f"<td style='text-align:right'>{money(i['qty'] * i['rate'])}</td></tr>"
        for i in items
    )

    notes = html.escape(data.get("notes", ""))

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Invoice {html.escape(data.get('invoice_number', ''))}</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;max-width:680px;margin:40px auto;color:#1a1a1a}}
table{{width:100%;border-collapse:collapse;margin-top:24px}}
th,td{{padding:8px;border-bottom:1px solid #ddd}}
th{{text-align:left;color:#666;font-size:13px;text-transform:uppercase}}
.total{{font-size:20px;font-weight:bold}}
.meta{{color:#666;font-size:14px}}
@media print{{body{{margin:0}}}}
</style></head><body>
<h1>Invoice {html.escape(data.get('invoice_number', ''))}</h1>
<p class="meta">From: {html.escape(data.get('from', ''))}<br>
To: {html.escape(data.get('to', ''))}<br>
Date: {html.escape(data.get('date', ''))} &middot; Due: {html.escape(data.get('due_date', ''))}</p>
<table>
<tr><th>Description</th><th style="text-align:right">Qty</th><th style="text-align:right">Rate</th><th style="text-align:right">Amount</th></tr>
{rows}
</table>
<p style="text-align:right;margin-top:16px">Subtotal: {money(subtotal)}<br>
{"Tax (" + str(tax_rate) + "%): " + money(tax) + "<br>" if tax_rate else ""}
<span class="total">Total: {money(total)}</span></p>
{"<p class='meta'>" + notes + "</p>" if notes else ""}
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="JSON invoice file (see example.json)")
    ap.add_argument("-o", "--output", help="output HTML file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
