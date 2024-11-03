from utils.helpers import calculate_age, calculate_bmi

def assemble_data_for_stroke_prediction(patient, medical_records):
    """
    Assembles the data required for stroke prediction based on patient and medical records.

    :param patient: Dictionary containing patient information.
    :param medical_records: List of dictionaries containing patient's medical records.
    :return: Dictionary with compiled data for prediction.
    """
    # Organize records by type
    medical_data = {record['type']: record for record in medical_records}

    # Assemble model data
    model_data = {
        "gender": patient.get("sex"),
        "age": calculate_age(patient.get("date_of_birth")),
        "ever_married": 'Yes' if patient.get("ever_married") else 'No',
        "hypertension": None,
        "heart_disease": None,
        "work_type": None,
        "Residence_type": None,
        "avg_glucose_level": None,
        "bmi": None,
        "smoking_status": None
    }

    # Process Blood Pressure and Hypertension
    bp_record = medical_data.get("BloodPressure", {})
    systolic = bp_record.get("systolic_pressure")
    diastolic = bp_record.get("diastolic_pressure")
    if systolic and diastolic:
        model_data["hypertension"] = 1 if (systolic >= 140 or diastolic >= 90) else 0

    # Process Disease History for Heart Disease
    disease_history = medical_data.get("DiseaseHistory", {})
    model_data["heart_disease"] = 1 if disease_history.get("disease_type") == "HeartDisease" else 0

    # Process Physical Exam data
    physical_exam = medical_data.get("PhysicalExam", {})
    model_data["work_type"] = physical_exam.get("work_type")
    model_data["Residence_type"] = physical_exam.get("residency_type")
    model_data["smoking_status"] = physical_exam.get("smoking_status")
    
    weight = physical_exam.get("weight")
    height = physical_exam.get("height")
    model_data["bmi"] = calculate_bmi(weight, height)

    # Process Blood Work
    blood_work = medical_data.get("BloodWork", {})
    model_data["avg_glucose_level"] = blood_work.get("glucose_level")

    return model_data