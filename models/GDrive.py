from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from google.oauth2 import service_account
import os

CREDENTIALS_FILE_PATH = os.path.join(os.getcwd(), "creds", "gdrive", "credentials.json")
SETTINGS_FILE_PATH = os.path.join(os.getcwd(), "settings.yml")
class GDrive():
    def __init__(self):

        #gauth = GoogleAuth(settings_file=SETTINGS_FILE_PATH)
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(CREDENTIALS_FILE_PATH)

        self.drive = GoogleDrive(gauth)
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
    
    def retrieve(self, id, name):
        file_obj = self.drive.CreateFile({'id': id})
        print(file_obj['title'])
        #file_obj.GetContentFile(f'{name}.png') 
