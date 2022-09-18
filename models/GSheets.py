import gspread
import os

SERVICE_ACCOUNT_FILE_PATH = os.path.join(os.getcwd(), "creds", "gsheet", "artbook-generator-2-076ef8beb61b.json")
CLIENT_SECRETS_FILE_PATH = os.path.join(os.getcwd(), "creds", "gsheet", "client_secrets.json")

SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive',
]

SUBMISSION_LINK_KEY = "1CUYBPbh3RFzQelq8Qt9e6diPwH__iTUV96AjZN71yQ8"

class GSheet():
    def __init__(self, key=SUBMISSION_LINK_KEY):

        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE_PATH)
        self.spreadsheets = gc.open_by_key(key)
        
    def retrieve(self, id, name):
        file_obj = self.drive.CreateFile({'id': id})
        print(file_obj['title'])
        file_obj.GetContentString()
        print(file_obj)
