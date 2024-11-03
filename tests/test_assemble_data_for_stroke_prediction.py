import unittest

import joblib
from utils.data_processing import assemble_data_for_stroke_prediction
from utils.helpers import calculate_age, calculate_bmi  # Import these directly if they are part of your module

class TestAssembleDataForStrokePrediction(unittest.TestCase):

    def setUp(self):
        # Sample patient data
        self.patient = {
            "id": "7b3e4fc8-74f6-4f08-914f-b151287cbc34",
            "date_of_birth": "1982-10-27T18:24:15.425024+00:00",
            "sex": "Male",
            "ever_married": True,
            "doctor_id": "8b3e4fc8-74f6-4f08-914f-b151287cbc34",
            "user_id": "9b3e4fc8-74f6-4f08-914f-b151287cbc34"
        }

        # Sample medical records data
        self.medical_records = [
            {
                "type": "BloodWork",
                "note": "notes",
                "patient_id": "7b3e4fc8-74f6-4f08-914f-b151287cbc34",
                "glucose_level": 4.2,
                "created_date_utc": "2024-10-27T18:24:15.425024+00:00",
                "created_by_id": "9d00ca02-70d5-49e8-8b20-a6176425c23a",
                "id": "112ed41c-30c6-4ed1-800b-db13a34be49a",
            },
            {
                "type": "BloodPressure",
                "note": "notes",
                "patient_id": "7b3e4fc8-74f6-4f08-914f-b151287cbc34",
                "systolic_pressure": 150,
                "diastolic_pressure": 95,
                "created_date_utc": "2024-10-27T18:24:15.425024+00:00",
                "created_by_id": "9d00ca02-70d5-49e8-8b20-a6176425c23a",
                "id": "212ed41c-30c6-4ed1-800b-db13a34be49a"
            },
            {
                "type": "PhysicalExam",
                "note": "notes",
                "patient_id": "7b3e4fc8-74f6-4f08-914f-b151287cbc34",
                "work_type": "Private",
                "residency_type": "Urban",
                "height": 1.75,
                "weight": 70,
                "smoking_status": "never smoked",
                "created_date_utc": "2024-10-27T18:24:15.425024+00:00",
                "created_by_id": "9d00ca02-70d5-49e8-8b20-a6176425c23a",
                "id": "312ed41c-30c6-4ed1-800b-db13a34be49a",
            },
            {
                "type": "DiseaseHistory",
                "note": "notes",
                "patient_id": "7b3e4fc8-74f6-4f08-914f-b151287cbc34",
                "disease_type": "HeartDisease",
                "created_date_utc": "2024-10-27T18:24:15.425024+00:00",
                "created_by_id": "9d00ca02-70d5-49e8-8b20-a6176425c23a",
                "id": "412ed41c-30c6-4ed1-800b-db13a34be49a"
            }
        ]

        self.preprocessor = joblib.load("preprocessor.joblib")

    def test_assemble_data_complete(self):
        """
        Test assembling data with all fields provided.
        """
        # Act
        result = assemble_data_for_stroke_prediction(self.patient, self.medical_records)

        # Assert
        self.assertEqual(result["gender"], "Male")
        self.assertEqual(result["age"], calculate_age(self.patient["date_of_birth"]))
        self.assertEqual(result["ever_married"], "Yes")
        self.assertEqual(result["hypertension"], 1)
        self.assertIsInstance(result["hypertension"], int)
        self.assertEqual(result["heart_disease"], 1)
        self.assertIsInstance(result["heart_disease"], int)
        self.assertEqual(result["work_type"], "Private")
        self.assertEqual(result["Residence_type"], "Urban")
        self.assertEqual(result["avg_glucose_level"], 4.2)
        self.assertEqual(result["bmi"], calculate_bmi(70, 1.75))
        self.assertEqual(result["smoking_status"], "never smoked")

    def test_assemble_data_no_hypertension(self):
        """
        Test that hypertension is set to 0 when blood pressure is normal.
        """
        # Normal blood pressure record
        normal_bp_records = [
            {"type": "BloodPressure", "systolic_pressure": 120, "diastolic_pressure": 80}
        ]

        # Act
        result = assemble_data_for_stroke_prediction(self.patient, normal_bp_records)

        # Assert
        self.assertEqual(result["hypertension"], 0)
        self.assertIsInstance(result["hypertension"], int)

if __name__ == '__main__':
    unittest.main()
