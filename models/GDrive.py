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
    
    def retrieve(self, id, name):
        file_obj = self.drive.CreateFile({'id': id})
        print(file_obj['title'])
        file_obj.GetContentString()
        print(file_obj)
