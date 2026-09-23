"""Behavior tests for the fictional, local-only recruitment example."""

from decimal import Decimal
import pathlib
import subprocess
import sys
import unittest

import recruitment


HERE = pathlib.Path(__file__).resolve().parent


class CommandLineTests(unittest.TestCase):
    def test_reader_command_runs_and_explains_both_shortlists(self):
        command = subprocess.run(
            [sys.executable, str(HERE / "recruitment.py")],
            cwd=HERE.parent,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(command.returncode, 0, command.stderr)
        self.assertIn("Flawed total xG/90 shortlist", command.stdout)
        self.assertIn("Corrected npxG/90 ranked subset", command.stdout)
        self.assertIn("Withheld", command.stdout)
        self.assertIn("Roberto McBaggio 0.64", command.stdout)
        self.assertIn("Elliot Ward 0.60", command.stdout)
        self.assertIn("Roberto McBaggio 0.43", command.stdout)
        self.assertIn("Mateo Kovac", command.stdout)
        self.assertIn("Full-cohort failure", command.stdout)
        self.assertIn("No ranking", command.stdout)
        self.assertIn("policy_id=", command.stdout)
        self.assertIn("record_id=", command.stdout)
        self.assertIn("denominator=", command.stdout)


class ScreeningTests(unittest.TestCase):
    def test_penalty_false_positive_leads_flawed_list_but_is_excluded(self):
        records = recruitment.read_records(HERE / "players.csv")
        flawed = recruitment.flawed_shortlist(records)
        corrected = recruitment.screen(records)

        self.assertEqual([item.name for item in flawed], [
            "Roberto McBaggio", "Mateo Kovac", "Elliot Ward"
        ])
        self.assertEqual(flawed[0].score.quantize(Decimal("0.01")), Decimal("0.64"))
        self.assertEqual([item.name for item in corrected.ranked], ["Elliot Ward"])
        self.assertEqual(corrected.ranked[0].score, Decimal("0.60"))
        self.assertEqual([item.name for item in corrected.excluded], ["Roberto McBaggio"])
        self.assertEqual(corrected.excluded[0].score.quantize(Decimal("0.01")), Decimal("0.43"))
        self.assertEqual([item.name for item in corrected.withheld], ["Mateo Kovac"])
        self.assertFalse(corrected.complete_cohort)

    def test_reasons_identify_ranked_metric_excluded_and_prescreen_excluded_outcomes(self):
        records = recruitment.read_records(HERE / "players.csv")
        ranked_and_metric_excluded = recruitment.screen(records)
        self.assertEqual(ranked_and_metric_excluded.ranked[0].reason,
                         "meets strict npxG/90 threshold")
        self.assertEqual(ranked_and_metric_excluded.excluded[0].reason,
                         "npxG/90 does not exceed 0.55")

        too_old = {**records[1], "record_id": "fictional-004", "age": "23"}
        prescreen = recruitment.screen([too_old])
        self.assertEqual(prescreen.ranked, ())
        self.assertIn("age", prescreen.excluded[0].reason)
        self.assertNotIn("npxG/90", prescreen.excluded[0].reason)

    def test_each_mismatch_withholds_instead_of_ranked_or_excluded(self):
        ward = recruitment.read_records(HERE / "players.csv")[1]
        differences = {
            "provider": "Provider B", "model": "v1", "season": "2024-25",
            "competition_scope": "other_league", "denominator": "all_competition_minutes",
            "penalty_treatment": "penalties_retained", "metric_id": "other_metric",
        }
        for field, changed in differences.items():
            with self.subTest(field=field):
                record = {**ward, field: changed}
                result = recruitment.screen([record])
                self.assertEqual(result.ranked, ())
                self.assertEqual(result.excluded, ())
                self.assertEqual(result.withheld[0].record_id, "fictional-002")
                self.assertIn(field, result.withheld[0].reason)
                self.assertFalse(result.complete_cohort)

    def test_strict_threshold_uses_unrounded_decimal(self):
        ward = recruitment.read_records(HERE / "players.csv")[1]
        at_threshold = {**ward, "league_minutes": "900", "total_xg": "5.50"}
        just_above = {**at_threshold, "record_id": "fictional-004", "total_xg": "5.5001"}
        result = recruitment.screen([at_threshold, just_above])
        self.assertEqual([item.record_id for item in result.excluded], ["fictional-002"])
        self.assertEqual([item.record_id for item in result.ranked], ["fictional-004"])
        self.assertGreater(result.ranked[0].score, Decimal("0.55"))
        self.assertEqual(result.ranked[0].score.quantize(Decimal("0.01")), Decimal("0.55"))

    def test_flawed_shortlist_still_applies_threshold_to_wrong_metric(self):
        ward = recruitment.read_records(HERE / "players.csv")[1]
        at_threshold = {**ward, "league_minutes": "900", "total_xg": "5.50"}
        just_above = {**at_threshold, "total_xg": "5.5001"}
        self.assertEqual(recruitment.flawed_shortlist([at_threshold]), ())
        self.assertEqual(len(recruitment.flawed_shortlist([just_above])), 1)

    def test_missing_or_invalid_evidence_is_withheld_not_excluded(self):
        ward = recruitment.read_records(HERE / "players.csv")[1]
        cases = [
            ({"record_id": ""}, "record_id"),
            ({"provider": ""}, "provider"),
            ({"penalty_xg": "NaN"}, "invalid evidence"),
            ({"penalty_xg": "9.00"}, "invalid evidence"),
            ({"league_minutes": "0"}, "invalid evidence"),
            ({"affordable": "unknown"}, "invalid evidence"),
            ({"penalty_count": "0", "penalty_xg": "0.79"}, "invalid evidence"),
        ]
        for changes, expected_reason in cases:
            with self.subTest(changes=changes):
                result = recruitment.screen([{**ward, **changes}])
                self.assertEqual(result.ranked, ())
                self.assertEqual(result.excluded, ())
                self.assertIn(expected_reason, result.withheld[0].reason)

    def test_full_cohort_from_unapproved_model_yields_no_ranking(self):
        records = recruitment.read_records(HERE / "players.csv")
        all_b = [{**record, "provider": "Provider B", "model": "v1"} for record in records]
        result = recruitment.screen(all_b)
        self.assertEqual(result.ranked, ())
        self.assertEqual(result.excluded, ())
        self.assertEqual(len(result.withheld), 3)
        self.assertFalse(result.complete_cohort)

    def test_duplicate_record_identifiers_are_withheld(self):
        ward = recruitment.read_records(HERE / "players.csv")[1]
        result = recruitment.screen([ward, {**ward, "name": "Different named record"}])
        self.assertEqual(result.ranked, ())
        self.assertEqual(len(result.withheld), 2)
        self.assertTrue(all("duplicate record_id" in item.reason for item in result.withheld))


if __name__ == "__main__":
    unittest.main()
