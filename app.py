from commons.constants import ARTBOOK_OUTPUT_PATH, BACKGROUND_FILE_PATH, GSHEET_SUBMISSION_CATEGORY, GSHEET_SUBMISSION_COL, SRC_FILE_PATH
import win32com.client
import os
from models.Photoshop import Photoshop
from models.GDrive import GDrive
from models.GSheets import GSheet
from commons import utils

def generatePdfs(dfCompleteRow, ps):
    category = dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]
    fileName = utils.getPdfName(dfCompleteRow)
    url = utils.resolveArtworkFinalUrl(dfCompleteRow)
    imageFilePath = gdrive.retrieve(
        utils.getGidFromGdriveUrl(url)
    )
    if not os.path.exists(os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Art.pdf")):
        utils.generateArtworkPdf(
            imageFilePath,
            BACKGROUND_FILE_PATH,
            os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Art.pdf")
        )

    print(f"Generating texts for {fileName}")

    if not os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Text.pdf"):
        ps.modifyLayerText("ArtworkTitle", 
            f'''{dfCompleteRow[GSHEET_SUBMISSION_COL.ARTWORK_TITLE.value]}'''
        )

        ps.modifyLayerText("ArtworkDesc", 
            f'''{dfCompleteRow[GSHEET_SUBMISSION_COL.ARTWORK_TEXT.value]}'''
        )

        ps.modifyLayerText("ArtistDesc", 
            utils.getParticipantDesc(dfCompleteRow)
        )

        ps.saveAsPdf(
            os.path.join(ARTBOOK_OUTPUT_PATH, category, f"{fileName}_Text.pdf")
        )

if __name__ == "__main__":
    gsheet = GSheet()
    # # gsheet.getDataframeFromSubmissionSheet()
    # gsheet.setColumnValue(0, GSHEET_SUBMISSION_COL.PROCESS_STATUS.value, "Success")
    # gsheet.updateSheets()

    gdrive = GDrive()
    # gdrive.retrieve('1xleUZaxR3S8DyVP_wY2-HRjf6PEiFqQD')
    ps = Photoshop(SRC_FILE_PATH)
    
    # id = 0
    # for _, row in gsheet.dfComplete.iterrows():
    #     id += 1
    #     print(id)
    #     print(type(id))
    #     # if row[GSHEET_SUBMISSION_COL.CATEGORY.value] != GSHEET_SUBMISSION_CATEGORY.COMIC.value:
    #     #     continue
    #     try:
    #         generatePdfs(row, ps)
    #         gsheet.setColumnValue(id, GSHEET_SUBMISSION_COL.PROCESS_STATUS.value, "Success")
    #     except Exception as err:
    #         print(err)
    #         gsheet.setColumnValue(id, GSHEET_SUBMISSION_COL.PROCESS_STATUS.value, "Failed")
    #         continue
        

    
    utils.generateCombinedPdfFromFiles()

    gsheet.updateSheets()

    




