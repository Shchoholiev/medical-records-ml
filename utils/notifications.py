import logging

from utils.cosmos_db import add_health_notification, get_user_by_user_id
from utils.email import send_email


def notify_patient_and_doctor(patient, disease):
    patient_id = patient.get("user_id")
    doctor_id = patient.get("doctor_id")

    if not patient_id or not doctor_id:
        logging.error("Patient ID or Doctor ID is missing.")
        return False

    patient_user = get_user_by_user_id(patient_id)
    doctor_user = get_user_by_user_id(doctor_id)

    if not patient_user or not doctor_user:
        logging.error("Could not retrieve patient or doctor user information.")
        return False

    patient_email = patient_user.get("email")
    doctor_email = doctor_user.get("email")

    if not patient_email or not doctor_email:
        logging.error("Patient or doctor email is missing.")
        return False

    subject = f"Health Notification: {disease} Alert"
    body = f"Dear {patient_user.get('name')},\n\nOur records indicate a risk for {disease}. Please consult your doctor for further evaluation.\n\nBest regards,\nHealthcare Team"

    patient_email_sent = send_email(subject, body, patient_email)
    doctor_email_sent = send_email(subject, f"Patient {patient_user.get('name')} may have {disease}. Please review their medical records.", doctor_email)

    if patient_email_sent and doctor_email_sent:
        notification = add_health_notification(
            title=f"{disease} Alert",
            text=f"Notification for potential {disease} risk sent to patient and doctor.",
            disease=disease,
            patient_id=patient_id
        )
        if notification:
            logging.info("Health notification created and emails sent successfully.")
            return True
        else:
            logging.error("Failed to create health notification.")
            return False
    else:
        logging.error("Failed to send email to either patient or doctor.")
        return False