"""Minimal review scheduling is deterministic and does not mutate learner truth."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.tools import review_schedule  # noqa: E402


class ReviewSchedule(unittest.TestCase):
    def observation(self, **overrides):
        row = {
            "observation_id": "OBS-1",
            "capability_ref": "CAP-X",
            "result": "DEMONSTRATED",
            "help": "NONE",
            "when": "2026-09-18",
        }
        row.update(overrides)
        return row

    def test_policy_intervals_are_fixed_and_transparent(self):
        self.assertEqual(review_schedule.next_review("INCORRECT", "2026-09-18"), "2026-09-19")
        self.assertEqual(review_schedule.next_review("CORRECT_WITH_HINT", "2026-09-18"), "2026-09-21")
        self.assertEqual(review_schedule.next_review("CORRECT_INDEPENDENT", "2026-09-18"), "2026-09-25")
        self.assertEqual(review_schedule.next_review("TRANSFER_INDEPENDENT", "2026-09-18"), "2026-10-02")

    def test_independent_success_maps_to_seven_day_review(self):
        scheduled = review_schedule.schedule(self.observation())
        self.assertEqual(scheduled["outcome"], "CORRECT_INDEPENDENT")
        self.assertEqual(scheduled["next_review"], "2026-09-25")

    def test_independent_transfer_maps_to_fourteen_day_review(self):
        scheduled = review_schedule.schedule(self.observation(), transfer=True)
        self.assertEqual(scheduled["outcome"], "TRANSFER_INDEPENDENT")
        self.assertEqual(scheduled["next_review"], "2026-10-02")

    def test_helped_success_maps_to_three_day_review(self):
        scheduled = review_schedule.schedule(self.observation(
            result="UNCERTAIN",
            help="HINT",
        ))
        self.assertEqual(scheduled["outcome"], "CORRECT_WITH_HINT")
        self.assertEqual(scheduled["next_review"], "2026-09-21")

    def test_failed_or_uncertain_unhelped_attempt_returns_tomorrow(self):
        for row in [
            self.observation(result="MISSING", help="NONE"),
            self.observation(result="UNCERTAIN", help="UNKNOWN"),
        ]:
            with self.subTest(row=row):
                scheduled = review_schedule.schedule(row)
                self.assertEqual(scheduled["outcome"], "INCORRECT")
                self.assertEqual(scheduled["next_review"], "2026-09-19")

    def test_timestamp_is_normalised_to_calendar_date(self):
        scheduled = review_schedule.schedule(self.observation(
            when="2026-09-18T19:42:00+04:00",
        ))
        self.assertEqual(scheduled["observed_on"], "2026-09-18")
        self.assertEqual(scheduled["next_review"], "2026-09-25")

    def test_due_returns_only_rows_due_on_or_before_date(self):
        rows = [
            {"capability_ref": "CAP-B", "observation_ref": "O2", "next_review": "2026-09-21"},
            {"capability_ref": "CAP-A", "observation_ref": "O1", "next_review": "2026-09-19"},
            {"capability_ref": "CAP-C", "observation_ref": "O3", "next_review": "2026-09-25"},
        ]
        self.assertEqual(
            [row["capability_ref"] for row in review_schedule.due(rows, "2026-09-21")],
            ["CAP-A", "CAP-B"],
        )

    def test_schedule_does_not_rewrite_observation_state(self):
        observation = self.observation()
        before = dict(observation)
        review_schedule.schedule(observation)
        self.assertEqual(observation, before)

    def test_unknown_outcome_is_rejected(self):
        with self.assertRaises(ValueError):
            review_schedule.next_review("FANCY_ALGORITHM", "2026-09-18")


if __name__ == "__main__":
    unittest.main()
