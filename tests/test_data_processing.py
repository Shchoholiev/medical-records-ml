import unittest
import joblib
import pandas as pd

class TestPreprocessDataForStrokeModel(unittest.TestCase):

    def setUp(self):
        # Sample input data simulating a preprocessed patient record
        self.sample_data = {
            'age': 55,
            'avg_glucose_level': 105.5,
            'bmi': 26.7,
            'gender': 'Male',
            'ever_married': 'Yes',
            'work_type': 'Private',
            'Residence_type': 'Urban',
            'smoking_status': 'never smoked',
            'hypertension': 1,
            'heart_disease': 1
        }

        self.model = joblib.load("random_forest_model.joblib")
        self.preprocessor = joblib.load("preprocessor.joblib")

    def test_output_shape(self):
        """
        Test that the output has the correct shape, given one row of input.
        """
        data_df = pd.DataFrame([self.sample_data])
        X_preprocessed = self.preprocessor.transform(data_df)

        self.assertEqual(X_preprocessed.shape[0], 1, "Output should have one row for a single input")
        expected_feature_count = 3 + 5  # 3 numeric, 5 encoded categories (assuming basic setup)
        self.assertGreaterEqual(X_preprocessed.shape[1], expected_feature_count, "Unexpected number of features")

    def test_model_prediction(self):
        """
        Test that the model produces a valid prediction after preprocessing.
        """
        data_df = pd.DataFrame([self.sample_data])
        X_preprocessed = self.preprocessor.transform(data_df)
        prediction = self.model.predict(X_preprocessed)
        
        self.assertEqual(prediction.shape, (1,), "Model should return a single prediction for one input")
        self.assertIn(prediction[0], [0, 1], "Prediction should be binary (e.g., 0 for no stroke, 1 for stroke)")

if __name__ == '__main__':
    unittest.main()
