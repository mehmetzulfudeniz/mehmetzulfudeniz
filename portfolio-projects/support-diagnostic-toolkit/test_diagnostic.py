import unittest

from diagnostic import DiagnosticResult, normalize_host


class DiagnosticToolkitTests(unittest.TestCase):
    def test_normalize_plain_host(self):
        self.assertEqual(normalize_host("example.com"), "example.com")

    def test_normalize_url(self):
        self.assertEqual(normalize_host("https://example.com/path"), "example.com")

    def test_result_serialization(self):
        result = DiagnosticResult(check="dns", target="example.com", ok=True)
        payload = result.to_dict()
        self.assertEqual(payload["check"], "dns")
        self.assertTrue(payload["ok"])


if __name__ == "__main__":
    unittest.main()
