import os
import unittest

from growth_engine import mom_growth, is_flagged, validate_feed


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(BASE_DIR, "fixtures")


class TestGrowthEngine(unittest.TestCase):

    def test_may_ethnic_wear_flagged(self):
        # GIVEN April -> May Ethnic Wear revenue
        previous = 104520.77
        current = 185107.61

        # WHEN growth and flag status are calculated
        growth = mom_growth(previous, current)
        status = is_flagged(growth)

        # THEN
        self.assertEqual(growth, 77.1)
        self.assertEqual(status, "flagged")

    def test_june_beauty_not_flagged(self):
        # GIVEN May -> June Beauty & Personal Care revenue
        previous = 35542.11
        current = 37559.07

        # WHEN
        growth = mom_growth(previous, current)
        status = is_flagged(growth)

        # THEN
        self.assertEqual(growth, 5.67)
        self.assertEqual(status, "not_flagged")

    def test_exact_boundary_escalates(self):
        # GIVEN an exact 8% increase
        previous = 100000
        current = 108000

        # WHEN
        growth = mom_growth(previous, current)
        status = is_flagged(growth)

        # THEN
        self.assertEqual(growth, 8.0)
        self.assertEqual(status, "escalate_exact_boundary")

    def test_corrupted_feed_validation(self):
        # GIVEN the corrupted fixture
        fixture = os.path.join(FIXTURES_DIR, "corrupted_feed.csv")

        # WHEN
        valid, errors = validate_feed(fixture)

        # THEN
        expected_errors = [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)",
        ]

        self.assertFalse(valid)
        self.assertEqual(errors, expected_errors)


if __name__ == "__main__":
    unittest.main()
