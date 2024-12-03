import os
import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient


# Base URL for the Inside Airbnb website
BASE_URL = "https://insideairbnb.com/get-the-data/"

# Directory to save the downloaded CSV files
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Azure Storage Account details
AZURE_CONNECTION_STRING = ""
CONTAINER_NAME = "boitemagique"
def upload_to_azure(file_path, blob_name):
    """Upload a file to Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"Uploaded {file_path} to Azure Blob Storage as {blob_name}.")
    except Exception as e:
        print(f"Failed to upload {file_path} to Azure Blob Storage: {e}")


def download_reviews_csv():
    try:
        # Fetch the webpage
        print(f"Fetching data from {BASE_URL}...")
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise an error for bad HTTP status
        
        # Parse the webpage
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        # Filter and download reviews.csv files
        for link in links:
            if "reviews.csv" in link["href"] and not link["href"].endswith(".gz"):
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

                # Upload the file to Azure Storage
                upload_to_azure(output_path, file_name)

        print("All reviews.csv files downloaded successfully.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_reviews_csv()



#   file_url.split("/")[-1]