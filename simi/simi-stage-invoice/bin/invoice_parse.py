#!/usr/bin/env python3
"""Parse Mission Pet Hospital invoice text (pdftotext -layout output).

Pure functions over text so the parsing — the part that silently failed
in Oct 2026 — is unit-testable. Used by bin/extract-invoice as a CLI:
reads invoice text on stdin, prints the extraction as JSON, and exits
non-zero with an EXTRACTION FAILED message when a required field is
missing.
"""
import json
import re
import sys


def invoice_filename(mdy_date, invoice_number):
    """Canonical Drive name for an invoice: invoice_yyyy_mm_dd_<id>.pdf
    (plain dated name when the number is unknown)."""
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", mdy_date or "")
    if not m:
        return "invoice_undated.pdf"
    base = "invoice_%s_%s_%s" % (m.group(3), m.group(1).zfill(2),
                                 m.group(2).zfill(2))
    if invoice_number:
        return "%s_%s.pdf" % (base, invoice_number)
    return base + ".pdf"


def parse_invoice_text(text):
    """Extract invoice_number, date, total, and line_items from invoice
    text. Raises ValueError naming every required field that is missing."""
    out = {"invoice_number": None, "date": None, "total": None,
           "line_items": []}
    m = re.search(r'(?m)^\d{1,2}/\d{1,2}/\d{4}\s+(\d{4,})', text)
    if m:
        out["invoice_number"] = m.group(1)
    m = re.search(r'(\d{1,2}/\d{1,2}/\d{4})\s+Due upon receipt', text)
    if m:
        out["date"] = m.group(1)
    m = re.search(r'INVOICE TOTAL\s+\$?([\d,]+\.\d{2})', text)
    if m:
        out["total"] = m.group(1).replace(',', '')
    for line in text.splitlines():
        m = re.match(r'\s*Simi\s+(.+?)\s+1\s+([\d,]+\.\d{2})\s*$', line)
        if m:
            desc = m.group(1).strip()
            if desc and float(m.group(2).replace(',', '')) > 0:
                out["line_items"].append(
                    {"description": desc,
                     "amount": m.group(2).replace(',', '')})
    missing = [k for k in ("invoice_number", "date", "total") if not out[k]]
    if missing:
        raise ValueError("could not parse %s from this PDF"
                         % ", ".join(missing))
    out["filename"] = invoice_filename(out["date"], out["invoice_number"])
    return out


def main():
    try:
        result = parse_invoice_text(sys.stdin.read())
    except ValueError as e:
        print("EXTRACTION FAILED: %s" % e, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
