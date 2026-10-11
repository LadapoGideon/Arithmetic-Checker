import unittest

from arithmetic_check import check_arithmetic, safe_eval, wrong_claims


class ArithmeticTests(unittest.TestCase):
    def test_safe_eval_respects_precedence(self):
        self.assertEqual(safe_eval("2 + 3 * 4"), 14)
        self.assertEqual(safe_eval("(2 + 3) * 4"), 20)

    def test_safe_eval_rejects_names_and_calls(self):
        with self.assertRaises(ValueError):
            safe_eval("__import__('os')")

    def test_correct_claims_pass(self):
        findings = check_arithmetic("So 2 + 2 = 4 and 3 * 3 = 9.")
        self.assertEqual([f["correct"] for f in findings], [True, True])

    def test_wrong_claim_is_reported(self):
        wrong = wrong_claims("The total is 12 * 4 = 50.")
        self.assertEqual(len(wrong), 1)
        self.assertEqual(wrong[0]["actual"], 48)

    def test_division_by_zero_is_marked_not_crashed(self):
        findings = check_arithmetic("Then 10 / 0 = 5.")
        self.assertIsNone(findings[0]["correct"])
        self.assertIn("division", findings[0]["error"])

    def test_decimal_claims(self):
        findings = check_arithmetic("Half of 5 is 2.5 so 5 / 2 = 2.5")
        self.assertTrue(findings[0]["correct"])


if __name__ == "__main__":
    unittest.main()
