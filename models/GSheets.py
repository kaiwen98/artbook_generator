from commons.constants import GSHEET_REGISTRATION_COL, GSHEET_SUBMISSION_COL
import gspread
import os
import pandas as pd
import numpy as np

SERVICE_ACCOUNT_FILE_PATH = os.path.join(os.getcwd(), "creds", "gsheet", "artbook-generator-2-076ef8beb61b.json")
CLIENT_SECRETS_FILE_PATH = os.path.join(os.getcwd(), "creds", "gsheet", "client_secrets.json")

SCOPES = [
'https://spreadsheets.google.com/feeds'
]

# Production ID
# SUBMISSION_LINK_KEY = "1CUYBPbh3RFzQelq8Qt9e6diPwH__iTUV96AjZN71yQ8"

# Development ID
SUBMISSION_LINK_KEY = "1sqU36bWCIp7sXQKz5T63PhPfKJ80xmjqHlhuQJmuuCg"

REGISTRATION_LINK_KEY = "1SE0wAl3BaWrWdvuIIGYV6uNWpjDoadEWN-Mndz8J2nU"

class GSheet():
    def __init__(self, key=SUBMISSION_LINK_KEY):

        """
            Shows basic usage of the Sheets API.
            Prints values from a sample spreadsheet.
        """
        
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE_PATH)
        self.sheetSubmission = gc.open_by_key(SUBMISSION_LINK_KEY).get_worksheet(0)
        self.sheetRegistration = gc.open_by_key(REGISTRATION_LINK_KEY).get_worksheet(0)
        self.getDataframeFromRegistrationSheet()
        self.getDataframeFromSubmissionSheet()

    def getDataframeFromSubmissionSheet(self):
        dataArr = self.sheetSubmission.get_all_values()
        # print(pd.DataFrame(dataArr[1:], columns=dataArr[0]))

        # Create a dataframe to manage entries
        self.dfSubmission = pd.DataFrame(dataArr[1:], columns=dataArr[0])

        # Create Process Status
        if GSHEET_SUBMISSION_COL.PROCESS_STATUS.value not in self.dfSubmission.columns:
            self.dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value] = np.nan
            self.dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value] = self.dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value].fillna(GSHEET_SUBMISSION_COL.PROCESS_STATUS)
            #print(self.dfSubmission)
        return self.dfSubmission
    
    def getDataframeFromRegistrationSheet(self):
        dataArr = self.sheetRegistration.get_all_values()

        # Create a dataframe to manage entries
        self.dfRegistration = pd.DataFrame(dataArr[1:], columns=dataArr[0])
        self.dfRegistration = self.dfRegistration[self.dfRegistration[GSHEET_REGISTRATION_COL.VALID.value] == 'Y']
        print(self.dfRegistration)

        return self.dfRegistration

    def setColumnValue(self, rowIndex, columnName, value):
        self.dfSubmission.at[rowIndex, columnName] = value

    def updateSheets(self):
        #print(self.dfSubmission)
        # print(self.df.values.tolist())
        #print(list(self.dfSubmission.columns))
        self.sheetSubmission.update([list(self.dfSubmission.columns)] + self.dfSubmission.values.tolist())
