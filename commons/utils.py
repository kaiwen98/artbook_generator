from PIL import Image
import os
import math
import re
from pdf2image import convert_from_path
import PyPDF2
import img2pdf
from pathlib import Path

from commons.constants import ASSET_IN_PATH, ASSET_OUT_PATH, GSHEET_REGISTRATION_COL, GSHEET_SUBMISSION_CATEGORY, GSHEET_SUBMISSION_COL
# A4_PX_DIMENSION = (2480, 2480)
A4_PX_DIMENSION = (2480, 2480)

def getCenteredOffset(bgSize, imageSize):
    return ((bgSize[0] - imageSize[0]) // 2, (bgSize[1] - imageSize[1]) // 2)

def generateArtworkPdfFromPdf(imageFilePath, backgroundFilePath, outputFilePath):
    images = convert_from_path(imageFilePath)
    for id, image in enumerate(images, start=1):
        outputFilePath = os.path.splitext(outputFilePath)[0] + f"_{id}" +  os.path.splitext(outputFilePath)[1]
        print(outputFilePath)
        pasteImageOnBackgroundAndSave(image, backgroundFilePath, outputFilePath)

def pasteImageOnBackgroundAndSave(image, backgroundFilePath, outputFilePath):
    imageHeight = image.size[1]
    newImageHeight = math.ceil(imageHeight * A4_PX_DIMENSION[0] / image.size[0])
    outfile = os.path.splitext(outputFilePath)[0] + ".pdf"

    image = image.resize(
        (A4_PX_DIMENSION[0], newImageHeight),
        Image.ANTIALIAS
    )

    backgroundImage = Image.open(backgroundFilePath)
    print(backgroundImage.size)
    offset = getCenteredOffset(backgroundImage.size, image.size)
    backgroundImage.paste(image, offset)
    # Path(outfile).write_bytes(img2pdf)
    backgroundImage.save(outfile, format="pdf", resolution=300)

def generateArtworkPdf(imageFilePath, backgroundFilePath, outputFilePath):
    ext = os.path.splitext(imageFilePath)[1]
    print(ext)
    if ext == '.pdf':
        generateArtworkPdfFromPdf(imageFilePath, backgroundFilePath, outputFilePath)
    else:
        image = Image.open(imageFilePath)
        pasteImageOnBackgroundAndSave(image, backgroundFilePath, outputFilePath)

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

def generateCombinedPdfFromFiles():
    pdfPages = [
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_Cover.pdf"), 'rb'),
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_Foreword.pdf"), 'rb'),
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_WS.pdf"), 'rb')
        ]

    pdfWriter =PyPDF2.PdfFileWriter()
    
    for folder in os.listdir(os.path.join(ASSET_OUT_PATH, "artbook")):
        print(folder)
        if folder == GSHEET_SUBMISSION_CATEGORY.COMIC.value:
            categoryPage = "Extravaganza_Comic.pdf"
        if folder == GSHEET_SUBMISSION_CATEGORY.DIGITAL.value:
            categoryPage = "Extravaganza_Digital.pdf"
        if folder == GSHEET_SUBMISSION_CATEGORY.TRAD.value:
            categoryPage = "Extravaganza_Traditional.pdf"

        pdfPages.append(
            open(os.path.join(ASSET_IN_PATH, categoryPage), 'rb')
        )

        for file in os.listdir(os.path.join(ASSET_OUT_PATH, "artbook", folder)):
            print(file)
            pdfPages.append(
                open(os.path.join(ASSET_OUT_PATH, "artbook", folder, file), 'rb')
            )
    
    pdfPages.append(
        open(os.path.join(ASSET_IN_PATH, "Extravaganza_Back.pdf"), 'rb')
        )

    for page in pdfPages:
        pageReader = PyPDF2.PdfFileReader(page)
        print("PDF SIZE: ", pageReader.pages[0].mediabox)
        pdfWriter.addPage(PyPDF2.PdfFileReader(page).getPage(0))

    pdfOutputFile = open(os.path.join(ASSET_OUT_PATH, "Extravaganza_Artbook.pdf"), 'wb')
    pdfWriter.write(pdfOutputFile)

    for page in pdfPages:
        page.close()
