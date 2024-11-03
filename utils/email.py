import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

def send_email(subject, body, recipient_email):
    try:
        sender_email = 'assets.manager.code@gmail.com'
        sender_password = os.getenv('GMAIL_PASSWORD')
        if not sender_password:
            logging.error("Sender password not found in environment variables.")
            return False

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)  # Login to the Gmail account
            server.sendmail(sender_email, recipient_email, message.as_string())
            
        logging.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
