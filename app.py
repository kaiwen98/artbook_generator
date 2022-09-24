from commons.constants import ARTBOOK_OUTPUT_PATH, BACKGROUND_FILE_PATH, GSHEET_REGISTRATION_COL, GSHEET_SUBMISSION_CATEGORY, GSHEET_SUBMISSION_COL, SRC_FILE_PATH
import win32com.client
import os
from models.Photoshop import Photoshop
from models.GDrive import GDrive
from models.GSheets import GSheet
from commons import utils

nameToCount = {}

def generatePdfs(dfCompleteRow, ps, nameToCount):
    
    category = dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]

    angleToRotate = dfCompleteRow[GSHEET_SUBMISSION_COL.ROTATE.value]
    angleToRotate = 0 if len(angleToRotate) == 0 else angleToRotate

    fileName = utils.getPdfName(dfCompleteRow)
    url = utils.resolveArtworkFinalUrl(dfCompleteRow)
    imageFilePath = gdrive.retrieve(
        utils.getGidFromGdriveUrl(url)
    )
    print(url)

    if \
        not os.path.exists(os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Art.pdf")) \
            :
        # or fileName not in nameToCount.keys():
        """
        If file is not yet created
        or file exists but was not created in the current run (Meaning you replace all files. Comment out to use cached artworks.)
        """
        nameToCount[fileName] = 0
        utils.generateArtworkPdf(
            imageFilePath,
            BACKGROUND_FILE_PATH,
            os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Art.pdf"),
            int(angleToRotate)
        )

    elif \
        os.path.exists(os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Art.pdf")) \
        and fileName in nameToCount.keys():
        """
        File exists and was created in the current run
        """
        nameToCount[fileName] += 1
        utils.generateArtworkPdf(
            imageFilePath,
            BACKGROUND_FILE_PATH,
            os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_{nameToCount[fileName]}_Art.pdf"),
            int(angleToRotate)
        )

    if not os.path.exists(os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Text.pdf")):
        print(f"Generating texts for {fileName}")
        utils.generateArttextPdf(
            ps,
            dfCompleteRow,
            category,
            fileName
        )

if __name__ == "__main__":
    gsheet = GSheet()
    gdrive = GDrive()
    ps = Photoshop(SRC_FILE_PATH)
    
    id = -1
    for _, row in gsheet.dfComplete.iterrows():
        id += 1
        print(row[GSHEET_REGISTRATION_COL.NAME.value])

        # Editable, set category to process.
        if row[GSHEET_SUBMISSION_COL.CATEGORY.value] != GSHEET_SUBMISSION_CATEGORY.DIGITAL.value:
            continue
        
        # Editable, set student to process.
        # if "Leow Young Linn Nikki" not in row[GSHEET_REGISTRATION_COL.NAME.value]:
        #     continue
            
        try:
            generatePdfs(row, ps, nameToCount)

            # Mark as success
            gsheet.setColumnValue(id, GSHEET_SUBMISSION_COL.PROCESS_STATUS.value, "Success")

        except Exception as err:
            print(err)

            # Mark as Failure
            gsheet.setColumnValue(id, GSHEET_SUBMISSION_COL.PROCESS_STATUS.value, "Failed")
            continue
        
    # Editable, set category to export
    utils.generateCombinedPdfFromFiles(category=GSHEET_SUBMISSION_CATEGORY.DIGITAL)

    # Update submission sheet with Statuses
    gsheet.updateSheets()

    




