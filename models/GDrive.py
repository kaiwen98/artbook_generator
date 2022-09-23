from commons.constants import ASSET_OUT_PATH
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from google.oauth2 import service_account
import os

CREDENTIALS_FILE_PATH = os.path.join(os.getcwd(), "creds", "gdrive", "credentials.json")
SETTINGS_FILE_PATH = os.path.join(os.getcwd(), "settings.yml")
class GDrive():
    def __init__(self):

        gauth = GoogleAuth(settings_file=SETTINGS_FILE_PATH)
        #gauth = GoogleAuth()
        gauth.LoadCredentialsFile(CREDENTIALS_FILE_PATH)

        self.drive = GoogleDrive(gauth)
    
    def retrieve(self, id):
        fileObj = self.drive.CreateFile({'id': id})
        print(fileObj['title'])
        filename = fileObj['title']
        print(f"MEME TYPE: {fileObj['mimeType']}")

        # Parsing pdf from application/pdf
        fileExt = fileObj['mimeType'].split('/')[1]

        # Check if uploaded with ext in name
        ext = os.path.splitext(filename)[-1].lower()

        if '.' not in ext:
            filename += f".{fileExt}"
            
        # if not os.path.exists(os.path.join(ASSET_OUT_PATH, "images", f"{filename}")):
        fileObj.GetContentFile(os.path.join(ASSET_OUT_PATH, "images", f"{filename}"))
        return os.path.join(ASSET_OUT_PATH, "images", f"{filename}")
            # print(file_obj)
