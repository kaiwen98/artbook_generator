from enum import Enum

class GSHEET_SUBMISSION_SUBMIT_CATEGORY(Enum):
    DIGITAL = "DIGITAL"
    TRAD = "TRAD"
    COMIC = "COMIC"

class GSHEET_REGISTRATION_COL(Enum):
    TIMESTAMP = 'Timestamp'
    RegistrationType = 'Registration Type'
    SCH_POC_NAME = 'Name of Point of Contact'
    SCH_CONTACT = 'Contact number'
    SCH_EMAIL = "Email", 
    SCH_SCHOOL = 'Academic Institution'
    NAME_LIST_LINK = 'Upload Name list of Participants (Please upload a document of Name of Paricipants, Age and Gender for each participant). Please download the Excel sheet from https://tinyurl.com/ex2022namelist, then upload to here!'
    NAME = 'Name (as in NRIC):'
    AGE = 'Age:'
    SCHOOL = 'Academic Institution:'
    GENDER = 'Gender'
    EMAIL = 'Email:'
    CONTACT = 'Contact Number:'
    PREV_ITERATIONS = 'Have you participated in previous iterations of Extravaganza?'
    TERMS_AGREE = 'If you agree to the above, please check here:'
    VALID = 'Valid?'

class GSHEET_SUBMISSION_COL(Enum):
    TIMESTAMP = 'Timestamp'
    EMAIL = 'Email Address'
    NAME = 'Name (as in NRIC) :'
    ARTWORK_TITLE = 'Title of Artwork :'
    ARTWORK_TEXT = "100-word sypnosis for the artwork. You can discuss its meaning to you, the process of creating it, the artwork medium, how it relates to this year's theme, etc!", 
    CATEGORY = 'I am submitting for ...'
    DIGITAL_FINAL = 'DIGITAL - Please upload your final submission artwork. Ensure it is named YOUR_FULL_NAME_final.png/jpeg .'
    DIGITAL_WIP1 = 'DIGITAL - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .'
    DIGITAL_WIP2 = 'DIGITAL - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .'
    COMIC_NUM_PANELS = 'Please declare the number of panels in your comic.'
    COMIC_FINAL = 'COMIC - Please upload your final submission comic pages in PDF. Ensure it is named YOUR_FULL_NAME_final.pdf .'
    COMIC_WIP1 = 'COMIC - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .'
    COMIC_WIP2 = 'COMIC - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .'
    TRAD_FINAL = 'Traditional - Please upload your final submission artwork. Ensure it is named YOUR_FULL_NAME_final.png/jpeg .'
    TRAD_WIP1 = 'Traditional - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .'
    TRAD_WIP2 = 'Traditional - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .'
    PROCESS_STATUS = 'ProcessStatus'


# GSHEET_SUBMISSION_COLS = {
#     'Timestamp': 'Timestamp', 
#     'Email': 'Email Address', 
#     'Name': 'Name (as in NRIC) :', 
#     'ArtworkTitle': 'Title of Artwork :', 
#     'ArtworkText': "100-word sypnosis for the artwork. You can discuss its meaning to you, the process of creating it, the artwork medium, how it relates to this year's theme, etc!", 
#     'SubmitFor': 'I am submitting for ...', 
#     'DigitalFinal': 'DIGITAL - Please upload your final submission artwork. Ensure it is named YOUR_FULL_NAME_final.png/jpeg .', 
#     'DigitalWip1': 'DIGITAL - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .', 
#     'DigitalWip1': 'DIGITAL - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .', 
#     'ComicNumPanels': 'Please declare the number of panels in your comic.', 
#     'ComicFinal': 'COMIC - Please upload your final submission comic pages in PDF. Ensure it is named YOUR_FULL_NAME_final.pdf .', 
#     'ComicWip1': 'COMIC - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .', 
#     'ComicWip2': 'COMIC - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .', 
#     'TradFinal': 'Traditional - Please upload your final submission artwork. Ensure it is named YOUR_FULL_NAME_final.png/jpeg .', 
#     'TradWip1': 'Traditional - Please upload the first WIP. Ensure it is named YOUR_FULL_NAME_wip1.png/jpeg .', 
#     'TradWip2': 'Traditional - Please upload the second WIP. Ensure it is named YOUR_FULL_NAME_wip2.png/jpeg .', 
#     'ProcessStatus': 'ProcessStatus'
# }