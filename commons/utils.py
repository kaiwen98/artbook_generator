from PIL import Image
import os
import math
import re

from commons.constants import GSHEET_REGISTRATION_COL, GSHEET_SUBMISSION_CATEGORY, GSHEET_SUBMISSION_COL
A4_PX_DIMENSION = (2480, 2480)

def getCenteredOffset(bgSize, imageSize):
    return ((bgSize[0] - imageSize[0]) // 2, (bgSize[1] - imageSize[1]) // 2)

def generateArtworkPdf(imageFilePath, backgroundFilePath, outputFilePath):

    image = Image.open(imageFilePath)
    imageHeight = image.size[1]
    newImageHeight = math.ceil(imageHeight * A4_PX_DIMENSION[0] / image.size[0])
    outfile = os.path.splitext(outputFilePath)[0] + ".pdf"

    image = image.resize(
        (A4_PX_DIMENSION[0], newImageHeight),
        Image.ANTIALIAS
    )

    backgroundImage = Image.open(backgroundFilePath)
    print(image.size)
    print(backgroundImage.size)
    offset = getCenteredOffset(backgroundImage.size, image.size)
    backgroundImage.paste(image, offset)

    backgroundImage.save(outfile, format="pdf", quality=100, subsampling=0)

def getGidFromGdriveUrl(url):
    print(url)
    print(re.split(r'\?id\=', url)[1])
    return re.split(r'\?id\=', url)[1]

def getPdfName(dfCompleteRow):
    # Reference title:
    # {CATEGORY}.{Name}
    print(f"{dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]}".replace(" ", "_"))
    return f"{dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}-{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]}".replace(" ", "_")

def resolveArtworkFinalUrl(dfCompleteRow):
    if dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.COMIC.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.COMIC_FINAL.value]
    elif dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.TRAD.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.TRAD_FINAL.value]
    elif dfCompleteRow[GSHEET_SUBMISSION_COL.CATEGORY.value] == GSHEET_SUBMISSION_CATEGORY.DIGITAL.value:
        return dfCompleteRow[GSHEET_SUBMISSION_COL.DIGITAL_FINAL.value]

def getParticipantDesc(dfCompleteRow):
    return f'''{dfCompleteRow[GSHEET_REGISTRATION_COL.NAME.value]} ({dfCompleteRow[GSHEET_REGISTRATION_COL.AGE.value]})\r\n{dfCompleteRow[GSHEET_REGISTRATION_COL.SCHOOL.value]}'''