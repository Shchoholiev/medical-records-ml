import datetime
import unittest
from utils.helpers import calculate_age, calculate_bmi, check_required_records_for_stroke

class TestCalculateAge(unittest.TestCase):
    def test_calculate_age_valid_date(self):
        # Test for a valid date of birth
        self.assertEqual(calculate_age("1990-01-01T18:24:15.425024+00:00"), datetime.datetime.today().year - 1990)

    def test_calculate_age_none(self):
        # Test for None as input
        self.assertIsNone(calculate_age(None))


class TestCalculateBMI(unittest.TestCase):
    def test_calculate_bmi_valid_values(self):
        # Test for valid weight and height
        self.assertAlmostEqual(calculate_bmi(70, 175), 22.86, places=2)

    def test_calculate_bmi_zero_height(self):
        # Test for zero height (should return None or handle division by zero)
        self.assertIsNone(calculate_bmi(70, 0))

    def test_calculate_bmi_none_values(self):
        # Test for None as input
        self.assertIsNone(calculate_bmi(None, 175))
        self.assertIsNone(calculate_bmi(70, None))
        self.assertIsNone(calculate_bmi(None, None))


class TestCheckRequiredRecordsForStroke(unittest.TestCase):
    def test_check_required_records_all_present(self):
        # Test with all required records present
        records = [
            {"type": "BloodPressure"},
            {"type": "BloodWork"},
            {"type": "DiseaseHistory"},
            {"type": "PhysicalExam"}
        ]
        self.assertTrue(check_required_records_for_stroke(records))

    def test_check_required_records_missing_some(self):
        # Test with some records missing
        records = [
            {"type": "BloodPressure"},
            {"type": "BloodWork"}
        ]
        self.assertFalse(check_required_records_for_stroke(records))

    def test_check_required_records_empty_list(self):
        # Test with an empty list of records
        self.assertFalse(check_required_records_for_stroke([]))

    def test_check_required_records_with_unrelated_types(self):
        # Test with unrelated record types
        records = [
            {"type": "BloodPressure"},
            {"type": "BloodWork"},
            {"type": "UnrelatedRecord"}
        ]
        self.assertFalse(check_required_records_for_stroke(records))

if __name__ == '__main__':
    unittest.main()
