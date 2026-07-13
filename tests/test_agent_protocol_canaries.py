import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_agent_canaries import CASE_IDS, VERSION, _parse_protocol_output, validate_agent_protocol_canaries_from_evidence


class AgentProtocolCanaryTests(unittest.TestCase):
    def test_accepts_exact_json_and_fenced_json(self):
        payload = '{"protocol_version":"0.1","agent":"hermes","case_id":"protocol-01","status":"ok","no_prose":true}'
        self.assertTrue(_parse_protocol_output(payload, "hermes", "protocol-01")["valid"])
        self.assertTrue(_parse_protocol_output("```json\n" + payload + "\n```", "hermes", "protocol-01")["valid"])

    def test_rejects_non_json_or_wrong_payload(self):
        self.assertFalse(_parse_protocol_output("I cannot comply", "hermes", "protocol-01")["valid"])
        self.assertFalse(_parse_protocol_output('{"protocol_version":"0.1"}', "hermes", "protocol-01")["valid"])

    def test_evidence_requires_ten_cases_per_agent(self):
        evidence = {"mode": "no-prose protocol verification", "hermes": [], "antigravity": []}
        self.assertFalse(validate_agent_protocol_canaries_from_evidence(evidence)["valid"])
        item = {"valid": True}
        evidence["hermes"] = [{"case_id": case_id, **item} for case_id in CASE_IDS]
        evidence["antigravity"] = [{"case_id": case_id, **item} for case_id in CASE_IDS]
        self.assertTrue(validate_agent_protocol_canaries_from_evidence(evidence)["valid"])


if __name__ == "__main__":
    unittest.main()
