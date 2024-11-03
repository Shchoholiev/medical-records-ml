import datetime
import logging

def calculate_age(dob):
    """
    Calculates age from date of birth.
    
    :param dob: Date of birth as a string in "YYYY-MM-DDTHH:MM:SS.ssssss+ZZ:ZZ" format.
    :return: Age in years.
    """
    if not dob:
        return None
    # Adjusted format to match the timestamp
    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%dT%H:%M:%S.%f%z")
    today = datetime.datetime.now(datetime.timezone.utc)
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_bmi(weight, height):
    """
    Calculates Body Mass Index (BMI).
    
    :param weight: Weight in kilograms.
    :param height: Height in centimeters.
    :return: BMI as a float.
    """
    if not weight or not height:
        return None
    height_in_meters = height / 100  # Assuming height is in cm
    bmi = weight / (height_in_meters ** 2)
    return bmi

def check_required_records_for_stroke(records):
    """
    Checks if all required medical record types are present for stroke prediction.
    
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
