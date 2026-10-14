# freelance-invoice-cli

Generate a clean, printable HTML invoice from a JSON file. No dependencies, no sign-up, no SaaS — just Python 3.

```bash
python3 invoice.py example.json -o invoice.html
```

Open `invoice.html` in a browser, or print to PDF (Ctrl/Cmd+P → Save as PDF).

## Invoice JSON format

```json
{
  "invoice_number": "INV-0001",
  "from": "Jane Doe, Freelance Developer",
  "to": "Acme Corp",
  "date": "2026-10-14",
  "due_date": "2026-10-28",
  "tax_rate": 0,
  "items": [
    {"description": "Website redesign", "qty": 1, "rate": 1800}
  ],
  "notes": "Net 14. Late payments accrue 1.5% monthly interest after the due date."
}
```

See [`example.json`](example.json) for a full example.

## Why a CLI instead of a web app?

If you're already comfortable in a terminal, this is faster than filling out a form every time — keep a JSON template per client, tweak the line items, and generate. No account, no data leaving your machine.

Prefer a web form instead? Use the free browser version: [invoice generator](https://kleogeos.github.io/freelancer-tools/invoice.html) · [rate calculator](https://kleogeos.github.io/freelancer-tools/rate-calculator.html)

Check a contract for missing clauses: [contract-checklist-cli](https://github.com/kleogeos/contract-checklist-cli)

Need the paperwork beyond invoices — proposals, contracts, late-payment emails, client scripts? [Freelancer Starter Kit ($15)](https://kleogeos.gumroad.com/l/nvjec)

## License

MIT — do whatever you want with it.
