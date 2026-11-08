"""Unit tests for bin/jeep-maintenance. The tests are the spec.

Run: python3 -m unittest discover -s tests -v
"""
import datetime
import importlib.util
from importlib.machinery import SourceFileLoader
import os
import unittest

BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "bin", "jeep-maintenance")
spec = importlib.util.spec_from_loader(
    "jeep_maintenance", SourceFileLoader("jeep_maintenance", BIN))
jm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jm)

CFG = {"due_soon_miles": 1000, "due_soon_days": 30}
TODAY = datetime.date(2026, 10, 29)
NOW_MI = 89857

HEADER = ["", "Actual Date", "Actual Mileage", "Owner", "Actor", "Location",
          "Job", "Parts", "Notes", "Type", "Interval (mi)", "Interval (mo)",
          "Due (mi)", "Due (date)"]


def other_row(date="", miles="", job="", typ="", int_mi="", int_mo="",
              due_mi="", due_date=""):
    return ["", date, miles, "P", "Self", "SF", job, "", "", typ,
            int_mi, int_mo, due_mi, due_date]


class ParseTests(unittest.TestCase):
    def test_parse_int_reads_grouped_mileage(self):
        self.assertEqual(jm.parse_int("86,233"), 86233)

    def test_parse_int_rejects_placeholders(self):
        for raw in ("", "?", "probably\nnever", None):
            self.assertIsNone(jm.parse_int(raw))

    def test_parse_date_reads_iso_and_rejects_text(self):
        self.assertEqual(jm.parse_date("2025-09-27"), datetime.date(2025, 9, 27))
        self.assertIsNone(jm.parse_date("?"))
        self.assertIsNone(jm.parse_date(""))

    def test_parse_interval_months(self):
        self.assertEqual(jm.parse_interval_months("12"), 12)
        self.assertEqual(jm.parse_interval_months("12 mo"), 12)
        self.assertEqual(jm.parse_interval_months("10 yr"), 120)
        self.assertIsNone(jm.parse_interval_months(""))

    def test_add_months_clamps_to_short_month(self):
        self.assertEqual(jm.add_months(datetime.date(2026, 1, 31), 1),
                         datetime.date(2026, 2, 28))
        self.assertEqual(jm.add_months(datetime.date(2025, 6, 22), 120),
                         datetime.date(2035, 6, 22))


class CollectTests(unittest.TestCase):
    def rows(self):
        return [
            ["", "Other"], [], HEADER,
            other_row("2024-08-28", "70,572", "Rotate\nTires", "Scheduled", "7500", "12"),
            other_row("", "", "Rotate Tires", "Scheduled", "7500", "12",
                      due_mi="78072", due_date="2025-08-28"),
            other_row("2025-06-22", "77,126", "Thermostat", "One-off"),
            other_row("", "", "Front Diff Gear Oil", "Scheduled", "30000"),
            other_row("", "0", "Spark Plugs", "Scheduled", "100000"),
            other_row("2025-06-22", "77,126", "Coolant Flush", "Scheduled", "150000", "120"),
            other_row("2025-09-27", "79,296", "Coolant Flush", "Scheduled", "150000", "120"),
        ]

    def test_ignores_one_off_rows(self):
        self.assertNotIn("Thermostat", jm.collect_scheduled(self.rows()))

    def test_job_names_are_normalized(self):
        self.assertIn("Rotate Tires", jm.collect_scheduled(self.rows()))

    def test_seed_row_without_a_date_means_never_done(self):
        facts = jm.collect_scheduled(self.rows())["Front Diff Gear Oil"]
        self.assertIsNone(facts["last_date"])
        self.assertEqual(facts["int_mi"], 30000)

    def test_latest_row_wins_for_last_done(self):
        facts = jm.collect_scheduled(self.rows())["Coolant Flush"]
        self.assertEqual(facts["last_date"], datetime.date(2025, 9, 27))
        self.assertEqual(facts["last_miles"], 79296)

    def test_spark_plugs_anchor_at_zero_miles(self):
        facts = jm.collect_scheduled(self.rows())["Spark Plugs"]
        self.assertEqual(facts["last_miles"], 0)
        self.assertEqual(facts["int_mi"], 100000)

    def test_upcoming_row_due_is_captured(self):
        facts = jm.collect_scheduled(self.rows())["Rotate Tires"]
        self.assertEqual(facts["due_mi"], 78072)
        self.assertEqual(facts["due_date"], datetime.date(2025, 8, 28))

    def test_upcoming_row_does_not_change_last_done(self):
        facts = jm.collect_scheduled(self.rows())["Rotate Tires"]
        self.assertEqual(facts["last_date"], datetime.date(2024, 8, 28))
        self.assertEqual(facts["last_miles"], 70572)


