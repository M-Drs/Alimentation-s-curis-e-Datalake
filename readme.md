# Airbnb Reviews Data Pipeline

This project automates the process of downloading Airbnb reviews datasets, retrieving secrets from Azure Key Vault, and uploading the datasets to Azure Blob Storage. 

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Notes](#notes)
- [License](#license)

## Overview

This script:
1. Scrapes the [Inside Airbnb](https://insideairbnb.com/get-the-data/) website to download `reviews.csv` files.
2. Retrieves secrets securely from Azure Key Vault.
3. Uploads the downloaded files to an Azure Blob Storage container.

## Features

- Scrapes and downloads datasets in `.csv` format from Inside Airbnb.
- Uses Azure Key Vault to securely store and retrieve credentials.
- Uploads files to Azure Blob Storage, maintaining folder structures.

## Requirements

- Python 3.8 or higher
- Azure subscription
- Azure Key Vault and Blob Storage set up
- The following Python libraries:
  - `os`
  - `requests`
  - `beautifulsoup4`
  - `dotenv`
  - `azure.storage.blob`
  - `azure.identity`
  - `azure.keyvault.secrets`

## Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
2. Install Dependencies
Use pip to install required Python libraries:

bash
Copier le code
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the root directory and define the following variables:

env
Copier le code
AZURE_CONNECTION_STRING=<your_azure_connection_string>
CONTAINER_NAME=<your_blob_container_name>
KEY_VAULT_URL=<your_key_vault_url>
secret_secondaire=<your_secondary_secret>
tenant_ID=<your_tenant_id>
client_ID_secondaire=<your_secondary_client_id>
client_ID_principal=<your_primary_client_id>
secret_name=<name_of_the_keyvault_secret>
STORAGE_ACCOUNT_URL=<your_storage_account_url>
4. Create an Output Directory
Ensure the downloads directory exists. This is where downloaded files will be stored.

bash
Copier le code
mkdir downloads
Usage
Run the script using the following command:

bash
Copier le code
python script_name.py
The script will:

Download reviews.csv files from Inside Airbnb.
Retrieve a secret from Azure Key Vault.
Upload the files to Azure Blob Storage.
Environment Variables
Variable Name	Description
AZURE_CONNECTION_STRING	Connection string for Azure Blob Storage.
CONTAINER_NAME	Name of the Azure Blob Storage container.
KEY_VAULT_URL	URL of your Azure Key Vault.
secret_secondaire	Secondary secret for authentication.
tenant_ID	Azure Active Directory tenant ID.
client_ID_secondaire	Secondary client ID for Azure authentication.
client_ID_principal	Primary client ID for Azure authentication.
secret_name	Name of the secret in Azure Key Vault.
STORAGE_ACCOUNT_URL	URL of your Azure Blob Storage account.
Notes
Ensure that your Azure Active Directory roles and permissions are correctly configured to allow access to Azure Key Vault and Blob Storage.
The script automatically creates the downloads directory if it doesn't exist.
Files are uploaded to Blob Storage with their relative paths preserved.
License
This project is licensed under the MIT License. See the LICENSE file for more details.