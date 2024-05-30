import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your service account credentials file
CREDENTIALS_FILE = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/uab-study-1c3d68af355c.json'

def authenticate_drive():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, 
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

def create_folder(service, folder_name, parent_folder_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
    return folder.get('id')

def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Upload Successful: {file_name}, File ID: {file.get('id')}")
    return file.get('id')

def upload_folder(service, folder_path, parent_folder_id=None):
    folder_name = os.path.basename(folder_path)
    folder_id = create_folder(service, folder_name, parent_folder_id)

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            upload_file(service, file_path, folder_id)
    return folder_id