"""Bucket conventions survive compilation into the learner products that require them."""
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from Shared.library.compile_inputs import compile_bucket  # noqa: E402
from Shared.library.resolve import build_index  # noqa: E402

PACKAGES = sorted((REPO / "Physics/library").glob("*.json"))


def records():
    return build_index([json.loads(path.read_text(encoding="utf-8")) for path in PACKAGES])


def compile_one(index, bucket_id):
    return compile_bucket(
        index,
        bucket_id,
        topic_id=f"TEST-{bucket_id}",
        title=index[bucket_id]["title"],
        subject="Physics",
        practice_control={"mode": "DESIGN_PREVIEW", "purpose": "PRACTICE"},
    )


def product(compiled, core):
    return next((row for row in compiled["plan"]["products"] if row["core"] == core), None)


class ConventionDelivery(unittest.TestCase):
    def test_every_supported_core1_or_core1a_carries_each_authored_statement(self):
        index = records()
        buckets = [record for record in index.values()
                   if record.get("_collection") == "buckets" and record.get("conventions")]
        self.assertTrue(buckets, "fixture must contain authored conventions")

        for bucket in buckets:
            compiled = compile_one(index, bucket["id"])
            for core in ("CORE1", "CORE1A"):
                compiled_product = product(compiled, core)
                if compiled_product is None:
                    continue
                blob = json.dumps(compiled_product, ensure_ascii=False)
                for convention in bucket["conventions"]:
                    with self.subTest(bucket=bucket["id"], core=core,
                                      convention=convention["id"]):
                        self.assertIn(convention["statement"], blob)

    def test_core1_declares_conventions_before_other_orientation_content(self):
        index = records()
        for bucket_id in ("BUCKET-VECTOR-REPRESENTATION", "BUCKET-RELATIVE-MOTION"):
            compiled = compile_one(index, bucket_id)
            orientation = product(compiled, "CORE1")
            self.assertIsNotNone(orientation)
            blocks = orientation["units"][0]["blocks"]
            self.assertEqual(blocks[0]["id"], "CORE1-CONVENTIONS")
            self.assertTrue(blocks[0]["text"].startswith(
                "Conventions to declare before reading quantities:"))

    def test_core1a_declares_conventions_before_first_teaching_move(self):
        index = records()
        compiled = compile_one(index, "BUCKET-RELATIVE-MOTION")
        study = product(compiled, "CORE1A")
        self.assertIsNotNone(study)
        first = study["units"][0]["blocks"][0]
        self.assertEqual(first["kind"], "TEXT")
        self.assertTrue(first["text"].startswith(
            "Conventions to declare before reading quantities:"))
        first_title = index["MIC-SAME-TIME"]["title"]
        self.assertLess(first["text"].index(index["BUCKET-RELATIVE-MOTION"]["conventions"][0]["statement"]),
                        first["text"].index(first_title))


if __name__ == "__main__":
    unittest.main()
