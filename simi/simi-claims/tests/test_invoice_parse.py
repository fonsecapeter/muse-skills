"""Spec for bin/invoice_parse — the Mission Pet Hospital invoice parser.

Fixtures are real pdftotext -layout output captured from Simi's actual
invoices, so the suite reads as documentation of what the parser does
with the documents it exists for.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bin"))
from invoice_parse import invoice_filename, parse_invoice_text

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return f.read()


class TestParseInvoiceText(unittest.TestCase):
    def test_extracts_invoice_number_date_and_total_from_a_real_invoice(self):
        out = parse_invoice_text(fixture("visit_312364.txt"))
        self.assertEqual(out["invoice_number"], "312364")
        self.assertEqual(out["date"], "02/17/2025")
        self.assertEqual(out["total"], "443.36")

    def test_strips_the_thousands_separator_from_the_total(self):
        out = parse_invoice_text(fixture("dental_296943.txt"))
        self.assertEqual(out["total"], "2377.28")

    def test_extracts_each_line_item_with_its_amount(self):
        out = parse_invoice_text(fixture("vaccines_278451.txt"))
        self.assertEqual(
            [(i["description"], i["amount"]) for i in out["line_items"]],
            [("Bordetella Oral Vaccine", "50.00"),
             ("Canine Influenza Vaccine", "50.00"),
             ("Lepto Vaccine", "50.00"),
             ("Canine Rabies Vaccine", "50.00")])

    def test_names_the_canonical_filename_for_the_invoice(self):
        out = parse_invoice_text(fixture("dental_296943.txt"))
        self.assertEqual(out["filename"], "invoice_2024_04_01_296943.pdf")

    def test_fails_loudly_when_a_required_field_is_missing(self):
        text = fixture("vaccines_278451.txt").replace("INVOICE TOTAL", "TOTAL")
        with self.assertRaises(ValueError) as ctx:
            parse_invoice_text(text)
        self.assertIn("total", str(ctx.exception))

    def test_fails_loudly_on_text_that_is_not_an_invoice(self):
        with self.assertRaises(ValueError) as ctx:
            parse_invoice_text("Simi went to the park today.\n")
        for field in ("invoice_number", "date", "total"):
            self.assertIn(field, str(ctx.exception))


class TestInvoiceFilename(unittest.TestCase):
    def test_carries_the_date_and_the_invoice_number(self):
        self.assertEqual(invoice_filename("10/13/2026", "344492"),
                         "invoice_2026_10_13_344492.pdf")

    def test_zero_pads_single_digit_months_and_days(self):
        self.assertEqual(invoice_filename("2/7/2026", "331234"),
                         "invoice_2026_02_07_331234.pdf")

    def test_falls_back_to_the_plain_dated_name_without_a_number(self):
        self.assertEqual(invoice_filename("03/05/2024", None),
                         "invoice_2024_03_05.pdf")

    def test_falls_back_to_undated_without_a_date(self):
        self.assertEqual(invoice_filename(None, "344492"),
                         "invoice_undated.pdf")


if __name__ == "__main__":
    unittest.main()
