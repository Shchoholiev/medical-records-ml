import os
import logging
from azure.cosmos import CosmosClient, exceptions

# Configuration
CONNECTION_STRING = os.getenv("medicalrecords_DOCUMENTDB")
DATABASE_NAME = "medical-records"
PATIENTS_CONTAINER_NAME = "patients"
MEDICAL_RECORDS_CONTAINER_NAME = "medical_records"

# Initialize Cosmos DB client and containers
client = CosmosClient.from_connection_string(CONNECTION_STRING)
database = client.get_database_client(DATABASE_NAME)
patients_container = database.get_container_client(PATIENTS_CONTAINER_NAME)
medical_records_container = database.get_container_client(MEDICAL_RECORDS_CONTAINER_NAME)

def get_patient_data(patient_id):
    """
    Fetches patient data from the Cosmos DB patients container.
    
    :param patient_id: The ID of the patient to search for.
    :return: Dictionary containing patient data or None if not found.
    """
    try:
        patient = patients_container.read_item(item=patient_id, partition_key=patient_id)
        return patient
    except exceptions.CosmosResourceNotFoundError:
        logging.error(f"Patient with ID {patient_id} not found.")
        return None

def get_medical_records_by_patient_id(patient_id):
    """
    Queries Cosmos DB for all medical records with the given patient_id.
    
    :param patient_id: The ID of the patient to search for.
    :return: A list of records for the specified patient_id.
    """
    try:
        query = "SELECT * FROM c WHERE c.patient_id = @patient_id"
        parameters = [{"name": "@patient_id", "value": patient_id}]
        
        results = medical_records_container.query_items(
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
