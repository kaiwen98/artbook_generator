from commons.constants import GSHEET_SUBMISSION_COL
import win32com.client
import os
from models.Photoshop import Photoshop
from models.GDrive import GDrive
from models.GSheets import GSheet
from commons import utils

assetPath = os.path.join(os.getcwd(), "assets")
assetInPath = os.path.join(assetPath, "in")
assetOutPath = os.path.join(assetPath, "out")

imageFilePath = os.path.join(assetInPath, "photo_2022-08-20_11-13-16.jpg")
outputFilePath = os.path.join(assetOutPath, "testa-art.pdf")
backgroundFilePath = os.path.join(assetInPath, "seed", "ExtravaganzaBookArtworkTemplate.png")

srcFilePath = os.path.join(assetInPath, "seed", "ExtravaganzaBookArttextTemplate.psd")
destFilePath = os.path.join(assetOutPath, "testa-text.pdf")

def generatePdfs(dfCompleteRow, ps):
    fileName = utils.getPdfName(dfCompleteRow)
    url = utils.resolveArtworkFinalUrl(dfCompleteRow)
    imageFilePath = gdrive.retrieve(
        utils.getGidFromGdriveUrl(url)
    )

    utils.generateArtworkPdf(
        imageFilePath,
        backgroundFilePath,
        os.path.join(assetOutPath, f"{fileName}_Art.pdf")
    )

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
        os.path.join(assetOutPath, f"{fileName}_Text.pdf")
    )

if __name__ == "__main__":
    gsheet = GSheet()
    # # gsheet.getDataframeFromSubmissionSheet()
    # gsheet.setColumnValue(0, "ProcessStatus", "Success")
    # gsheet.updateSheets()
    gdrive = GDrive()
    gdrive.retrieve('1xleUZaxR3S8DyVP_wY2-HRjf6PEiFqQD')
    ps = Photoshop(srcFilePath)
    for id, row in gsheet.dfComplete.iterrows():
        generatePdfs(row, ps)
        break
    




