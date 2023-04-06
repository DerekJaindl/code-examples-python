import requests
import json
import os
import zipfile
import shutil
from datetime import datetime

API_KEY = "731b7858-fd51-4db6-a1c1-a5c645c117a1"
ACCOUNT_ID = "35951c14-a12d-472e-a085-bc156a0c4ca9"
BASE_URL = f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}"
ACCESS_TOKEN = "eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAQxw1DzLbSAgAAKvglhcy20gCAAVqJLLzmXxLkPzZBzRX_4oVAAEAAAAYAAIAAAAdAAAABQAAAA0AJAAAADFhYzc3NWNhLTc1YzQtNDFhOS1iZTAxLTMzNTRiZjQ2ZDQwYiIAJAAAADFhYzc3NWNhLTc1YzQtNDFhOS1iZTAxLTMzNTRiZjQ2ZDQwYhIAAQAAAAYAAABqd3RfYnIjACQAAAAxYWM3NzVjYS03NWM0LTQxYTktYmUwMS0zMzU0YmY0NmQ0MGI.3IKqsKXSg8OPAb7eZyWhwp9V3GkitTJVlHcX-tMuaxNwG0GB30CaisDsH5SXO2K4lcRFjEYWW8-g7qqWqtk30M7XMjsX5Aoc2Sep58Ix4KTUFaKgkF1BMcPmu6jFVyYZuH86_hOftckvVIricQPOcIrFmx3eKYtAKhA1-II9bCKnYSPo6dCyTwtE05TV1TJa_5vWdhHOfUcWWL8QW_zpI13w0rg902cY7aSUlRVqvdunu7yHfXj0W5pxWVWNeavhi1SpAzSj76bJd70r7kXev19mj1EsRrimCQKD0kPmvL8NpAm7_XIl_J5XgMXP73rNSdhxUEvLsTrhns_g4a6uNA"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))
def delete_folder_contents(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# Functions from the previous combined script
def get_envelope_list_status_changes(from_date, to_date, status_list):
    url = f"{BASE_URL}/envelopes"
    querystring = {
        "from_date": from_date,
        "to_date": to_date,
        "status": ",".join(status_list)
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def get_envelope(envelope_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}"
    response = requests.get(url, headers=headers)
    return response.json()

def export_envelope_data_to_file(envelope_details, file_name):
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(envelope_details, outfile, indent=2, ensure_ascii=False)

def log_download(status, file_name, log_file="download_logs.txt"):
    with open(log_file, "a", encoding="utf-8") as f:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {status} - {file_name}\n"
        f.write(log_entry)

def download_combined_documents(envelope_id, sender_username):
    url = f"{BASE_URL}/envelopes/{envelope_id}/documents/combined"
    querystring = {
        "certificate": "true",
        "include_metadata": "true"
    }

    response = requests.get(url, headers=headers, params=querystring)

    download_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{sender_username}_Combined_{envelope_id}_{download_date}.pdf"
    folder_path = f"{sender_username}_documents"

    create_folder_if_not_exists(folder_path)  # Create the sender folder if it doesn't exist

    if response.status_code == 200:
        with open(os.path.join(folder_path, file_name), "wb") as f:
            f.write(response.content)
        print(f"Successfully downloaded combined documents for envelope ID: {envelope_id}")
        log_download("Success", file_name)
    else:
        print(f"Failed to download combined documents for envelope ID: {envelope_id}, status code: {response.status_code}")
        log_download("Failed", file_name)

# New functions for getting recipients and exporting to a JSON file
def get_envelope_recipients(envelope_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}/recipients"
    response = requests.get(url, headers=headers)
    return response.json()

def export_recipients_data_to_file(recipients_data, file_name):
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(recipients_data, outfile, indent=2, ensure_ascii=False)

# New functions for getting envelope documents and exporting to a JSON file
def get_envelope_documents(envelope_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}/documents"
    response = requests.get(url, headers=headers)
    return response.json()

def export_documents_data_to_file(documents_data, file_name):
    with open(file_name, "w", encoding="utf-8") as outfile:
        json.dump(documents_data, outfile, indent=2, ensure_ascii=False)

# Main part of the combined script
from_date = "2023-03-10"
to_date = "2023-03-12"
status_list = ["completed"]

envelopes_data = get_envelope_list_status_changes(from_date, to_date, status_list)

# Check if "envelopes" key is present in envelopes_data
if "envelopes" not in envelopes_data:
    print("Error: 'envelopes' key is missing in envelopes_data. Please check the API response.")
    exit()

envelope_ids = [envelope['envelopeId'] for envelope in envelopes_data['envelopes']]

envelope_details = []
for envelope_id in envelope_ids:
    envelope_detail = get_envelope(envelope_id)
    envelope_details.append(envelope_detail)

## Export the full set of data for each envelope to a JSON file
export_envelope_data_to_file(envelope_details, "envelope_details.json")

# Load envelope details from the JSON file
with open("envelope_details.json", "r", encoding="utf-8") as f:
    envelope_details = json.load(f)

# Download combined documents and certificate of completion for each envelope ID
for detail in envelope_details:
    envelope_id = detail["envelopeId"]
    sender_username = detail["sender"]["userName"].replace(" ", "_")  # Replace spaces with underscores
    download_combined_documents(envelope_id, sender_username)

sender_folders = set([detail["sender"]["userName"].replace(" ", "_") for detail in envelope_details])

for sender_folder in sender_folders:
    zip_folder(sender_folder + "_documents", sender_folder + "_documents.zip")

for sender_folder in sender_folders:
    folder_path = sender_folder + "_documents"
    zip_folder(folder_path, sender_folder + "_documents.zip")
    delete_folder_contents(folder_path)
    os.rmdir(folder_path)

# Load envelope details from the JSON file
with open("envelope_details.json", "r", encoding="utf-8") as f:
    envelope_details = json.load(f)

recipients_data = {}
for detail in envelope_details:
    envelope_id = detail["envelopeId"]
    recipients = get_envelope_recipients(envelope_id)
    recipients_data[envelope_id] = recipients

# Export the recipients data to a JSON file
export_recipients_data_to_file(recipients_data, "envelope_recipients.json")

# Load envelope details from the JSON file
with open("envelope_details.json", "r", encoding="utf-8") as f:
    envelope_details = json.load(f)

documents_data = {}
for detail in envelope_details:
    envelope_id = detail["envelopeId"]
    documents = get_envelope_documents(envelope_id)
    documents_data[envelope_id] = documents

# Export the documents data to a JSON file
export_documents_data_to_file(documents_data, "envelope_documents.json")
