import os
import requests
import logging

def authenticate():
    """
    Authenticates with the blockchain API to retrieve an access token.
    
    :return: Access token string if successful, None otherwise.
    """
    username = os.getenv("BLOCKCHAIN_API_USERNAME")
    password = os.getenv("BLOCKCHAIN_API_PASSWORD")
    
    if not username or not password:
        logging.error("Blockchain API username or password not set in environment variables.")
        return None

    auth_url = "https://medical-records-blockchain.azurewebsites.net/auth/login"
    auth_payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(auth_url, json=auth_payload)
        
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            if access_token:
                logging.info("Authentication successful. Access token retrieved.")
                return access_token
            else:
                logging.error("Authentication response did not contain an access token.")
                return None
        else:
            logging.error("Authentication failed. Status code: %s", response.status_code)
            return None
    except requests.RequestException as e:
        logging.error("An error occurred during authentication: %s", e)
        return None

def is_blockchain_valid():
    """
    Checks if the blockchain is valid by sending a GET request to the validation endpoint.
    
    :return: True if blockchain is valid, False otherwise.
    """
    access_token = authenticate()
    if not access_token:
        logging.error("Could not retrieve access token. Blockchain validation aborted.")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        validation_url = "https://medical-records-blockchain.azurewebsites.net/blocks/validate"
        response = requests.get(validation_url, headers=headers)
        
        if response.status_code == 200:
            logging.info("Blockchain is valid.")
            return True
        else:
            logging.warning("Blockchain validation failed. Status code: %s", response.status_code)
            return False
    except requests.RequestException as e:
        logging.error("An error occurred while validating the blockchain: %s", e)
        return False
