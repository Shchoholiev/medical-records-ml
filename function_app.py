import datetime
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import logging
import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

app = func.FunctionApp()

CONNECTION_STRING = os.getenv("medicalrecords_DOCUMENTDB")
DATABASE_NAME = "medical-records"
CONTAINER_NAME = "medical_records"

client = CosmosClient.from_connection_string(CONNECTION_STRING)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)
patients_container = database.get_container_client("patients")

stroke_model = joblib.load("random_forest_model.joblib")

@app.cosmos_db_trigger(
    arg_name="azcosmosdb", 
    container_name=CONTAINER_NAME,
    database_name=DATABASE_NAME, 
    connection="medicalrecords_DOCUMENTDB",
    lease_container_name="medical_records_lease",
    lease_database_name="lease",
    create_lease_container_if_not_exists=True)  
def new_medical_record_trigger(azcosmosdb: func.DocumentList):
    logging.info('Python Cosmos DB trigger processed a batch of documents.')
    
    for doc in azcosmosdb:
        patient_id = doc.get("patient_id")
        logging.info(f"Processing document for patient_id: {patient_id}")
        
        if not patient_id:
            return
        
        patient = get_patient_data(patient_id)
        
        medical_records = get_medical_records_by_patient_id(patient_id)
        if not check_required_records_for_stroke(medical_records):
            logging.warning(f"One or more required records for stroke prediction are missing for patient_id: {patient_id}")
            return
        
        logging.info(f"All required records for stroke prediction are present for patient_id: {patient_id}")

        medical_data = assemble_data_for_stroke_prediction(patient, medical_records)
        preprocessed_data = preprocess_data_for_stroke_model(medical_data)
        result = stroke_model.predict(preprocessed_data)

        logging.info(f"Stroke prediction for patient_id {patient_id}: {result[0]}")
        

def get_medical_records_by_patient_id(patient_id):
    """
    Queries Cosmos DB for all medical records with the given patient_id.
    
    :param patient_id: The ID of the patient to search for.
    :return: A list of records for the specified patient_id.
    """
    try:
        query = "SELECT * FROM c WHERE c.patient_id = @patient_id"
        parameters = [{"name": "@patient_id", "value": patient_id}]
        
        results = container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        )
        
        records = list(results)
        logging.info(f"Found {len(records)} records for patient_id {patient_id}")
        return records

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error querying Cosmos DB for patient_id {patient_id}: {e}")
        return []

def get_patient_data(patient_id):
    """
    Fetches patient data from the Cosmos DB patients container.
    """
    try:
        patient = patients_container.read_item(item=patient_id, partition_key=patient_id)
        return patient
    except exceptions.CosmosResourceNotFoundError:
        logging.error(f"Patient with ID {patient_id} not found.")
        return None
    
def check_required_records_for_stroke(records):
    """
    Checks if the required medical record types are present in the patient's records.
    
    :param records: List of medical records for a patient.
    :return: Boolean indicating if all required types are present.
    """
    required_types = {"BloodPressure", "BloodWork", "DiseaseHistory", "PhysicalExam"}
    found_types = {record.get("type") for record in records if record.get("type")}

    missing_types = required_types - found_types
    if missing_types:
        logging.info(f"Missing required records: {missing_types}")
        return False
    return True

def calculate_age(dob):
    """
    Calculates age from date of birth.
    """
    if not dob:
        return None
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_bmi(weight, height,):
    """
    Calculates BMI.
    """
    if not weight or not height:
        return None
    height_in_meters = height / 100  # assuming height is in cm
    bmi = weight / (height_in_meters ** 2)
    return bmi

def assemble_data_for_stroke_prediction(patient, medical_records):
    medical_data = {record['type']: record for record in medical_records}

    # Assemble model data
    model_data = {
        "gender": patient.get("sex"),
        "age": calculate_age(patient.get("date_of_birth")),
        "ever_married": patient.get("ever_married"),
        "hypertension": None,
        "heart_disease": None,
        "work_type": None,
        "Residence_type": None,
        "avg_glucose_level": None,
        "bmi": None,
        "smoking_status": None
    }

    # Hypertension calculation
    bp_record = medical_data["BloodPressure"]
    systolic = bp_record.get("systolic_pressure")
    diastolic = bp_record.get("diastolic_pressure")
    if systolic and diastolic:
        model_data["hypertension"] = (systolic >= 140 or diastolic >= 90)

    # Heart disease
    disease_history = medical_data["DiseaseHistory"]
    if disease_history.get("disease_type") == "HeartDisease":
        model_data["heart_disease"] = True

    # Physical Exam data
    physical_exam = medical_data["PhysicalExam"]
    model_data["work_type"] = physical_exam.get("work_type")
    model_data["Residence_type"] = physical_exam.get("residency_type")
    model_data["smoking_status"] = physical_exam.get("smoking_status")
    
    weight = physical_exam.get("weight")
    height = physical_exam.get("height")
    model_data["bmi"] = calculate_bmi(weight, height, model_data["gender"])

    # Blood Work
    blood_work = medical_data["BloodWork"]
    model_data["avg_glucose_level"] = blood_work.get("glucose_level")

    return model_data

def preprocess_data_for_stroke_model(prepared_data):
    """
    Preprocesses data for the model using the same pipeline as training.

    :param prepared_data: Dictionary with data fields prepared for model input
    :return: Preprocessed data ready for model prediction
    """
    data_df = pd.DataFrame([prepared_data])

    # Define numeric and categorical features
    numeric_features = ['age', 'avg_glucose_level', 'bmi']
    categorical_features = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']

    # Define preprocessing steps for numeric features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Fill NaNs in numeric columns with mean
        ('scaler', StandardScaler())
    ])

    # Define preprocessing steps for categorical features
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill NaNs in categorical columns with most frequent value
        ('encoder', OneHotEncoder())
    ])

    # Combine transformations
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Apply preprocessing to the input data
    X_preprocessed = preprocessor.fit_transform(data_df)

    return X_preprocessed