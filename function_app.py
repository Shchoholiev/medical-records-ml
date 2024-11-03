import logging
import azure.functions as func
import joblib
import pandas as pd
from utils.blockchain import is_blockchain_valid
from utils.cosmos_db import get_patient_data, get_medical_records_by_patient_id
from utils.data_processing import assemble_data_for_stroke_prediction
from utils.helpers import check_required_records_for_stroke
from utils.notifications import notify_patient_and_doctor

# Initialize Function App
app = func.FunctionApp()

stroke_model = joblib.load("random_forest_model.joblib")
preprocessor = joblib.load("preprocessor.joblib")

@app.cosmos_db_trigger(
    arg_name="azcosmosdb",
    container_name="medical_records",
    database_name="medical-records",
    connection="medicalrecords_DOCUMENTDB",
    lease_container_name="medical_records_lease",
    lease_database_name="lease",
    create_lease_container_if_not_exists=True
)
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
        if not is_blockchain_valid():
            logging.warning("Blockchain is invalid. Prediction will not be made.")
            return

        logging.info(f"Assembled data for stroke prediction")

        data_df = pd.DataFrame([medical_data])
        preprocessed_data = preprocessor.transform(data_df)

        logging.info(f"Preprocessed data for stroke prediction")
        
        result = stroke_model.predict(preprocessed_data)
        logging.info(f"Stroke prediction for patient_id {patient_id}: {result[0]}")

        if result[0]:
            logging.info("Patient is in the risk of stroke")
            notify_patient_and_doctor(patient, "Stroke")
        else:
            logging.info("Patient doesn't have the risk of stroke")
            
