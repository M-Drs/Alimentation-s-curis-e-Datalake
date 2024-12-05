import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Base URL for the Inside Airbnb website
BASE_URL = "https://insideairbnb.com/get-the-data/"
# Directory to save the downloaded CSV files
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

load_dotenv()
 # Azure Storage Account details   
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING") 
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
# Azure Key Vault URL
KEY_VAULT_URL = os.getenv("KEY_VAULT_URL")
secret_secondaire = os.getenv("secret_secondaire")
tenant_ID = os.getenv("tenant_ID")
client_ID_secondaire =os.getenv("client_ID_secondaire")
client_ID_principal = os.getenv("client_ID_principal")
secret_name = os.getenv("secret_name")
STORAGE_ACCOUNT_URL = os.getenv("STORAGE_ACCOUNT_URL")

def get_secret(secret_name):
    """Retrieve a secret from Azure Key Vault."""
    try:
        # Authenticate using DefaultAzureCredential
        credential = ClientSecretCredential(tenant_ID,client_ID_secondaire,secret_secondaire)
        
        # Connect to the Key Vault
        client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
        
        # Get the secret
        retrieved_secret = client.get_secret(secret_name)
        print(f"Secret '{secret_name}' value: {retrieved_secret.value}")
        return retrieved_secret.value
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None
    
def upload_to_azure():
    secure_credential = ClientSecretCredential(tenant_ID, client_ID_principal, secret_value)
    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=secure_credential)

    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    """Upload a file to Azure Blob Storage."""
    for root, _, files in os.walk(OUTPUT_DIR):
     for file in files:
        local_file_path = os.path.join(root, file)
        blob_name = os.path.relpath(local_file_path, OUTPUT_DIR)  # Maintain folder structure
        print(f"Uploading {local_file_path} as {blob_name}...")
        with open(local_file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)

def download_reviews_csv():
    try:
        # Fetch the webpage
        print(f"Fetching data from {BASE_URL}...")
        response = requests.get(BASE_URL)
        response.encoding = "utf-8"
        response.raise_for_status()  # Raise an error for bad HTTP status
        
        # Parse the webpage
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        # Filter and download reviews.csv files
        for link in links:
            if "reviews.csv" in link["href"] and not link["href"].endswith(".gz") : 
                
                file_url = link["href"]
                file_name = file_url.split("/")[-6] +'_'+ file_url.split("/")[-4] +'_'+ file_url.split("/")[-1]
                output_path = os.path.join(OUTPUT_DIR, file_name   )

                print(f"Downloading {file_name} from {file_url}...")
                
                file_response = requests.get(file_url)
                
                file_response.raise_for_status()  # Ensure successful download

                # Save the file locally
                with open(output_path, "wb") as file:
                    file.write(file_response.content)
                print(f"Saved: {output_path}")

        print("All reviews.csv files downloaded successfully.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    download_reviews_csv()
    secret_value = get_secret(secret_name)
    upload_to_azure()



