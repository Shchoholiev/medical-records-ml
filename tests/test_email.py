import unittest
import os
import logging
from utils.email import send_email

class IntegrationTestSendEmail(unittest.TestCase):
    
    def test_send_email(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Ensure environment variable for the password is set
        sender_password = os.getenv('GMAIL_PASSWORD')
        self.assertIsNotNone(sender_password, "GMAIL_PASSWORD environment variable is not set.")
        
        # Define test data
        subject = "Integration Test Email Subject"
        body = "This is a test email sent as part of an integration test."
        recipient_email = "serhii.shchoholiev@nure.ua"  # Use a real, safe test email for this

        # Call the send_email function and assert it returns True
        result = send_email(subject, body, recipient_email)
        self.assertTrue(result, "Email should be sent successfully in the integration test.")

# Run tests
if __name__ == '__main__':
    unittest.main()
