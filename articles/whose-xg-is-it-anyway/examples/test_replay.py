import unittest
from replay import OFFERS, invoke, screen_record


class ReplayTests(unittest.TestCase):
    def setUp(self):
        OFFERS.clear()
        self.record = dict(player_id="mcbaggio-21", source="A/v3.4",
                           season="2025/26", scope="domestic_league",
                           evidence="season-2025-26-mcbaggio",
                           minutes=2684, total_xg="19.08", penalty_xg="3.16")

    def test_penalties_change_the_decision(self):
        result = screen_record(self.record)
        self.assertEqual(result.get("status"), "excluded")
        self.assertEqual(result.get("npxg"), "15.92")
        self.assertEqual(result.get("npxg_per_90"), "0.53")
        self.assertEqual(result.get("evidence"), "season-2025-26-mcbaggio")

    def test_strict_threshold_uses_unrounded_rate(self):
        self.record.update(minutes=2700, penalty_xg="0", total_xg="16.5")
        self.assertEqual(screen_record(self.record).get("status"), "excluded")
        self.record["total_xg"] = "16.501"
        self.assertEqual(screen_record(self.record).get("status"), "passes_metric")

    def test_incompatible_source_is_withheld(self):
        self.record["source"] = "B/v1"
        self.assertEqual(screen_record(self.record).get("status"), "withheld")

    def test_missing_penalties_are_not_assumed_zero(self):
        self.record.pop("penalty_xg")
        self.assertEqual(screen_record(self.record).get("status"), "withheld")

    def test_invalid_evidence_is_withheld(self):
        for changes in [dict(minutes=0), dict(total_xg="NaN"),
                        dict(penalty_xg="20"), dict(scope="all_competitions")]:
            with self.subTest(changes=changes):
                self.assertEqual(screen_record(self.record | changes).get("status"), "withheld")

    def test_authorised_screen_returns_actual_result(self):
        result = invoke("recruitment", "screen_recruits", {"player_id": "mcbaggio-21"})
        self.assertEqual(result.get("status"), "excluded")
        self.assertEqual(result.get("policy"), "recruitment-v1")

    def test_caller_cannot_override_policy(self):
        result = invoke("recruitment", "screen_recruits",
                        {"player_id": "mcbaggio-21", "policy": "old-policy"})
        self.assertEqual(result.get("status"), "rejected_request")

    def test_denied_offer_does_not_execute(self):
        result = invoke("recruitment", "submit_offer",
                        {"player_id": "mcbaggio-21", "GBP": 25000000})
        self.assertEqual(result.get("status"), "denied")
        self.assertEqual(OFFERS, [])

    def test_unknown_role_is_denied(self):
        self.assertEqual(invoke("unknown", "screen_recruits",
                                {"player_id": "mcbaggio-21"}).get("status"), "denied")


if __name__ == "__main__":
    unittest.main()
