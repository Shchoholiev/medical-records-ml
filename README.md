# medical-records-ml
Machine Learning model for stroke prediction integrated with a blockchain-based system that securely stores medical records. The solution includes automated alerts to patients and medical personnel for potential stroke risks, enhancing early detection and timely intervention.

## Table of Contents
- [Features](#features)
- [Stack](#stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)

## Features
- Machine learning model for predicting stroke risk using patient medical data.
- Integration with blockchain to ensure secure and tamper-proof storage of medical records.
- Automated triggering of stroke risk prediction upon new medical record entry.
- Alerts and notifications sent via email to both patients and their doctors for timely intervention.
- Uses Azure Cosmos DB as the backend database for storing medical and patient data.
- Docker and Dev Container support for consistent development environments.
- Unit and integration tests for key components including blockchain validation and notification services.

## Stack
- Python 3.11
- Jupyter Notebook for model training and experimentation
- Azure Functions (serverless compute platform)
- Azure Cosmos DB (NoSQL cloud database)
- Blockchain API for record validation and security
- Docker for containerization and environment management
- Email notification via Gmail SMTP service

## Installation

### Prerequisites
- Python 3.11 installed locally
- Docker installed (for containerized development)
- Azure account with Cosmos DB provisioned
- Gmail account with app password for sending notifications

### Setup Instructions

Clone the repository:
```bash
git clone https://github.com/Shchoholiev/medical-records-ml.git
cd medical-records-ml
```

Create and activate a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install required Python packages:
```bash
pip install -r requirements.txt
```

For development container setup (optional), use VSCode with the included `.devcontainer` configuration or build the provided Dockerfile as needed.

Run unit and integration tests to verify setup:
```bash
python -m unittest discover tests
```

Deploy or run the Azure Function app locally:
```bash
func start
```

## Configuration

Set the following environment variables before running or deploying the app:

- **medicalrecords_DOCUMENTDB**: Azure Cosmos DB connection string.
- **BLOCKCHAIN_API_USERNAME**: Username for blockchain API authentication.
- **BLOCKCHAIN_API_PASSWORD**: Password for blockchain API authentication.
- **GMAIL_PASSWORD**: App password for the Gmail account used to send email notifications.

Example on Unix-like systems:
```bash
export medicalrecords_DOCUMENTDB="your_cosmos_connection_string"
export BLOCKCHAIN_API_USERNAME="your_blockchain_username"
export BLOCKCHAIN_API_PASSWORD="your_blockchain_password"
export GMAIL_PASSWORD="your_gmail_app_password"
```

Make sure your Azure Cosmos DB has the following containers initialized:
- `patients`
- `medical_records`
- `users`
- `health_notifications`

Emails will be sent from the fixed sender: `assets.manager.code@gmail.com`. Use an app-specific password for Gmail (`GMAIL_PASSWORD`) and ensure less secure apps or app password settings are properly configured for sending emails.
