import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_longform_plan import (
    build_first100_manifest,
    build_first100_guard_config,
    validate_first100_guard_config,
    build_longform_contract,
    validate_first100_manifest,
    validate_longform_contract,
    build_longform_first100_dry_run,
)


class LongformCandidatePlanTests(unittest.TestCase):
    def test_eighteen_volume_contract_is_scale_consistent(self):
        result = validate_longform_contract(build_longform_contract())
        self.assertTrue(result["valid"], result["errors"])

    def test_rejects_wrong_total_chapter_count(self):
        contract = build_longform_contract()
        contract["volumes"][0]["chapter_target"] = 99
        self.assertFalse(validate_longform_contract(contract)["valid"])

    def test_rejects_missing_longform_price_engine(self):
        contract = build_longform_contract()
        contract.pop("price_engine")
        self.assertFalse(validate_longform_contract(contract)["valid"])

    def test_rejects_missing_cross_city_witness_medium(self):
        contract = build_longform_contract()
        contract.pop("cross_city_witness_medium")
        self.assertFalse(validate_longform_contract(contract)["valid"])

    def test_first_hundred_has_ten_payoffs_and_no_prose(self):
        result = validate_first100_manifest(build_first100_manifest())
        self.assertTrue(result["valid"], result["errors"])

    def test_guard_config_preserves_canonical_lifecycle_and_single_concealment(self):
        config = build_first100_guard_config()
        self.assertTrue(validate_first100_guard_config(config)["valid"])
        config["concealment_period"]["max_uses"] = 2
        self.assertFalse(validate_first100_guard_config(config)["valid"])


if __name__ == "__main__":
    unittest.main()