class AssessTests(unittest.TestCase):
    def facts(self, **kw):
        base = {"last_date": None, "last_miles": None, "int_mi": None,
                "int_months": None, "due_mi": None, "due_date": None}
        base.update(kw)
        return base

    def test_never_done_is_due_now(self):
        item = jm.assess("Engine Air Filter", self.facts(int_mi=20000),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "DUE NOW")
        self.assertEqual(item.reasons, ["never done"])

    def test_miles_past_due_is_due_now(self):
        item = jm.assess("Rotate Tires",
                         self.facts(last_date=datetime.date(2024, 8, 28),
                                    last_miles=70572, int_mi=7500, int_months=12),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "DUE NOW")

    def test_zero_anchored_target_within_soon_window_is_due_soon(self):
        item = jm.assess("Spark Plugs",
                         self.facts(last_miles=0, int_mi=90500),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "DUE SOON")

    def test_zero_anchored_target_far_off_is_ok(self):
        item = jm.assess("Spark Plugs",
                         self.facts(last_miles=0, int_mi=100000),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "OK")

    def test_fresh_service_is_ok(self):
        item = jm.assess("Engine Oil",
                         self.facts(last_date=datetime.date(2026, 6, 28),
                                    last_miles=86233, int_mi=7000, int_months=12),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "OK")

    def test_time_interval_alone_can_be_due(self):
        item = jm.assess("Brake Fluid",
                         self.facts(last_date=datetime.date(2023, 1, 1),
                                    int_months=36),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "DUE NOW")

    def test_due_row_in_the_future_is_ok_without_any_actual(self):
        item = jm.assess("Spark Plugs", self.facts(due_mi=100000),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "OK")

    def test_due_row_in_the_past_is_due_now(self):
        item = jm.assess("Rotate Tires",
                         self.facts(last_date=datetime.date(2024, 8, 28),
                                    last_miles=70572, int_mi=7500,
                                    due_mi=78072,
                                    due_date=datetime.date(2025, 8, 28)),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "DUE NOW")
        self.assertIn("due at 78,072 mi", item.reasons)

    def test_due_row_wins_over_computed_interval(self):
        item = jm.assess("Cabin Air Filter",
                         self.facts(last_date=datetime.date(2026, 10, 1),
                                    last_miles=89000, int_mi=20000,
                                    due_mi=109000),
                         NOW_MI, TODAY, CFG)
        self.assertEqual(item.status, "OK")


class ReadTests(unittest.TestCase):
    def test_read_info_pulls_mileage_and_date(self):
        rows = [["Jeep Info"], ["Year", "2017"],
                ["Current mileage", "89857"], ["Mileage date", "2026-10-29"]]
        self.assertEqual(jm.read_info(rows),
                         (89857, datetime.date(2026, 10, 29)))

    def test_read_last_oil_takes_the_last_usable_row(self):
        rows = [[], ["", "Oil Changes"], [], HEADER,
                ["", "2024-03-20", "65,005"],
                ["", "2026-06-28", "86,233"],
                ["", "?", "?"]]
        self.assertEqual(jm.read_last_oil(rows),
                         (datetime.date(2026, 6, 28), 86233))


INFO = [["Current mileage", "89857"], ["Mileage date", "2026-10-29"]]
DONE = datetime.date(2026, 11, 2)


