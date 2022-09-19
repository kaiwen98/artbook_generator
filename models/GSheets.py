from commons.constants import ASSET_OUT_PATH, GSHEET_REGISTRATION_COL, GSHEET_SUBMISSION_COL
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

DF_PRINT_PATH = os.path.join(ASSET_OUT_PATH, "df_print.csv")

class GSheet():
    def __init__(self, key=SUBMISSION_LINK_KEY):

        """
            Shows basic usage of the Sheets API.
            Prints values from a sample spreadsheet.
        """
        
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE_PATH)
        self.sheetSubmission = gc.open_by_key(SUBMISSION_LINK_KEY).get_worksheet(0)
        self.sheetRegistration = gc.open_by_key(REGISTRATION_LINK_KEY).get_worksheet(0)
        self.dfRegistration = self.getDataframeFromRegistrationSheet()
        self.dfSubmission = self.getDataframeFromSubmissionSheet()

        # Left join
        print(self.dfSubmission.set_index(GSHEET_SUBMISSION_COL.NAME.value).shape)
        self.dfComplete = self.dfSubmission.set_index(GSHEET_SUBMISSION_COL.NAME.value).join(
            self.dfRegistration.drop([GSHEET_REGISTRATION_COL.TIMESTAMP.value], axis=1).set_index(GSHEET_REGISTRATION_COL.NAME.value)
        )

        # Remove duplicate indices
        self.dfComplete = self.dfComplete[~self.dfComplete.index.duplicated(keep='last')]

        print(self.dfComplete)

        self.dfComplete = self.dfComplete.assign(**{
            GSHEET_REGISTRATION_COL.NAME.value: self.dfSubmission[GSHEET_SUBMISSION_COL.NAME.value].values.tolist()
        })

        print(self.dfComplete)
        
        self.dfComplete.to_csv(DF_PRINT_PATH)
    
    def getDataFromParticipants(self, key: GSHEET_REGISTRATION_COL | GSHEET_SUBMISSION_COL):
        return self.dfComplete[key]

    def getDataframeFromSubmissionSheet(self):
        dataArr = self.sheetSubmission.get_all_values()
        # print(pd.DataFrame(dataArr[1:], columns=dataArr[0]))

        # Create a dataframe to manage entries
        dfSubmission = pd.DataFrame(dataArr[1:], columns=dataArr[0])
        #print(self.dfSubmission.columns)

        # Trim all whitespaces
        dfSubmission[[
            GSHEET_SUBMISSION_COL.NAME.value,
        ]] = dfSubmission[[
            GSHEET_SUBMISSION_COL.NAME.value,
        ]].applymap(
            lambda x:\
                x\
                # Trim whitespaces
                .strip()\
                # Convert to Camelcase
                .title() 
            if isinstance(x, str) else x
        )

        # Create Process Status
        if GSHEET_SUBMISSION_COL.PROCESS_STATUS.value not in dfSubmission.columns:
            dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value] = np.nan
            dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value] = dfSubmission[GSHEET_SUBMISSION_COL.PROCESS_STATUS.value].fillna(GSHEET_SUBMISSION_COL.PROCESS_STATUS)
            #print(self.dfSubmission)
        return dfSubmission
    
    def getDataframeFromRegistrationSheet(self):
        dataArr = self.sheetRegistration.get_all_values()

        # Create a dataframe to manage entries
        dfRegistration = pd.DataFrame(dataArr[1:], columns=dataArr[0])

        # String processing
        dfRegistration[[
            GSHEET_REGISTRATION_COL.NAME.value,
            GSHEET_REGISTRATION_COL.SCHOOL.value
        ]] = dfRegistration[[
            GSHEET_REGISTRATION_COL.NAME.value,
            GSHEET_REGISTRATION_COL.SCHOOL.value
        ]].applymap(
            lambda x:\
                x\
                # Trim whitespaces
                .strip()\
                # Convert to Camelcase
                .title() 
            if isinstance(x, str) else x
        )
        #print(self.dfRegistration.columns)
        dfRegistration = dfRegistration[dfRegistration[GSHEET_REGISTRATION_COL.VALID.value] == 'Y']
        #print(self.dfRegistration)

        return dfRegistration

    def setColumnValue(self, rowIndex, columnName, value):
        self.dfSubmission.at[rowIndex, columnName] = value

    def updateSheets(self):
        #print(self.dfSubmission)
        # print(self.df.values.tolist())
        #print(list(self.dfSubmission.columns))
        #print(GSHEET_SUBMISSION_COL.list())
        self.sheetSubmission.update([list(self.dfSubmission.columns)] + self.dfSubmission[GSHEET_SUBMISSION_COL.list()].values.tolist())