class PlanLogTests(unittest.TestCase):
    def rows(self):
        return [
            ["", "Other"], [], HEADER,
            other_row("2024-08-28", "70,572", "Rotate\nTires", "Scheduled",
                      "7500", "12"),
            other_row("", "", "Rotate Tires", "Scheduled", "7500", "12",
                      due_mi="78072", due_date="2025-08-28"),
            other_row("", "", "Cabin Air Filter", "Scheduled", "20000", "24",
                      due_mi="89857", due_date="2026-10-29"),
        ]

    def plan(self, rows, job, miles=90123, **kw):
        return jm.plan_log("Other", "Info", rows, INFO, job, DONE, miles, **kw)

    def test_actual_row_is_appended_with_due_and_notes_blank(self):
        writes, _ = self.plan(self.rows(), "Cabin Air Filter")
        tab, rng, values = writes[0]
        self.assertEqual((tab, rng), ("Other", "A7:N7"))
        row = values[0]
        self.assertEqual(row[1], "2026-11-02")
        self.assertEqual(row[2], "90123")
        self.assertEqual(row[6], "Cabin Air Filter")
        self.assertEqual(row[8], "")
        self.assertEqual(row[12:], ["", ""])

    def test_upcoming_row_rolls_forward_to_the_new_due(self):
        writes, summary = self.plan(self.rows(), "Cabin Air Filter")
        self.assertIn(("Other", "K6:N6", [["20000", "24", "110123", "2028-11-02"]]),
                      writes)
        self.assertIn("Next due for Cabin Air Filter: 110,123 mi / 2028-11-02",
                      summary)

    def test_existing_upcoming_row_is_reused_not_duplicated(self):
        writes, _ = self.plan(self.rows(), "Rotate Tires")
        ranges = [rng for _, rng, _ in writes]
        self.assertIn("K5:N5", ranges)
        self.assertNotIn("A8:N8", ranges)

    def test_scheduled_job_without_an_upcoming_row_gets_one_appended(self):
        rows = [["", "Other"], [], HEADER,
                other_row("2025-09-27", "79,296", "Transmission\nFluid",
                          "Scheduled", "30000", "36")]
        writes, _ = self.plan(rows, "Transmission Fluid", miles=109500)
        self.assertIn(("Other", "A6:N6",
                       [["", "", "", "P", "", "", "Transmission\nFluid", "", "",
                         "Scheduled", "30000", "36", "139500", "2029-11-02"]]),
                      writes)

    def test_one_off_log_writes_no_due_row(self):
        writes, _ = self.plan(self.rows(), "Replace Wiper Blades")
        self.assertEqual(len([w for w in writes if w[0] == "Other"]), 1)
        self.assertEqual(writes[0][2][0][9], "One-off")

    def test_anchor_advances_when_the_logged_mileage_is_newer(self):
        writes, summary = self.plan(self.rows(), "Cabin Air Filter")
        self.assertIn(("Info", "B1", [["90123"]]), writes)
        self.assertIn(("Info", "B2", [["2026-11-02"]]), writes)
        self.assertTrue(any("anchor advanced" in s for s in summary))

    def test_anchor_is_not_rewound_by_late_logged_work(self):
        writes, summary = self.plan(self.rows(), "Cabin Air Filter", miles=80000)
        self.assertFalse(any(tab == "Info" for tab, _, _ in writes))
        self.assertTrue(any("anchor unchanged" in s for s in summary))


class PlanOilLogTests(unittest.TestCase):
    def rows(self):
        return [["", "2025-09-07", "78,732"],
                ["", "2026-06-28", "86,233"],
                ["", "", "", "", "", "", "", "", "", "", "", "",
                 "  - drain"]]

    def test_oil_row_lands_under_the_last_change_with_its_interval(self):
        writes, summary = jm.plan_oil_log("Oil Changes", "Info", self.rows(),
                                          INFO, DONE, 90000,
                                          oil="valvoline clean & restore",
                                          oil_filter="mobil 1")
        tab, rng, values = writes[0]
        self.assertEqual((tab, rng), ("Oil Changes", "A3:K3"))
        self.assertEqual(values[0][1:4], ["2026-11-02", "90000", "3767"])
        self.assertEqual(values[0][7], "valvoline clean & restore")
        self.assertIn("interval 3,767 mi", summary[0])


if __name__ == "__main__":
    unittest.main()
